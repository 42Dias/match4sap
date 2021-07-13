import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
"""if os.getenv('GAE_INSTANCE'):
     SECRET_KEY = os.environ.get('SECRET_KEY')
else: """
SECRET_KEY = 'fd3h&uqymrcsyo(_5%&@!jbf182o5)k!)xty=fm056gk34^3v3'

DEBUG = True

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third Party Apps
    'allauth',
    'allauth.account',
    'localflavor',
    'widget_tweaks',

    # Local Apps
    'assessment.apps.AssessmentConfig',
    'headhunters.apps.HeadhuntersConfig',
    'orders.apps.OrdersConfig',
    'pages.apps.PagesConfig',
    'professionals.apps.ProfessionalsConfig',
    'users.apps.UsersConfig',
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

ROOT_URLCONF = 'match4sap.urls'

SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SETTINGS_PATH, 'templates')],
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

WSGI_APPLICATION = 'match4sap.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '2841',
        'PORT': 5432,
    }
}

DATABASES['default']['HOST'] = 'localhost'
if os.getenv('GAE_INSTANCE'):
    pass
else:
    DATABASES['default']['HOST'] = 'localhost'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

PROJECT_APPS = (
'MyApp'
)
JENKINS_TASKS = (
'django_jenkins.tasks.run_pep8',
'django_jenkins.tasks.run_pyflakes'
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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

""" STATIC_URL = 'https://storage.googleapis.com/match4sap/static/'

STATIC_ROOT = 'static/' """

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_ROOT = '/static/'

# Media files
MEDIA_URL = 'https://storage.googleapis.com/match4sap/media/'
MEDIA_ROOT = 'media/'

# Django-allauth config
SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT = 'home'

ACCOUNT_SESSION_REMEMBER = True

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "optional"

# Stripe
STRIPE_TEST_PUBLISHABLE_KEY = os.environ.get('STRIPE_TEST_PUBLISHABLE_KEY')
STRIPE_TEST_SECRET_KEY = os.environ.get('STRIPE_TEST_SECRET_KEY')

# Django-storages
""" DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = 'match4sap' """

# My configs
AUTH_USER_MODEL = 'users.CustomUser'

DEFAULT_FROM_EMAIL = 'no.reply@42dias.com.br'
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

EMAIL_HOST = 'smtp.dreamhost.com'
EMAIL_HOST_USER = 'no.reply@42dias.com.br'
EMAIL_HOST_PASSWORD = "B31nteractive"
EMAIL_PORT = 465
EMAIL_USE_TLS = True

#PRECISA CRIAR O EMAIL COM O DOMINIO DA MATCH4SAP