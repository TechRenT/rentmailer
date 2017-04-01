from eflowerlite.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    'localhost',
    '162.243.125.175',
]

SECRET_KEY = get_env_variable("SECRET_KEY")