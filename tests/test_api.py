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

        # TODO assert properties

    def test_get_repository(self):
        repository = self.api.get_repository('rycus86', 'github-proxy')
        
        self.assertIsNotNone(repository)
        
        self.assertIn('namespace', repository)
        self.assertIn('name', repository)
        self.assertIn('user', repository)
        self.assertIn('repository_type', repository)
        self.assertIn('is_private', repository)
        self.assertIn('is_automated', repository)
        self.assertIn('description', repository)
        self.assertIn('full_description', repository)
        self.assertIn('last_updated', repository)
        self.assertIn('pull_count', repository)
        self.assertIn('star_count', repository)

    def test_get_repository_tags(self):
        tags = self.api.get_tags('rycus86', 'github-proxy')

        self.assertIsNotNone(tags)
        self.assertGreater(tags.get('count'), 0)
        self.assertEqual(len(tags.get('results')), tags.get('count'))

        for tag in tags.get('results'):
            self.assertIn('name', tag)
            self.assertIn('last_updated', tag)
            self.assertIn('full_size', tag)
