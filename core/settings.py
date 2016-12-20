"""
Django settings for core project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import configparser
import email.utils

import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = configparser.ConfigParser()

#Fallback config file
default_config_file_path = os.path.abspath(os.path.join(BASE_DIR, "..", "settings.ini"))

#Actual config file
CONFIG_FILE = os.environ.get("DJANGO_CONFIG_FILE", default_config_file_path)

#Read the config file
config.read(CONFIG_FILE)

DATABASE_URL = config['database']['URL']

DEBUG = config.getboolean('debug', 'DEBUG')

MEDIA_ROOT = config['files']['MEDIA_ROOT']
STATIC_ROOT = config['files']['STATIC_ROOT']

MEDIA_URL = config['urls']['MEDIA_URL']
STATIC_URL = config['urls']['STATIC_URL']

SERVE_STATIC = config.getboolean('debug', 'SERVE_STATIC')
ALLOWED_HOSTS = [host.strip() for host in config['production'].get('ALLOWED_HOSTS', "").split(",")]

STATICFILES_STORAGE = config['files']['STORAGE']

EMAIL_BACKEND = config['email'].get('BACKEND', 'django.core.mail.backends.console.EmailBackend')
SERVER_EMAIL = config['email'].get('SERVER_ADDRESS', 'root@localhost')

TIME_ZONE = config['internationalization']['TIME_ZONE']
LANGUAGE_CODE = config['internationalization']['LANGUAGE_CODE']

ADMINS = [email.utils.parseaddr(a.strip()) for a in config['email']['ERRORS'].split(",")]
MANAGERS = [email.utils.parseaddr(a.strip()) for a in config['email']['MANAGERS'].split(",")]

DATABASES = {'default': dj_database_url.config(default=DATABASE_URL)}
SECRET_KEY = config['django']['SECRET_KEY']


RQ_QUEUES = {
  'default': {
    'HOST': 'localhost',
    'PORT': 6379,
    'DB': 0,
    'DEFAULT_TIMEOUT': 360,
  },
  'syncthing_configurator': {
    'HOST': 'localhost',
    'PORT': 6379,
    'DB': 0,
    'DEFAULT_TIMEOUT': 600
  }
}

# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = ('adminsortable', "django_rq",)

INTERNAL_APPS = (
  'munkimanager', 
  'syncthingmanager',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + INTERNAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'core.urls'

WSGI_APPLICATION = 'core.wsgi.application'

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
    'rq_console': {
      'format': '%(asctime)s %(message)s',
      'datefmt': '%H:%M:%S',
    },
  },
  'handlers': {
    'rq_console': {
      'level': 'INFO',
      'class': 'rq.utils.ColorizingStreamHandler',
      'formatter': 'rq_console',
      'exclude': ['%(asctime)s'],
      
    },
    'mail_admins': {
      'level': 'ERROR',
      'class': 'django.utils.log.AdminEmailHandler',
    }
  },
  'loggers': {
    'rq.worker': {
      'handlers': ['rq_console', 'mail_admins']
    }
  }
}