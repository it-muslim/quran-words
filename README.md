# Quran Words API
[![Build Status](https://travis-ci.org/it-muslim/quran-words.svg?branch=master)](https://travis-ci.org/it-muslim/quran-words)
## Setup
### Requirements
*Production*:

[docker, docker-compose](https://www.docker.com/products/docker-desktop)

*Development*:

[git](https://git-scm.com/), 
[python3.6 or later](https://www.python.org/), 
[pip](https://pypi.python.org/pypi)

### Setup steps

Run the following terminal commands to get started:

*Production*

- `git clone https://github.com/it-muslim/quran-words.git`
- `cd quran-words`
- `cp .env.example .env`
- `pip install -r django\requirements\development.txt`
- `python django\manage.py runserver`
- `python django\manage.py createsuperuser`

*Development*

- `git clone https://github.com/it-muslim/quran-words.git`
- `docker-machine start default`
- `cd quran-words`
- `cp .env.example .env`
- Edit .env file DJANGO_EXECUTION_ENVIRONMENT line, to run project with postgres database
    `DJANGO_EXECUTION_ENVIRONMENT=PRODUCTION`
    `DEBUG=0`
- Windows: If it's first time you run project on machine, create volume to store persistent data (postgres)

    `docker volume create --name=postgres`

    and run

    `docker-compose -f docker-compose-win.yml up`
- Linux/macOS::
    `docker-compose up`
- Check  containers are running:
    - Windows: http://192.168.99.100/admin/
    - Linux/macOS: at http://127.0.0.1/admin/

## Testing

You can run the tests using the following command

`python django/manage.py test`

Additional information can be found in
[our wiki](https://github.com/it-muslim/quran-words/wiki/Tests)

## Documentation

You can access documentation by relative `/api/` path of running api server
API schema located at `/api/schema/`

# Quran Words frontend
## Setup

Run the following terminal commands to get started:
    `cd frontend/angular`
    `npm install`
    `npm run start`
    access frontend at [http://127.0.0.1:4200](http://127.0.0.1:4200)
