#Django settings for AICS project.
import dj_database_url
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
SITE_ROOT=os.path.dirname(os.path.realpath(__file__))

# Celery import
#import djcelery

#djcelery.setup_loader()

DEBUG = True 
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '.herokuapp.com').split(':')
#import dj_database_url

DATABASES = { 
	     'default' : dj_database_url.config(default="sqlite:/AICSDB.db")

		}

#GRAPPELLI_ADMIN_TITLE = 'AICS ADMINISTRATION'


'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'AICSDB',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'blubamboo',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
'''


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Africa/Accra'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"






AWS_ACCESS_KEY_ID = "AKIAJ74LCB66L66FPHGA"
AWS_SECRET_ACCESS_KEY = "mhYmTFrVmaXeGo0kUiGJ4G2CN5htCInxks8662cZ"
AWS_STORAGE_BUCKET_NAME = "aicsfiles"
AWS_S3_CUSTOM_DOMAIN = "aicsfiles"
AWS_REDUCED_REDUNDANCY = False # We enable this server-wide on our staging server's S3 buckets
AWS_PRELOAD_METADATA = True # You want this to be on!
AWS_S3_SECURE_URLS = False
AWS_HEADERS = { 'Cache-Control': 'max-age=2592000' }
AWS_QUERYSTRING_AUTH = False


MY_DEFAULT_STORAGE = 'crew.s3storage.S3BotoStorage' # Used below
DEFAULT_FILE_STORAGE = MY_DEFAULT_STORAGE
COMPRESS_STORAGE = MY_DEFAULT_STORAGE # use with django-compressor
STATICFILES_STORAGE = MY_DEFAULT_STORAGE # use with django-staticfiles
FILER_PUBLICMEDIA_STORAGE = 'crew.example_prefixes.filer_storage_s3' # user with django-filer
# Finally, we want to use reduced redundancy storage for all thumbnails:
FILER_PUBLICMEDIA_THUMBNAIL_STORAGE = 'crew.example_prefixes.filer_thumb_storage_s3'
THUMBNAIL_DEFAULT_STORAGE = 'crew.example_prefixes.S3BotoStorageReducedRedundancy'


MEDIA_ROOT = 'smedia/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/smedia/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = 'static/'



# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths
    os.path.join(SITE_ROOT, 'assets'),
    #os.path.join(SITE_ROOT,'filer/static/filer'),
    #os.path.join(SITE_ROOT,'certificatefiles'),
    #os.path.join(SITE_ROOT,'crewContractfiles'),
    #os.path.join(SITE_ROOT,'crewcertfiles'),
)
FILER_DEBUG = True
# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ')f84@7_!)0rd9m#wmdp%jy@dvtd1we45p4v1x97#l$kvy71nhg'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'AICS.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'AICS.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	os.path.join(SITE_ROOT,'templates'),
)


TEMPLATE_CONTEXT_PROCESSORS = TCP+ (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth'  # admin app wants this too
)

SUIT_CONFIG = {
    
     'MENU': (
	'sites',
          {'app': 'filer','label': 'Files', 'icon':'icon-file'},
          {'app': 'crew', 'label': 'Crew Module','icon':'icon-user','models': ('crew_detail', 'crew_certification','crew_contract','rank','rank_trash')},
          {'app': 'inventory','label': 'Inventory','icon':'icon-th'},
          {'app': 'ports_cargo_opr','label': 'Ports Operation','icon':'icon-tint'},
          {'app': 'vessel','icon':'icon-plane'},
          {'app': 'certificate','icon':'icon-leaf'},
         
          
          
    ),
    'MENU_EXCLUDE': ('django_evolution' ),
    'CONFIRM_UNSAVED_CHANGES': True,
    'SHOW_REQUIRED_ASTERISK': True,
    'SEARCH_URL': '',
    
    'ADMIN_NAME': 'AICS ADMINISTRATION',
    'MENU_OPEN_FIRST_CHILD': True,
    
    
}
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'easy_thumbnails.processors.scale_and_crop',
    #'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)
FILER_STATICMEDIA_PREFIX ='/static/filer/'
FILER_IS_PUBLIC_DEFAULT =False
FILER_ENABLE_PERMISSIONS =False
FILER_PAGINATE_BY = 10


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
   # 'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crew',
    'certificate',
    'countries',
    'vessel',
    'ports_cargo_opr',
    'inventory',
    'aicsUser',
    #'request',
    'model_report',
    'suit',
    'reversion',
    'easy_thumbnails',
    'filer',
    'mptt',
    'storages',
    
    #'djcelery',
    #'scheduler',
    #'kombu.transport.django',
    # Uncomment the next line to enable the admin:
     #'grappelli',
     'django.contrib.admin',
     'django_evolution',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

#BROKER_URL = "django://"




#CELERYBEAT_SCHEDULE = {
    # Executes every Monday morning at 7:30 A.M
   # 'add-every-monday-morning': {
     #   'task': 'tasks.add',
       # 'schedule': crontab(hour=7, minute=30, day_of_week=1),
       # 'args': (16, 16),
  #  },
#}
#CELERY_TIMEZONE = 'UTC'

#CELERY_TIMEZONE = 'Africa/Accra'
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
