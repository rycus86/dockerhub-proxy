import json
from unittest_helper import TestBase

import app


class AppTest(TestBase):
    def setUp(self):
        app.app.testing = True
        self.client = app.app.test_client()

    def test_get_user(self):
        response = self.client.get('/users/rycus86')

        self._verify_response(response)

        user = json.loads(response.data)

        self.verify_user_details(user)

    def test_list_repositories(self):
        response = self.client.get('/repositories/rycus86')

        self._verify_response(response)

        repos = json.loads(response.data)

        self.verify_repository_list(repos)

    def test_get_repository(self):
        response = self.client.get('/repositories/rycus86/github-proxy')

        self._verify_response(response)

        repo = json.loads(response.data)

        self.verify_repository(repo, full=True)

    def test_list_tags(self):
        response = self.client.get('/repositories/rycus86/github-proxy/tags')

        self._verify_response(response)

        tags = json.loads(response.data)

        self.verify_tags(tags)

    def test_get_dockerfile(self):
        response = self.client.get('/repositories/rycus86/github-proxy/dockerfile')

        self._verify_response(response)

        dockerfile = json.loads(response.data)

        self.verify_dockerfile(dockerfile)

    def test_get_autobuild_settings(self):
        response = self.client.get('/repositories/rycus86/github-proxy/autobuild')

        self._verify_response(response)

        settings = json.loads(response.data)

        self.verify_autobuild_settings(settings)

    def test_list_comments(self):
        response = self.client.get('/repositories/library/nginx/comments')

        self._verify_response(response)

        comments = json.loads(response.data)

        self.verify_comments(comments)

    def test_list_build_history(self):
        response = self.client.get('/repositories/rycus86/github-proxy/builds')

        self._verify_response(response)

        history = json.loads(response.data)

        self.verify_build_history(history)

    def test_get_build_details(self):
        response = self.client.get('/repositories/rycus86/github-proxy/builds/bt9rkscwy2kuthbm2u9dchk')

        self._verify_response(response)

        details = json.loads(response.data)

        self.verify_build_details(details)

    def _verify_response(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.charset, 'utf-8')
