import json
import unittest

import app


class AppTest(unittest.TestCase):
    
    def setUp(self):
        app.app.testing = True
        self.client = app.app.test_client()

    def test_get_user(self):
        response = self.client.get('/users/rycus86')
        
        self._verify_response(response)

        user = json.loads(response.data)

        self.assertIsNotNone(user)
# TODO check user details

    def test_list_repositories(self):
        response = self.client.get('/repositories/rycus86')
        
        self._verify_response(response)

        repos = json.loads(response.data)

        self.assertIsNotNone(repos)
        self.assertGreater(len(repos), 0)

        for repo in repos:
            pass
# TODO check repo details

    def test_get_repository(self):
        response = self.client.get('/repositories/rycus86/github-proxy')
        
        self._verify_response(response)

        repo = json.loads(response.data)

        self.assertIsNotNone(repo)
# TODO check repo details

    def test_list_tags(self):
        response = self.client.get('/repositories/rycus86/github-proxy/tags')
        
        self._verify_response(response)

        tags = json.loads(response.data)

        self.assertIsNotNone(tags)
        self.assertGreater(len(tags), 0)

        for tag in tags:
            pass
# TODO check tag details

    def _verify_response(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.charset, 'utf-8')

