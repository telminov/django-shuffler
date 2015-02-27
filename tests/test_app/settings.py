import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'nokey'
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []


INSTALLED_APPS = (
    'test_app',
)

MIDDLEWARE_CLASSES = ()

ROOT_URLCONF = 'test_app.urls'

WSGI_APPLICATION = 'test_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
