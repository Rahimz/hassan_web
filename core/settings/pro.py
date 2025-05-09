from .base import *

SECRET_KEY = pro_secret_key

DEBUG = False 

ALLOWED_HOSTS = ['agharebparast.ir', 'www.agharebparast.ir']

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASS,
        'HOST': 'localhost',
        'PORT': DB_PORT,
    }
}

CSRF_TRUSTED_ORIGINS = [
    'https://agharebparast.ir',
    'https://www.agharebparast.ir',
]