from __future__ import absolute_import

from bot.celery import app

# don't remove 'add' as is serves as a (manual) test for celery

@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)
