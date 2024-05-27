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
    'django_object_actions',
    'django_filters',
    'api_service.apps.ApiServiceConfig',
    'frontend',
    'rest_framework',
    'websockets',
    'datasets_synchronization',
    'institutions',
    'tags',
    'user_files',
    'biomarkers',
    'feature_selection',
    'statistical_properties',
    'django_generate_secret_key',
    'webpack_loader',
    'django_email_verification',
    'genes',
    'inferences',
    'molecules_details',
    'chunked_upload',
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

# Redis
REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)

# Channels
ASGI_APPLICATION = "multiomics_intermediate.routing.application"
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
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


# Redirection
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
VERSION: str = '5.1.6'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Max result DataFrame row count. If the number of rows is higher
# the DataFrame is truncated. None for prevent truncation
RESULT_DATAFRAME_LIMIT_ROWS: int = int(os.getenv('RESULT_DATAFRAME_LIMIT_ROWS', 300000))

# MongoDB's credentials (should be set as ENV vars)
MONGO_SETTINGS = {
    'username': os.getenv('MONGO_USERNAME', 'root'),
    'password': os.getenv('MONGO_PASSWORD', 'example'),
    'host': os.getenv('MONGO_HOST', '127.0.0.1'),
    'port': os.getenv('MONGO_PORT', '27017'),
    'db': os.getenv('MONGO_DB', 'multiomics'),  # Keep "multiomics" for backward compatibility
    'timeout': os.getenv('MONGO_TIMEOUT_MS', 5000)  # Connection timeout
}

# Celery settings. Uses same Redis as Channels and same RESULT_BACKEND as BROKER_URL
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

# Result experiment table view config
TABLE_SETTINGS = {
    'page_size': os.getenv('TABLE_PAGE_SIZE', 10)  # Default page size
}

# Number of rows in which the CSV or Mongo's collection is retrieved when an Experiment is computed
EXPERIMENT_CHUNK_SIZE: int = int(os.getenv('EXPERIMENT_CHUNK_SIZE', 500))

# Number of elements to compute external sorting in Rust
SORT_BUFFER_SIZE: int = int(os.getenv('SORT_BUFFER_SIZE', 2_000_000))

# Time limit in seconds for a correlation analysis to be computed. If the experiment is not finished in this time, it is
# marked as TIMEOUT_EXCEEDED
COR_ANALYSIS_SOFT_TIME_LIMIT: int = int(os.getenv('COR_ANALYSIS_SOFT_TIME_LIMIT', 10800))  # 3 hours

# Time limit in seconds for a Feature Selectio experiment to be computed. If the experiment is not finished in this time, it is
# marked as TIMEOUT_EXCEEDED
FS_SOFT_TIME_LIMIT: int = int(os.getenv('FS_SOFT_TIME_LIMIT', 10800))  # 3 hours

# Time limit in seconds for a StatisticalValidation to be computed. If It's not finished in this time, it is
# marked as TIMEOUT_EXCEEDED
STAT_VALIDATION_SOFT_TIME_LIMIT: int = int(os.getenv('STAT_VALIDATION_SOFT_TIME_LIMIT', 10800))  # 3 hours

# Time limit in seconds for a TrainedModel to be computed. If It's not finished in this time, it is
# marked as TIMEOUT_EXCEEDED
TRAINED_MODEL_SOFT_TIME_LIMIT: int = int(os.getenv('TRAINED_MODEL_SOFT_TIME_LIMIT', 10800))  # 3 hours

# Time limit in seconds for an InferenceExperiment to be computed. If It's not finished in this time, it is
# marked as TIMEOUT_EXCEEDED
INFERENCE_SOFT_TIME_LIMIT: int = int(os.getenv('INFERENCE_SOFT_TIME_LIMIT', 10800))  # 3 hours

# Time limit in seconds for a CGDSStudy to be synchronized. If It's not finished in this time, it is
# marked as TIMEOUT_EXCEEDED
SYNC_STUDY_SOFT_TIME_LIMIT: int = int(os.getenv('SYNC_STUDY_SOFT_TIME_LIMIT', 3600))  # 1 hour

# Number of elements to format the INSERT query statement from an experiment's result. This prevents memory errors
INSERT_CHUNK_SIZE: int = int(os.getenv('INSERT_CHUNK_SIZE', 1000))

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

# Django email settings (https://docs.djangoproject.com/en/3.2/ref/settings/#email)
EMAIL_NEW_USER_CONFIRMATION_ENABLED: bool = os.getenv('EMAIL_NEW_USER_CONFIRMATION_ENABLED', 'false') == 'true'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT: int = int(os.getenv('EMAIL_PORT', 0))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@multiomix.org')

