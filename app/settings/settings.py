from pathlib import Path
from django.urls import reverse_lazy
from celery.schedules import crontab


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-+q640znnpj98b*v+c!66^nl4!$ej_oe66t^*w@50oj(r**5hhj'

CSRF_TRUSTED_ORIGINS = ['http://riseua.online',]

DEBUG = False

ALLOWED_HOSTS = ['riseua.online', 'localhost', '127.0.0.1']

AUTH_USER_MODEL = 'accounts.User'
LOGIN_REDIRECT_URL = reverse_lazy('index')
LOGOUT_REDIRECT_URL = reverse_lazy('index')
LOGIN_URL = reverse_lazy('login')

# Розрішити доступ до Debug Toolbar тільки для локального розробника
INTERNAL_IPS = ['127.0.0.1']

# Налаштування для панелі інструментів
# DEBUG_TOOLBAR_CONFIG = {
#     'SHOW_TOOLBAR_CALLBACK': lambda request: True,
# }

# PayPal Api
PAYPAL_CLIENT_ID = 'AbPXGGe2lC1udAZcX1NLZmJ18OtYZuBtkjPNAw4tl7CGPmpvgZF3FpO_9Cg0ycvBwqC_T7cp0FN8fOhd'
PAYPAL_SECRET_KEY = 'ECvSnLZDpRxBJ3hyvk-wVu0cJy4tGeIcSjrPaBhkaxSAJS0E4xtTkAhUc8EO_M21lerq-fYZf4oxzbnd'

# LiqPay Api (Sandbox)
LIQPAY_PUBLIC_KEY = 'sandbox_i69234533774'
LIQPAY_PRIVATE_KEY = 'sandbox_K7Mlrs8wcb5Meoa39wQAn0knsEXyZJbXPnBv4aa3'

# WiQ Api
WIQ_API_URL = 'https://wiq.ru/api/'
WIQ_API_KEY = 'a37502755bcf12331f1b957cdb420ad3'

# GlobalSmm Api
GLOBALSMM_API_URL = 'https://global-smm.com/api/v2/'
GLOBALSMM_API_KEY = 'b3e9a678aca8c3657dd23ef40572368e'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # pay tools
    # 'payments',
    'liqpay',

    # tools
    'django_extensions',
    'crispy_forms',
    'crispy_bootstrap5',
    'debug_toolbar',
    'storages',

    # apps
    'accounts',
    'support',
    'posts',
    'comments',
    'services'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',

    # 'services.middleware.HostHeaderCheckMiddleware'
]

ROOT_URLCONF = 'settings.urls'


"""
Шляхи до папок із шаблонами.
"""
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates' / 'elements',
            BASE_DIR / 'templates' / 'accounts',
            BASE_DIR / 'templates' / 'comments',
            BASE_DIR / 'templates' / 'posts',
            BASE_DIR / 'templates' / 'support',
            BASE_DIR / 'templates' / 'services'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # other
                'settings.context_processors.footer_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'settings.wsgi.application'

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }

    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'defaultdb',
        'USER': 'doadmin',
        'PASSWORD': 'AVNS_9yJqs7hR2bHbcIt8aPv',
        'HOST': 'riseserver-do-user-14570332-0.b.db.ondigitalocean.com',
        'PORT': '25060'
    },
}

AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
)

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


STATIC_URL = 'static_content/'
STATIC_ROOT = BASE_DIR / '..' / 'static'
STATICFILES_DIRS = [
    STATIC_ROOT / 'static_content',
]

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / '..' / 'static' / 'media'

LANGUAGE_CODE = 'uk-uk'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

"""
Crispy Form
"""
CRISPY_TEMPLATE_PACK = 'bootstrap5'


"""
Celery
"""
CELERY_BROKER_URL = 'amqp://localhost'

CELERY_BEAT_SCHEDULE = {
    'rehadlering_invalid_orders': {
        'task': 'services.tasks.rehadlering_invalid_orders',
        'schedule': crontab(minute='*/15'),
    },
    'checking_completed_orders': {
        'task': 'services.tasks.checking_completed_orders',
        'schedule': crontab(minute='*/15'),
    }
}


AWS_S3_REGION_NAME = 'fra1'
AWS_S3_ENDPOINT_URL = 'https://risestaticfiles.fra1.digitaloceanspaces.com'
AWS_ACCESS_KEY_ID = 'DO0083866TYUQ24MC9FK'
AWS_SECRET_ACCESS_KEY = 'uw5chEbo3IsMJEgFMolLz9yBFe+uaai7/XRhtDG1ixA'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_STORAGE_BUCKET_NAME = 'static'
AWS_DEFAULT_ACL = 'public-read'
STATIC_URL = 'https://risestaticfiles.fra1.digitaloceanspaces.com/static/'
MEDIA_URL = 'https://risestaticfiles.fra1.digitaloceanspaces.com/static/'
