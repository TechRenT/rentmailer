from eflowerlite.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    'localhost',
    '162.243.125.175',
]

SECRET_KEY = get_env_variable("SECRET_KEY")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'eflowerlite_prod',
        'USER': 'u_eflowerlite',
        'PASSWORD': 'J3r3m1ah',
        'HOST': 'localhost',
        'PORT': '',
    }
}