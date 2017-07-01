# Docker Hub Proxy

A simple `Python` [Flask](http://flask.pocoo.org) *REST* server to proxy calls to *Docker Hub*.

[![Build Status](https://travis-ci.org/rycus86/dockerhub-proxy.svg?branch=master)](https://travis-ci.org/rycus86/dockerhub-proxy)
[![Build Status](https://img.shields.io/docker/build/rycus86/dockerhub-proxy.svg)](https://hub.docker.com/r/rycus86/dockerhub-proxy)
[![Coverage Status](https://coveralls.io/repos/github/rycus86/dockerhub-proxy/badge.svg?branch=master)](https://coveralls.io/github/rycus86/dockerhub-proxy?branch=master)
[![Code Climate](https://codeclimate.com/github/rycus86/dockerhub-proxy/badges/gpa.svg)](https://codeclimate.com/github/rycus86/dockerhub-proxy)

## Usage

The *Docker Hub* API is implemented using [agithub](https://github.com/jpaugh/agithub) and supports
authenticated calls using these environment variables:

- `DOCKERHUB_USERNAME`: a valid *Docker Hub* username
- `DOCKERHUB_PASSWORD`: password for the same *Docker Hub* account
- `DOCKERHUB_TOKEN`: alternatively an authenticated *Docker Hub* token can be used instead of
  username and password

To get a reference to the `DockerHub` class use something like:
```python
api = DockerHub(username=os.environ.get('DOCKERHUB_USERNAME'),
                password=os.environ.get('DOCKERHUB_PASSWORD'),
                token=os.environ.get('DOCKERHUB_TOKEN'))
```

The `api.DockerHub` class wraps endpoints with the following methods:

- `get_user_details(username)`:
  Returns the details of a *Docker Hub* user.
- `get_repositories(username, <page_size>, <limit>)`:
  Returns *all* the repositories of a user.  
  It will paginate through pages having `page_size` results at most (default: `100`)
  and will limit the total maximum results to `limit` (default: `10000`)
- `get_repository(username, repository_name)`:
  Returns the details of a single repository.
- `get_tags(username, repository_name, <page_size>, <limit>)`:
  Returns *all* the available tags of a repository.  
  It will paginate through pages having `page_size` results at most (default: `100`)
  and will limit the total maximum results to `limit` (default: `1000`)
- `get_dockerfile(username, repository_name)`:
  Returns the contents of the *raw Dockerfile* of a repository.
- `get_autobuild_settings(username, repository_name)`:
  Returns the autobuild settings of a repository.  
  It will only work for autobuilds.
- `get_comments(username, repository_name, <page_size>, <limit>)`:
  Returns *all* the comments of a repository.
  It will paginate through pages having `page_size` results at most (default: `100`)
  and will limit the total maximum results to `limit` (default: `1000`)
- `get_build_history(username, repository_name, <page_size>, <limit>)`:
  Returns the details for *all* the builds of a repository.
  It will paginate through pages having `page_size` results at most (default: `100`)
  and will limit the total maximum results to `limit` (default: `1000`)
- `get_build_details(username, repository_name, build_code)`:
  Returns the details of a single build of a repository.

The `app` module is responsible for the *REST* presentation layer exposing *JSON* endpoints.
The exposed endpoints are cached using [Flask-Cache](https://pythonhosted.org/Flask-Cache).

Configuration options:

- `HTTP_HOST`: the host (interface) for *Flask* to bind to (default: `127.0.0.1`)
- `HTTP_PORT`: the port to bind to (default: `5000`)
- `CORS_ORIGINS`: comma separated list of *origins* to allow *cross-domain* `GET` requests from
  (default: `http://localhost:?.*`)

To allow connections from other hosts apart from `localhost` set the `HTTP_PORT` environment
variable to `0.0.0.0` or as appropriate.

List of endpoints:

- `/users/<username>`:
  returns the *Docker Hub* user's details
- `/repositories/<username>`:
  returns the user's repositories
- `/repositories/<username>/<repository>`:
  returns the details of a single repository
- `/repositories/<username>/<repository>/tags`:
  returns the available tags of a repository
- `/repositories/<username>/<repository>/dockerfile`:
  returns the *raw Dockerfile* of a repository (for autobuilds)
- `/repositories/<username>/<repository>/autobuild`:
  returns the autobuild settings of a repository
- `/repositories/<username>/<repository>/comments`:
  returns the comments of a repository
- `/repositories/<username>/<repository>/builds`:
  returns the list of builds for a repository
- `/repositories/<username>/<repository>/builds/<build_code>`:
  returns the details of a single build for a repository

## Docker

The web application is built as a *Docker* image too based on *Alpine Linux*
for 3 architectures with the following tags:

- `latest`: for *x86* hosts  
  [![Layers](https://images.microbadger.com/badges/image/rycus86/dockerhub-proxy.svg)](https://microbadger.com/images/rycus86/dockerhub-proxy "Get your own image badge on microbadger.com")
- `armhf`: for *32-bits ARM* hosts  
  [![Layers](https://images.microbadger.com/badges/image/rycus86/dockerhub-proxy:armhf.svg)](https://microbadger.com/images/rycus86/dockerhub-proxy:armhf "Get your own image badge on microbadger.com")
- `aarch64`: for *64-bits ARM* hosts  
  [![Layers](https://images.microbadger.com/badges/image/rycus86/dockerhub-proxy:aarch64.svg)](https://microbadger.com/images/rycus86/dockerhub-proxy:aarch64 "Get your own image badge on microbadger.com")

`latest` is auto-built on [Docker Hub](https://hub.docker.com/r/rycus86/dockerhub-proxy)
while the *ARM* builds are uploaded from [Travis](https://travis-ci.org/rycus86/dockerhub-proxy).

To run it:
```shell
docker run -d --name="dockerhub-proxy" -p 5000:5000          \
  -e DOCKERHUB_USERNAME='user' -e DOCKERHUB_PASSWORD='pass'  \
  -e CORS_ORIGINS='http://site.example.com,*.website.com'    \
  rycus86/dockerhub-proxy:latest
```

Or with *docker-compose* (for a *Raspberry Pi* for example):
```yaml
version: '2'
services:

  dockerhub-proxy:
    image: rycus86/dockerhub-proxy:armhf
    read_only: true
    expose:
      - "5000"
    restart: always
    environment:
      - HTTP_HOST=0.0.0.0
    env_file:
      - dockerhub-secrets.env
```

This way you can keep the secrets in the `env_file` instead of passing them to the *Docker*
client from the command line.
