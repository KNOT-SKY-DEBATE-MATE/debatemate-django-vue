"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from decouple import config
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# Debug Mode
# https://docs.djangoproject.com/en/5.1/ref/settings/#std:setting-DEBUG

DEBUG = config('DEBUG', default=False, cast=bool)


# Django Secret Key
# https://docs.djangoproject.com/en/5.1/ref/settings/#secret-key

if not DEBUG:
    SECRET_KEY = config('SECRET_KEY')
else:
    # fallback for development
    SECRET_KEY = "nfg6CUJ1ySCnyFrCXmisrmxtwBuRZ5TsSeeb4fZVpK96ls3Qx2HQCSHI8cdUAt8te80"


# Allowed Hosts
# https://docs.djangoproject.com/en/5.1/ref/settings/#allowed-hosts

ALLOWED_HOSTS = ['*']


# Application definition
# https://docs.djangoproject.com/en/5.1/ref/settings/#installed-apps

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'channels', 
    'apps.user',
    'apps.group',
    'apps.meeting',
]


# Authentication
LOGIN_URL = '/user/authentication/'

# https://docs.djangoproject.com/en/5.1/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = '/user/'


# Rest framework
# https://docs.djangoproject.com/en/5.1/ref/settings/#rest-framework

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}


# Middleware5
# https://docs.djangoproject.com/en/5.1/topics/http/middleware/

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]


# Root URL configuration
# https://docs.djangoproject.com/en/5.1/ref/settings/#root-urlconf

ROOT_URLCONF = 'config.urls'


# CSRF
# https://docs.djangoproject.com/en/5.1/ref/settings/#csrf-cookie-name

CSRF_COOKIE_NAME = 'csrftoken'
CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'


# Templates
# https://docs.djangoproject.com/en/5.1/ref/settings/#templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# WSGI
# https://docs.djangoproject.com/en/5.1/ref/settings/#wsgi-application

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

if not DEBUG and False:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('POSTGRES_DB'),
            'USER': config('POSTGRES_USER'),
            'PASSWORD': config('POSTGRES_PASSWORD'),
            'HOST': 'localhost',
            'PORT': config('POSTGRES_PORT'),
            'CONN_MAX_AGE': 600,
            'OPTIONS': {
                'sslmode': 'require',
            },
        }
    }

else:
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password hashers
# https://docs.djangoproject.com/en/5.1/ref/settings/#password-hashers

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.ScryptPasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]


# Authentication backends
# https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#specifying-authentication-backends

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


# Authentication
# https://django-allauth.readthedocs.io/en/latest/configuration.html

ACCOUNT_AUTHENTICATION_METHOD = 'email'


# Email
# https://django-allauth.readthedocs.io/en/latest/configuration.html

ACCOUNT_EMAIL_REQUIRED = True


# Username
# https://django-allauth.readthedocs.io/en/latest/configuration.html

ACCOUNT_USERNAME_REQUIRED = True


# allauth SocialAccount providers
# https://django-allauth.readthedocs.io/en/latest/configuration.html#socialaccount-providers

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID'),
            'secret': config('GOOGLE_CLIENT_SECRET'),
            'key': ''
        },
        'SCOPE': ['profile', 'email'],  # Googleから取得する情報
        'AUTH_PARAMS': {'access_type': 'offline'},
    }
}

# Django contrib.sites
# Site ID (django.contrib.sites)

SITE_ID = config('SITE_ID', default=1, cast=int)


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Authentication backends
# https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#specifying-authentication-backends


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# ASGI
ASGI_APPLICATION = 'config.asgi.application'

# Channels レイヤーの設定
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(os.getenv('REDIS_HOST', 'redis'), 
                      int(os.getenv('REDIS_PORT', 6379)))],
        },
    },
}