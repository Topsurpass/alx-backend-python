#!/usr/bin/env python3
"""This module contains test fixtures for the client module"""

import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
from typing import Dict
from fixtures import TEST_PAYLOAD
from requests import HTTPError


class TestGithubOrgClient(unittest.TestCase):
    """Test fixture for testing methods in GithubOrgClient class"""
    @parameterized.expand([
        ('google', {'name': 'Google'}),
        ('abc', {'name': 'abc'})
    ])
    @patch('client.get_json')
    def test_org(self, org: str, rtr: Dict, mock_obj: MagicMock) -> None:
        """Test the method org and patch get_json method to prevent
        external call"""
        githubObj = GithubOrgClient(org)
        mock_obj.return_value = MagicMock(return_value=rtr)
        self.assertEqual(githubObj.org(), rtr)
        mock_obj.assert_called_once_with(
                "https://api.github.com/orgs/{}".format(org))

    def test_public_repos_url(self) -> None:
        """Test _public_repos_url method by mocking org method to
        behave like a property rather than method. This is done so
        as to give a predefined value to the org rather than running
        the org function and having to patch other external dependencies
        used within it."""

        with patch(
                'client.GithubOrgClient.org',
                new_callable=PropertyMock
                ) as mock_obj:
            url = "https://api.github.com/orgs/google/repos"
            mock_obj.return_value = {
                         'repos_url': url
                }
            self.assertEqual(
                    GithubOrgClient('google')._public_repos_url, url)

    """Mulpiple patching"""
    @patch('client.get_json')
    def test_public_repos(self, mock_obj: MagicMock) -> None:
        """Mulpiple patching"""
        repo_list = [
                {'name': 'Topsurpass'},
                {'name': 'Temitope'}
            ]
        rtn_obj = {'repos_url': repo_list}
        mock_obj.return_value = rtn_obj['repos_url']

        with patch(
                'client.GithubOrgClient._public_repos_url',
                new_callable=PropertyMock
                ) as mock_patch_obj:
            mock_patch_obj.return_value = repo_list
            new_obj = GithubOrgClient('github').public_repos()
            self.assertEqual(new_obj, ['Topsurpass', 'Temitope'])
            mock_patch_obj.assert_called_once()
        mock_obj.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(
            self,
            repo: Dict,
            key: str,
            outcome: bool
            ) -> None:
        """Test has_license method"""
        obj = GithubOrgClient('google')
        obj_rtn_val = obj.has_license(repo, key)
        self.assertEqual(obj_rtn_val, outcome)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration Testing: Mock code that sends external
    requests only"""

    @classmethod
    def setUpClass(cls) -> None:
        """Start up method before the test fixture"""
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            """Get payload value"""
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Tests the `public_repos` method."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """Tests the `public_repos` method with a license."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """A clean up function after the test fixture"""
        cls.get_patcher.stop()
