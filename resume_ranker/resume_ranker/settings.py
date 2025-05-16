import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-1234567890abcdefghijklmnopqrstuvwxyz')

# Change this to use environment variable for production/development settings
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Updated to include common deployment platforms
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.herokuapp.com', '.render.com', '.pythonanywhere.com', '.netlify.app', '.vercel.app']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
    'whitenoise.runserver_nostatic',  # Added for static file serving
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Added for static file serving
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Updated CORS settings to dynamically include deployment domains
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Add production URLs to CORS_ALLOWED_ORIGINS from ALLOWED_HOSTS
for host in ALLOWED_HOSTS:
    if host.startswith('.'):  # It's a domain pattern like .herokuapp.com
        CORS_ALLOWED_ORIGINS.extend([
            f"https://{host.lstrip('.')}",
            f"https://www.{host.lstrip('.')}"
        ])
    elif host not in ['localhost', '127.0.0.1']:  # Skip localhost entries
        CORS_ALLOWED_ORIGINS.extend([
            f"https://{host}",
            f"http://{host}"
        ])

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'resume_ranker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR.parent, 'frontend_build'),  # Adjusted path to match project structure
        ],
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

WSGI_APPLICATION = 'resume_ranker.wsgi.application'

# Database configuration - updated to support PostgreSQL on deployment platforms
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configure PostgreSQL from environment variables if available (for deployment)
if 'DATABASE_URL' in os.environ:
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static and media files settings
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Updated path to match the frontend_build location
STATICFILES_DIRS = [
    os.path.join(BASE_DIR.parent, 'frontend_build'),  # Adjusted path to match project structure
]

# Configure whitenoise for static file compression
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default auto field for new models
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# File Uploads
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = not DEBUG  # Only secure in production
CSRF_COOKIE_SECURE = not DEBUG  # Only secure in production

# Add HTTPS settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True