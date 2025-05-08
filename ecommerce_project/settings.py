"""
Django settings for ecommerce_project project modificado para Render.com
"""

import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env si existe
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-izer_&-#k93#67c8t@s=cdaf1uv9h#lfwgqw(fa8dtc1)kavh8')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.onrender.com']
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']

# Application definition
# Asegurarse de que la parte de instalación de WhiteNoise sea correcta
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # Debe ir ANTES de whitenoise
    'store.apps.StoreConfig',
]

# El middleware de WhiteNoise debe ir justo después de SecurityMiddleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Debe ir en esta posición
    # Resto de middlewares...
]

# Configuración de archivos estáticos - Asegurarse de que estas líneas estén presentes
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Debe coincidir con el nombre de directorio que creamos

# Usar el almacenamiento comprimido de WhiteNoise para estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configuración para archivos de medios
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuraciones específicas para Render
import os
import dj_database_url

# Base de datos para producción
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

# Permitir que Render acceda al sitio
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.onrender.com']
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']

# Configuración del puerto para Render
PORT = int(os.environ.get('PORT', 8001))