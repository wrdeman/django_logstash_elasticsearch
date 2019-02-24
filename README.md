# Django app for demonstrating effects of concurrency.

A small and very basic Django application.

## Start
`docker-compose run web django-admin migrate`

`docker-compose run web django-admin loaddate demo/data/initial.json`

`docker-compose exec web python manage.py collectstatic`

`docker-compose up`

# Multiple concurrent requests
To create 100 requests with concurrency=3:
`uname=admin pward=testpassword ./splatter.sh`
