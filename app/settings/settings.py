from pathlib import Path
from django.urls import reverse_lazy
from celery.schedules import crontab


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-+q640znnpj98b*v+c!66^nl4!$ej_oe66t^*w@50oj(r**5hhj'

CSRF_TRUSTED_ORIGINS = ['https://rise.ua', 'http://rise.ua']

DEBUG = False

ALLOWED_HOSTS = ['*']

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
WIQ_API_KEY = '204129a74754fc8c0c6185b4f2062833'

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
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'prodaction': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'rise_server',
            'USER': 'postgres',
            'PASSWORD': 'supreme128',
            'HOST': '10.114.0.4',
            'PORT': '5432'
        },
}


# AUTHENTICATION_BACKENDS = (
#     'allauth.account.auth_backends.AuthenticationBackend',
# )

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
        'schedule': crontab(minute='*/5'),
    },
    'checking_completed_orders': {
        'task': 'services.tasks.checking_completed_orders',
        'schedule': crontab(minute='*/15'),
    }
}