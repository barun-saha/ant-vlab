# Django settings for the Advanced Networking Virtual Lab

ANT_PATH = '/home/barun/codes/www/vlabs'
SECRET_KEY_PATH = '/'.join([ANT_PATH, 'secret.txt',])
CREDENTIALS_PATH = '/'.join([ANT_PATH, 'credentials.py',])


from utils import generate_secret_key as GS
from utils import generate_credentials as GC

# Create the secret key and credentials file at target locations
GS.generate_secret(SECRET_KEY_PATH)
GC.generate_credentials(SECRET_KEY_PATH, CREDENTIALS_PATH)


from credentials import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

### Identify environment -- custom settings variable
__ENV_PROD__ = True
###


ADMINS = (
    ('Barun Saha', 'barun<DOT>saha04<AT>gmail<DOT>com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': app_credentials['db_name'],
        'USER': app_credentials['db_user'],
        'PASSWORD': app_credentials['db_password'],
        'HOST': app_credentials['db_host'],
        'PORT': app_credentials['db_port'],
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB'
        },
    }
}


SECRET_KEY = app_credentials['secret_key']
#SECRET_KEY = '*nx6_(1-tqrplw-omsbt8sl&ualjvn)i5rdpsa%yy(ey5ovvr4'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Kolkata'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 2

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"

# Path where the code is placed -- Barun
SITE_BASE_PATH = '/home/barun/codes/www/vlabs/'
#SITE_BASE_PATH = '/home/soumen/Gittest/ant-vlab/src/codes/www/vlabs/'

# Prod
MEDIA_ROOT = SITE_BASE_PATH + 'media/'


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"

MEDIA_URL = '/cse28/ant/v_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

import os

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_URLCONF = 'vlabs.urls'

#TEMPLATES = [
#    {
#        'BACKEND': 'django.template.backends.django.DjangoTemplates',
#        'DIRS': [os.path.join(BASE_DIR, 'templates')],
#        'APP_DIRS': True,
#        'OPTIONS': {
#            'context_processors': [
#                'django.template.context_processors.debug',
#                'django.template.context_processors.request',
#                'django.contrib.auth.context_processors.auth',
#                'django.contrib.messages.context_processors.messages',
#            ],
#        },
#    },
#]

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

    # Prod
    SITE_BASE_PATH + 'templates',
)

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'ant',
    'ns2trace',
    #'django.contrib.comments',
    #'ajaxcomments',
    'ant.templatetags',
    # Change #21, #2
    #'threadedcomments',
    # Change #32,
    'django_js_reverse',
    'django_rq',
)

SESSION_COOKIE_AGE = 1800  # 30 min
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True


#from settings_env.database import *
#from settings_env.secret import *


## Environment specific settings files
#if __ENV_PROD__:
    #from settings_env.production import *
#else:
    #from settings_env.development import *

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_URL = '/ant_static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static_media/')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

REDIS_QNAME = 'q_ant'

RQ_QUEUES = {
    REDIS_QNAME: {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'PASSWORD': app_credentials['redis_password'],
        'DEFAULT_TIMEOUT': 120,
    }
}
