import re
import logging
from threading import Lock
from agithub.base import API, ConnectionProperties, Client

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(module)s.%(funcName)s - %(message)s')
logger = logging.getLogger('dockerhub-proxy')


def _with_login(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self.login()
        response = method(self, *args, **kwargs)

        if not response:
            logger.warn('Failed to fetch response, possible authentication issue, retrying after login...')

            self.login()
            response = method(self, *args, **kwargs)

        return response

    return wrapper


class LoginFailedException(BaseException):
    def __init__(self, *args):
        super(LoginFailedException, self).__init__(*args)


class DockerHubClient(Client):
    def __init__(self, auth_token):
        super(DockerHubClient, self).__init__()
        self._auth_token = auth_token

    def has_auth_token(self):
        return self._auth_token is not None

    def set_auth_token(self, token):
        self._auth_token = token

    def request(self, method, url, body_data, headers):
        final_url = self._add_trailing_slash(url)
        final_headers = self._add_authorization_header(headers)

        status, response = super(DockerHubClient, self).request(method, final_url, body_data, final_headers)

        self._drop_auth_token_if_not_successful(status)

        return status, response

    @staticmethod
    def _add_trailing_slash(url):
        return re.sub(r'([^/])(\?|$)', r'\1/\2', url, count=1)

    def _add_authorization_header(self, headers):
        if self._auth_token:
            new_headers = headers.copy()
            new_headers['Authorization'] = 'JWT %s' % self._auth_token
            return new_headers

        else:
            return headers

    def _drop_auth_token_if_not_successful(self, status):
        if status / 100 != 2:
            self._auth_token = None


class DockerHub(API):
    # noinspection PyMissingConstructor
    def __init__(self, username=None, password=None, auth_token=None, **kwargs):
        self._username = username
        self._password = password

        self._login_lock = Lock()

        props = ConnectionProperties(
            api_url=kwargs.pop('api_url', 'hub.docker.com'),
            secure_http=True
        )

        self.setClient(DockerHubClient(auth_token))
        self.setConnectionProperties(props)

    def login(self):
        with self._login_lock:
            if not self._username or not self._password:
                if self.client.has_auth_token():
                    return  # let's go with the existing token instead
    
                raise LoginFailedException('Missing username or password')
    
            status, response = self.v2.users.login.post(body={'username': self._username, 'password': self._password})
    
            if status == 200:
                self.client.set_auth_token(response.get('token'))
    
            else:
                raise LoginFailedException('HTTP %s' % status, response)

    def get_user_details(self, username):
        return self._check_and_return(self.v2.users[username].get)

    def get_repositories(self, username, page_size=100):
        return self._fetch_all_pages(self.v2.repositories[username].get, page=1, page_size=page_size)

    def get_repository(self, username, repository_name):
        return self._check_and_return(self.v2.repositories[username][repository_name].get)

    def get_tags(self, username, repository_name, page_size=100):
        return self._fetch_all_pages(self.v2.repositories[username][repository_name].tags.get, page=1, page_size=page_size)
    
    def get_dockerfile(self, username, repository_name):
        return self._check_and_return(self.v2.repositories[username][repository_name].dockerfile.get)

    def get_autobuild_settings(self, username, repository_name):
        return self._check_and_return(self.v2.repositories[username][repository_name].autobuild.get)

    def get_comments(self, username, repository_name, page_size=100):
        # TODO limit this ?
        return self._fetch_all_pages(self.v2.repositories[username][repository_name].comments.get, page=1, page_size=page_size)

    def get_build_history(self, username, repository_name, page_size=100):
        # TODO limit this ?
        return self._fetch_all_pages(self.v2.repositories[username][repository_name].buildhistory.get, page=1, page_size=page_size)

    def get_build_details(self, username, repository_name, build_code):
        return self._check_and_return(self.v2.repositories[username][repository_name].buildhistory[build_code].get)

    @staticmethod
    def _check_and_return(incomplete_request):
        status, response = incomplete_request()

        if status == 200:
            return response

    @staticmethod
    def _fetch_all_pages(incomplete_request, page, page_size):
        results = list()

        while True:
            kwargs = {'page_size': page_size}

            if page > 1:
                kwargs['page'] = page

            status, response = incomplete_request(**kwargs)

            if status == 200:
                results.extend(response.get('results'))

                if response.get('next'):
                    page += 1

                else:
                    count = response.get('count')

                    return {
                        'count': count,
                        'results': results
                    }

            else:
                break
