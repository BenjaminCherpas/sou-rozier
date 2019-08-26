# -*- coding: utf-8 -*-

import os.path
import sys


DEBUG = True

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite3.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr'

gettext = lambda s: s
LANGUAGES = (
    ('fr', gettext(u'Français')),
    #('en', gettext(u'English')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.abspath(PROJECT_PATH+'/public/media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.abspath(PROJECT_PATH+'/public/static/')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath(PROJECT_PATH+'/static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.abspath(PROJECT_PATH + '/templates')
        ],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                'django.template.context_processors.request',
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.contrib.messages.context_processors.messages",
                "balafon.Search.context_processors.quick_search_form",
                "balafon.Crm.context_processors.crm",
                "balafon.Users.context_processors.user_config",
                'pierres_folles.course.context_processors.homepage',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'debug': DEBUG,
        },

    },
]

MIDDLEWARE = (
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    "coop_cms.utils.RequestMiddleware",
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'pierres_folles.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'pierres_folles.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'coop_cms.perms_backends.ArticlePermissionBackend',
    'django.contrib.auth.backends.ModelBackend',  # Django's default auth backend
    'coop_cms.apps.email_auth.auth_backends.EmailAuthBackend'
)

# LOCALE_PATHS = (
#     PROJECT_PATH+'/locale/',
# )
#
# LOCALE_INDEPENDENT_MEDIA_URL = True
# import re
# LOCALE_INDEPENDENT_PATHS = (
#   re.compile('^/sitemap\.xml$'),
#   #re.compile('^/crm/.*$'),
# )

#SOUTH_SKIP_MIGRATIONS = True
#SOUTH_TESTS_MIGRATE = False

EMAIL_IMAGE_FOLDER = 'emailing'
SEARCH_FORM_LIST = 'balafon.config.SEARCH_FORMS'
BALAFON_DEFAULT_COUNTRY = 'France'
BALAFON_MY_COMPANY = "La Course des Pierres Folles"
BALAFON_AS_HOMEPAGE = False
BALAFON_NOTIFICATION_EMAIL = 'ljean@apidev.fr'
BALAFON_NO_ENTITY_TYPE = True
# BALAFON_NEWSLETTER_SOURCES = (
#    ('', '#content'),
#)

#BALAFON_PDF_TEMPLATES = (
#    ('pdf/small_labels.html', gettext(u'small labels')),
#    ('pdf/address_strip.html', gettext(u'address strip')),
#    ('pdf/list_of_actions.html', gettext(u'Liste des actions')),
#)


# BALAFON_PDF_FORM_EXTRA_FIELDS = (
#     ('start_at', 'Etiquettes blanches', '0'),
# )
#
#
# def start_at_label_context_patch(template, context):
#     contacts = context['contacts']
#     try:
#         start_at = int(context['start_at'])
#     except ValueError:
#         start_at = 0
#     context['contacts'] = [None]*start_at + list(contacts)
#     return context
#
#
# BALAFON_PDF_FORM_CONTEXT_HOOKS = {
#     'pdf/agipa_21.html': start_at_label_context_patch,
# }


#LOCALE_REDIRECT_PERMANENT = False
#COOP_CMS_ARTICLE_CLASS = 'apps.content.models.Page'
#COOP_CMS_NAVTREE_CLASS = 'content.NavTree'
#COOP_BAR_MODULES = ('balafon.Emailing.coop_bar_cfg',)
#COOP_BAR_MODULES = ('apps.content.coop_bar_cfg',)
#DJALOHA_LINK_MODELS = ('content.Page',)
COOP_HTML_EDITOR = 'ck-editor'
HTML_EDITOR_LINK_MODELS = ('basic_cms.Article',)
COOP_CMS_ARTICLE_LOGO_SIZE = "1200"
COOP_CMS_NEWSLETTER_TEMPLATES = (
    ('newsletters/basic_newsletter.html', u'Newsletter Course'),
)
CKEDITOR_CSS_CLASSES = [
    #"{name: 'Highlight', element: 'span', attributes: {'class': 'highlight'}}",
    #"{name: 'Red Title', element: 'h3', styles: {color: '#880000'}}",
]
COOP_CMS_ARTICLE_TEMPLATES = (
    ('homepage.html', u'Accueil'),
    ('standard.html', u'Standard'),
    ('standard_nologo.html', u'Standard sans logo'),
    ('standard_sponsors.html', u'Standard sponsors'),
)
COOP_CMS_FROM_EMAIL = u'"La course des Pierres Folles" <contact@la-course-des-pierres-folles.fr>'
COOP_CMS_TEST_EMAILS = ('"Your name" <coop_cms@mailinator.com>',)
COOP_CMS_SITE_PREFIX = ''
COOP_CMS_REPLY_TO = 'contact@la-course-des-pierres-folles.fr'
COOP_CMS_TITLE_OPTIONAL = True
THUMBNAIL_FORMAT = 'PNG'
LOGIN_REDIRECT_URL = "/"

#COMMENTS_APP = "site1.agenda"

PAYPLUG_SETTINGS = {
    'base_url': 'https://www.payplug.com/p/CmYJ',
}

INSCRIPTIONS_ACTIVE = False

INSTALLED_APPS = (
    #contribs
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    #balafon
    'balafon',
    'balafon.Crm',
    'balafon.Search',
    'balafon.Emailing',
    #'balafon.Profile',
    'balafon.Users',

    #externals
    'coop_html_editor',
    #'html_field',
    'colorbox',
    'coop_cms.apps.coop_bootstrap',
    'coop_cms',
    'coop_bar',
    'coop_cms.apps.basic_cms',
    #'coop_cms.apps.rss_sync',
    #'jhouston',
    
    #3rd parties
    'django_extensions',
    'floppyforms',
    'sorl.thumbnail',
    #'modeltranslation'
    'wkhtmltopdf',
    'snowpenguin',

    'sortedm2m',
    'photologue',

    'pierres_folles.course',
    
    'django.contrib.admin',
    'django.contrib.admindocs',
)

if len(sys.argv) > 1 and 'test' == sys.argv[1]:
    INSTALLED_APPS = INSTALLED_APPS + ('coop_cms.apps.test_app',)


# import warnings
# warnings.filterwarnings('ignore', r"django.contrib.localflavor is deprecated")
# warnings.filterwarnings('ignore', "django.conf.urls.defaults is deprecated; use django.conf.urls instead")
# warnings.filterwarnings(
#     'ignore', "django.contrib.localflavor is deprecated. Use the separate django-localflavor-* packages instead."
# )
try:
    from .local_settings import *
except ImportError:
    from .local_settings_prod import *
