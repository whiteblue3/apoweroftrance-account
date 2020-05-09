"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import json
from django.conf.locale.en import formats as en_formats
from google.oauth2 import service_account
import logging.config
from django.utils.log import DEFAULT_LOGGING

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_FILE = os.path.join(BASE_DIR, 'secret.json')

secret = json.loads(open(SECRET_FILE).read())


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret['SECRET_KEY']
JWT_SECRET_KEY = secret['JWT_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'rangefilter',
    'django_admin_listfilter_dropdown',
    'admin_numeric_filter',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    'app',
    'accounts',

    'rest_framework',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'drf_yasg.middleware.SwaggerExceptionMiddleware',
    'app.remove_next_middleware.RemoveNextMiddleware',
    'app.json404_middleware.JSON404Middleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USERNAME'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT')
    },
}


# https://jupiny.com/2018/02/27/caching-using-redis-on-django/
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{0}:{1}/{2}".format(
            os.environ.get('REDIS_URL'), os.environ.get('REDIS_PORT'), os.environ.get('REDIS_DB')
        ),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_FORMAT = 'Y-m-d'

DATETIME_FORMAT = 'Y-m-d G:i:s'

DATE_INPUT_FORMATS = (
    '%Y-%m-%d',
)
TIME_INPUT_FORMATS = (
    '%H:%M:%S',
)
DATETIME_INPUT_FORMATS = (
    '%Y-%m-% %H:%M:%S',
)

en_formats.DATETIME_FORMAT = 'Y-m-d G:i:s.u'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# # Local storage
# STATIC_URL = '/static/'
# STATIC_DIR = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [
#     STATIC_DIR,
# ]
# STATIC_ROOT = os.path.join(BASE_DIR, '.static')

# Uncomment using cloud storage
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# https://blog.jun2.org/development/2019/07/23/django-security-options.html

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 63072000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
X_FRAME_OPTIONS = 'SAMEORIGIN'


HTTP_PROTOCOL = "http"
DOMAIN_URL = "127.0.0.1:8081"


# Disable Django's logging setup
LOGGING_CONFIG = None

LOGLEVEL = os.environ.get('LOGLEVEL', 'info').upper()

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        # 'file': {
        #             'level': 'INFO',
        #             'class': 'logging.handlers.TimedRotatingFileHandler',
        #             'filename': os.path.join('/var/log/uwsgi/app', 'django'),
        #             'when': 'D',  # this specifies the interval
        #             'interval': 1,  # defaults to 1, only necessary for other values
        #             'backupCount': 7,  # how many backup file to keep, 7 days
        #             'formatter': 'default',
        #         },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
    },
    'loggers': {
        # default for all undefined Python modules
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        # '': {
        #     'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        #     'handlers': ['console'],
        # },
        # # Our application code
        # 'app': {
        #     'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        #     # Avoid double logging because of root logger
        #     'propagate': False,
        # },
        # # Prevent noisy modules from logging to Sentry
        # 'noisy_module': {
        #     'level': 'ERROR',
        #     'handlers': ['console'],
        #     'propagate': False,
        # },
        # Default runserver request logging
        'django.server': DEFAULT_LOGGING['loggers']['django.server'],
    },
})


##################
# JWT Auth Setup #
##################

AUTH_USER_MODEL = 'accounts.User'

# Configure the accounts in Django Rest Framework to be JWT
# http://www.django-rest-framework.org/
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'accounts.backends.JWTAuthentication',
    ),
    'EXCEPTION_HANDLER': 'app.exceptions.core_exception_handler',
}

AUTHENTICATION_BACKENDS = (
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',
    'django.contrib.auth.backends.ModelBackend',
    'accounts.backends.JWTAuthentication',
)


#################
# Swagger Setup #
#################

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        },
    },
}


################
# AWS S3 Setup #
################

# AWS_ACCESS_KEY_ID = config_secret_common['AWS_ACCESS_KEY_ID']
# AWS_SECRET_ACCESS_KEY = config_secret_common['AWS_SECRET_ACCESS_KEY']
#
# AWS_S3_REGION_NAME = 'ap-northeast-2'
# AWS_S3_SIGNATURE_VERSION = 's3v4'
#
# STATICFILES_LOCATION = 'static'
# STATICFILES_STORAGE = 'django_utils.storage_backend.s3_backend.StaticStorage'
# AWS_DEFAULT_ACL = None
# AWS_S3_ENCRYPTION = False
# DEFAULT_FILE_STORAGE = 'django_utils.storage_backend.s3_backend.MediaStorage'
# MEDIAFILES_LOCATION = 'media'