# Django email verification settings (https://pypi.org/project/django-email-verification/0.0.7/)
EMAIL_ACTIVE_FIELD = 'is_active'
EMAIL_SERVER = EMAIL_HOST
EMAIL_ADDRESS = EMAIL_HOST_USER
EMAIL_FROM_ADDRESS = DEFAULT_FROM_EMAIL
EMAIL_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_MAIL_SUBJECT = os.getenv('EMAIL_MAIL_SUBJECT', 'Confirm your email')
EMAIL_MAIL_HTML = 'mail_body.html'
EMAIL_PAGE_TEMPLATE = 'confirm_template.html'
EMAIL_PAGE_DOMAIN = 'https://multiomix.org'


# Modulector settings
MODULECTOR_SETTINGS = {
    'host': os.getenv('MODULECTOR_HOST', '127.0.0.1'),
    'port': os.getenv('MODULECTOR_PORT', '8001')
}

# BioAPI settings
BIOAPI_SETTINGS = {
    'host': os.getenv('BIOAPI_HOST', '127.0.0.1'),
    'port': os.getenv('BIOAPI_PORT', '8002')
}

# Multiomix-aws-emr
AWS_EMR_SETTINGS = {
    'host': os.getenv('AWS_EMR_HOST', '127.0.0.1'),
    'port': os.getenv('AWS_EMR_PORT', '8003'),
    'shared_folder_data': os.getenv('AWS_EMR_SHARED_FOLDER_DATA', '/data-spark'),
    'shared_folder_results': os.getenv('AWS_EMR_SHARED_FOLDER_RESULTS', '/results-spark')
}

# If True, indicates that the service of Multiomix-aws-emr is enabled
# (https://github.com/omics-datascience/multiomix-aws-emr)
ENABLE_AWS_EMR_INTEGRATION: bool = os.getenv('ENABLE_AWS_EMR_INTEGRATION', 'false') == 'true'

# If True, sends the 'debug' parameter to Multiomix-aws-emr service to log the Spark execution
EMR_DEBUG_IS_ENABLED: bool = os.getenv('EMR_DEBUG_IS_ENABLED', 'false') == 'true'

# Value used to indicate tha data is not present in a dataset
NON_DATA_VALUE: str = 'NA'


# Feature Selection settings

# Number of cores used to run the survival RF model
N_JOBS_RF: int = int(os.getenv('N_JOBS_RF', 1))

# Number of cores used to compute CrossValidation
N_JOBS_CV: int = int(os.getenv('N_JOBS_CV', 1))

# Number of cores used to compute GridSearch for the CoxNetSurvivalAnalysis
COX_NET_GRID_SEARCH_N_JOBS: int = int(os.getenv('COX_NET_GRID_SEARCH_N_JOBS', 2))

# Minimum and maximum number of iterations user can select to run the BBHA/PSO algorithm
MIN_ITERATIONS_METAHEURISTICS: int = int(os.getenv('MIN_ITERATIONS_METAHEURISTICS', 1))
MAX_ITERATIONS_METAHEURISTICS: int = int(os.getenv('MAX_ITERATIONS_METAHEURISTICS', 20))

# Minimum and maximum number of stars in the BBHA algorithm
MIN_STARS_BBHA: int = int(os.getenv('MIN_STARS_BBHA', 5))
MAX_STARS_BBHA: int = int(os.getenv('MAX_STARS_BBHA', 90))

# Maximum number of features to select in the CoxRegression algorithm
MAX_FEATURES_COX_REGRESSION: int = int(os.getenv('MAX_FEATURES_COX_REGRESSION', 60))

# Maximum number of features to allow to run a Blind Search algorithm (the number of computed combination is _N!_).
# If the number of features is greater than this value, the algorithm is disabled and only metaheuristic
# algorithms are allowed
MAX_FEATURES_BLIND_SEARCH: int = int(os.getenv('MAX_FEATURES_BLIND_SEARCH', 7))

# Minimum number of features to allow the user to run metaheuristics algorithms (>=). This prevents to run metaheuristic
# on datasets with a small number of features which leads to experiments with more metaheuristics agents than number
# of total features combinations. We recommend to set this parameter to a value N such that
# N! > maxNumberOfAgents * maxNumberMetaheuristicsIterations.
# Also, this must be less than or equal to the MAX_FEATURES_BLIND_SEARCH value
MIN_FEATURES_METAHEURISTICS: int = int(os.getenv('MIN_FEATURES_METAHEURISTICS', 7))

# Minimum number of combinations to allow the Spark execution (if less, the execution is done locally). This is computed
# as the number of agents in the metaheuristic multiplied by the number of iterations. This prevents to run Spark jobs
# (which are slow to start) on small experiments to save time and resources.
# Only considered if the Spark execution is enabled (ENABLE_AWS_EMR_INTEGRATION = True)
MIN_COMBINATIONS_SPARK: int = int(os.getenv('MIN_COMBINATIONS_SPARK', 60))
