from pathlib import Path
import os
from django.contrib import staticfiles
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY ='django-insecure-h=2gh5_oxqekwh7-$ym0w=78aoqls9+cs^+&kzy=+x3&c4g_#&'

DEBUG = True

ALLOWED_HOSTS = [
    'www.karpaty-aqua.store', 'karpaty-aqua.store','localhost'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'market.apps.MarketConfig',
    'django.contrib.humanize',
    "users.apps.UsersConfig",
    'cart.apps.CartConfig',
    'order.apps.OrderConfig',
    "crispy_forms",
    "crispy_tailwind",
    'admin_panel',
    'django.contrib.sitemaps',
    'bot.apps.BotConfig',

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

ROOT_URLCONF = 'BudMarket.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'market/templates']
        ,
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

WSGI_APPLICATION = 'BudMarket.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shopdb',
        'USER': 'admin',
        'PASSWORD': '1231',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}

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

LANGUAGE_CODE = 'uk'
TIME_ZONE = 'Europe/Kiev'
DATETIME_FORMAT = 'Y-m-d H:i:s'
USE_I18N = True
USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/karpaty-aqua/media/'


CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"


LOGIN_REDIRECT_URL = "/market"
LOGOUT_REDIRECT_URL = "/market"

CSRF_TRUSTED_ORIGINS = ['http://194.15.112.50',
                        'http://localhost',
                        'http://karpaty-aqua.store'
                        ]

CORS_ALLOWED_ORIGINS = ['http://194.15.112.50',
                        'http://localhost',
                        'http://karpaty-aqua.store']

CORS_ORIGIN_WHITELIST = ['http://194.15.112.50',
                         'localhost',
                         'http://karpaty-aqua.store']

load_dotenv()  # Load environment variables from .env file

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

LIQPAY_PUBLIC_KEY = 'sandbox_i69207852812'
LIQPAY_PRIVATE_KEY = 'sandbox_6EExRwNHnX6Xdu7xfEZ9SHEu5qokMpCHrajy6fa7'
LIQPAY_API_URL = 'https://www.liqpay.ua/api/request'

LOGIN_URL = '/users/login_required/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'log.log',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
