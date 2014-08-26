# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'supernova',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'supernova',
        'PASSWORD': 'supernova',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
