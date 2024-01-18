from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'verceldb',
        'USER': 'default',
        'PASSWORD': 'ohFu63DTAUMZ',
        'HOST': 'ep-broad-dawn-93276111-pooler.us-east-2.postgres.vercel-storage.com',
        'PORT': '5432'
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

#Envío de Email
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "centralioficial@gmail.com"
EMAIL_HOST_PASSWORD = "shgl vbmo iyld hhkx"

EMAIL_PORT = 587