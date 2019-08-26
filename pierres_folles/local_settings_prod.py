# -*- coding: utf-8 -*-

import sys

DEBUG = False
#SERVE_STATIC = True

ADMINS = (
    ('Luc JEAN', 'ljean@apidev.fr'),
)

MANAGERS = ADMINS

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'test.db',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'apidev_soucourse',
            'USER': 'apidev_soucourse',
            'PASSWORD': '@fond-la-F8urme',
            'HOST': 'postgresql-apidev.alwaysdata.net',
            'PORT': '',
        }
    }

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    'www.course-des-pierres-folles.fr',
    'www.course-des-pierres-folles.fr.',
    'course-des-pierres-folles.fr',
    'course-des-pierres-folles.fr.',
    'staging.course-des-pierres-folles.fr',
    'staging.course-des-pierres-folles.fr.',
]

EMAIL_HOST = 'smtp-apidev.alwaysdata.net'
EMAIL_PORT = 25
EMAIL_SUBJECT_PREFIX = 'course-des-pierres-folles '
EMAIL_HOST_PASSWORD = '@fond-la-F8urme'
EMAIL_HOST_USER = 'contact@course-des-pierres-folles.fr'
SECRET_KEY = '8!-1hjkhk@6tGhgejjhvs6GnJnge7$Op9.=+/lE'

DEFAULT_FROM_EMAIL = 'La Course des Pierres Folles <contact@course-des-pierres-folles.fr>'
COOP_CMS_FROM_EMAIL = DEFAULT_FROM_EMAIL

WKHTMLTOPDF_CMD = r'/home/apidev/utils/bin/wkhtmltopdf-amd64'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
        },
        'coop_cms': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
        },
        'balafon_crm': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
        },
    }
}

COOP_CMS_TEST_EMAILS = (
    u'luc.jean.42@free.fr',
    u'luc_jean_42@yahoo.fr',
    u'ljean@apidev.fr',
    u'luc.jean@gmail.com',
    u'ljean-42810@laposte.net',
    u'jean.luc0560@orange.fr',
)

#sys.path.insert(1, '/home/apidev/customers/sou-rozier/course/env/lib/python2.6/site-packages/')

