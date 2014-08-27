# Supernova

> The best web search written in 3 days on [Summer Scientific Schools](http://warsztatywww.wikidot.com/en).

## Installation

    $ git clone git@github.com:pathes/supernova.git
    $ cd supernova

    $ virtualenv .  # or: virtualenv -p python3 .
    $ . bin/activate
    
    $ pip install -r requirements.txt
    # if does not work, start with with installing Django
    $ pip install https://www.djangoproject.com/download/1.7c3/tarball/

    $ supernova/manage.py migrate

## Run

    $ supernova/manage.py runserver

## Celery

    $ rabbitmq-server
    $ celery -A bot worker -l info

To test:

    $ ./manage.py shell

    >>> from bot import tasks
    >>> x = tasks.add.delay(5,5)  # or with other function from tasks
    >>> x.status
    'SUCCESS'
    >>> x.get()
    10

