#!/usr/bin/env python3

GithubOrgClient = __import__('client').GithubOrgClient


a = GithubOrgClient('google')
print(a.org)
#print(a._public_repos_url)
