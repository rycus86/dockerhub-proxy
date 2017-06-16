import os
import logging
from flask import Flask, jsonify, make_response
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


if __name__ == '__main__':
    app.run(host=os.environ.get('HTTP_HOST', '127.0.0.1'),
            port=int(os.environ.get('HTTP_PORT', '5000')),
            debug=False)