# AWS_STORAGE_BUCKET_NAME = 'api-prod-gloground-com'
#
# # STORAGE_DOMAIN = '%s.s3-accelerate.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# STORAGE_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME)
# STATIC_URL = "https://%s/%s/" % (STORAGE_DOMAIN, STATICFILES_LOCATION)


##############################
# Google Cloud Storage Setup #
##############################

GCP_PROJECT_ID = secret['GCP_PROJECT_ID']
GCP_STORAGE_BUCKET_NAME = secret['GCP_STORAGE_BUCKET_NAME']
GCP_SERVICE_ACCOUNT_JSON = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
GCP_USE_SERVICE_ACCOUNT_JSON = True

STORAGE_DOMAIN = "https://storage.cloud.google.com/%s" % GCP_STORAGE_BUCKET_NAME

GS_CREDENTIALS = service_account.Credentials.from_service_account_file(GCP_SERVICE_ACCOUNT_JSON)
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = secret['GS_BUCKET_NAME']

STATIC_URL = "https://storage.cloud.google.com/%s/" % GS_BUCKET_NAME


#####################
# File Upload Setup #
#####################

FILE_UPLOAD_PERMISSIONS = 0o777
FILE_UPLOAD_MAX_MEMORY_SIZE = 10240000
DATA_UPLOAD_MAX_MEMORY_SIZE = 10240000

STORAGE_DRIVER = "gcs"


#############
# AES Setup #
#############

AES_KEY = secret['AES_KEY']
AES_SECRET = secret['AES_SECRET']


