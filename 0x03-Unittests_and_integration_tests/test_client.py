#!/usr/bin/env python3
"""This module contains test fixtures for the client module"""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from client import GithubOrgClient
from parameterized import parameterized
from typing import Dict, Any


class TestGithubOrgClient(unittest.TestCase):
    """Test fixture for testing methods in GithubOrgClient class"""
    @parameterized.expand([
        ('google', {'name': 'Google'}),
        ('abc', {'name': 'abc'})
    ])
    @patch('client.get_json')
    def test_org(self, org: str, rtr: Dict, mock_obj: Any) -> None:
        """Test the method org and patch get_json method to prevent
        external call"""
        githubObj = GithubOrgClient(org)
        mock_obj.return_value = Mock(return_value=rtr)
        self.assertEqual(githubObj.org(), rtr)
        mock_obj.assert_called_once_with(
                "https://api.github.com/orgs/{}".format(org))
    
    def test_public_repos_url(self) -> None:
        """Test _public_repos_url method by mocking org method to
        behave like a property rather than method. This is done so
        as to give a predefined value to the org rather than running
        the org function and having to patch other external dependencies
        used within it."""

        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_obj:
            url = "https://api.github.com/orgs/google/repos"
            mock_obj.return_value = {
                         'repos_url': url
                }
            self.assertEqual(
                    GithubOrgClient('google')._public_repos_url, url)





        
