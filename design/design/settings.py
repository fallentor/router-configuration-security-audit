"""
Django settings for Demo_device project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s*uj9ck(kt-)dj&ngg56*zh*lhu-)p6v3egy)*m%r#4xkv_rpv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'audit',
    'device',
    'tactic',
    'log'
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

ROOT_URLCONF = 'design.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'design.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',  # 必须在 AuthenticationMiddleware 前面
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',   # 必须在 AuthenticationMiddleware 后面
    'log.RequestLogMiddleware.RequestLogMiddleware',
]

# session 过期时间（秒）
SESSION_COOKIE_AGE = 60 * 30 

# 设置用户退出浏览器删除session
SESSION_EXPIRE_AT_BROWSER_CLOSE = True 

# 文件上传大小
MAX_FILE_SIZE = 5 * 1024 * 1024   # 5MB
FILE_UPLOAD_MAX_MEMORY_SIZE = MAX_FILE_SIZE

SIMPLEUI_HOME_INFO = False
SIMPLEUI_CONFIG = {
    'system_keep': False, # 关闭系统菜单
    'menu_display': ['任务管理', '设备管理','策略管理', '用户管理', '日志管理'],
    'dynamic': True,    # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时动态展示菜单内容
    'menus': [{
        'app': 'device',
        'name': '设备管理',
        'icon': 'fa fa-atom',
        'models': [{
            'name': '节点管理',
            'icon': 'fas fa-network-wired',
            'url': '/device/'
        }]
    }, {
        'app': 'auth',
        'name': '用户管理',
        'icon': 'el el-icon-s-check',
        'models': [{
            'name': '系统用户',
            'url': 'auth/user/',
            'icon': 'el el-icon-s-custom'
        }]
    },{
        'app': 'tactic',
        'name': '策略管理',
        'url': '/tactic/',
        'icon': 'fa fa-gear',
        'models': [{
            'name': '策略组管理',
            'url': '/tactic/tacticGroup_list/',
            'icon': 'fas fa-shield-virus'
        }, {
            'name': '策略管理',
            'url': '/tactic/tactic_list/',
            'icon': 'fas fa-cog'
        }]
    },{
        'app': 'log',
        'name': '日志管理',
        'icon': 'fa fa-file',
        'models': [{
            'name': '系统日志',
            'url': '/log/',
            'icon': 'fas fa-list-alt'
        }]
    }, {
        'app': 'audit',
        'name': '任务管理',
        'url': '/audit/',
        'icon': 'fa fa-gear',
        'models': [{
            'name': '采集与审计',
            'url': '/audit/audit_list/',
            'icon': 'fas fa-user-shield'
        }, {
            'name': '结果可视化',
            'url': '/audit/visualization/',
            'icon': 'fas fa-magnifying-glass-chart'
        }, {
            'name': '报表管理',
            'url': '/audit/report_export/',
            'icon': 'fas fa-file-medical'
        }]
    }]
}