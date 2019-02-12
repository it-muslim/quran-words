# QuranWords Django App
QuranWords Project in development and production environments.

## Requirements for production
- Docker
- Docker Compose

## Development
- Clone project
- Create *.env* from the example files in the root folder and edit it appropriately
- Install dependencies `pip install -r requirements\development.txt`
- Run `python manage.py runserver`

## Development on Docker
1. Clone project to machine (if you using docker-toolbox it has to be root directory of Windows ec C:/Users/Public/dev/)
2. On windows run terminal with admin rights (docker terminal, powershell), or use bash on Linux.
3. Check your docker daemon is running 
    `docker-machine status` if it is not "Running" `docker-machine start default`
4. Go to project directory 
    `cd /path/to/quran-words`
5. Create .env file from .env.example
    `cp .env.example .env`
6. Edit .env file DJANGO_EXECUTION_ENVIRONMENT line, to run project with postgres database
    `DJANGO_EXECUTION_ENVIRONMENT=PRODUCTION`
7. If it's first time you run project on machine, create volume to store persistent data (postgres)
    `docker volume create --name=postgres`
8. Start containers
    `docker-compose up`
9. At first start it should create database for project, so you need to restart the project
    Stop running containers `Ctrl + C`
    Start them again `docker-compose up`
10. Check  containers are running:
    Django at http://127.0.0.1:8000 (for linux) or http://192.168.99.100:8000 (for windows)
11. To access running container. Start new terminal windows, and run
    `docker exec -it web01 sh`
12. Run migrations for django: 
    `python3 manage.py migrate`