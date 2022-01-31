import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "d+-z=5rj97w4i+m8w$=tatwji%_q^6k@be@0a#qdpj^km*jrjq"

# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = ['127.0.0.1', '192.168.0.100','aas-system.herokuapp.com']

DEBUG = False
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps
    'app_accounts',
    'app_admin',
    'app_ecc',
    'app_customer',
    'app_products',
    # Packages
    'webpush',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main_aas.urls'

AUTH_USER_MODEL = 'app_accounts.UserMaster'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'main_aas.wsgi.application'

DATABASES = {
        'default': {
            'ENGINE': 'djongo',
            'NAME': 'db_aas',
            'CLIENT': {
                'host': 'mongodb+srv://neelpatel:neel@clusteraas.lfdgn.mongodb.net/db_aas?retryWrites=true&w=majority'
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'accidentsecurities@gmail.com'
EMAIL_HOST_PASSWORD = 'AccidentSecurities@PS'

WEBPUSH_SETTINGS = {
   "VAPID_PUBLIC_KEY": 'BIPWxxiBkBE3u9EXPxL_YX_Ln8DWuAT4fWI7v0Kvg5gcznjCZrwSC3xqB29TiS-gQk-muugnCZCSftwZOfFBx60',
   "VAPID_PRIVATE_KEY": 'PQV1uacR8tffrzRg8L6miSLGIUiFSD8Chg7WSwx5LN0',
   "VAPID_ADMIN_EMAIL": 'accidentsecurities@gmail.com'
}