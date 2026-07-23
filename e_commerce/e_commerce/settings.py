# Configurações do projeto e_commerce (Django 5.0.1)

from pathlib import Path
import os

# Diretório raiz do projeto (onde está manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta usada para criptografia (mantenha em segredo em produção)
SECRET_KEY = 'django-insecure--&^3ia3c-sa*+5+-+xkn^q9z33+lnhw+-z5hi618=^2*tp-2u0'

# Modo debug ativado para desenvolvimento (desative em produção)
DEBUG = True

# Hosts permitidos (preencher com o domínio em produção)
ALLOWED_HOSTS = []

# Aplicativos instalados no projeto
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',  # Aplicativo principal do e-commerce
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

# Define o modelo de usuário personalizado (core.User)
AUTH_USER_MODEL = 'core.User'

# Configuração da URL raiz do projeto
ROOT_URLCONF = 'e_commerce.urls'

# Configuração de templates (HTML)
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

WSGI_APPLICATION = 'e_commerce.wsgi.application'

# Configuração do banco de dados SQLite (arquivo db.sqlite3)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validadores de senha
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator' },
]

# Internacionalização
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Arquivos estáticos (CSS, JavaScript, imagens)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Chave primária padrão para novos modelos
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Arquivos de mídia (uploads de usuários)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
