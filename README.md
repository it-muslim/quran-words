# QuranWords Django App
QuranWords Project in development and production environments.

## Requirements
- Docker
- Docker Compose

## Development
- Clone project
- Create *.env* from the example files in the root folder and edit as appropriate
- Run `docker-compose up`
- Visit localhost:8000 // or Windows -> http://192.168.99.100:8000/

- connect to django container
 docker exec -it web01 sh

- connect to postgresql container
 docker exec -it db01 sh
 su postgres
 psql

 - To install requirement modules use:
 pip install -r requirements/development.txt


## Production
- Follow the first 2 steps outlined above
- Run `docker-compose -f docker-compose.prod.yml up --build -d`
- Run `docker-compose -f docker-compose.prod.yml run web python3 manage.py migrate`
- Run `docker-compose -f docker-compose.prod.yml run web python3 manage.py collectstatic`
- Visit the website

- To install requirement modules use:
 pip install -r requirements/production.txt
