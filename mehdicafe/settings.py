import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
#SECRET_KEY = "django-insecure-n7sb(#w40z+s!$tee*76mw!9@^c@8&jaw%a+(3=wz3#qx=n&xm"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['mehdimchow.pythonanywhere.com']

# Prevents hackers from "framing" your site
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    'blog',
    'marketplace',
    'tinymce',
    'taggit',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mehdicafe.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'blog.context_processors.system_matrix',
            ],
        },
    },
]

WSGI_APPLICATION = "mehdicafe.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Media settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CSRF_TRUSTED_ORIGINS = ['https://mehdimchow.pythonanywhere.com']

# TINYMCE MODERN EDITOR CONFIGURATION
TINYMCE_DEFAULT_CONFIG = {
    "height": "700px",
    "width": "100%",
    "menubar": False,
    "statusbar": True,
    "skin": "oxide",
    "promotion": False,
    "toolbar_mode": "wrap",

    # 1. Added 'codesample' to the plugins list
    "plugins": "advlist autolink lists link image charmap preview anchor searchreplace visualblocks code codesample fullscreen insertdatetime media table help wordcount",

    # 2. Added 'codesample' icon to the end of the toolbar
    "toolbar": (
        "fullscreen preview | blocks | "
        "bold italic underline strikethrough | alignleft aligncenter alignright alignjustify | "
        "bullist numlist outdent indent | link image media table | "
        "removeformat | code codesample wordcount"
    ),

    "quickbars_selection_toolbar": "bold italic | h2 h3 | blockquote quicklink",
    "quickbars_insert_toolbar": "image media table",

    "content_style": """
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            font-size: 16px;
            line-height: 1.8;
            max-width: 100%;
            margin: 0 auto;
            padding: 2rem;
            color: #1f2937;
            background-color: #ffffff;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #111827;
            font-weight: 700;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
        }
        p { margin-bottom: 1.25em; }
        blockquote {
            border-left: 4px solid #3b82f6;
            padding-left: 1rem;
            color: #4b5563;
            font-style: italic;
            background: #f8fafc;
            padding: 1rem;
            border-radius: 0 8px 8px 0;
        }
        a { color: #2563eb; text-decoration: underline; }
        img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            margin: 2rem 0;
        }
        /* Style for inline code */
        code {
            background-color: #f1f5f9;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-family: monospace;
            font-size: 14px;
        }
        /* 3. New style for the Codesample block inside the editor */
        pre[class*="language-"] {
            background: #1e293b !important;
            color: #f8fafc !important;
            padding: 1.5rem;
            border-radius: 12px;
            font-family: 'Fira Code', 'Courier New', monospace;
            font-size: 14px;
            margin: 1.5rem 0;
            overflow: auto;
        }
    """,
}

# LIVE GMAIL SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mmc1641992@gmail.com'
EMAIL_HOST_PASSWORD = os.getenv('GMAIL_PASSWORD')
#EMAIL_HOST_PASSWORD = 'acvu hakb pbjy kjuy' # <--- PASTE IT HERE

# TMDB API Configuration
TMDB_API_KEY = os.getenv('TMDB_API')