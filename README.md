# airflow-docker

This repository contains **Dockerfile** of [apache-airflow](https://github.com/apache/airflow).

## Informations

* Based on Python (3.6-slim) official Image [python:3.6-slim](https://hub.docker.com/_/python/) and uses the official [Postgres](https://hub.docker.com/_/postgres/) as backend and [Redis](https://hub.docker.com/_/redis/) as queue
* Install [Docker](https://www.docker.com/)
* Install [Docker Compose](https://docs.docker.com/compose/install/)
* Following the Airflow release from [Python Package Index](https://pypi.python.org/pypi/apache-airflow)

## Installation

Clone this repository

    git clone https://github.com/saianupkumarp/airflow-docker.git

## Build

Build the airflow (Recommended)

    docker build --rm -t airflow-image:1.10.4 .

Optionally install [Extra Airflow Packages](https://airflow.incubator.apache.org/installation.html#extra-package) and/or python dependencies before build time by adding the following line in the Dockerfile above the line 62:

    && pip install -r requirements.txt \

Optionally install [Extra Airflow Packages](https://airflow.incubator.apache.org/installation.html#extra-package) and/or python dependencies at build time by following command :

    docker build --rm --build-arg AIRFLOW_DEPS="datadog,dask" -t airflow-image:1.10.4 .
    docker build --rm --build-arg PYTHON_DEPS="flask_oauthlib>=0.9" -t airflow-image:1.10.4 .

or combined

    docker build --rm --build-arg AIRFLOW_DEPS="datadog,dask" --build-arg PYTHON_DEPS="flask_oauthlib>=0.9" -t airflow-image:1.10.4 .

## Usage

By default, docker-airflow runs Airflow with **SequentialExecutor** :

    docker run -d -p 8080:8080 airflow-image webserver

If you want to run another executor, use the other docker-compose.yml files provided in this repository.

For **LocalExecutor** :

    docker-compose -f docker-compose-LocalExecutor.yml up -d

For **CeleryExecutor** (Recommended) :

    docker-compose -f docker-compose-CeleryExecutor.yml up -d

If you want to use Ad hoc query, make sure you've configured connections:
Go to Admin -> Connections and Edit "airflow_db" set this values (equivalent to values in airflow.cfg/docker-compose*.yml) :
- Host : postgres
- Schema : airflow
- Login : airflow
- Password : airflow

For encrypted connection passwords (in Local or Celery Executor), you must have the same fernet_key. By default docker-airflow generates the fernet_key at startup which is already in the docker-compose-LocalExecutor.ym, you have to set an environment variable in the docker-compose (ie: docker-compose-LocalExecutor.yml) file to set the same key accross containers. To generate a fernet_key :

    docker run airflow-image python -c "from cryptography.fernet import Fernet; FERNET_KEY = Fernet.generate_key().decode(); print(FERNET_KEY)"

## Custom Airflow plugins

Airflow allows for custom user-created plugins which are typically found in `${AIRFLOW_HOME}/plugins` folder. Documentation on plugins can be found [here](https://airflow.apache.org/plugins.html)

In order to incorporate plugins into your docker container
- Create the plugins folders `plugins/` with your custom plugins.
- Mount the folder as a volume by doing either of the following:
    - Include the folder as a volume in command-line `-v $(pwd)/plugins/:/usr/local/airflow/plugins`
    - Use docker-compose-LocalExecutor.yml which contains support for adding the plugins folder as a volume

## Install custom python package

- Create a file "requirements.txt" with the desired python modules
- Mount this file as a volume `-v $(pwd)/requirements.txt:/requirements.txt` (or add it as a volume in docker-compose file)
- The entrypoint.sh script execute the pip install command (with --user option)

## UI Links

- Airflow: [localhost:8080](http://localhost:8080/)


## Authentication

By default, the config file which is under `config/airflow.cfg` is enabled with web authentication, to disable it, change the boolean value from "True" to "False"

Below is the configuaration to enable,

    # Set to true to turn on authentication:
    # https://airflow.apache.org/security.html#web-authentication
    authenticate = True
    auth_backend = airflow.contrib.auth.backends.password_auth

Follow the below steps to create the users,

Get the container id,

    docker container ls

Jump onto the contianer bash by it's id,

    # With root user
    docker exec -it -u root <container id> bash

Execute the follow script under the airflow folder with in the python console

    python
    import airflow
    from airflow import models, settings
    from airflow.contrib.auth.backends.password_auth import PasswordUser
    from sqlalchemy import create_engine

    user = PasswordUser(models.User())
    user.username = ''
    user.email = ''
    user.password = ''

    # Make the value true if you want the user to be a administrator
    user.superuser = False

    engine = create_engine("postgresql://airflow:airflow@postgres:5432/airflow")
    session = settings.Session(bind=engine)
    session.add(user)
    session.commit()
    session.close()
    exit()

Enter `exit` and hit enter to come out of the container bash

## Steps to clear the docker images and containers

1. List all containers (only IDs)
    ```
    docker ps -aq
    ```
2. Stop all running containers
    ```
    docker stop $(docker ps -aq)
    ```
3. Remove all containers
    ```
    docker rm $(docker ps -aq)
    ```
4. Remove all images
    ```
    docker rmi $(docker images -q)
    ```

NB: Use only incase you want to clear all the dockers and containers

## Docker Compose commands 

To stop

    docker-compose -f docker-compose-*.yml stop

To stop and remove

    docker-compose -f docker-compose-*.yml down

To restart

    docker-compose -f docker-compose-*.yml restart

To bring the container up again

    docker-compose -f docker-compose-*.yml up -d

## TODO

    AWS ECS
    Kubernetes
    Bash Script for Docker cleaning

# Wanna help?

Fork, improve and PR. ;-)
