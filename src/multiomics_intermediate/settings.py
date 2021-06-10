"""
Django settings for multiomics_intermediate project.

Generated by 'django-admin startproject' using Django 3.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from typing import Optional

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$y(kf*_31b@@n_%1h!ae^-fgp%kbi3iu_u#-wj0_btk@#y+aq*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'api_service',
    'frontend',
    'rest_framework',
    'websockets',
    'datasets_synchronization',
    'institutions',
    'tags',
    'user_files',
    'statistical_properties',
    'django_generate_secret_key',
    'webpack_loader',
    'django_email_verification',
    'genes'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'multiomics_intermediate.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'email/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'multiomics_intermediate.context_processors.enable_security',
            ],
        },
    },
]

WSGI_APPLICATION = 'multiomics_intermediate.wsgi.application'

# Channels
ASGI_APPLICATION = "multiomics_intermediate.routing.application"
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(os.getenv('REDIS_HOST', '127.0.0.1'), os.getenv('REDIS_PORT', 6379))],
        },
    },
}

# For Webpack hashing. More in https://owais.lone.pw/blog/webpack-plus-reactjs-and-django/
# Repo: https://github.com/owais/django-webpack-loader
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'frontend/dist/',
        'STATS_FILE': os.path.join(BASE_DIR, 'frontend/static/frontend/dist/webpack-stats.json'),
        'CACHE': not DEBUG
    }
}

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': os.getenv('POSTGRES_USERNAME', 'root'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'example'),
        'HOST': os.getenv('POSTGRES_HOST', '127.0.0.1'),
        'PORT': os.getenv('POSTGRES_PORT', 5432),
        'NAME': os.getenv('POSTGRES_DB', 'multiomics')  # Keep "multiomics" for backward compatibility
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Redirections
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'

# Security settings
ENABLE_SECURITY: bool = os.getenv('ENABLE_SECURITY', 'false') == 'true'
SESSION_COOKIE_SECURE = ENABLE_SECURITY
CSRF_COOKIE_SECURE = ENABLE_SECURITY
SECURE_REFERRER_POLICY = 'same-origin'

# +++++ Custom settings +++++

# Current Multiomix version
VERSION: str = '4.6.0'

# Max result DataFrame row count. If the number of rows is higher
# the DataFrame is truncated. None for prevent truncation
RESULT_DATAFRAME_LIMIT_ROWS: int = int(os.getenv('RESULT_DATAFRAME_LIMIT_ROWS', 300000))

# MongoDB credentials (should be setted as ENV vars)
MONGO_SETTINGS = {
    'username': os.getenv('MONGO_USERNAME', 'root'),
    'password': os.getenv('MONGO_PASSWORD', 'example'),
    'host': os.getenv('MONGO_HOST', '127.0.0.1'),
    'port': os.getenv('MONGO_PORT', '27017'),
    'db': os.getenv('MONGO_DB', 'multiomics'),  # Keep "multiomics" for backward compatibility
    'timeout': os.getenv('MONGO_TIMEOUT_MS', 5000)  # Connection timeout
}

# Result experiment table view config
TABLE_SETTINGS = {
    'page_size': os.getenv('TABLE_PAGE_SIZE', 10)  # Default page size
}

# To compute pending experiment on server start
COMPUTE_PENDING_EXPERIMENTS_AT_STARTUP: bool = os.getenv('COMPUTE_PENDING_EXPERIMENTS_AT_STARTUP', 'true') == 'true'

# Number of rows in which the CSV or Mongo's collection is retrieved when an Experiment is computed
EXPERIMENT_CHUNK_SIZE: int = int(os.getenv('EXPERIMENT_CHUNK_SIZE', 500))

# Number of elements to compute external sorting in Rust
SORT_BUFFER_SIZE: int = int(os.getenv('SORT_BUFFER_SIZE', 2_000_000))

# Number of threads used in ThreadPool to run experiments. Please take memory in consideration
# IMPORTANT: needs a server restart
THREAD_POOL_SIZE: int = int(os.getenv('THREAD_POOL_SIZE', 5))

# Number of elements to format the INSERT query statement from an experiment's result. This prevent memory errors
INSERT_CHUNK_SIZE: int = int(os.getenv('INSERT_CHUNK_SIZE', 1000))

# Indicates if the experiment is computed inside a DB transaction or handle manually by Python
USE_TRANSACTION_IN_EXPERIMENT: bool = os.getenv('USE_TRANSACTION_IN_EXPERIMENT', 'true') == 'true'

# Number of last experiments returned to the user in the "Last experiments" panel in Pipeline page
NUMBER_OF_LAST_EXPERIMENTS: int = int(os.getenv('NUMBER_OF_LAST_EXPERIMENTS', 4))

# Maximum number of open tabs allowed
MAX_NUMBER_OF_OPEN_TABS: int = int(os.getenv('MAX_NUMBER_OF_OPEN_TABS', 8))

# Timeout (in seconds) of connection to cBioPortal in CGDSStudy synchronization
CGDS_CONNECTION_TIMEOUT: int = int(os.getenv('CGDS_CONNECTION_TIMEOUT', 5))

# Timeout (in seconds) of chunk reading in CGDSStudy synchronization
CGDS_READ_TIMEOUT: int = int(os.getenv('CGDS_READ_TIMEOUT', 60))

# Chunk size (in bytes) in which CGDSStudy file is retrieved during CGDSStudy synchronization
CGDS_CHUNK_SIZE: int = int(os.getenv('CGDS_CHUNK_SIZE', 2097152))  # Default 2MB

# Threshold to check if the GEM data is ordinal or continuous. If the number of different values is <= this value
# it's considered ordinal
THRESHOLD_ORDINAL: int = int(os.getenv('THRESHOLD_ORDINAL', 5))

# Threshold of GEM file size (in MB) to make the GEM dataset available in memory. This has a HUGE impact in analysis
# performance. If the size is less or equal this thresholds, it's allocated in memory, otherwise it'll be read lazily
# from disk. If it's None GGCA allocates in memory automatically when GEM dataset size is small (<= 100MB)
THRESHOLD_GEM_SIZE_TO_COLLECT: Optional[int]
threshold_gem_size_to_collect_str: Optional[str] = os.getenv('THRESHOLD_GEM_SIZE_TO_COLLECT')
if threshold_gem_size_to_collect_str is not None:
    THRESHOLD_GEM_SIZE_TO_COLLECT = int(threshold_gem_size_to_collect_str)
else:
    THRESHOLD_GEM_SIZE_TO_COLLECT = None

# Django email settings. All this settings are got from https://pypi.org/project/django-email-verification/
EMAIL_NEW_USER_CONFIRMATION_ENABLED: bool = os.getenv('EMAIL_NEW_USER_CONFIRMATION_ENABLED', 'false') == 'true'
EMAIL_ACTIVE_FIELD = 'is_active'
EMAIL_SERVER = os.getenv('EMAIL_SERVER')
EMAIL_PORT: int = int(os.getenv('EMAIL_PORT', 0))
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_FROM_ADDRESS = os.getenv('EMAIL_FROM_ADDRESS', 'noreply@multiomix.org')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_MAIL_SUBJECT = os.getenv('EMAIL_MAIL_SUBJECT', 'Confirm your email')
EMAIL_MAIL_HTML = 'mail_body.html'
EMAIL_PAGE_TEMPLATE = 'confirm_template.html'
EMAIL_PAGE_DOMAIN = 'https://multiomix.org'

# Modulector settings
MODULECTOR_SETTINGS = {
    'host': os.getenv('MODULECTOR_HOST', '127.0.0.1'),
    'port': os.getenv('MODULECTOR_PORT', '8001')
}

# Value used to indicate tha data is not present in a dataset
NON_DATA_VALUE: str = 'NA'
