import os
import unittest

from api import DockerHub


class DockerHubTest(unittest.TestCase):
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

    def test_get_user_details(self):
        user = self.api.get_user_details('rycus86')

        self.assertIsNotNone(user)

        for expected in ('id', 'username', 'full_name', 'location', 'company',
                         'profile_url', 'date_joined', 'gravatar_url', 'type'):
            self.assertIn(expected, user)

    def test_get_repositories(self):
        repos = self.api.get_repositories('rycus86')

        self.assertIsNotNone(repos)
        self.assertGreater(repos.get('count'), 0)
        self.assertEqual(len(repos.get('results')), repos.get('count'))

    def test_get_repositories_with_pagination(self):
        repos = self.api.get_repositories('library')

        self.assertIsNotNone(repos)
        self.assertGreater(repos.get('count'), 0)
        self.assertEqual(len(repos.get('results')), repos.get('count'))
