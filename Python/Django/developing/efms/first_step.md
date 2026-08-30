# 企业文件管理系统（EFMS）第一阶段：基础框架搭建

项目GitHub地址👉 [GitHub: wephiles/efms](https://github.com/wephiles/efms)

项目本机地址 👉 [Local: efms](E:\Code\PyProjects\efms)

## 文档信息

| 项目名称 | 企业文件管理系统（EFMS）                    |
| -------- | ------------------------------------------- |
| 阶段     | 第一阶段：基础框架搭建                      |
| 技术栈   | Django 5.x + DRF + PostgreSQL + Redis + JWT |
| 编写日期 | 2026-04-19                                  |

---

## 目录

1. [环境准备与项目初始化](#1-环境准备与项目初始化)
2. [项目配置](#2-项目配置)
3. [数据库模型设计](#3-数据库模型设计)
4. [用户认证系统实现](#4-用户认证系统实现)
5. [API接口实现](#5-api接口实现)
6. [安全策略实现](#6-安全策略实现)
7. [测试与验证](#7-测试与验证)

---

## 1. 环境准备与项目初始化

### 1.1 系统环境要求

在开始开发之前，请确保您的开发环境满足以下要求：

| 软件       | 版本要求 | 说明                  |
| ---------- | -------- | --------------------- |
| Python     | 3.10+    | 推荐使用 3.11 或 3.12 |
| PostgreSQL | 14+      | 主数据库              |
| Redis      | 6.0+     | 缓存和会话存储        |
| pip        | 最新版   | Python 包管理器       |
| virtualenv | 最新版   | 虚拟环境管理          |

### 1.2 创建项目目录和虚拟环境

```bash
# 创建项目根目录
mkdir -p ~/projects/efms
cd ~/projects/efms

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Linux/macOS
source venv/bin/activate
# Windows
# venv\Scripts\activate
```

### 1.3 安装项目依赖

创建 `requirements.txt` 文件：

```text
# requirements.txt

# Django 核心
Django==5.0.4

# Django REST Framework
djangorestframework==3.15.1
djangorestframework-simplejwt==5.3.1

# 数据库
psycopg2-binary==2.9.9

# Redis 缓存
redis==5.0.4
django-redis==5.4.0

# 用户认证和安全
django-cors-headers==4.3.1
django-ratelimit==4.1.0
bcrypt==4.1.2

# 验证码
django-simple-captcha==0.6.0

# API 文档
drf-spectacular==0.27.2

# 工具库
python-dotenv==1.0.1
Pillow==10.3.0
celery==5.4.0
django-celery-beat==2.6.0

# 开发工具
flake8==7.0.0
black==24.4.2
isort==5.13.2
```

执行安装命令：

```bash
pip install -r requirements.txt
```

---

如果使用uv管理项目：

```toml
[project]
name = "efms"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "bcrypt==4.1.2",
    "black==24.4.2",
    "celery==5.4.0",
    "django==5.0.4",
    "django-celery-beat==2.6.0",
    "django-cors-headers==4.3.1",
    "django-debug-toolbar>=6.3.0",
    "django-ratelimit==4.1.0",
    "django-redis==5.4.0",
    "django-simple-captcha==0.6.0",
    "djangorestframework==3.15.1",
    "djangorestframework-simplejwt==5.3.1",
    "drf-spectacular==0.27.2",
    "flake8==7.0.0",
    "isort==5.13.2",
    "pillow==10.3.0",
    "psycopg2-binary==2.9.9",
    "python-dotenv==1.0.1",
    "redis==5.0.4",
]

```

### 1.4 创建 `Django` 项目

```bash
# 创建 Django 项目
django-admin startproject config .

# 创建核心应用模块
python manage.py startapp users
python manage.py startapp departments
python manage.py startapp authentication
python manage.py startapp common

# 创建存放自定义模块的目录
mkdir -p utils
touch utils/__init__.py
touch utils/validators.py
touch utils/exceptions.py
touch utils/mixins.py
touch utils/helpers.py
```

### 1.5 项目目录结构

完成初始化后，项目目录结构如下：

```
efms/
├── venv/                          # 虚拟环境
├── config/                        # 项目配置目录
│   ├── __init__.py
│   ├── settings/                  # 分环境配置
│   │   ├── __init__.py
│   │   ├── base.py               # 基础配置
│   │   ├── development.py        # 开发环境配置
│   │   └── production.py         # 生产环境配置
│   ├── urls.py                   # 主路由配置
│   ├── asgi.py
│   └── wsgi.py
├── users/                         # 用户管理模块
│   ├── __init__.py
│   ├── models.py                 # 用户模型
│   ├── serializers.py            # 序列化器
│   ├── views.py                  # 视图
│   ├── urls.py                   # 路由
│   ├── admin.py                  # Admin 配置
│   ├── permissions.py            # 权限类
│   └── migrations/
├── departments/                   # 部门管理模块
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
├── files/                   # 文件管理模块
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
├── authentication/                # 认证模块
│   ├── __init__.py
│   ├── backends.py               # 自定义认证后端
│   ├── jwt.py                    # JWT 工具类
│   ├── throttling.py             # 限流类
│   └── middleware.py             # 认证中间件
├── common/                        # 公共模块
│   ├── __init__.py
│   ├── models.py                 # 公共模型基类
│   ├── responses.py              # 统一响应格式
│   ├── pagination.py             # 分页类
│   └── constants.py              # 常量定义
├── utils/                         # 工具模块
│   ├── __init__.py
│   ├── validators.py             # 验证器
│   ├── exceptions.py             # 自定义异常
│   ├── mixins.py                 # 通用 Mixin
│   └── helpers.py                # 辅助函数
├── media/                         # 媒体文件目录
├── static/                        # 静态文件目录
├── logs/                          # 日志目录
├── manage.py                      # Django 管理脚本
├── requirements.txt               # 依赖清单
├── .env                          # 环境变量配置
└── .gitignore                    # Git 忽略配置
```

---

## 2. 项目配置

### 2.1 环境变量配置

创建 `.env` 文件存储敏感配置：

```bash
# ============================================================================================
# ======================================== Django 配置 ========================================
# Django 的加密盐，用于生成 session、CSRF token、密码重置链接等。生产环境必须换成随机复杂字符串，且严禁泄露。
DJANGO_SECRET_KEY=your-secret-key-here-change-in-production

## True 表示开启调试模式（显示详细错误页、自动重载代码）。生产环境必须设为 False。
#DJANGO_DEBUG=True

# 允许访问该 Django 应用的域名/IP 白名单，防止 HTTP Host 头攻击。这里只允许本地访问。
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# ============================================================================================
# ========================================= 数据库配置 =========================================
# 数据库名称，项目将连接名为 efms_db 的库。
DB_NAME=efms_db

# 连接数据库的用户名，此处为 efms_user。
DB_USER=efms_user

# 对应用户的密码，目前是占位符，需要替换成真实密码。
DB_PASSWORD=your-db-password

# 数据库服务器地址，localhost 表示数据库和 Django 在同一台机器上。
DB_HOST=localhost

# PostgreSQL 默认端口 5432。
DB_PORT=5432

# ============================================================================================
# ======================================== redis 配置 =========================================
# redis 服务地址，本地为 localhost。
REDIS_HOST=localhost

# redis 默认端口 6379。
REDIS_PORT=6379

# redis 连接密码（如果设置了 requirepass）。此处为空表示无密码。
REDIS_PASSWORD=

# ============================================================================================
# ========================================= JWT 配置 ==========================================
# 访问令牌的有效期，单位是分钟。这里 120 表示 2 小时后过期，需要刷新。
JWT_ACCESS_TOKEN_LIFETIME=120

# 刷新令牌的有效期，10080 分钟即 7 天。用户可在 7 天内通过刷新令牌换取新的 access token，无需重新登录。
JWT_REFRESH_TOKEN_LIFETIME=10080

# ============================================================================================
# ========================================== 邮件配置 ==========================================
# SMTP 服务器地址，此处是示例域名 smtp.example.com，实际使用时需换成你的邮件服务商（如 smtp.qq.com、smtp.gmail.com）。
EMAIL_HOST=smtp.example.com

# SMTP 端口，587 通常是 TLS 加密端口。
EMAIL_PORT=587

# True 表示启用 TLS 加密。
EMAIL_USE_TLS=True

# 发件邮箱账号，示例为 noreply@example.com。
EMAIL_HOST_USER=noreply@example.com

# 邮箱授权码或登录密码（占位符，必须替换）。
EMAIL_HOST_PASSWORD=your-email-password

# ============================================================================================
# ========================================== 短信配置 ==========================================
# 短信服务商的 Access Key（如阿里云、腾讯云）。
SMS_ACCESS_KEY=
# 对应的 Secret Key。
SMS_SECRET_KEY=
# 短信签名（需在短信平台报备）。
SMS_SIGN_NAME=

# ============================================================================================
# ========================================= 文件存储配置 ========================================
# 用户上传文件的本地存储根目录。~/root 表示当前用户家目录下的 root 文件夹。生产环境可能换成云存储路径。
FILE_STORAGE_ROOT=~/EFMS_ROOT

# 允许上传的单个文件最大体积，5368709120 字节 = 5 GB。
MAX_FILE_SIZE=5368709120

# cors 配置
CORS_ALLOWED_ORIGINS=http://localhost:8080,http://localhost:3000,http://127.0.0.1:8080,http://127.0.0.1:3000
```

### 2.2 创建分环境配置

首先创建配置目录：

```bash
mkdir -p config/settings
touch config/settings/__init__.py
touch config/settings/base.py
touch config/settings/development.py
touch config/settings/production.py
```

#### 2.2.1 基础配置 (config/settings/base.py)

```python
# config/settings/base.py
"""
Django 基础配置文件
包含所有环境共用的配置项
"""

import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# # 项目根目录
# __file__: 是当前脚本的路径
# pathlib.Path(): 将路径字符串转换为 pathlib.Path 对象，便于进行路径操作
# resolve(): 将相对路径解析为绝对路径，并消除符号链接，确保路径真实、完整
# .parent: 返回当前文件所在 目录 的 Path 对象（相当于 os.path.dirname）
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # efms 目录 -- 项目根目录
load_dotenv(BASE_DIR / '.env')

# NOTE: base.py 中日志配置指向了 BASE_DIR / 'logs' / 'django.log',
#   如果项目首次运行或在新服务器部署时，logs 文件夹不存在，Django 启动会直接报错 FileNotFoundError。
#   修复：确保项目根目录下有一个空的 logs/ 目录，或者在 base.py 顶部加一段自动创建目录的代码(推荐)
# LOGGING = {
#         ...,
#         'file': {
#             'class': 'logging.handlers.RotatingFileHandler',
#             # NOTE: 就在这里
#             ...
#         },
#         ...
# }
(BASE_DIR / 'logs').mkdir(parents=True, exist_ok=True)

# 安全配置
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-change-me-in-production')
DEBUG = False
ALLOWED_HOSTS = [h.strip() for h in os.getenv(
    'DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,192.168.31.128'
).split(',') if h.strip()]

# 应用定义
INSTALLED_APPS = [
    # Django 内置应用
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # XXX: 第三方应用
    'django_filters',
    'rest_framework',
    'rest_framework_simplejwt',
    # JWT 开启了黑名单功能，所以必须注册 app
    'rest_framework_simplejwt.token_blacklist',  # ← 必须加上这一行
    'corsheaders',
    'django_ratelimit',
    'captcha',
    'drf_spectacular',
    'django_celery_beat',

    # 项目应用
    'users',
    'files',
    'departments',
    'authentication',
    'common',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # NOTE: 根据官方文档，CorsMiddleware 必须放在 CommonMiddleware 之前，才能正确处理跨域预检请求（OPTIONS）。
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    'authentication.middleware.LoginLogMiddleware',  # 登录日志中间件
]

# URL 配置
ROOT_URLCONF = 'config.urls'

# 模板配置
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

# WSGI 配置
WSGI_APPLICATION = 'config.wsgi.application'

# # 数据库配置 -- 测试时可以使用 sqlite3
# 默认配置: 使用 sqlite3
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# 我们使用 PostgreSql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'efms_db'),
        'USER': os.getenv('DB_USER', 'efms_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'CONN_MAX_AGE': 600,  # 从 60s -> 600s
        'OPTIONS': {
            'connect_timeout': 10,
            # 新增: 30秒查询超时 在数据库层面卡死超过30秒的恶意或劣质查询，保护数据库不被拖垮。
            'options': '-c statement_timeout=30000',
        },
    }
}

# XXX: redis 缓存配置
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')

REDIS_URL_BASE = f'{REDIS_HOST}:{REDIS_PORT}'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        # 无密码 → redis://localhost:6379/1
        # 有密码 → redis://:mypassword@localhost:6379/1
        'LOCATION': f'redis://{REDIS_URL_BASE}/1' if not REDIS_PASSWORD else f'redis://:{REDIS_PASSWORD}@{REDIS_URL_BASE}/1',
        # 'LOCATION': f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/1',
        # 'LOCATION': f'{REDIS_URL_BASE}/1' if not REDIS_PASSWORD else f'redis://:{REDIS_PASSWORD}@{REDIS_URL_BASE}/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
            }
        },
        'KEY_PREFIX': 'efms:'
    }
}

# 会话配置（使用 redis）
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 86400 * 7  # 7天
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# 密码验证
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 10,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'utils.validators.CustomPasswordValidator',  # 自定义密码验证器
    },
]

# XXX: 国际化配置
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# XXX: 静态文件配置
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# 媒体文件配置
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 文件存储根目录
FILE_STORAGE_ROOT = os.path.expanduser(os.getenv('FILE_STORAGE_ROOT', '~/root'))

# 默认主键字段类型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 自定义用户模型
AUTH_USER_MODEL = 'users.User'

# XXX: REST Framework 配置
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'common.pagination.CustomPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'common.responses.custom_exception_handler',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    }
}

# XXX: JWT 配置
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(
        minutes=int(os.getenv('JWT_ACCESS_TOKEN_LIFETIME', 120))
    ),
    'REFRESH_TOKEN_LIFETIME': timedelta(
        minutes=int(os.getenv('JWT_REFRESH_TOKEN_LIFETIME', 10080))
    ),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# XXX: CORS 配置
CORS_ALLOW_ALL_ORIGINS = False

# NOTE: 硬编码了 http://localhost:3000 等地址，生产环境虽然 development.py 被隔离了，
#   但 base.py 里的 localhost 依然会生效。建议生产环境的真实域名（如 https://www.myefms.com）通过 .env 文件注入
#   （通过 .env 注入生产域名，开发环境由 development.py 覆盖）
#   # base.py
#   CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000,http://localhost:8080').split(',')
# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:3000',
#     'http://localhost:8080',
#     'http://127.0.0.1:3000',
#     'http://127.0.0.1:8080',
# ]
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in os.getenv(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:8080,http://localhost:3000,http://127.0.0.1:8080,http://127.0.0.1:3000'
).split(',') if origin.strip()]
CORS_ALLOW_CREDENTIALS = True

# XXX: API 文档配置
SPECTACULAR_SETTINGS = {
    'TITLE': '企业文件管理系统 API',
    'DESCRIPTION': 'EFMS 企业文件管理系统 RESTful API 文档',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
}

# 验证码配置
CAPTCHA_IMAGE_SIZE = (120, 40)
CAPTCHA_LENGTH = 4
CAPTCHA_TIMEOUT = 300  # 5分钟

# 登录安全配置
LOGIN_MAX_ATTEMPTS = 3
LOGIN_LOCKOUT_DURATION = 60  # 分钟
MAX_CONCURRENT_SESSIONS = 3

# 密码有效期配置
PASSWORD_EXPIRE_DAYS = 90
PASSWORD_EXPIRE_WARNING_DAYS = 7

# 日志配置
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
        'json': {
            'format': '{"level": "%(levelname)s", "time": "%(asctime)s", "module": "%(module)s", "message": "%(message)s"}',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 1024 * 1024 * 100,  # 100MB
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8',  # 必须加
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'efms': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Celery 配置
# NOTE: 在现代的 Celery 5.x 中，建议加上时区和任务追踪的明确配置，避免时区导致的定时任务时间错乱：
CELERY_WORKER_PREFETCH_MULTIPLIER = 1  # 防止长任务阻塞队列
CELERY_ACKS_LATE = True  # 任务执行完再确认，防止 worker 挂掉丢失任务

CELERY_BROKER_URL = f'redis://{REDIS_URL_BASE}/2' if not REDIS_PASSWORD else f'redis://:{REDIS_PASSWORD}@{REDIS_URL_BASE}/2'
CELERY_RESULT_BACKEND = f'redis://{REDIS_URL_BASE}/3' if not REDIS_PASSWORD else f'redis://:{REDIS_PASSWORD}@{REDIS_URL_BASE}/3'
# CELERY_BROKER_URL = f'{REDIS_URL_BASE}/2' if not REDIS_PASSWORD else f'redis://:{REDIS_PASSWORD}@{REDIS_URL_BASE}/2'
# CELERY_RESULT_BACKEND = f'{REDIS_URL_BASE}/3' if not REDIS_PASSWORD else f'redis://:{REDIS_PASSWORD}@{REDIS_URL_BASE}/3'
# CELERY_BROKER_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/2'
# CELERY_RESULT_BACKEND = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/3'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True
CELERY_TASK_TRACK_STARTED = True
# NOTE: 硬超时（TimeLimit）到期时，Celery 会直接向 Worker 进程发送 SIGKILL (强制杀死)，任务连一点“临终遗言”的机会都没有。
#   对于文件处理任务，可能会导致临时文件没清理、数据库事务没回滚等僵尸状态。
#   修复：配合使用软超时（SoftTimeLimit），它会先发 SIGTERM，让任务能捕获异常并做清理：
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60  # 25分钟软超时，抛出 SoftTimeLimitExceeded 异常
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30分钟后如果还没死，再硬杀

# 邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.example.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
```

#### 2.2.2 开发环境配置 (config/settings/development.py)

```python
# config/settings/development.py
"""
开发环境配置
"""

import socket
from .base import *

# 开发模式
DEBUG = True

# 允许所有主机访问
ALLOWED_HOSTS = ['*']

# 开发环境数据库（可使用 SQLite）
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# 调试工具栏
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

# # 原来的: INTERNAL_IPS = ['127.0.0.1']
# NOTE: 如果你以后使用 Docker 容器跑 Django，或者通过局域网 IP（如 192.168.x.x）访问，Debug Toolbar 将不会显示。
#   记得 import socket

INTERNAL_IPS = ['127.0.0.1', '10.0.2.2']
# 自动获取当前主机 IP，方便局域网调试
try:
    INTERNAL_IPS.append(socket.gethostbyname(socket.gethostname()))
except Exception:
    pass

# 开发环境 CORS
# NOTE: 根据 django-cors-headers 的严格规则：
#   CORS_ALLOW_CREDENTIALS 和 CORS_ALLOW_ALL_ORIGINS 不能同时为 True。这会在开发环境启动时直接抛出 ValueError。
CORS_ALLOW_CREDENTIALS = False
CORS_ALLOW_ALL_ORIGINS = True

# 开发环境日志级别
LOGGING['loggers']['django']['level'] = 'DEBUG'
LOGGING['loggers']['efms']['level'] = 'DEBUG'

# # 开发环境静态文件
# STATICFILES_DIRS = [BASE_DIR / 'static']

# # TODO: 如果在开发环境想直接调试 Celery 任务而不启动 worker，可以在 development.py 加：
# CELERY_TASK_ALWAYS_EAGER = True
# CELERY_TASK_EAGER_PROPAGATES = True
```

#### 2.2.3 生产环境配置 (config/settings/production.py)

```python
# config/settings/production.py
"""
生产环境配置
"""

from .base import *

# 生产模式
DEBUG = False

# 安全配置
# NOTE: 生产环境中你开启了 SECURE_SSL_REDIRECT = True（强制 HTTPS）。
#   但通常生产环境会使用 Nginx 作为反向代理，Nginx 负责卸载 SSL，然后通过 HTTP 把请求转发给 Django。
#   如果不告诉 Django“我前面有个代理，真实请求其实是 HTTPS”，Django 会认为用户访问的是 HTTP，然后无限循环重定向。
# 告诉 Django 从 HTTP_X_FORWARDED_PROTO 获取真实协议
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# 生产环境 CORS
CORS_ALLOW_ALL_ORIGINS = False

# 生产环境日志级别
LOGGING['loggers']['django']['level'] = 'WARNING'
LOGGING['loggers']['efms']['level'] = 'INFO'
# 文件日志使用 JSON 格式
LOGGING['handlers']['file']['formatter'] = 'json'
```

#### 2.2.4 修改 settings/__init__.py

```python
# config/settings/__init__.py
"""
根据环境变量加载对应的配置文件
"""

import os

settings_module = os.getenv('DJANGO_SETTINGS_MODULE', 'config.settings.development')

if settings_module == 'config.settings.development':
    from .development import *
elif settings_module == 'config.settings.production':
    from .production import *
else:
    from .base import *
```

### 2.3 修改 manage.py

```python
#!/usr/bin/env python
# manage.py

import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
```

---

## 3. 数据库模型设计

### 3.1 公共模型基类 (common/models.py)

```python
# common/models.py
"""
公共模型基类
提供所有模型公用的字段和方法
"""

# # NOTE: 如何使用本模块的 BaseModel
# class Document(BaseModel):
#     file_name = models.CharField('文件名', max_length=255)
#     folder = models.ForeignKey('Folder', on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = 'biz_document'
#         verbose_name = '文档'
#         verbose_name_plural = '文档'
#         default_related_name = 'documents'
#
#         indexes = [
#             # IMPORTANT: 1. 必须把基类的索引显式写出来，并加上符合规范的 name
#             models.Index(fields=['created_at'], name='idx_biz_document_created_at'),
#             # NOTE: 根据最左前缀原则, 如果你写了 fields=['is_deleted', 'deleted_at'] 就不需要再写 fields=['is_deleted'] 了
#             #   意思是：只要你建了 (is_deleted, deleted_at) 这个联合索引，
#             #   当你的查询条件只有 is_deleted 时（比如 NotDeletedManager 里的 filter(is_deleted=False)），
#             #   数据库是可以直接使用这个联合索引的，不需要单独再建一个 is_deleted 的单列索引。
#             models.Index(fields=['is_deleted'], name='idx_biz_document_is_deleted'),
#             models.Index(fields=['is_deleted', 'deleted_at'], name='idx_biz_document_deleted_time'),
#
#             # IMPORTANT: 2. 然后再写自己特有的索引
#             models.Index(fields=['file_name'], name='idx_biz_document_name'),
#             models.Index(fields=['folder'], name='idx_biz_document_folder'),
#
#         ]

from django.db import models
from django.utils import timezone
import uuid


# Create your models here.
# common/models.py

# # 关于本文件中模型类的继承:
#               models.Model
#             /     |       \
# TimeStampModel  UUIDModel  SoftDeleteModel
#             \     |       /
#              \    |     /
#               BaseModel

# # 关于本模型中管理类的继承
#          models.Manager
#          /            \
# NotDeletedManager  AllManager


class TimeStampModel(models.Model):
    """
    时间戳模型基类
    自动记录创建时间和更新时间
    """
    # db_index: 若为 True，Django 会为该字段在数据库中创建索引，可加速对该字段的查询和过滤，默认为 False。
    # Note: auto_now_add: 只有在首次创建记录的时候把当前时间加上去, 后续如果对记录进行修改, 这个值不会改变
    #   作为对比, auto_now 会在每次修改记录的时候将字段值修改为当前时间
    created_at = models.DateTimeField(
        '创建时间',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        '更新时间',
        auto_now=True
    )

    class Meta:
        # 让 TimeStampModel 不可以独立实例化, 必须经过某个类继承 TimeStampModel,
        #   继承这个类之后, 继承这个类的子类就会自动拥有 created_at 和 updated_at 这两个字段
        #   可以简单理解为 接口 -- 只是为了易于理解, 其实并非接口, 只不过和接口的行为很像

        # Note: 因为本类是 abstract=True，这里不能指定 name 参数,
        #   必须让 Django 在生成具体子表时自动分配唯一名称
        abstract = True
        indexes = [
            models.Index(fields=['created_at'])
        ]


class UUIDModel(models.Model):
    """
    UUID 主键模型基类
    使用 UUID 作为主键, 避免 ID 被猜测
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID'
    )

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """
    软删除模型基类
    删除时不真正删除数据, 而是标记为已删除
    """
    is_deleted = models.BooleanField(
        '是否删除', default=False,
    )

    deleted_at = models.DateTimeField(
        '删除时间',
        null=True,
        blank=True
    )

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['is_deleted'])
        ]

    def soft_delete(self):
        """软删除"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])

    def restore(self):
        """恢复删除"""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=['is_deleted', 'deleted_at'])

    def hard_delete(self):
        """硬删除 - 真正删除"""
        super().delete()

    @classmethod
    def bulk_soft_delete(cls, queryset):
        """批量软删除"""
        return queryset.update(
            is_deleted=True,
            deleted_at=timezone.now()
        )

    @classmethod
    def bulk_restore(cls, queryset):
        """批量恢复"""
        return queryset.update(
            is_deleted=False,
            deleted_at=None
        )


class NotDeletedManager(models.Manager):
    """
    活跃记录管理器
    默认只查询未删除的记录
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class AllManager(models.Manager):
    """
    全部记录管理器
    包含所有记录（包括已删除的）
    """
    pass


class BaseModel(UUIDModel, TimeStampModel, SoftDeleteModel):
    """
    基础模型类
    包含 UUID 主键、时间戳和软删除功能
    """
    # 默认管理器：只返回未删除的记录
    objects = NotDeletedManager()
    # 全部记录管理器（包括已删除的）
    all_objects = AllManager()

    class Meta:
        abstract = True

        # BaseModel 不需要额外定义 indexes，
        #   它会自动继承上面 TimeStampModel 和 SoftDeleteModel 里的索引定义
```

### 3.2 常量定义 (common/constants.py)

```python
# common/constants.py
"""
系统常量定义
"""

__all__ = [
    'KiB', 'MiB', 'GiB',
    'UserRole', 'UserStatus', 'Gender', 'DepartmentStatus', 'SecurityLevel', 'FileStatus',
    'ApprovalStatus', 'ApprovalType', 'LogLevel', 'DepartmentLevel', 'LoginResultType',
    'ActionType', 'ModuleType', 'CodeType', 'CodePurposeType', 'LoginLogoutActionType',
    'ROLE_LEVELS', 'SECURITY_LEVEL_RANK',
    'DEFAULT_DEPT_QUOTA', 'FILE_TYPE_CONFIG', 'DEPARTMENT_LEVEL_RANK',
    'EXTENSION_TO_CATEGORY', 'MAX_SINGLE_FILE_SIZE', 'DEFAULT_FILE_SIZE',
]

from typing import TypedDict

from django.db.models import TextChoices

# 计算机二进制单位定义
KiB = 1024
MiB = 1024 * KiB
GiB = 1024 * MiB
DEFAULT_FILE_SIZE = 100 * MiB
MAX_SINGLE_FILE_SIZE = 5 * GiB


# # 关于 TextChoices 继承顺序: 为什么要先继承 str 再 Enum:
# class Status(TextChoices):
#     PENDING = 'PENDING', 'pending'
#     APPROVED = 'APPROVED', 'approved'
# 先 str 后 Enum:
#   TextChoices 的 MRO: TextChoices -> str -> Enum -> object
# 反之:
#   TextChoices -> EnumMeta -> Enum -> str   -> object
# 如果继承顺序是 Enum -> str:
#   我们 print(Status.PENDING) 则会根据 MRO 先去寻找 Enum 的 __str__ 魔法方法;
#       那么打印的结果是: Status.PENDING, 而不是 PENDING
# 如果继承顺序是 str -> Enum:
#   我们 调用 .upper()方法或进行字符串拼接 则会先去调用字符串的原生方法

# 代码段: 模仿 Django 的 TextChoices 类实现
# from enum import Enum
# class TextChoices(str, Enum):
#     def __new__(cls, value: str, label: str):
#         # 下面的 `# noinspection PyTypeChecker`: noinspect 注释用来压制警告
#         # noinspection PyTypeChecker
#         obj = str.__new__(cls, value)
#         obj._value_ = value
#         obj.label = label
#
#         # 假设一个类 UserRole 继承了 TextChoices, 那么这里的 obj 是 UserRole 对象,
#         # !!但是, isinstance(obj) == str 这个断言的结果是 True!
#         return obj
#
#     def __str__(self):
#         return self.value
#
#     def __init_subclass__(cls, **kwargs):  # 这里的 cls 不是 TextChoices 类, 而是 继承了TextChoices的子类本身
#         super().__init_subclass__(**kwargs)
#         cls.choices = [(m.value, m.label) for m in cls]
#         cls.values = [m.value for m in cls]
#         cls.labels = [m.label for m in cls]


class UserRole(TextChoices):
    """用户角色枚举"""
    SUPER_ADMIN = 'SUPER_ADMIN', '超级管理员'
    SENIOR_ADMIN = 'SENIOR_ADMIN', '高级管理员'
    ADMIN = 'ADMIN', '普通管理员'
    EMPLOYEE = 'EMPLOYEE', '普通员工'


class UserStatus(TextChoices):
    """用户状态枚举"""
    ACTIVE = 'ACTIVE', '在职'
    RESIGNED = 'RESIGNED', '离职'
    ON_LEAVE = 'ON_LEAVE', '请假'
    DISABLED = 'DISABLED', '停用'


class Gender(TextChoices):
    """性别枚举"""
    MALE = 'MALE', '男'
    FEMALE = 'FEMALE', '女'
    SECRET = 'SECRET', '保密'


class DepartmentStatus(TextChoices):
    """'部门'状态枚举"""
    ACTIVE = 'ACTIVE', '正常'
    DISABLED = 'DISABLED', '停用'


class SecurityLevel(TextChoices):
    """文件安全等级枚举"""
    TOP_SECRET = 'TOP_SECRET', '绝密'
    CONFIDENTIAL = 'CONFIDENTIAL', '机密'
    NORMAL = 'NORMAL', '普通'
    PUBLIC = 'PUBLIC', '公共'


class DepartmentLevel(TextChoices):
    """部门等级枚举"""
    TOP_LEVEL = 'TOP_LEVEL', '顶级'
    HIGH_LEVEL = 'HIGH_LEVEL', '高级'
    MIDDLE_LEVEL = 'MIDDLE_LEVEL', '中级'
    LOW_LEVEL = 'LOW_LEVEL', '低级'


class ApprovalStatus(TextChoices):
    """审批状态枚举"""
    PENDING = 'PENDING', '待审批'
    APPROVED = 'APPROVED', '已通过'
    REJECTED = 'REJECTED', '已拒绝'
    CANCELLED = 'CANCELLED', '已撤回'
    EXPIRED = 'EXPIRED', '已过期'


class ApprovalType(TextChoices):
    """审批类型枚举"""
    FILE_DELETE = 'FILE_DELETE', '删除文件'
    SECURITY_LEVEL_CHANGE = 'SECURITY_LEVEL_CHANGE', '安全等级变更'
    USER_REGISTRATION = 'USER_REGISTRATION', '用户注册审核'
    USER_STATUS_CHANGE = 'USER_STATUS_CHANGE', '用户状态变更'
    CROSS_DEPT_ACCESS = 'CROSS_DEPT_ACCESS', '跨部门访问'
    STORAGE_EXPANSION = 'STORAGE_EXPANSION', '存储扩容'
    API_KEY_REQUEST = 'API_KEY_REQUEST', 'API Key 申请'


class LogLevel(TextChoices):
    """日志级别枚举"""
    CRITICAL = 'CRITICAL', '关键'
    IMPORTANT = 'IMPORTANT', '重要'
    NORMAL = 'NORMAL', '一般'


class ActionType(TextChoices):
    """操作类型枚举"""
    CREATE = 'CREATE', '新建'
    READ = 'READ', '读取'
    UPDATE = 'UPDATE', '更新'
    DELETE = 'DELETE', '删除'
    LOGIN = 'LOGIN', '登录'
    LOGOUT = 'LOGOUT', '登出'
    APPLY = 'APPLY', '申请'
    APPROVE = 'APPROVE', '审批通过'
    REJECT = 'REJECT', '审批拒绝'
    EXPORT = 'EXPORT', '导出'
    DOWNLOAD = 'DOWNLOAD', '下载'
    UPLOAD = 'UPLOAD', '上传'


class ModuleType(TextChoices):
    """模块类型枚举"""
    FILE = 'FILE', '文件'
    USER = 'USER', '用户'
    DEPT = 'DEPT', '部门'
    APPROVAL = 'APPROVAL', '审批'
    SYSTEM = 'SYSTEM', '系统'
    AUTH = 'AUTH', '授权'


class CodeType(TextChoices):
    """验证码枚举"""
    PHONE_CODE = 'PHONE_CODE', '手机验证码'
    EMAIL_CODE = 'EMAIL_CODE', '邮箱验证码'
    IMAGE_CODE = 'IMAGE_CODE', '图形验证码'


class CodePurposeType(TextChoices):
    """验证码用途枚举"""
    REGISTER = 'REGISTER', '注册'
    LOGIN = 'LOGIN', '登录'
    RESET_PASSWORD = 'RESET_PASSWORD', '重置密码'
    BIND_PHONE = 'BIND_PHONE', '绑定手机'
    BIND_EMAIL = 'BIND_EMAIL', '绑定邮箱'


class LoginLogoutActionType(TextChoices):
    """用户登录/登出行为枚举"""
    LOGIN = 'LOGIN', '登录'
    LOGOUT = 'LOGOUT', '登出'
    LOGIN_FAILED = 'LOGIN_FAILED', '登录失败'
    FORCE_LOGOUT = 'FORCE_LOGOUT', '强制登出'


class LoginResultType(TextChoices):
    """登录结果枚举"""
    SUCCESS = 'SUCCESS', '成功'
    FAILURE = 'FAILURE', '失败'


ROLE_LEVELS: dict[UserRole, int] = {
    UserRole.EMPLOYEE: 1,
    UserRole.ADMIN: 2,
    UserRole.SENIOR_ADMIN: 3,
    UserRole.SUPER_ADMIN: 4,
}

# 文件安全等级的权重定义
SECURITY_LEVEL_RANK: dict[SecurityLevel, int] = {
    SecurityLevel.PUBLIC: 1,
    SecurityLevel.NORMAL: 2,
    SecurityLevel.CONFIDENTIAL: 3,
    SecurityLevel.TOP_SECRET: 4,
}

# 部门的权重等级定义
DEPARTMENT_LEVEL_RANK: dict[DepartmentLevel, int] = {
    DepartmentLevel.TOP_LEVEL: 4,
    DepartmentLevel.HIGH_LEVEL: 3,
    DepartmentLevel.MIDDLE_LEVEL: 2,
    DepartmentLevel.LOW_LEVEL: 1,
}

# 默认部门存储配额（字节）
DEFAULT_DEPT_QUOTA = 20 * GiB


# LINK: departments.models.Department.update_storage_used
class FileStatus(TextChoices):
    """文件状态枚举"""
    NORMAL = 'NORMAL', '正常'
    LOCKED = 'LOCKED', '锁定'
    APPROVING = 'APPROVING', '审批中'


# frozenset[str] 语法需要 Python 3.9+。Django 5.x 支持 Python 3.10+，所以这不是问题，但如果需要向后兼容，可以使用:
# `from __future__ import annotations`  # 文件开头添加
class FileTypeRule(TypedDict):
    extensions: frozenset[str]
    max_size: int


# 文件相关配置
FILE_TYPE_CONFIG: dict[str, FileTypeRule] = {
    'word': {
        'extensions': frozenset(['.doc', '.docx', '.odt']),
        'max_size': 100 * MiB,
    },
    'excel': {
        'extensions': frozenset(['.xls', '.xlsx', '.csv']),
        'max_size': 100 * MiB,
    },
    'ppt': {
        'extensions': frozenset(['.ppt', '.pptx', '.odp']),
        'max_size': 200 * MiB,
    },
    'pdf': {
        'extensions': frozenset(['.pdf']),
        'max_size': 200 * MiB,
    },
    'text': {
        'extensions': frozenset(['.txt', '.md', '.log', '.gitignore']),
        'max_size': 50 * MiB,
    },
    'code': {
        'extensions': frozenset(
            ['.py', '.java', '.c', '.cpp', '.js', '.go', '.rs', '.ts', '.jsx', '.tsx', '.html', '.css',
             '.scss', '.sql', '.sh', '.php', '.vue', '.svelte']),
        'max_size': 50 * MiB,
    },
    'config': {
        'extensions': frozenset(['.json', '.yaml', '.yml', '.toml', '.xml']),
        'max_size': 50 * MiB,
    },
    'image': {
        'extensions': frozenset(['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp']),
        'max_size': 50 * MiB,
    },
    'audio': {
        'extensions': frozenset(['.mp3', '.wav', '.flac', '.aac', '.ogg']),
        'max_size': 500 * MiB,
    },
    'video': {
        'extensions': frozenset(['.mp4', '.avi', '.mkv', '.mov', '.wmv']),
        'max_size': 2 * GiB,
    },
    'archive': {
        'extensions': frozenset(['.zip', '.rar', '.7z', '.tar', '.gz']),
        'max_size': MAX_SINGLE_FILE_SIZE,
    },
    'design': {
        'extensions': frozenset(['.psd', '.ai', '.sketch', '.fig']),
        'max_size': 2 * GiB,
    },
    'other': {
        'extensions': frozenset(),
        'max_size': MAX_SINGLE_FILE_SIZE,
    },
}

# 反向索引：扩展名 → 类别（O(1) 查找）
EXTENSION_TO_CATEGORY: dict[str, str] = {}
for _category, _config in FILE_TYPE_CONFIG.items():
    for _ext in _config['extensions']:
        EXTENSION_TO_CATEGORY[_ext] = _category

```

### 3.3 部门模型 (departments/models.py)

```python
# departments/models.py
"""
部门管理模型
"""

from collections import deque

from django.db import models
from django.core.validators import MinLengthValidator

from common.models import BaseModel, NotDeletedManager
from common.constants import DEFAULT_DEPT_QUOTA, DepartmentStatus, DEPARTMENT_LEVEL_RANK, DepartmentLevel, FileStatus


# Create your models here.

# departments/models.py


class Department(BaseModel):
    """
    部门模型
    支持多级树形结构
    """
    # 在一个支持多级树形结构的'部门'表中，**全局**强制要求'部门'名称唯一是不合理的。
    #   比如：一级部门叫“研发中心”，二级'部门'可能也会叫“研发部”，甚至不同的顶级分公司下都可能有“人力资源部”。
    name = models.CharField(
        '部门名称',
        max_length=100,
    )
    code = models.CharField(
        '部门编码',
        max_length=20,
        unique=True,
        validators=[MinLengthValidator(2)],
        help_text='如: TECH、HR、FIN等'
    )

    # 注意: BaseModel 中实现了软删除, 但是以前我也写了 on_delete=models.CASCADE(级联删除)
    #   这意味着，如果有人（或通过某些脚本）对父部门调用了 hard_delete()，
    #   底下的所有子部门在数据库层面会被物理删除，连软删除恢复的机会都没有，这破坏了软删除的初衷。
    #   修复: 使用 SET_NULL
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='上级部门'
    )
    head = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_departments',
        verbose_name='部门负责人'
    )
    description = models.TextField(
        '部门描述',
        blank=True,
        default=''
    )

    # 笔记：
    #   从 Django 3.2 开始，Django 提供了一个更高级的用法：你可以直接把枚举类本身传给 choices，
    #   不需要加 .choices。Django 底层会自动去提取。
    #   如: choices=DepartmentStatus
    status = models.CharField(
        '部门状态',
        max_length=20,
        choices=DepartmentStatus,
        default=DepartmentStatus.ACTIVE,
    )
    sort_order = models.IntegerField(
        '部门排序权重',
        default=DEPARTMENT_LEVEL_RANK[DepartmentLevel.LOW_LEVEL],
        help_text='数字越大权重越高, 排名越靠前'
    )
    storage_quota = models.BigIntegerField(
        '部门存储配额(字节)',
        default=DEFAULT_DEPT_QUOTA
    )
    storage_used = models.BigIntegerField(
        '部门已用存储(字节)',
        default=0
    )

    # 管理器
    objects = NotDeletedManager()  # 只返回未删除的记录 -- 即部门的状态为 ACTIVE 的部门

    # 关于返回所有记录的管理器, 已经继承自 BaseModel -- all_objects = AllManager()

    class Meta:
        db_table = 'departments'
        verbose_name = '部门'
        verbose_name_plural = verbose_name
        ordering = ['-sort_order', 'code']

        indexes = [
            models.Index(fields=['status'], name='idx_departments_status'),
            models.Index(fields=['code'], name='idx_departments_code'),
            models.Index(fields=['parent'], name='idx_departments_parent'),
            models.Index(fields=['head'], name='idx_departments_head'),
            models.Index(fields=['-sort_order', 'code'], name='idx_departments_sort_code'),
            # 加上基类的索引
            models.Index(fields=['created_at'], name='idx_departments_created_at'),
            models.Index(fields=['is_deleted'], name='idx_departments_is_deleted'),
        ]

        # 联合唯一约束
        # 注意:
        #   在 PostgreSQL（Django 最常用的数据库）中，创建唯一约束时，数据库会自动在底层创建一个对应的唯一索引。
        #   已经定义了两个带条件的唯一约束，数据库其实已经为 name 字段建好了“部分索引”；
        #   此时如果在 name 字段再显式加一个 db_index=True(以前加的), 数据库就会额外再建一个“全量普通索引”。
        constraints = [
            models.UniqueConstraint(
                fields=['parent', 'name'],
                name='unique_dept_name_under_same_parent',
                # 顶级部门 parent 可能为 null, 需要处理 null 值的唯一性
                condition=models.Q(parent_isnull=False)
            ),
            # 如果顶级'部门'名称也要唯一, 可以单独加一个
            models.UniqueConstraint(
                fields=['name'],
                name='unique_top_level_dept_name',
                condition=models.Q(parent_isnull=True)
            )
        ]

    def __str__(self):
        return self.name

    @property
    def full_path(self):
        """获取部门完整路径"""
        # 注意: 这种基于外键的属性，不应该去修改属性本身的代码，而是应该在视图层/查询层解决。
        #   当你知道你需要用到 full_path 时，在获取部门列表的 QuerySet 后面加上 select_related:
        #   departments = Department.objects.select_related('parent__parent__parent').all()
        #   这样 Django 会通过 JOIN 一次性把前三级的部门数据拿出来
        #   此时循环调用 dept.full_path 就完全是 0 次额外查询了！
        path = [self.name]
        parent = self.parent
        while parent:
            path.insert(0, parent.name)  # # ⚠️ 这里会触发查询
            parent = parent.parent  # ⚠️ 这里又会触发查询
        return ' / '.join(path)

    @property
    def level(self):
        """获取部门层级"""
        level = 0
        parent = self.parent
        while parent:
            level += 1
            parent = parent.parent
        return level

    @property
    def storage_usage_percentage(self):
        """存储使用率百分比"""
        if self.storage_quota == 0:
            return 0
        return round((self.storage_used / self.storage_quota) * 100, 2)

    def get_all_children_ids(self):
        """获取所有子部门ID（内存构建法，完美解决 N+1 问题，兼容所有 Django 版本）"""
        # 代码段: 内存构建树
        # 1. 一次性查出所有部门的 id 和 parent_id
        all_depts = list(
            self.__class__.objects.values('id', 'parent_id')
        )

        # 2. 在内存中构建 父ID -> [子ID列表] 的映射字典(O(N)时间复杂度)
        children_map = {}
        for dept in all_depts:
            parent_id = dept['parent_id']
            if parent_id not in children_map:
                children_map[parent_id] = []
            children_map[parent_id].append(dept['id'])

        # 3. 使用双端队列进行 BFS 找出所有子孙 ID
        children_ids = []
        queue = deque(children_map.get(self.pk, []))  # 获取直属子部门放入队列

        while queue:
            current_id = queue.popleft()
            children_ids.append(current_id)
            # 将当前部门的子部门继续加入到队列中
            if current_id in children_map:
                queue.extend(children_map[current_id])

        return children_ids

    def get_all_children(self):
        """
        获取所有子部门(递归/CET/内存构建树)

        """
        # # 注意: 可优化性能
        #     使用了递归的方式来实现 get_all_children、get_all_members 和 full_path。
        #     在 Python 中递归查询数据库是 Django 性能杀手。如果部门有 4 层，每层 10 个部门，
        #     获取所有子部门将触发 1 + 10 + 100 + 1000 = 1111 次 SQL 查询。当调用 update_storage_used 时，性能会灾难性下降。

        # 代码段: 旧的递归查找子孙部门的代码 性能会很差
        #   children = list(self.children.all())
        #   for child in children:
        #       children.extend(child.get_all_children())
        #   return children

        # 代码段: 使用 CTE 一次性获取所有子孙部门ID，解决递归 N+1 问题
        #   from django.db.models import With, F, OuterRef
        #   dept = Department.objects.filter(pk=self.pk)
        #   recursive = With(
        #       dept,
        #       With.recursive(
        #           lambda cte: cte.union(
        #               Department.objects.filter(parent_id=OuterRef('pk'))
        #           )
        #       )
        #   )
        #   # 返回包含自己和所有子孙的 ID 列表
        #   return list(
        #       recursive.annotate(dept_id=F('pk')).values_list('dept_id', flat=True)
        #   )

        # 代码段: 内存构建树
        children_ids = self.get_all_children_ids()
        # 如果不需要保持顺序，使用 in_bulk 效率更高
        children_dict = self.__class__.objects.in_bulk(children_ids)
        return list(children_dict.values())

    def get_all_members(self):
        """获取所有 部门下的成员(包括子部门)"""
        from users.models import User
        # dept_ids = [self.id] + [d.id for d in self.get_all_children()]
        # return User.objects.filter(department_id__in=dept_ids)

        # 获取自身 ID + 所有子孙 ID
        dept_ids = [self.pk] + self.get_all_children_ids()
        return User.objects.filter(department_id__in=dept_ids)

    def update_storage_used(self):
        """更新已用存储"""
        from django.db.models import Sum
        from files.models import File

        # 统计 当前部门以及当前部门的所有子部门(递归) 的文件状态为正常的文件所占用的空间
        # dept_ids = [self.id] + [d.id for d in self.get_all_children()]
        dept_ids = [self.pk] + self.get_all_children_ids()
        total_size = File.objects.filter(
            department_id__in=dept_ids,
            is_deleted=False,
        ).aggregate(total=Sum('file_size'))['total'] or 0

        self.storage_used = total_size
        self.save(update_fields=['storage_used'])

```

### 3.4 用户模型 (users/models.py)

```python
# users/models.py
"""
用户管理模型
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator, MinLengthValidator
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.db import transaction

from common.models import BaseModel, NotDeletedManager, AllManager
from common.constants import UserRole, UserStatus, Gender, CodeType, CodePurposeType, LoginResultType
from common.constants import LoginLogoutActionType


# Create your models here.

# users/models.py


class UserManager(NotDeletedManager, BaseUserManager):
    """
    自定义用户管理器
    支持使用 手机号、邮箱或账号登录
    """

    # 注意: get_queryset 已经被 NotDeletedManager 处理了，默认过滤 is_deleted=False
    #   不要重写 get_queryset 方法，否则会覆盖 NotDeletedManager 的逻辑

    def create_user(self, login_account, password=None, **extra_fields):
        """创建普通用户"""
        # 继承 BaseUserManager 后必须实现 create_user 和 create_superuser 方法
        if not login_account:
            raise ValueError("Login Account is required. (登录账号不能为空)")
        user = self.model(
            login_account=login_account,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login_account, password=None, **extra_fields):
        """创建超级用户"""
        # 继承 BaseUserManager 后必须实现 create_user 和 create_superuser 方法
        extra_fields.setdefault('role', UserRole.SUPER_ADMIN)
        extra_fields.setdefault('status', UserStatus.ACTIVE)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(login_account, password, **extra_fields)

    def get_by_natural_key(self, username):
        """支持使用手机号、邮箱或账号登录"""
        # 尝试按照登录账号查找
        try:
            # 警告:
            #   Django 的认证系统会调用 get_by_natural_key 来查找用户。如果你软删除了一个用户，但他还能登录系统，这是一个安全隐患。
            #   此处为什么不写 return self.get(login_account=username, is_deleted=False)
            #   因为 本类 已经继承了 NotDeletedManager 这个类, 这个类的 get_queryset() 天然过滤了已经删除的用户
            return self.get(login_account=username)
        except self.model.DoesNotExist:
            pass

        # 尝试按照手机号查找
        try:
            return self.get(phone=username)
        except self.model.DoesNotExist:
            pass

        # 尝试按照邮箱查找
        try:
            return self.get(email=username)
        except self.model.DoesNotExist:
            pass

        raise self.model.DoesNotExist(
            f'未找到用户: {username}'
        )


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    用户模型
    继承 Django 的 AbstractBaseUser 类来实现自定义模型
    继承 common.models.BaseModel
    BaseModel 继承了: common.models.UUIDModel, common.models.TimeStampModel, common.models.SoftDeleteModel
    """
    employee_id = models.CharField(
        '员工工号',
        max_length=20,
        unique=True,
        db_index=True,
        editable=False,
        help_text='格式: EMP-YYYYMMDD-XXX'
    )

    login_account = models.CharField(
        '登录账号',
        max_length=50,
        unique=True,
        db_index=True,
        validators=[
            MinLengthValidator(4),
            RegexValidator(
                regex=r'^[a-zA-Z][a-zA-Z0-9_]*$',
                message='账号必须以字母开头，只能包含字母、数字和下划线'
            )
        ]
    )

    # 用户名(显示名称)
    username = models.CharField(
        '用户名',
        max_length=20,
        db_index=True,
    )

    phone = models.CharField(
        '手机号',
        max_length=11,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r'^1[3-9]\d{9}$',
                message='请输入有效的11位手机号',
            )
        ]
    )

    email = models.EmailField(
        '邮箱',
        unique=True,
        null=True,
        blank=True,
        db_index=True,
    )

    avatar = models.ImageField(
        '头像',
        upload_to='avatars/%Y/%m/',
        null=True,
        blank=True,
    )

    gender = models.CharField(
        '性别',
        max_length=10,
        choices=Gender,
        default=Gender.SECRET,
    )

    role = models.CharField(
        '角色',
        max_length=20,
        choices=UserRole,  # 笔记: ✅ Django 3.2+ 支持直接传枚举类
        default=UserRole.EMPLOYEE,  # 笔记: 关于此处能写成: ✅ default=UserRole.EMPLOYEE,  Django 3.2+ 支持直接传枚举成员
    )

    department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members',
        verbose_name='所属部门',
    )

    position = models.CharField(
        '职位',
        max_length=50,
        blank=True,
        default='',
    )

    status = models.CharField(
        '状态',
        max_length=20,
        choices=UserStatus,
        default=UserStatus.ACTIVE,
    )

    join_date = models.DateField(
        '入职日期',
        null=True,
        blank=True,
    )

    leave_date = models.DateField(
        '离职日期',
        null=True,
        blank=True,
    )

    last_login_time = models.DateTimeField(
        '最后登录时间',
        null=True,
        blank=True,
    )

    last_login_ip = models.GenericIPAddressField(
        '最后登录IP',
        null=True,
        blank=True,
    )

    login_failed_count = models.IntegerField(
        '登录失败次数',
        default=0,
    )

    # 账户锁定时间
    locked_until = models.DateTimeField(
        '锁定至',
        null=True,
        blank=True,
    )

    password_changed_at = models.DateTimeField(
        '密码修改时间',
        default=timezone.now,
    )

    password_history = models.JSONField(
        '密码历史',
        default=list,
        help_text='存储最近三次密码的哈希值'
    )

    remark = models.TextField(
        '备注',
        blank=True,
        default=''
    )

    # Django 内置字段
    is_staff = models.BooleanField(
        '是否员工',
        default=False,
        help_text='决定用户是否可以登录 Admin 站点',
    )

    is_active = models.BooleanField(
        '是否激活',
        default=True,
        help_text='用户是否激活'
    )

    # 管理器
    objects = UserManager()  # 只查找未被软删除的记录
    all_objects = AllManager()  # 返回所有记录 包含被软删除的记录

    # 设置登录字段 -- Django 认证系统会使用 USERNAME_FIELD 指定的字段作为登录标识

    # 注意: 这个配置项，用来告诉 Django："在我的系统里，用来唯一标识用户身份、用于登录的字段不叫 username，而叫 login_account"
    #   AbstractBaseUser 内部强制要求子类必须设置这个属性。如果不设置，Django 在启动或执行迁移时会抛出类似这样的错误：
    USERNAME_FIELD = 'login_account'

    # 注意: 这个列表，用来告诉 Django 的 createsuperuser 命令：
    #   "在命令行创建超级用户时，除了要求输入 USERNAME_FIELD 指定的账号和密码之外，还要交互式地要求用户输入这些字段。"

    # 重要: 关于 REQUIRED_FIELDS 的两条铁律
    #   1：绝对不能把 USERNAME_FIELD 里面的字段放进去！
    #   2：绝对不能把 password 放进去！
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['role', 'status']),
            models.Index(fields=['department', 'status']),
            models.Index(fields=['status', 'is_deleted']),  # 常用过滤组合
            models.Index(fields=['join_date']),  # 入职日期查询
        ]

    def __str__(self):
        return f'{self.username}({self.employee_id})'

    @property
    def is_admin(self):
        """是否为管理员(包括超级管理员、高级管理员、普通管理员)"""
        return self.role in frozenset(
            [UserRole.SUPER_ADMIN.value, UserRole.SENIOR_ADMIN.value, UserRole.ADMIN.value]
        )

    @property
    def is_super_admin(self):
        """是否为超级管理员"""
        return self.role == UserRole.SUPER_ADMIN.value

    @property
    def is_senior_admin(self):
        """是否为高级管理员"""
        return self.role == UserRole.SENIOR_ADMIN.value

    @property
    def is_department_admin(self):
        """是否为部门管理员"""
        return self.role == UserRole.ADMIN.value

    @property
    def is_locked(self):
        if self.locked_until:
            return self.locked_until > timezone.now()
        return False

    @property
    def is_password_expired(self):
        """密码是否过期"""
        if not self.password_changed_at:
            return True

        expire_days = getattr(settings, 'PASSWORD_EXPIRE_DAYS', 90)
        expire_date = self.password_changed_at + timedelta(days=expire_days)
        return timezone.now() > expire_date

    @property
    def days_until_password_expire(self):
        """距离密码过期还有多少天"""
        if not self.password_changed_at:
            return 0
        expire_days = getattr(settings, 'PASSWORD_EXPIRE_DAYS', 90)
        expire_date = self.password_changed_at + timedelta(days=expire_days)
        remaining = expire_date - timezone.now()
        return max(0, remaining.days)

    def generate_employee_id(self):
        """生成员工工号"""
        # 注意: 本方法存在并发竞态条件
        #   如果两个请求几乎同时创建用户，它们可能读到相同的 last_user，从而生成相同的 employee_id，
        #       导致 IntegrityError（因为 employee_id 是 unique=True）。
        #   解决方案：使用 select_for_update() 加行锁，并配合事务：
        today = timezone.now().strftime('%Y%m%d')

        # 查找今天已有的最大序号
        # 注意: 查找最大工号的时候, 也需要查找已经被删除用户的 -- 所以要用 User.all_objects 而不是 User.objects
        #   否则，假如有一个 用户 EMP-20010506-0001, 但是其被删除了
        #   如果不查找 被软删除的用户, 那么生成的用户就还是 EMP-20010506-0001!
        prefix = f'EMP-{today}-'

        # # 旧代码
        # last_user = User.objects.filter(
        #     employee_id__startswith=prefix,
        # ).order_by('-employee_id').first()

        # 代码段: 使用 select_for_update() 加行锁
        last_user = User.all_objects.select_for_update().filter(
            employee_id__startswith=prefix,
        ).order_by('-employee_id').first()

        if last_user:
            try:
                last_num = int(last_user.employee_id[-4:])
                new_num = last_num + 1
            except ValueError:
                new_num = 1
        else:
            new_num = 1
        return f'{prefix}{new_num:04d}'

    def save(self, *args, **kwargs):
        """保存时自动生成员工工号"""

        if not self.employee_id:
            # 注意:
            #   必须在事务中调用，select_for_update 才会生效
            with transaction.atomic():
                self.employee_id = self.generate_employee_id()
        super().save(*args, **kwargs)

    def increase_login_count(self):
        """增加登录失败次数"""

        self.login_failed_count += 1
        # 达到最大失败次数, 锁定账户 登录错误 3 次 锁定 60 分钟
        max_attempts = getattr(settings, 'LOGIN_MAX_ATTEMPTS', 3)
        lockout_duration = getattr(settings, 'LOGIN_LOCKOUT_DURATION', 60)

        # 小优化 -- 只有登录超过最大次数了, 账户被锁定了，才更新锁定账户到期的时间(locked_until 字段)
        update_fields = ['login_failed_count']

        if self.login_failed_count >= max_attempts:
            self.locked_until = timezone.now() + timedelta(minutes=lockout_duration)
            update_fields.append('locked_until')

        self.save(update_fields=update_fields)

    def reset_login_failed(self):
        """重置登录失败次数"""
        self.login_failed_count = 0
        self.locked_until = None
        self.save(update_fields=['login_failed_count', 'locked_until'])

    def update_login_info(self, ip_address):
        """更新登录信息"""
        self.last_login_time = timezone.now()
        self.last_login_ip = ip_address

        # self.reset_login_failed()  # ← 这里内部调用了 save()
        # 改成如下:
        self.login_failed_count = 0
        self.locked_until = None

        self.save(update_fields=[
            'last_login_time',
            'last_login_ip',
            'login_failed_count',
            'locked_until']
        )

    def add_password_to_history(self, password_hash):
        """将密码添加到历史记录"""
        history = self.password_history or []
        history.insert(0, password_hash)
        # 只保留最近三次
        if len(history) > 3:
            self.password_history = history[:3]
        self.password_changed_at = timezone.now()
        self.save(update_fields=['password_history', 'password_changed_at'])


class UserSession(BaseModel):
    """
    用户会话模型
    用于管理用户登录会话和并发控制
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sessions',
        verbose_name='用户'
    )

    session_key = models.CharField(
        '会话 key',
        max_length=100,
        unique=True,
        db_index=True,
    )

    refresh_token = models.CharField(
        '刷新令牌',
        max_length=500,
        unique=True,
        db_index=True,
    )

    ip_address = models.GenericIPAddressField(
        'IP 地址',
    )

    user_agent = models.CharField(
        '用户代理',
        max_length=500,
        blank=True,
        default='',
    )

    device_info = models.JSONField(
        '设备信息',
        default=dict,
    )

    expires_at = models.DateTimeField(
        '过期时间',
    )

    is_active = models.BooleanField(
        '是否活跃',
        default=True,
    )

    class Meta:
        db_table = 'user_sessions'
        verbose_name = '用户会话'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        # 笔记: 在业务中，最常查询的应该是「某个用户的所有活跃会话」，可以加一个联合索引：
        indexes = [
            models.Index(fields=['user', 'is_active'], name='idx_session_user_active'),
            models.Index(fields=['expires_at'], name='idx_session_expires_at'),
        ]

    def __str__(self):
        return f'Username: {self.user.username}, IP: {self.ip_address}'

    @property
    def is_expired(self):
        """会话是否过期"""
        return timezone.now() > self.expires_at


class VerificationCode(BaseModel):
    """
    验证码模型
    用于存储手机验证码和邮箱验证码
    """
    code_type = models.CharField(
        '验证码类型',
        max_length=10,
        choices=CodeType,
    )

    purpose = models.CharField(
        '用途',
        max_length=20,
        choices=CodePurposeType,
    )

    target = models.CharField(
        '目标手机号/邮箱',
        max_length=100,
        db_index=True,
    )

    code = models.CharField(
        '验证码',
        max_length=10,
    )

    expires_at = models.DateTimeField(
        '过期时间',
    )

    is_used = models.BooleanField(
        '是否已使用',
        default=False,
    )

    used_at = models.DateTimeField(
        '使用时间',
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'verification_codes'
        verbose_name = '验证码'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        # 笔记: 验证码校验时最常见的查询是：根据 target + purpose 找到最新的未使用验证码。
        indexes = [
            models.Index(fields=['target', 'purpose', 'is_used'], name='idx_verify_code_lookup'),
        ]

    def __str__(self):
        return f'{self.target} - {self.code}'

    @property
    def is_expired(self):
        """验证码是否过期"""
        return timezone.now() > self.expires_at

    @property
    def is_valid(self):
        """验证码是否有效"""
        return not self.is_used and not self.is_expired

    def mark_as_used(self):
        """标记为已使用"""
        self.is_used = True
        self.used_at = timezone.now()
        self.save(update_fields=['is_used', 'used_at'])


class LoginLog(BaseModel):
    """
    登录日志模型
    记录用户登录/登出行为
    """
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='login_logs',
        verbose_name='用户',
    )

    action = models.CharField(
        '操作类型',
        max_length=20,
        choices=LoginLogoutActionType,
    )

    ip_address = models.GenericIPAddressField(
        'IP 地址',
    )

    user_agent = models.CharField(
        '用户代理',
        max_length=500,
        blank=True,
        default='',
    )

    device_info = models.JSONField(
        '设备信息',
        default=dict,
    )

    location = models.CharField(
        '登录地点',
        max_length=100,
        blank=True,
        default='',
    )

    result = models.CharField(
        '登录结果',
        max_length=10,
        choices=LoginResultType,
    )

    failure_reason = models.CharField(
        '失败原因',
        max_length=200,
        blank=True,
        default='',
    )

    class Meta:
        db_table = 'login_logs'
        verbose_name = '登录日志'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        # 笔记: 查询某个用户的登录历史是很常见的需求
        indexes = [
            models.Index(fields=['user', 'created_at'], name='idx_login_log_user_time'),
            models.Index(fields=['action', 'result'], name='idx_login_log_action_result'),
        ]

    def __str__(self):
        return f'user: {self.user}, action: {self.action}, IP: {self.ip_address}'

```

### 3.5 文件模型(files/models.py)

> [!Note] 
>
> 当前阶段主要是为了能够占位

```python
# files/models.py

"""
文件数据管理模型
"""

# Create your models here.


from django.db import models

from common.models import BaseModel


class File(BaseModel):
    # 警告:
    #  字段名不要写成 department_id
    #  Django 的 ForeignKey 有一个约定 — 你把字段命名为 department，Django 会在数据库层面自动创建 department_id 列;
    #   这样你就可以通过 file.department 访问关联的部门对象，通过 file.department_id 获取部门 ID。
    #   如果把字段命名为 department_id，那 file.department_id 返回的就不是对象了，而且你也无法方便地拿到关联对象。
    department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='files',
        verbose_name='所属部门',
    )

    file_size = models.BigIntegerField(
        '文件大小(字节)',
        default=0
    )

    class Meta:
        db_table = 'files'
        verbose_name = '文件'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']


def __str__(self):
    return f'{self.pk}({str(self.file_size)}bytes)'

```

### 3.5 创建数据库迁移

首先要创建 PostgreSQL数据库：

```bash
# 注册的超级管理员账户
psql.exe" -U postgres

# 创建数据库
CREATE DATABASE efmsproject ENCODING 'UTF8';

# 退出 命令行
\q
```

```bash
# 创建迁移文件
python manage.py makemigrations common
python manage.py makemigrations departments
python manage.py makemigrations users
python manage.py makemigrations files

# 上面四行命令可以全部合为一行代码:
python manage.py makemigrations

# 执行迁移
python manage.py migrate
```

```bash
# 以后只要输入这两行命令即可
python manage.py makemigrations
python manage.py migrate
```

---

## 4. 用户认证系统实现

### 4.1 自定义验证器 (utils/validators.py)

```python
# utils/validators.py
"""
自定义验证器
"""

import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    """
    自定义密码验证器
    要求密码包含大小写字母、数字和特殊字符
    """
    
    def __init__(self, min_length=10, max_length=20):
        self.min_length = min_length
        self.max_length = max_length
    
    def validate(self, password, user=None):
        errors = []
        
        # 检查长度
        if len(password) < self.min_length:
            errors.append(_('密码长度不能少于 %(min_length)d 位') % {'min_length': self.min_length})
        if len(password) > self.max_length:
            errors.append(_('密码长度不能超过 %(max_length)d 位') % {'max_length': self.max_length})
        
        # 检查是否包含大写字母
        if not re.search(r'[A-Z]', password):
            errors.append(_('密码必须包含至少一个大写字母'))
        
        # 检查是否包含小写字母
        if not re.search(r'[a-z]', password):
            errors.append(_('密码必须包含至少一个小写字母'))
        
        # 检查是否包含数字
        if not re.search(r'\d', password):
            errors.append(_('密码必须包含至少一个数字'))
        
        # 检查是否包含特殊字符
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password):
            errors.append(_('密码必须包含至少一个特殊字符'))
        
        # 检查是否包含用户名或手机号
        if user:
            if user.login_account and user.login_account.lower() in password.lower():
                errors.append(_('密码不能包含登录账号'))
            if user.phone and user.phone in password:
                errors.append(_('密码不能包含手机号'))
        
        if errors:
            raise ValidationError(errors)
    
    def get_help_text(self):
        return _(
            '密码长度为 %(min_length)d-%(max_length)d 位，'
            '必须包含大写字母、小写字母、数字和特殊字符' % {
                'min_length': self.min_length,
                'max_length': self.max_length
            }
        )


def validate_phone(value):
    """验证手机号格式"""
    if not re.match(r'^1[3-9]\d{9}$', value):
        raise ValidationError(_('请输入有效的11位手机号'))


def validate_email(value):
    """验证邮箱格式"""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, value):
        raise ValidationError(_('请输入有效的邮箱地址'))


def validate_login_account(value):
    """验证登录账号格式"""
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]{3,19}$', value):
        raise ValidationError(_('账号必须以字母开头，4-20位，只能包含字母、数字和下划线'))
```

### 4.2 自定义异常 (utils/exceptions.py)

```python
# utils/exceptions.py
"""
自定义异常类
"""

from rest_framework import status
from rest_framework.exceptions import APIException


class BusinessException(APIException):
    """
    业务异常基类
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '业务处理失败'
    default_code = 'business_error'
    
    def __init__(self, detail=None, code=None, status_code=None):
        if detail is not None:
            self.detail = {'message': detail, 'code': code or self.default_code}
        else:
            self.detail = {'message': self.default_detail, 'code': self.default_code}
        
        if status_code is not None:
            self.status_code = status_code


class AuthenticationFailedException(BusinessException):
    """认证失败异常"""
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = '认证失败'
    default_code = 'authentication_failed'


class PermissionDeniedException(BusinessException):
    """权限不足异常"""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = '权限不足'
    default_code = 'permission_denied'


class NotFoundException(BusinessException):
    """资源不存在异常"""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = '资源不存在'
    default_code = 'not_found'


class ValidationException(BusinessException):
    """验证失败异常"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '数据验证失败'
    default_code = 'validation_error'


class AccountLockedException(BusinessException):
    """账户锁定异常"""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = '账户已被锁定'
    default_code = 'account_locked'


class PasswordExpiredException(BusinessException):
    """密码过期异常"""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = '密码已过期，请修改密码'
    default_code = 'password_expired'


class TooManyAttemptsException(BusinessException):
    """尝试次数过多异常"""
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = '操作过于频繁，请稍后再试'
    default_code = 'too_many_attempts'


class VerificationCodeException(BusinessException):
    """验证码异常"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '验证码错误'
    default_code = 'verification_code_error'
```

### 4.3 统一响应格式 (common/responses.py)

```python
# common/responses.py
"""
统一响应格式
"""

from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import traceback
from django.conf import settings
from utils.exceptions import BusinessException


def standard_response(data=None, message='success', code=200, status_code=status.HTTP_200_OK):
    """
    标准响应格式
    
    Args:
        data: 响应数据
        message: 响应消息
        code: 业务状态码
        status_code: HTTP状态码
    
    Returns:
        Response 对象
    """
    return Response(
        {
            'code': code,
            'message': message,
            'data': data,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        },
        status=status_code
    )


def success_response(data=None, message='操作成功'):
    """成功响应"""
    return standard_response(data=data, message=message, code=200)


def error_response(message='操作失败', code=400, status_code=status.HTTP_400_BAD_REQUEST, detail=None):
    """错误响应"""
    response_data = {
        'code': code,
        'message': message,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    if detail:
        response_data['detail'] = detail
    return Response(response_data, status=status_code)


def custom_exception_handler(exc, context):
    """
    自定义异常处理器
    """
    # 调用 DRF 默认异常处理器
    from rest_framework.views import exception_handler
    response = exception_handler(exc, context)
    
    if response is not None:
        # 处理 DRF 异常
        if isinstance(exc, BusinessException):
            return response
        
        # 标准化错误响应格式
        error_data = {
            'code': response.status_code,
            'message': '请求处理失败',
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                error_data['message'] = response.data['detail']
            elif 'message' in response.data:
                error_data['message'] = response.data['message']
            else:
                # 处理字段验证错误
                errors = []
                for field, messages in response.data.items():
                    if isinstance(messages, list):
                        errors.append(f'{field}: {", ".join(messages)}')
                    else:
                        errors.append(f'{field}: {messages}')
                error_data['message'] = '; '.join(errors)
                error_data['detail'] = response.data
        
        response.data = error_data
    
    else:
        # 处理非 DRF 异常
        if settings.DEBUG:
            error_data = {
                'code': 500,
                'message': str(exc),
                'detail': traceback.format_exc(),
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
        else:
            error_data = {
                'code': 500,
                'message': '服务器内部错误',
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
        response = Response(error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response
```

### 4.4 分页类 (common/pagination.py)

```python
# common/pagination.py
"""
自定义分页类
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class CustomPagination(PageNumberPagination):
    """
    自定义分页类
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'
    
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('code', 200),
            ('message', 'success'),
            ('data', OrderedDict([
                ('list', data),
                ('pagination', OrderedDict([
                    ('total', self.page.paginator.count),
                    ('page', self.page.number),
                    ('page_size', self.page.paginator.per_page),
                    ('total_pages', self.page.paginator.num_pages),
                ]))
            ])),
            ('timestamp', self.get_timestamp())
        ]))
    
    def get_timestamp(self):
        from datetime import datetime
        return datetime.utcnow().isoformat() + 'Z'
```

### 4.5 JWT 工具类 (authentication/jwt.py)

```python
# authentication/jwt.py
"""
JWT 工具类
"""

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from users.models import UserSession
import uuid


class JWTUtils:
    """JWT 工具类"""
    
    @staticmethod
    def generate_tokens(user):
        """
        为用户生成 JWT Token
        
        Args:
            user: 用户对象
        
        Returns:
            dict: 包含 access_token 和 refresh_token 的字典
        """
        refresh = RefreshToken.for_user(user)
        
        # 添加自定义声明
        refresh['username'] = user.username
        refresh['role'] = user.role
        refresh['employee_id'] = user.employee_id
        
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'expires_in': settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
        }
    
    @staticmethod
    def verify_token(token):
        """
        验证 Token 是否有效
        
        Args:
            token: JWT Token 字符串
        
        Returns:
            dict: Token 解码后的数据
            None: Token 无效
        """
        try:
            access_token = AccessToken(token)
            return {
                'user_id': access_token['user_id'],
                'username': access_token.get('username', ''),
                'role': access_token.get('role', ''),
                'exp': access_token['exp'],
            }
        except (TokenError, InvalidToken):
            return None
    
    @staticmethod
    def refresh_access_token(refresh_token):
        """
        使用 refresh_token 刷新 access_token
        
        Args:
            refresh_token: 刷新令牌
        
        Returns:
            dict: 包含新 access_token 的字典
            None: Token 无效
        """
        try:
            refresh = RefreshToken(refresh_token)
            user_id = refresh['user_id']
            
            # 检查用户是否存在且活跃
            from users.models import User
            try:
                user = User.objects.get(id=user_id, is_active=True, is_deleted=False)
            except User.DoesNotExist:
                return None
            
            # 生成新的 access_token
            return {
                'access_token': str(refresh.access_token),
                'expires_in': settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
            }
        except (TokenError, InvalidToken):
            return None
    
    @staticmethod
    def blacklist_token(refresh_token):
        """
        将 Token 加入黑名单（登出时使用）
        
        Args:
            refresh_token: 刷新令牌
        """
        try:
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()
            return True
        except (TokenError, InvalidToken):
            return False


class SessionManager:
    """会话管理器"""
    
    @staticmethod
    def create_session(user, refresh_token, request):
        """
        创建用户会话
        
        Args:
            user: 用户对象
            refresh_token: 刷新令牌
            request: 请求对象
        """
        # 获取客户端信息
        ip_address = SessionManager.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # 解析设备信息
        device_info = SessionManager.parse_user_agent(user_agent)
        
        # 计算过期时间
        expires_at = timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
        
        # 检查并发会话数量
        SessionManager.check_concurrent_sessions(user)
        
        # 创建会话
        session = UserSession.objects.create(
            user=user,
            session_key=str(uuid.uuid4()),
            refresh_token=refresh_token,
            ip_address=ip_address,
            user_agent=user_agent,
            device_info=device_info,
            expires_at=expires_at
        )
        
        return session
    
    @staticmethod
    def get_client_ip(request):
        """获取客户端 IP 地址"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        return ip
    
    @staticmethod
    def parse_user_agent(user_agent):
        """解析 User Agent"""
        # 简单解析，实际可使用 user-agents 库
        device_info = {
            'user_agent': user_agent,
            'is_mobile': 'Mobile' in user_agent,
            'is_tablet': 'Tablet' in user_agent,
            'is_pc': 'Mobile' not in user_agent and 'Tablet' not in user_agent,
        }
        
        # 解析浏览器
        if 'Chrome' in user_agent:
            device_info['browser'] = 'Chrome'
        elif 'Firefox' in user_agent:
            device_info['browser'] = 'Firefox'
        elif 'Safari' in user_agent:
            device_info['browser'] = 'Safari'
        elif 'Edge' in user_agent:
            device_info['browser'] = 'Edge'
        else:
            device_info['browser'] = 'Unknown'
        
        # 解析操作系统
        if 'Windows' in user_agent:
            device_info['os'] = 'Windows'
        elif 'Mac' in user_agent:
            device_info['os'] = 'MacOS'
        elif 'Linux' in user_agent:
            device_info['os'] = 'Linux'
        elif 'Android' in user_agent:
            device_info['os'] = 'Android'
        elif 'iOS' in user_agent:
            device_info['os'] = 'iOS'
        else:
            device_info['os'] = 'Unknown'
        
        return device_info
    
    @staticmethod
    def check_concurrent_sessions(user):
        """
        检查并发会话数量
        如果超过限制，踢出最早的会话
        """
        max_sessions = getattr(settings, 'MAX_CONCURRENT_SESSIONS', 3)
        
        # 获取当前活跃会话
        active_sessions = UserSession.objects.filter(
            user=user,
            is_active=True,
            expires_at__gt=timezone.now()
        ).order_by('created_at')
        
        # 如果超过限制，踢出最早的会话
        if active_sessions.count() >= max_sessions:
            sessions_to_remove = active_sessions[:active_sessions.count() - max_sessions + 1]
            for session in sessions_to_remove:
                session.is_active = False
                session.save(update_fields=['is_active'])
    
    @staticmethod
    def invalidate_session(refresh_token):
        """使会话失效"""
        try:
            session = UserSession.objects.get(refresh_token=refresh_token)
            session.is_active = False
            session.save(update_fields=['is_active'])
            return True
        except UserSession.DoesNotExist:
            return False
    
    @staticmethod
    def invalidate_all_sessions(user):
        """使用户所有会话失效（强制下线）"""
        UserSession.objects.filter(
            user=user,
            is_active=True
        ).update(is_active=False)
```

### 4.6 限流类 (authentication/throttling.py)

```python
# authentication/throttling.py
"""
自定义限流类
"""

from rest_framework.throttling import SimpleRateThrottle
from django.core.cache import cache
from django.conf import settings


class LoginRateThrottle(SimpleRateThrottle):
    """
    登录限流
    同一 IP 每分钟最多 10 次
    """
    scope = 'login'
    rate = '10/min'
    
    def get_cache_key(self, request, view):
        # 使用 IP 作为限流标识
        ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


class VerificationCodeRateThrottle(SimpleRateThrottle):
    """
    验证码发送限流
    同一手机号/邮箱每分钟 1 次，每天 10 次
    """
    scope = 'verification_code'
    
    def get_cache_key(self, request, view):
        # 获取目标（手机号或邮箱）
        target = request.data.get('phone') or request.data.get('email') or request.data.get('target')
        if not target:
            return None
        
        # 每分钟限流
        return f'throttle_code_{target}'
    
    def allow_request(self, request, view):
        if self.rate is None:
            return True
        
        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True
        
        # 检查每分钟限制
        self.history = self.cache.get(self.key, [])
        self.now = self.timer()
        
        # 清理过期记录
        self.history = [t for t in self.history if t > self.now - 60]
        
        if len(self.history) >= 1:
            return False
        
        # 检查每日限制
        daily_key = f'{self.key}_daily'
        daily_count = cache.get(daily_key, 0)
        if daily_count >= 10:
            return False
        
        # 更新计数
        self.history.insert(0, self.now)
        self.cache.set(self.key, self.history, 60)
        cache.set(daily_key, daily_count + 1, 86400)  # 24小时
        
        return True


class FileUploadRateThrottle(SimpleRateThrottle):
    """
    文件上传限流
    同一用户每分钟最多 5 次
    """
    scope = 'file_upload'
    rate = '5/min'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


class FileDownloadRateThrottle(SimpleRateThrottle):
    """
    文件下载限流
    同一用户每分钟最多 20 次
    """
    scope = 'file_download'
    rate = '20/min'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


class APIRateThrottle(SimpleRateThrottle):
    """
    API 通用限流
    同一用户每分钟最多 100 次
    """
    scope = 'api'
    rate = '100/min'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
```

### 4.7 登录日志中间件 (authentication/middleware.py)

```python
# authentication/middleware.py
"""
认证相关中间件
"""

from django.utils import timezone
from users.models import LoginLog
from authentication.jwt import SessionManager


class LoginLogMiddleware:
    """
    登录日志中间件
    记录用户登录/登出行为
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # 处理请求前的逻辑
        
        response = self.get_response(request)
        
        # 处理响应后的逻辑
        # 这里可以添加额外的日志记录逻辑
        
        return response
    
    @staticmethod
    def log_login(user, request, action='LOGIN', result='SUCCESS', failure_reason=''):
        """
        记录登录日志
        
        Args:
            user: 用户对象
            request: 请求对象
            action: 操作类型
            result: 结果
            failure_reason: 失败原因
        """
        ip_address = SessionManager.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        device_info = SessionManager.parse_user_agent(user_agent)
        
        LoginLog.objects.create(
            user=user,
            action=action,
            ip_address=ip_address,
            user_agent=user_agent,
            device_info=device_info,
            result=result,
            failure_reason=failure_reason
        )
```

---

## 5. API接口实现

### 5.1 用户序列化器 (users/serializers.py)

```python
# users/serializers.py
"""
用户相关序列化器
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

from users.models import VerificationCode, UserSession
from common.constants import UserRole, UserStatus, Gender
from utils.validators import validate_phone, validate_email

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    用户信息序列化器
    """
    department_name = serializers.CharField(source='department.name', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'employee_id', 'login_account', 'username', 'phone', 'email',
            'avatar', 'gender', 'gender_display', 'role', 'role_display',
            'department', 'department_name', 'position', 'status', 'status_display',
            'join_date', 'last_login_time', 'last_login_ip', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'employee_id', 'login_account', 'role', 'status',
            'last_login_time', 'last_login_ip', 'created_at', 'updated_at'
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    """
    用户创建序列化器
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = [
            'login_account', 'username', 'password', 'password_confirm',
            'phone', 'email', 'gender', 'role', 'department', 'position',
            'join_date', 'remark'
        ]
    
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({'password_confirm': '两次密码输入不一致'})
        return attrs
    
    def validate_phone(self, value):
        if value:
            validate_phone(value)
            if User.objects.filter(phone=value).exists():
                raise serializers.ValidationError('该手机号已被注册')
        return value
    
    def validate_email(self, value):
        if value:
            validate_email(value)
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError('该邮箱已被注册')
        return value
    
    def validate_login_account(self, value):
        if User.objects.filter(login_account=value).exists():
            raise serializers.ValidationError('该账号已存在')
        return value
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data, password=password)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    用户更新序列化器
    """
    class Meta:
        model = User
        fields = [
            'username', 'phone', 'email', 'avatar', 'gender',
            'position', 'remark'
        ]
    
    def validate_phone(self, value):
        if value:
            validate_phone(value)
            instance = self.instance
            if instance and User.objects.filter(phone=value).exclude(id=instance.id).exists():
                raise serializers.ValidationError('该手机号已被其他用户使用')
        return value
    
    def validate_email(self, value):
        if value:
            validate_email(value)
            instance = self.instance
            if instance and User.objects.filter(email=value).exclude(id=instance.id).exists():
                raise serializers.ValidationError('该邮箱已被其他用户使用')
        return value


class PasswordChangeSerializer(serializers.Serializer):
    """
    修改密码序列化器
    """
    old_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('原密码错误')
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({'new_password_confirm': '两次密码输入不一致'})
        
        # 检查新密码是否与旧密码相同
        user = self.context['request'].user
        if user.check_password(attrs['new_password']):
            raise serializers.ValidationError({'new_password': '新密码不能与原密码相同'})
        
        # 检查是否与历史密码重复
        for old_hash in user.password_history:
            from django.contrib.auth.hashers import check_password
            if check_password(attrs['new_password'], old_hash):
                raise serializers.ValidationError({'new_password': '新密码不能与最近3次密码相同'})
        
        return attrs
    
    def save(self):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        
        # 保存旧密码到历史
        user.add_password_to_history(user.password)
        
        # 设置新密码
        user.set_password(new_password)
        user.save()
        
        return user


class PasswordResetSerializer(serializers.Serializer):
    """
    重置密码序列化器
    """
    target = serializers.CharField(required=True)  # 手机号或邮箱
    code = serializers.CharField(required=True, min_length=6, max_length=6)
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    def validate_target(self, value):
        # 验证目标是否存在
        if '@' in value:
            if not User.objects.filter(email=value).exists():
                raise serializers.ValidationError('该邮箱未注册')
        else:
            if not User.objects.filter(phone=value).exists():
                raise serializers.ValidationError('该手机号未注册')
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({'new_password_confirm': '两次密码输入不一致'})
        
        # 验证验证码
        target = attrs['target']
        code = attrs['code']
        
        try:
            vc = VerificationCode.objects.get(
                target=target,
                code=code,
                purpose='RESET_PASSWORD',
                is_used=False
            )
            if vc.is_expired:
                raise serializers.ValidationError({'code': '验证码已过期'})
        except VerificationCode.DoesNotExist:
            raise serializers.ValidationError({'code': '验证码错误'})
        
        attrs['verification_code'] = vc
        return attrs
    
    def save(self):
        target = self.validated_data['target']
        new_password = self.validated_data['new_password']
        vc = self.validated_data['verification_code']
        
        # 获取用户
        if '@' in target:
            user = User.objects.get(email=target)
        else:
            user = User.objects.get(phone=target)
        
        # 保存旧密码到历史
        user.add_password_to_history(user.password)
        
        # 设置新密码
        user.set_password(new_password)
        user.save()
        
        # 标记验证码已使用
        vc.mark_as_used()
        
        return user


class VerificationCodeSerializer(serializers.Serializer):
    """
    发送验证码序列化器
    """
    CODE_TYPE_CHOICES = [('PHONE', '手机'), ('EMAIL', '邮箱')]
    PURPOSE_CHOICES = [
        ('REGISTER', '注册'),
        ('LOGIN', '登录'),
        ('RESET_PASSWORD', '重置密码'),
        ('BIND_PHONE', '绑定手机'),
        ('BIND_EMAIL', '绑定邮箱'),
    ]
    
    code_type = serializers.ChoiceField(choices=CODE_TYPE_CHOICES, required=True)
    purpose = serializers.ChoiceField(choices=PURPOSE_CHOICES, required=True)
    target = serializers.CharField(required=True)
    captcha_key = serializers.CharField(required=False)  # 图形验证码key
    captcha_code = serializers.CharField(required=False)  # 图形验证码
    
    def validate_target(self, value):
        code_type = self.initial_data.get('code_type')
        purpose = self.initial_data.get('purpose')
        
        if code_type == 'PHONE':
            validate_phone(value)
            # 注册时检查手机号是否已存在
            if purpose == 'REGISTER' and User.objects.filter(phone=value).exists():
                raise serializers.ValidationError('该手机号已被注册')
            # 绑定时检查是否已被其他用户绑定
            if purpose == 'BIND_PHONE':
                request = self.context.get('request')
                if request and request.user.is_authenticated:
                    if User.objects.filter(phone=value).exclude(id=request.user.id).exists():
                        raise serializers.ValidationError('该手机号已被其他用户绑定')
        else:
            validate_email(value)
            if purpose == 'REGISTER' and User.objects.filter(email=value).exists():
                raise serializers.ValidationError('该邮箱已被注册')
            if purpose == 'BIND_EMAIL':
                request = self.context.get('request')
                if request and request.user.is_authenticated:
                    if User.objects.filter(email=value).exclude(id=request.user.id).exists():
                        raise serializers.ValidationError('该邮箱已被其他用户绑定')
        
        return value
```

### 5.2 认证序列化器 (authentication/serializers.py)

```python
# authentication/serializers.py
"""
认证相关序列化器
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from datetime import timedelta

from users.models import VerificationCode
from common.constants import UserStatus
from utils.exceptions import AccountLockedException, AuthenticationFailedException

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    """
    登录序列化器
    支持账号/手机号/邮箱 + 密码登录
    """
    login_account = serializers.CharField(required=True)  # 可以是账号、手机号或邮箱
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        write_only=True
    )
    
    def validate(self, attrs):
        login_account = attrs.get('login_account')
        password = attrs.get('password')
        
        # 尝试查找用户
        user = None
        if '@' in login_account:
            # 邮箱登录
            try:
                user = User.objects.get(email=login_account)
            except User.DoesNotExist:
                pass
        elif login_account.isdigit() and len(login_account) == 11:
            # 手机号登录
            try:
                user = User.objects.get(phone=login_account)
            except User.DoesNotExist:
                pass
        else:
            # 账号登录
            try:
                user = User.objects.get(login_account=login_account)
            except User.DoesNotExist:
                pass
        
        if user is None:
            raise AuthenticationFailedException('用户不存在')
        
        # 检查账户状态
        if user.is_locked:
            raise AccountLockedException(
                f'账户已被锁定，请 {user.locked_until.strftime("%Y-%m-%d %H:%M")} 后再试'
            )
        
        if user.status == UserStatus.DISABLED.value:
            raise AuthenticationFailedException('账户已被停用')
        
        if user.status == UserStatus.RESIGNED.value:
            raise AuthenticationFailedException('该账户已离职')
        
        if not user.is_active:
            raise AuthenticationFailedException('账户未激活')
        
        # 验证密码
        if not user.check_password(password):
            # 增加失败次数
            user.increment_login_failed()
            raise AuthenticationFailedException('密码错误')
        
        # 检查密码是否过期
        if user.is_password_expired:
            raise AuthenticationFailedException(
                '密码已过期，请通过找回密码功能重置密码',
                code='password_expired'
            )
        
        attrs['user'] = user
        return attrs


class LoginResponseSerializer(serializers.Serializer):
    """
    登录响应序列化器
    """
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    expires_in = serializers.IntegerField()
    user = serializers.DictField()


class RegisterSerializer(serializers.Serializer):
    """
    注册序列化器
    """
    REGISTER_TYPE_CHOICES = [
        ('PHONE', '手机号注册'),
        ('EMAIL', '邮箱注册'),
        ('ACCOUNT', '账号注册'),
    ]
    
    register_type = serializers.ChoiceField(choices=REGISTER_TYPE_CHOICES, required=True)
    login_account = serializers.CharField(required=False)  # 账号注册时必填
    phone = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        write_only=True
    )
    password_confirm = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        write_only=True
    )
    username = serializers.CharField(required=True, max_length=50)
    code = serializers.CharField(required=True, min_length=6, max_length=6)
    
    def validate(self, attrs):
        register_type = attrs.get('register_type')
        
        # 根据注册类型验证必填字段
        if register_type == 'PHONE':
            if not attrs.get('phone'):
                raise serializers.ValidationError({'phone': '手机号不能为空'})
            target = attrs['phone']
        elif register_type == 'EMAIL':
            if not attrs.get('email'):
                raise serializers.ValidationError({'email': '邮箱不能为空'})
            target = attrs['email']
        else:  # ACCOUNT
            if not attrs.get('login_account'):
                raise serializers.ValidationError({'login_account': '账号不能为空'})
            if not attrs.get('phone'):
                raise serializers.ValidationError({'phone': '手机号不能为空'})
            target = attrs['phone']
            
            # 检查账号是否已存在
            if User.objects.filter(login_account=attrs['login_account']).exists():
                raise serializers.ValidationError({'login_account': '该账号已存在'})
        
        # 验证密码
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': '两次密码输入不一致'})
        
        # 验证验证码
        code = attrs['code']
        try:
            vc = VerificationCode.objects.get(
                target=target,
                code=code,
                purpose='REGISTER',
                is_used=False
            )
            if vc.is_expired:
                raise serializers.ValidationError({'code': '验证码已过期'})
        except VerificationCode.DoesNotExist:
            raise serializers.ValidationError({'code': '验证码错误'})
        
        attrs['verification_code'] = vc
        attrs['target'] = target
        return attrs
    
    def create(self, validated_data):
        register_type = validated_data['register_type']
        vc = validated_data['verification_code']
        
        # 创建用户
        user_data = {
            'username': validated_data['username'],
            'password': validated_data['password'],
        }
        
        if register_type == 'PHONE':
            user_data['phone'] = validated_data['phone']
            user_data['login_account'] = validated_data['phone']  # 使用手机号作为登录账号
        elif register_type == 'EMAIL':
            user_data['email'] = validated_data['email']
            user_data['login_account'] = validated_data['email'].split('@')[0]  # 使用邮箱前缀作为登录账号
        else:  # ACCOUNT
            user_data['login_account'] = validated_data['login_account']
            user_data['phone'] = validated_data['phone']
        
        user = User.objects.create_user(**user_data)
        
        # 标记验证码已使用
        vc.mark_as_used()
        
        return user


class TokenRefreshSerializer(serializers.Serializer):
    """
    Token 刷新序列化器
    """
    refresh = serializers.CharField(required=True)
    
    def validate_refresh(self, value):
        from authentication.jwt import JWTUtils
        
        result = JWTUtils.refresh_access_token(value)
        if result is None:
            raise serializers.ValidationError('无效的刷新令牌')
        
        self.new_access_token = result
        return value


class LogoutSerializer(serializers.Serializer):
    """
    登出序列化器
    """
    refresh = serializers.CharField(required=True)
    
    def validate_refresh(self, value):
        from authentication.jwt import JWTUtils, SessionManager
        
        # 将 Token 加入黑名单
        JWTUtils.blacklist_token(value)
        # 使会话失效
        SessionManager.invalidate_session(value)
        
        return value
```

### 5.3 认证视图 (authentication/views.py)

```python
# authentication/views.py
"""
认证相关视图
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.conf import settings
import random
import string

from authentication.serializers import (
    LoginSerializer, LoginResponseSerializer, RegisterSerializer,
    TokenRefreshSerializer, LogoutSerializer
)
from authentication.jwt import JWTUtils, SessionManager
from authentication.throttling import LoginRateThrottle, VerificationCodeRateThrottle
from authentication.middleware import LoginLogMiddleware
from users.serializers import (
    UserSerializer, VerificationCodeSerializer,
    PasswordChangeSerializer, PasswordResetSerializer
)
from users.models import VerificationCode
from common.responses import success_response, error_response
from utils.exceptions import BusinessException


class LoginView(APIView):
    """
    用户登录视图
    """
    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]
    
    @extend_schema(
        request=LoginSerializer,
        responses={
            200: LoginResponseSerializer,
            400: OpenApiResponse(description='请求参数错误'),
            401: OpenApiResponse(description='认证失败'),
            403: OpenApiResponse(description='账户被锁定'),
        },
        description='用户登录，支持账号/手机号/邮箱 + 密码登录'
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # 生成 Token
        tokens = JWTUtils.generate_tokens(user)
        
        # 创建会话
        SessionManager.create_session(user, tokens['refresh_token'], request)
        
        # 更新登录信息
        ip_address = SessionManager.get_client_ip(request)
        user.update_login_info(ip_address)
        
        # 记录登录日志
        LoginLogMiddleware.log_login(user, request, action='LOGIN', result='SUCCESS')
        
        # 构建响应数据
        user_data = UserSerializer(user).data
        response_data = {
            'access_token': tokens['access_token'],
            'refresh_token': tokens['refresh_token'],
            'expires_in': tokens['expires_in'],
            'user': user_data
        }
        
        return success_response(response_data, message='登录成功')


class LogoutView(APIView):
    """
    用户登出视图
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        request=LogoutSerializer,
        responses={
            200: OpenApiResponse(description='登出成功'),
        },
        description='用户登出，使 Token 失效'
    )
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 记录登出日志
        LoginLogMiddleware.log_login(request.user, request, action='LOGOUT', result='SUCCESS')
        
        return success_response(message='登出成功')


class RegisterView(APIView):
    """
    用户注册视图
    """
    permission_classes = [AllowAny]
    throttle_classes = [VerificationCodeRateThrottle]
    
    @extend_schema(
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(description='注册成功'),
            400: OpenApiResponse(description='请求参数错误'),
        },
        description='用户注册，支持手机号/邮箱/账号三种注册方式'
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        
        return success_response(
            {'user_id': str(user.id), 'employee_id': user.employee_id},
            message='注册成功'
        )


class TokenRefreshView(APIView):
    """
    Token 刷新视图
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=TokenRefreshSerializer,
        responses={
            200: OpenApiResponse(description='刷新成功'),
            400: OpenApiResponse(description='无效的刷新令牌'),
        },
        description='使用 refresh_token 刷新 access_token'
    )
    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return success_response(
            serializer.new_access_token,
            message='Token 刷新成功'
        )


class SendVerificationCodeView(APIView):
    """
    发送验证码视图
    """
    permission_classes = [AllowAny]
    throttle_classes = [VerificationCodeRateThrottle]
    
    @extend_schema(
        request=VerificationCodeSerializer,
        responses={
            200: OpenApiResponse(description='发送成功'),
            400: OpenApiResponse(description='请求参数错误'),
            429: OpenApiResponse(description='请求过于频繁'),
        },
        description='发送验证码（手机短信/邮箱）'
    )
    def post(self, request):
        serializer = VerificationCodeSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        code_type = serializer.validated_data['code_type']
        purpose = serializer.validated_data['purpose']
        target = serializer.validated_data['target']
        
        # 生成验证码
        code = ''.join(random.choices(string.digits, k=6))
        
        # 设置过期时间
        if code_type == 'PHONE':
            expires_minutes = 5
        else:
            expires_minutes = 10
        
        # 保存验证码
        vc = VerificationCode.objects.create(
            code_type=code_type,
            purpose=purpose,
            target=target,
            code=code,
            expires_at=timezone.now() + timedelta(minutes=expires_minutes)
        )
        
        # 发送验证码（实际项目中需要对接短信/邮件服务）
        if code_type == 'PHONE':
            # TODO: 调用短信服务发送验证码
            # send_sms(target, code)
            pass
        else:
            # TODO: 调用邮件服务发送验证码
            # send_email(target, code)
            pass
        
        # 开发环境返回验证码（生产环境需要删除）
        if settings.DEBUG:
            return success_response({'code': code}, message='验证码发送成功')
        
        return success_response(message='验证码发送成功')


class PasswordChangeView(APIView):
    """
    修改密码视图
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        request=PasswordChangeSerializer,
        responses={
            200: OpenApiResponse(description='修改成功'),
            400: OpenApiResponse(description='请求参数错误'),
        },
        description='修改密码，需要验证原密码'
    )
    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message='密码修改成功，请重新登录')


class PasswordResetView(APIView):
    """
    重置密码视图
    """
    permission_classes = [AllowAny]
    throttle_classes = [VerificationCodeRateThrottle]
    
    @extend_schema(
        request=PasswordResetSerializer,
        responses={
            200: OpenApiResponse(description='重置成功'),
            400: OpenApiResponse(description='请求参数错误'),
        },
        description='通过验证码重置密码'
    )
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message='密码重置成功')


class CurrentUserView(APIView):
    """
    获取当前用户信息视图
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        responses={
            200: UserSerializer,
        },
        description='获取当前登录用户的详细信息'
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return success_response(serializer.data)
    
    @extend_schema(
        request=UserSerializer,
        responses={
            200: UserSerializer,
        },
        description='更新当前用户信息'
    )
    def put(self, request):
        from users.serializers import UserUpdateSerializer
        serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(serializer.data, message='信息更新成功')
```

### 5.4 路由配置

#### 5.4.1 认证路由 (authentication/urls.py)

```python
# authentication/urls.py
"""
认证相关路由
"""

from django.urls import path
from authentication.views import (
    LoginView, LogoutView, RegisterView, TokenRefreshView,
    SendVerificationCodeView, PasswordChangeView, PasswordResetView,
    CurrentUserView
)

app_name = 'authentication'

urlpatterns = [
    # 登录登出
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # 注册
    path('register/', RegisterView.as_view(), name='register'),
    
    # Token 管理
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 验证码
    path('send-code/', SendVerificationCodeView.as_view(), name='send_code'),
    
    # 密码管理
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    
    # 当前用户
    path('me/', CurrentUserView.as_view(), name='current_user'),
]
```

#### 5.4.2 主路由配置 (config/urls.py)

```python
# config/urls.py
"""
主路由配置
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # API v1
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/departments/', include('departments.urls')),
    
    # API 文档
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # 验证码
    path('captcha/', include('captcha.urls')),
]

# 开发环境静态文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

---

## 6. 安全策略实现

### 6.1 用户权限类 (users/permissions.py)

```python
# users/permissions.py
"""
自定义权限类
"""

from rest_framework import permissions
from common.constants import UserRole


class IsSuperAdmin(permissions.BasePermission):
    """
    超级管理员权限
    """
    message = '需要超级管理员权限'
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == UserRole.SUPER_ADMIN.value
        )


class IsSeniorAdmin(permissions.BasePermission):
    """
    高级管理员权限（包括超级管理员）
    """
    message = '需要高级管理员权限'
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in [
            UserRole.SUPER_ADMIN.value,
            UserRole.SENIOR_ADMIN.value
        ]


class IsAdmin(permissions.BasePermission):
    """
    管理员权限（包括超级管理员、高级管理员、普通管理员）
    """
    message = '需要管理员权限'
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in [
            UserRole.SUPER_ADMIN.value,
            UserRole.SENIOR_ADMIN.value,
            UserRole.ADMIN.value
        ]


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    资源所有者或管理员权限
    """
    message = '只能操作自己的数据或需要管理员权限'
    
    def has_object_permission(self, request, view, obj):
        # 管理员可以操作所有对象
        if request.user.role in [
            UserRole.SUPER_ADMIN.value,
            UserRole.SENIOR_ADMIN.value,
            UserRole.ADMIN.value
        ]:
            return True
        
        # 检查是否是对象的所有者
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        
        return obj == request.user


class IsDepartmentMember(permissions.BasePermission):
    """
    部门成员权限
    普通管理员只能操作本部门数据
    """
    message = '只能操作本部门数据'
    
    def has_object_permission(self, request, view, obj):
        # 高级管理员及以上可以操作所有对象
        if request.user.role in [
            UserRole.SUPER_ADMIN.value,
            UserRole.SENIOR_ADMIN.value
        ]:
            return True
        
        # 检查部门
        if hasattr(obj, 'department'):
            return obj.department == request.user.department
        if hasattr(obj, 'user'):
            return obj.user.department == request.user.department
        
        return False


class IsActiveUser(permissions.BasePermission):
    """
    活跃用户权限
    检查用户状态是否正常
    """
    message = '账户状态异常'
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        from common.constants import UserStatus
        return request.user.status == UserStatus.ACTIVE.value


class CanManageUser(permissions.BasePermission):
    """
    用户管理权限
    根据角色判断是否有权限管理目标用户
    """
    message = '无权管理该用户'
    
    def has_object_permission(self, request, view, obj):
        # obj 是被操作的用户对象
        target_user = obj
        current_user = request.user
        
        # 超级管理员可以管理所有用户（除了其他超级管理员）
        if current_user.role == UserRole.SUPER_ADMIN.value:
            return True
        
        # 高级管理员可以管理普通管理员和普通员工
        if current_user.role == UserRole.SENIOR_ADMIN.value:
            return target_user.role in [
                UserRole.ADMIN.value,
                UserRole.EMPLOYEE.value
            ]
        
        # 普通管理员只能管理本部门的普通员工
        if current_user.role == UserRole.ADMIN.value:
            return (
                target_user.role == UserRole.EMPLOYEE.value and
                target_user.department == current_user.department
            )
        
        return False
```

### 6.2 Admin 配置 (users/admin.py)

```python
# users/admin.py
"""
用户管理 Admin 配置
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from users.models import User, UserSession, VerificationCode, LoginLog
from common.constants import UserRole, UserStatus


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    用户 Admin 配置
    """
    list_display = [
        'employee_id', 'username', 'login_account', 'phone', 'email',
        'role', 'status', 'department', 'last_login_time', 'is_active'
    ]
    list_filter = ['role', 'status', 'gender', 'department', 'is_active']
    search_fields = ['employee_id', 'username', 'login_account', 'phone', 'email']
    readonly_fields = ['employee_id', 'last_login_time', 'last_login_ip', 'created_at', 'updated_at']
    
    fieldsets = (
        (None, {'fields': ('employee_id', 'login_account', 'password')}),
        (_('个人信息'), {
            'fields': ('username', 'phone', 'email', 'avatar', 'gender', 'position')
        }),
        (_('权限信息'), {
            'fields': ('role', 'department', 'status', 'is_active', 'is_staff', 'is_superuser')
        }),
        (_('登录信息'), {
            'fields': ('last_login_time', 'last_login_ip', 'login_failed_count', 'locked_until')
        }),
        (_('时间信息'), {
            'fields': ('join_date', 'leave_date', 'password_changed_at', 'created_at', 'updated_at')
        }),
        (_('其他信息'), {
            'fields': ('remark', 'groups', 'user_permissions')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'login_account', 'username', 'password1', 'password2',
                'phone', 'email', 'role', 'department', 'status'
            ),
        }),
    )
    
    ordering = ['-created_at']
    
    def save_model(self, request, obj, form, change):
        """保存时自动设置员工工号"""
        if not obj.employee_id:
            obj.employee_id = obj.generate_employee_id()
        super().save_model(request, obj, form, change)


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """
    用户会话 Admin 配置
    """
    list_display = ['user', 'ip_address', 'device_info', 'is_active', 'expires_at', 'created_at']
    list_filter = ['is_active']
    search_fields = ['user__username', 'ip_address']
    readonly_fields = ['user', 'session_key', 'refresh_token', 'ip_address', 'user_agent', 'device_info', 'expires_at', 'created_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    """
    验证码 Admin 配置
    """
    list_display = ['target', 'code_type', 'purpose', 'code', 'is_used', 'expires_at', 'created_at']
    list_filter = ['code_type', 'purpose', 'is_used']
    search_fields = ['target', 'code']
    readonly_fields = ['created_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    """
    登录日志 Admin 配置
    """
    list_display = ['user', 'action', 'ip_address', 'result', 'created_at']
    list_filter = ['action', 'result']
    search_fields = ['user__username', 'ip_address']
    readonly_fields = ['user', 'action', 'ip_address', 'user_agent', 'device_info', 'location', 'result', 'failure_reason', 'created_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
```

---

## 7. 测试与验证

### 7.1 创建测试脚本

创建 `scripts/test_api.py` 文件用于测试 API：

```python
# scripts/test_api.py
"""
API 测试脚本
"""

import requests
import json

BASE_URL = 'http://localhost:8000/api/v1'


def test_register():
    """测试注册"""
    print('\n=== 测试注册 ===')
    
    # 先发送验证码
    code_response = requests.post(f'{BASE_URL}/auth/send-code/', json={
        'code_type': 'PHONE',
        'purpose': 'REGISTER',
        'target': '13800138000'
    })
    print(f'发送验证码: {code_response.json()}')
    
    # 注册
    register_response = requests.post(f'{BASE_URL}/auth/register/', json={
        'register_type': 'PHONE',
        'phone': '13800138000',
        'password': 'Test@123456',
        'password_confirm': 'Test@123456',
        'username': '测试用户',
        'code': '123456'  # 开发环境可使用任意验证码
    })
    print(f'注册结果: {json.dumps(register_response.json(), indent=2, ensure_ascii=False)}')
    
    return register_response.json()


def test_login():
    """测试登录"""
    print('\n=== 测试登录 ===')
    
    response = requests.post(f'{BASE_URL}/auth/login/', json={
        'login_account': '13800138000',
        'password': 'Test@123456'
    })
    print(f'登录结果: {json.dumps(response.json(), indent=2, ensure_ascii=False)}')
    
    if response.status_code == 200:
        return response.json()['data']['access_token']
    return None


def test_get_current_user(token):
    """测试获取当前用户信息"""
    print('\n=== 测试获取当前用户信息 ===')
    
    response = requests.get(
        f'{BASE_URL}/auth/me/',
        headers={'Authorization': f'Bearer {token}'}
    )
    print(f'用户信息: {json.dumps(response.json(), indent=2, ensure_ascii=False)}')


def test_change_password(token):
    """测试修改密码"""
    print('\n=== 测试修改密码 ===')
    
    response = requests.post(
        f'{BASE_URL}/auth/password/change/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'old_password': 'Test@123456',
            'new_password': 'NewTest@123456',
            'new_password_confirm': 'NewTest@123456'
        }
    )
    print(f'修改密码结果: {json.dumps(response.json(), indent=2, ensure_ascii=False)}')


def test_logout(token, refresh_token):
    """测试登出"""
    print('\n=== 测试登出 ===')
    
    response = requests.post(
        f'{BASE_URL}/auth/logout/',
        headers={'Authorization': f'Bearer {token}'},
        json={'refresh': refresh_token}
    )
    print(f'登出结果: {json.dumps(response.json(), indent=2, ensure_ascii=False)}')


if __name__ == '__main__':
    # 运行测试
    # test_register()
    
    login_result = test_login()
    if login_result:
        token = login_result['data']['access_token']
        refresh_token = login_result['data']['refresh_token']
        
        test_get_current_user(token)
        # test_change_password(token)
        # test_logout(token, refresh_token)
```

### 7.2 运行项目

```bash
# 创建日志目录
mkdir -p logs

# 创建数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级管理员
python manage.py createsuperuser

# 收集静态文件
python manage.py collectstatic

# 启动开发服务器
python manage.py runserver 0.0.0.0:8000
```

### 7.3 访问 API 文档

启动服务器后，可以访问以下地址查看 API 文档：

- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
- OpenAPI Schema: http://localhost:8000/api/schema/

### 7.4 测试 API 接口

使用 curl 或 Postman 测试 API：

```bash
# 发送验证码
curl -X POST http://localhost:8000/api/v1/auth/send-code/ \
  -H "Content-Type: application/json" \
  -d '{"code_type": "PHONE", "purpose": "REGISTER", "target": "13800138000"}'

# 注册
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "register_type": "PHONE",
    "phone": "13800138000",
    "password": "Test@123456",
    "password_confirm": "Test@123456",
    "username": "测试用户",
    "code": "123456"
  }'

# 登录
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"login_account": "13800138000", "password": "Test@123456"}'

# 获取当前用户信息（需要替换 YOUR_TOKEN）
curl -X GET http://localhost:8000/api/v1/auth/me/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# 刷新 Token
curl -X POST http://localhost:8000/api/v1/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'

# 登出
curl -X POST http://localhost:8000/api/v1/auth/logout/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

---

## 附录

### A. 项目依赖清单

```
Django==5.0.4
djangorestframework==3.15.1
djangorestframework-simplejwt==5.3.1
psycopg2-binary==2.9.9
redis==5.0.4
django-redis==5.4.0
django-cors-headers==4.3.1
django-ratelimit==4.1.0
bcrypt==4.1.2
django-simple-captcha==0.6.0
drf-spectacular==0.27.2
python-dotenv==1.0.1
Pillow==10.3.0
celery==5.4.0
django-celery-beat==2.6.0
```

### B. 环境变量配置模板

```bash
# .env.example

# Django 配置
DJANGO_SECRET_KEY=your-secret-key-here-change-in-production
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# 数据库配置
DB_NAME=efms_db
DB_USER=efms_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# JWT 配置
JWT_ACCESS_TOKEN_LIFETIME=120
JWT_REFRESH_TOKEN_LIFETIME=10080

# 邮件配置
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@example.com
EMAIL_HOST_PASSWORD=your-email-password

# 文件存储配置
FILE_STORAGE_ROOT=~/root
MAX_FILE_SIZE=5368709120
```

### C. Git 忽略配置

```gitignore
# .gitignore

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# Django
*.log
local_settings.py
db.sqlite3
media/
staticfiles/

# Environment
.env
.env.local
.env.*.local

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
htmlcov/
.pytest_cache/

# Celery
celerybeat-schedule
celerybeat.pid
```

### D. 常见问题解决

**Q1: 数据库连接失败**

```bash
# 检查 PostgreSQL 服务状态
sudo systemctl status postgresql

# 创建数据库和用户
sudo -u postgres psql
CREATE DATABASE efms_db;
CREATE USER efms_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE efms_db TO efms_user;
```

**Q2: Redis 连接失败**

```bash
# 检查 redis 服务状态
sudo systemctl status redis

# 启动 redis
sudo systemctl start redis
```

**Q3: 迁移失败**

```bash
# 删除迁移文件重新迁移
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
```

---

## 总结

本文档详细介绍了企业文件管理系统（EFMS）第一阶段基础框架搭建的完整步骤，包括：

1. **环境准备与项目初始化**：创建项目目录、安装依赖、初始化 Django 项目
2. **项目配置**：分环境配置、数据库配置、Redis 配置、JWT 配置等
3. **数据库模型设计**：用户模型、部门模型、会话模型、验证码模型等
4. **用户认证系统实现**：JWT 认证、登录注册、密码管理、会话管理
5. **API 接口实现**：RESTful API 设计、序列化器、视图、路由
6. **安全策略实现**：权限控制、限流、密码验证、账户锁定

