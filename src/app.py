import os
import logging
from flask import Flask, jsonify
from flask_cache import Cache

from api import DockerHub

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

api = DockerHub(username=os.environ.get('DOCKER_USERNAME'),
                password=os.environ.get('DOCKER_PASSWORD'),
                token=os.environ.get('DOCKER_TOKEN'))

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(module)s.%(funcName)s - %(message)s')
logger = logging.getLogger('docker-proxy')
logger.setLevel(logging.INFO)


@app.route('/users/<username>')
@cache.memoize(timeout=300)
def get_user(username):
    logger.info('Fetching user details for %s', username)
    return jsonify(api.get_user_details(username))


@app.route('/repositories/<username>')
@cache.memoize(timeout=300)
def list_repositories(username):
    logger.info('Fetching repositories for %s', username)
    return jsonify(api.get_repositories(username))


@app.route('/repositories/<username>/<repository>')
@cache.memoize(timeout=300)
def get_repository(username, repository):
    logger.info('Fetching repository details for %s/%s', username, repository)
    return jsonify(api.get_repository(username, repository))


@app.route('/repositories/<username>/<repository>/tags')
@cache.memoize(timeout=300)
def list_tags(username, repository):
    logger.info('Fetching tags for %s/%s', username, repository)
    return jsonify(api.get_tags(username, repository))


@app.route('/repositories/<username>/<repository>/dockerfile')
@cache.memoize(timeout=300)
def get_dockerfile(username, repository):
    logger.info('Fetching the Dockerfile for %s/%s', username, repository)
    return jsonify(api.get_dockerfile(username, repository))


@app.route('/repositories/<username>/<repository>/autobuild')
@cache.memoize(timeout=300)
def get_autobuild_settings(username, repository):
    logger.info('Fetching autobuild settings for %s/%s', username, repository)
    return jsonify(api.get_autobuild_settings(username, repository))


@app.route('/repositories/<username>/<repository>/comments')
@cache.memoize(timeout=300)
def list_comments(username, repository):
    logger.info('Fetching comments for %s/%s', username, repository)
    return jsonify(api.get_comments(username, repository))


@app.route('/repositories/<username>/<repository>/builds')
@cache.memoize(timeout=300)
def list_build_history(username, repository):
    logger.info('Fetching build history for %s/%s', username, repository)
    return jsonify(api.get_build_history(username, repository))


@app.route('/repositories/<username>/<repository>/builds/<build_code>')
@cache.memoize(timeout=300)
def get_build_details(username, repository, build_code):
    logger.info('Fetching details for build #%s on %s/%s', build_code, username, repository)
    return jsonify(api.get_build_details(username, repository, build_code))


if __name__ == '__main__':
    app.run(host=os.environ.get('HTTP_HOST', '127.0.0.1'),
            port=int(os.environ.get('HTTP_PORT', '5000')),
            debug=False)
