from __future__ import absolute_import

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

import nltk
from supernova.settings import BASE_DIR
import os
nltk.data.path.append(os.path.abspath(os.path.join(BASE_DIR, 'index')))
