import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+hm_dpos_^_@25*4wjqz5)v)adzn6i91c=@tzjgn&$s1nbr^3m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['django-links.herokuapp.com', 'mysite.com', '127.0.0.1', 'localhost', '0.0.0.0']


# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'dal_legacy_static',
    #'grappelli',
    #'dal_queryset_sequence',
    #
    'accounts',
    #
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    #other
    'faicon',
    'colorfield',
    'embed_video',
    'crispy_forms',
    'social_django',
    'django_cleanup', # delete media from system

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.vk',

    #'smart_selects',
    #local
    'django.contrib.humanize',
    'cardapp',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'smarturlprj.urls'

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
                # socials
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                # `allauth` needs this from django
                'django.template.context_processors.request',
            ],
        },
    },
]
TEMPLATE_DIRS = (
                    os.path.join(os.path.dirname(__file__),'templates'),
)
WSGI_APPLICATION = 'smarturlprj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dcdhtapfcml74q',
        'HOST': 'ec2-54-246-67-245.eu-west-1.compute.amazonaws.com',
        'POST': 5432,
        'USER': 'wcuxsegozaepim',
        'PASSWORD': 'ad78c914819096586d4eebf9f922dcdaa3a6292148718ea41f76b7400d8b3c5f',
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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
#SESSION_COOKIE_AGE = 86400

#PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

CRISPY_TEMPLATE_PACK = 'bootstrap3'

AUTH_USER_MODEL = 'accounts.CustomUser'

LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = '/'
#LOGIN_URL = 'login'
#LOGOUT_URL = 'logout'

# messages
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# отправка на почту
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 2525
#EMAIL_USE_SSL = True
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'iwebpro.ru@mail.ru'
EMAIL_HOST_PASSWORD = 'Mail4Django_prjs'
#DEFAULT_FROM_EMAIL = 'No reply <noreply@mail.ru>'
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# for postgres
SOCIAL_AUTH_POSTGRES_JSONFIELD = True

SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['user_id',]
SOCIAL_AUTH_USER_MODEL = 'accounts.CustomUser'

AUTHENTICATION_BACKENDS = [
    #'account.authentication.EmailAuthBackend',
    #'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.vk.VKOAuth2',
# бекенд классической аутентификации, чтобы работала авторизация через обычный логин и пароль
    'django.contrib.auth.backends.ModelBackend',
    #allauth
    'allauth.account.auth_backends.AuthenticationBackend',
]
SOCIAL_AUTH_VK_OAUTH2_KEY = '7628028'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'k6oNkK8MccTcmyIfvLRD'
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email', 'photos']

X_FRAME_OPTIONS = 'ALLOWALL'
XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']
#USE_DJANGO_JQUERY = True
SITE_ID = 1
