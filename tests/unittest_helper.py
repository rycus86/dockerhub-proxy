from unittest import TestCase


class TestBase(TestCase):

    def verify_user_details(self, user):
        self.assertIsNotNone(user)

        for expected in ('id', 'username', 'full_name', 'location', 'company',
                         'profile_url', 'date_joined', 'gravatar_url', 'type'):
            self.assertIn(expected, user)

    def verify_repository_list(self, repos):
        self.assertIsNotNone(repos)

        self.assertIn('count', repos)
        self.assertIn('results', repos)
        self.assertGreater(repos.get('count'), 0)
        self.assertEqual(len(repos.get('results')), repos.get('count'))

        for repo in repos.get('results'):
            self.verify_repository(repo)

    def verify_repository(self, repository, full=False):
        self.assertIsNotNone(repository)
        self.assertIn('namespace', repository)
        self.assertIn('name', repository)
        self.assertIn('user', repository)
        self.assertIn('repository_type', repository)
        self.assertIn('is_private', repository)
        self.assertIn('is_automated', repository)
        self.assertIn('description', repository)
        self.assertIn('last_updated', repository)
        self.assertIn('pull_count', repository)
        self.assertIn('star_count', repository)

        if full:
            self.assertIn('full_description', repository)

    def verify_tags(self, tags):
        self.assertIsNotNone(tags)
        self.assertIn('count', tags)
        self.assertIn('results', tags)
        self.assertGreater(tags.get('count'), 0)
        self.assertEqual(len(tags.get('results')), tags.get('count'))

        for tag in tags.get('results'):
            self.assertIn('name', tag)
            self.assertIn('last_updated', tag)
            self.assertIn('full_size', tag)

    def verify_dockerfile(self, dockerfile):
        self.assertIsNotNone(dockerfile)
        self.assertIn('contents', dockerfile)
        self.assertIsNotNone(dockerfile.get('contents'))
        self.assertGreater(len(dockerfile.get('contents')), 0)

    def verify_autobuild_settings(self, settings):
        self.assertIsNotNone(settings)

        for expected in ('active', 'build_name', 'build_tags', 'docker_url', 'provider',
                         'repo_type', 'repo_web_url', 'source_url'):
            self.assertIn(expected, settings)

        tags = settings.get('build_tags')

        self.assertGreater(len(tags), 0)

        for tag in tags:
            for expected in ('dockerfile_location', 'name', 'source_name', 'source_type'):
                self.assertIn(expected, tag)

    def verify_comments(self, comments):
        self.assertIsNotNone(comments)
        self.assertGreater(comments.get('count'), 0)
        self.assertEqual(len(comments.get('results')), min(comments.get('count'), 1000))

        for comment in comments.get('results'):
            self.assertIn('id', comment)
            self.assertIn('user', comment)
            self.assertIn('comment', comment)
            self.assertIn('created_on', comment)
            self.assertIn('updated_on', comment)

    def verify_build_history(self, history):
        self.assertIsNotNone(history)
        self.assertGreater(history.get('count'), 0)
        self.assertEqual(len(history.get('results')), min(history.get('count'), 1000))

        for item in history.get('results'):
            self.assertIn('id', item)
            self.assertIn('build_code', item)
            self.assertIn('dockertag_name', item)
            self.assertIn('cause', item)
            self.assertIn('status', item)
            self.assertIn('created_date', item)
            self.assertIn('last_updated', item)

    def verify_build_details(self, details):
        self.assertIsNotNone(details)

        for expected in ('id', 'build_code', 'dockertag_name', 'build_results',
                         'cause', 'created_date', 'last_updated', 'status'):
            self.assertIn(expected, details)

        results = details.get('build_results')

        for expected in ('build_code', 'build_path', 'docker_repo', 'docker_tag', 'docker_user',
                         'dockerfile_contents', 'readme_contents', 'error', 'failure', 'logs',
                         'created_at', 'last_updated', 'source_branch', 'source_type', 'source_url'):
            self.assertIn(expected, results)

