from pathlib import Path
import os
from django.core.exceptions import ImproperlyConfigured
from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.getenv('DEBUG', 0)))

ALLOWED_HOSTS = ALLOWED_HOSTS = [
    h.strip() for h in os.getenv('ALLOWED_HOSTS', '').split(',')
    if h.strip()
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'django_filters',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'health_professionals',
    'appointments',
    'authentication'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        # Se estiver em DEBUG, pode retornar um padrão,
        # se não, trava o sistema por segurança.
        if DEBUG:
            return "config_local"
        error_msg = f"A variável de ambiente {var_name} não está definida."
        raise ImproperlyConfigured(error_msg)


DATABASES = {
    'default': {

        'ENGINE': os.getenv('DB_ENGINE'),
        'PORT': os.getenv('POSTGRES_PORT'),

        'NAME': get_env_variable('POSTGRES_DB'),
        'USER': get_env_variable('POSTGRES_USER'),
        'PASSWORD': get_env_variable('POSTGRES_PASSWORD'),
        'HOST': get_env_variable('POSTGRES_HOST'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = "/static/"

# /data/web/static
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
# /data/web/media
MEDIA_ROOT = BASE_DIR / 'media'


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}

# Define tempo de vida dos tokens de autenticação
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Token expira em 1 hora
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),     # Refresh expira em 1 dia
    'ROTATE_REFRESH_TOKENS': True,                   # Gera novo refresh a cada uso
    'BLACKLIST_AFTER_ROTATION': True,                # Invalida refresh antigo
    'UPDATE_LAST_LOGIN': True,                       # Atualiza último login
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
if DEBUG:
    # Desenvolvimento: permite localhost nas portas comuns de frontend
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",  # React/Next.js padrão
        "http://localhost:5173",  # Vite padrão
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
else:
    # Produção: apenas domínios oficiais
    CORS_ALLOWED_ORIGINS = [
        h.strip() for h in os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
        if h.strip()
    ]

# Permite envio de cookies e credenciais (necessário para JWT e sessões)
CORS_ALLOW_CREDENTIALS = True

# Métodos HTTP permitidos (adicione conforme necessário)
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Headers que o frontend pode enviar
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Configurações da documentação swagger
SPECTACULAR_SETTINGS = {
    'TITLE': 'API de Agendamentos',
    'DESCRIPTION': 'Gestão de profissionais de saúde e consultas',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
}


# --- LOGS DE ACESSO E ERROS ---
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'django_errors.log',
            'formatter': 'verbose',
        },
        'file_access': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'django_access.log',
            'formatter': 'simple',
        },
        # NOVO: Log específico para appointments e profissionais
        'file_app': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'app.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file_errors'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['file_access'],
            'level': 'INFO',
            'propagate': False,
        },
        'core': {
            'handlers': ['console', 'file_errors'],
            'level': 'INFO',
            'propagate': True,
        },
        # NOVO: Logs dos seus apps
        'appointments': {
            'handlers': ['console', 'file_app'],
            'level': 'INFO',
            'propagate': False,
        },
        'health_professionals': {
            'handlers': ['console', 'file_app'],
            'level': 'INFO',
            'propagate': False,
        },
        'authentication': {
            'handlers': ['console', 'file_app'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