###############
# Email Setup #
###############

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = secret['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = secret['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER


#################
# Account Setup #
#################

ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS =1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
# ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400 # 1 day in seconds
# ACCOUNT_LOGOUT_REDIRECT_URL = '/'

AUTH_DOMAIN_URL = "127.0.0.1:8081"
ACCOUNT_API_PATH = "/v1/user"


ACTIVATE_ACCOUNT_EMAIL_TITLE = "회원가입 이메일 인증 안내"
ACTIVATE_ACCOUNT_EMAIL_BODY = "안녕하세요.\n" \
                              "\n" \
                              "A Power of Trance 의 회원이 되신 것을 진심으로 축하드립니다\n" \
                              "아래 링크를 클릭하면 회원가입 인증이 완료됩니다\n" \
                              "\n" \
                              "%s\n" \
                              "\n" \
                              "감사합니다\n"
ACTIVATE_ACCOUNT_EMAIL_HTML = "<!DOCTYPE html><html lang='kr'><body>안녕하세요.<br />" \
                              "<br />" \
                              "A Power of Trance 의 회원이 되신 것을 진심으로 축하드립니다<br />" \
                              "아래 링크를 클릭하면 회원가입 인증이 완료됩니다<br />" \
                              "<br />" \
                              "<a href='%s' target='_blank'>회원가입 완료하기</a><br />" \
                              "감사합니다</body></html>"

RESET_PASSWORD_EMAIL_TITLE = "비밀번호 재설정 안내"
RESET_PASSWORD_EMAIL_BODY = "회원님 안녕하세요.\n" \
                            "\n" \
                            "비밀번호 재설정을 요청하셨습니다.\n" \
                            "임시 비밀번호는 %s 입니다\n" \
                            "아래의 링크를 눌러 비밀번호를 재설정을 완료하세요.\n" \
                            "\n" \
                            "%s\n" \
                            "\n" \
                            "※ 회원님께서 위의 링크를 클릭하지 않으면 임시비밀번호는 최종 변경되지 않습니다.\n" \
                            "※ 회원님께서 재설정 요청을 하지 않은 경우 아무런 조치를 취하실 필요가 없습니다.\n" \
                            "※ 해당 메일은 답장 하실 수 없습니다. 궁금한 점이 있다면, 아래로 문의해 주시기 바랍니다.\n" \
                            "- 문의 메일 : apoweroftrance@gmail.com\n" \
                            "\n" \
                            "감사합니다\n"
RESET_PASSWORD_EMAIL_HTML = "<!DOCTYPE html><html lang='kr'><body>회원님 안녕하세요.<br />" \
                            "<br />" \
                            "비밀번호 재설정을 요청하셨습니다.<br />" \
                            "임시 비밀번호는 %s 입니다<br />" \
                            "아래의 링크를 눌러 비밀번호를 재설정하세요.<br />" \
                            "<br />" \
                            "<a href='%s' target='_blank'>비밀번호 재설정하기</a><br />" \
                            "<br />" \
                            "※ 회원님께서 위의 링크를 클릭하지 않으면 임시비밀번호는 최종 변경되지 않습니다.<br />" \
                            "※ 회원님께서 재설정 요청을 하지 않은 경우 아무런 조치를 취하실 필요가 없습니다.<br />" \
                            "※ 해당 메일은 답장 하실 수 없습니다. 궁금한 점이 있다면, 아래로 문의해 주시기 바랍니다.<br />" \
                            "- 문의 메일 : apoweroftrance@gmail.com<br />" \
                            "<br />" \
                            "<br />" \
                            "감사합니다</body></html>"

NOTIFY_SECURITY_ALERT_EMAIL_TITLE = "신규 로그인 알림"
NOTIFY_SECURITY_ALERT_EMAIL_BODY = "새로운 디바이스에서 계정에 로그인되었습니다. 본인이 로그인한 것이 맞나요?\n" \
                                   "*위치는 로그인 IP 주소를 기준으로 한 근접한 위치입니다.\n\n" \
                                   "본인이 맞는 경우,\n" \
                                   "이 메시지를 무시하셔도 됩니다. 별도로 취해야 할 조치는 없습니다.\n\n" \
                                   "본인이 아닌 경우,\n" \
                                   "계정이 해킹되었을 수 있으며, 계정 보안을 위해 몇 가지 조치를 취해야 합니다. \n" \
                                   "조치를 취해주세요 -> %s\n" \
                                   "보다 안전한 조치를 위해 빠르게 임시비밀번호로 변경하시는 것이 좋습니다\n" \
                                   "비밀번호 변경: %s\n" \
                                   "위의 링크를 클릭하여 임시비밀번호로 변경하신 후에는 반드시 비밀번호를 원하는 비밀번호로 변경해주세요\n" \
                                   "최근 6개월 이내에 사용한 이전의 비밀번호는 개인정보 보호법에 따라 재사용하실수 없습니다\n\n" \
                                   "A Power of Trance에서 보낸 이메일인지 어떻게 알 수 있나요?\n" \
                                   "본 이메일의 링크는 “https://”로 시작하고 “apoweroftrance.com”을 포함합니다.\n" \
                                   "브라우저에 표시된 자물쇠 아이콘을 통해서도 안전한 사이트인지 확인할 수 있습니다."

NOTIFY_SECURITY_ALERT_EMAIL_HTML = "<!DOCTYPE html><html lang='kr'><body>" \
                                   "새로운 디바이스에서 계정에 로그인되었습니다. 본인이 로그인한 것이 맞나요?<br />" \
                                   "*위치는 로그인 IP 주소를 기준으로 한 근접한 위치입니다.<br /><br />" \
                                   "본인이 맞는 경우,<br />" \
                                   "이 메시지를 무시하셔도 됩니다. 별도로 취해야 할 조치는 없습니다.<br /><br />" \
                                   "본인이 아닌 경우,<br />" \
                                   "계정이 해킹되었을 수 있으며, 계정 보안을 위해 몇 가지 조치를 취해야 합니다. " \
                                   "시작하려면 지금 비밀번호를 재설정하세요.<br />" \
                                   "<a href='%s' target='_blank'>조치를 취해주세요</a><br /><br />" \
                                   "보다 안전한 조치를 위해 빠르게 임시비밀번호로 변경하시는 것이 좋습니다<br />" \
                                   "<a href='%s' target='_blank'>비밀번호 변경</a><br />" \
                                   "위의 링크를 클릭하여 임시비밀번호로 변경하신 후에는 반드시 비밀번호를 원하는 비밀번호로 변경해주세요<br />" \
                                   "최근 6개월 이내에 사용한 이전의 비밀번호는 개인정보 보호법에 따라 재사용하실수 없습니다<br /><br />" \
                                   "A Power of Trance에서 보낸 이메일인지 어떻게 알 수 있나요?<br />" \
                                   "본 이메일의 링크는 “http://”로 시작하고 “apoweroftrance.com”을 포함합니다.<br />" \
                                   "브라우저에 표시된 자물쇠 아이콘을 통해서도 안전한 사이트인지 확인할 수 있습니다.</body></html>"
