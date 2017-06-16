import os
from unittest import SkipTest
from unittest_helper import TestBase

from api import DockerHub, LoginFailedException


class DockerHubTest(TestBase):
    def setUp(self):
        username = os.environ.get('DOCKER_USERNAME')
        password = os.environ.get('DOCKER_PASSWORD')

        self.api = DockerHub(username=username, password=password)

        if username and password:
            self._login()

    def _login(self):
        self.api.login()

        self.assertTrue(self.api.client.has_auth_token(),
                        msg='Failed to get an authentication token')

    def test_invalid_login(self):
        with self.assertRaises(LoginFailedException):
            DockerHub(username='fake', password='N0tG00d').login()

    def test_invalid_token_is_renewed(self):
        self.api.client.set_auth_token('1nv4l!d')

        user = self.api.get_user_details('rycus86')

        self.assertIsNotNone(user)

    def test_does_not_discard_token_if_access_details_are_missing(self):
        if not self.api.client.has_auth_token():
            raise SkipTest('No access token present')

        self.assertTrue(self.api.client.has_auth_token())

        setattr(self.api, '_username', '')
        setattr(self.api, '_password', '')

        self.assertTrue(self.api.client.has_auth_token())

        self.api.login()

        self.assertTrue(self.api.client.has_auth_token())

    def test_returns_none_when_invalid(self):
        repo = self.api.get_repository('rycus86', 'bad-invalid-wrong')

        self.assertIsNone(repo)

    def test_get_user_details(self):
        user = self.api.get_user_details('rycus86')

        self.verify_user_details(user)

    def test_get_repositories(self):
        repos = self.api.get_repositories('rycus86')

        self.verify_repository_list(repos)

    def test_get_repositories_with_pagination(self):
        repos = self.api.get_repositories('library')

        self.verify_repository_list(repos)

    def test_get_repository(self):
        repository = self.api.get_repository('rycus86', 'github-proxy')

        self.verify_repository(repository, full=True)

    def test_get_repository_tags(self):
        tags = self.api.get_tags('rycus86', 'github-proxy')

        self.verify_tags(tags)

    def test_get_dockerfile(self):
        dockerfile = self.api.get_dockerfile('rycus86', 'github-proxy')

        self.verify_dockerfile(dockerfile)

    def test_get_autobuild_settings(self):
        settings = self.api.get_autobuild_settings('rycus86', 'github-proxy')

        self.verify_autobuild_settings(settings)

    def test_get_comments(self):
        comments = self.api.get_comments('library', 'nginx', limit=1000)

        self.verify_comments(comments)

    def test_get_build_history(self):
        history = self.api.get_build_history('rycus86', 'github-proxy', limit=1000)

        self.verify_build_history(history)

    def test_get_build_details(self):
        details = self.api.get_build_details('rycus86', 'github-proxy', 'bt9rkscwy2kuthbm2u9dchk')

        self.verify_build_details(details)
