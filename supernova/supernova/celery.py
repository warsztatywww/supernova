from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supernova.settings')

app = Celery('supernova',
             broker='amqp://guest@localhost//',
             backend='amqp://guest@localhost//',
             include=[
                 'bot.tasks',
             ])


if __name__ == '__main__':
    app.start()
