# <img src="https://uploads-ssl.webflow.com/5ea5d3315186cf5ec60c3ee4/5edf1c94ce4c859f2b188094_logo.svg" alt="Pip.Services Logo" width="200"> <br/> Commandline Template Engine application in Python

This application is the implementation of the Template Engine V1 in the development of an AI agent
Template Engine V1 - Create software component skeletons from templates

<a name="links"></a> Quick links:

* [API Reference](docs)
* [Change Log](CHANGELOG.md)
* [License](License)
* [ToDo List](TODO.md)
* [Usage Notes](USAGE.md)


## Get

Get the microservice source from BitBucket:
```bash
git clone git@bitbucket.org:entinco/eic-templateengine.git
```

Install the microservice dependencies:
```bash
cd cmd-templateengine-python

pip install -r requirements.txt
```

Get docker image for the microservice:
```bash
docker pull entinco/cmd-templateengine-python:latest
```

Launch the microservice with all infrastructure services using docker-compose:
```bash
docker-compose -f ./docker/docker-compose.yml
```

## Develop

For development you shall install the following prerequisites:
* Python 3.6+
* Visual Studio Code or another IDE of your choice
* Docker

Install dependencies:
```bash
pip install -r requirements.txt
```

Before running tests launch infrastructure services and required microservices:
```bash
docker-compose -f ./docker-compose.dev.yml up
```

Run automated tests:
```bash
pytest
```

Generate API documentation:
```bash
./docgen.ps1
```

Before committing changes run dockerized build and test as:
```bash
./build.ps1
./test.ps1
./package.ps1
./run.ps1
./clear.ps1
```

## Contacts

This microservice was created by and is currently maintained by *Enterprise Innovation Consulting*.
