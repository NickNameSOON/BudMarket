from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-h=2gh5_oxqekwh7-$ym0w=78aoqls9+cs^+&kzy=+x3&c4g_#&'

DEBUG = True

ALLOWED_HOSTS = ['*']

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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Kiev'

DATETIME_FORMAT = 'Y-m-d H:i:s'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR / 'media'

MEDIA_URL = '/media/'

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = "tailwind"

LOGIN_REDIRECT_URL = "/market"
LOGOUT_REDIRECT_URL = "/market"

CSRF_TRUSTED_ORIGINS = ['https://b847-62-122-202-247.ngrok-free.app']

CORS_ALLOWED_ORIGINS = ['https://b847-62-122-202-247.ngrok-free.app']

CORS_ORIGIN_WHITELIST = ['https://b847-62-122-202-247.ngrok-free.app']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_POST = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'volodymyr.r.savchuk@ukd.edu.ua'
EMAIL_HOST_PASSWORD = 'EbIE21ODiSa34d50'


WAYFORPAY_ACCOUNT = 'freelance_user_663e1b76e16a3'
WAYFORPAY_SECRET_KEY = 'a93171a82971a88fa32e7208d10d2ac297a165a7'
WAYFORPAY_API_URL = 'https://secure.wayforpay.com/pay'

LOGIN_URL = '/users/login_required/'
