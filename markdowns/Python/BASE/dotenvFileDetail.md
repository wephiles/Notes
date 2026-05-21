# 本文件主要说明 `.env` 文件中各字段的作用

# 1、智谱清言关于 `.env` 文件的说明

```.env
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

# Redis 配置 
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

# 短信配置
SMS_ACCESS_KEY=
SMS_SECRET_KEY=
SMS_SIGN_NAME=

# 文件存储配置
FILE_STORAGE_ROOT=E:\\Documents\\EFMS_ROOT
MAX_FILE_SIZE=5368709120
```

## 一、`Django` 核心配置



| 字段                   | 说明                                                         |
| ---------------------- | ------------------------------------------------------------ |
| `DJANGO_SECRET_KEY`    | Django 的"万能钥匙"，用于签名 Cookie、Session、CSRF Token、密码重置邮件中的 token 等。一旦泄露，攻击者可伪造任何签名。 |
| `DJANGO_DEBUG`         | 开发利器：`True` 时页面报错会显示完整堆栈信息；生产环境必须为 `False`，否则敏感信息全部暴露。 |
| `DJANGO_ALLOWED_HOSTS` | Django 的 HTTP Host 白名单。浏览器发来的请求头 `Host` 必须在此列表中，否则 Django 返回 400 Bad Request，防止 **HTTP Host 头注入攻击**。 |

### 在代码中如何使用（`settings.py`）

```
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')

# 典型场景：生产环境判断
if not DEBUG:
    # 生产环境的安全配置
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
```

> **安全提醒：** `SECRET_KEY` 绝对不能提交到 Git！应在 `.gitignore` 中排除 `.env`，生产环境通过服务器环境变量或密钥管理服务注入。

## 二、数据库配置（`PostgreSQL`）



| 字段          | 说明                                                         |
| ------------- | ------------------------------------------------------------ |
| `DB_NAME`     | 数据库名称。Django 启动时会连接到此数据库，并在此库中创建/迁移所有表。 |
| `DB_USER`     | 数据库登录用户。建议每个项目使用独立用户，而非 `postgres` 超级用户，遵循**最小权限原则**。 |
| `DB_PASSWORD` | 对应用户的密码。同样严禁泄露，严禁提交到版本控制。           |
| `DB_HOST`     | 数据库服务器地址。`localhost` 意味着数据库和 Django 在同一台机器；生产环境常改为内网 IP 或域名。 |
| `DB_PORT`     | PostgreSQL 默认端口 `5432`。如果改过端口需要同步修改。       |

### 在代码中如何使用

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

### 典型流程

```
python manage.py makemigrations   # 生成迁移文件
python manage.py migrate          # 在 efms_db 中建表/修改表结构
```

> **提示：** 数据库需要提前创建：`CREATE DATABASE efms_db;` 并授权给 `efms_user`。

## 三、`Redis` 配置



| 字段             | 说明                                                         |
| ---------------- | ------------------------------------------------------------ |
| `REDIS_HOST`     | Redis 服务地址。与数据库类似，本地开发用 `localhost`，生产用内网地址。 |
| `REDIS_PORT`     | Redis 默认端口 `6379`。                                      |
| `REDIS_PASSWORD` | Redis 的认证密码。生产环境**必须设置**，否则裸露的 Redis 可被任意访问。为空表示无密码（仅开发用）。 |

### 在 `Django` 项目中的典型用途

`Redis` 在 `Django` 项目中通常用于：

```
# 1. 缓存后端
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/1",
    }
}

# 2. Django Channels 的消息代理
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(os.getenv('REDIS_HOST'), int(os.getenv('REDIS_PORT')))],
        },
    },
}

# 3. Django REST Framework 的 Token 限流
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    }
}

# 4. 你的 EFMS 项目中：文件操作队列、在线用户数统计、文件预览临时缓存等
```

> **为什么要用 Redis？** 比如你的文件管理系统需要记录"某文件正被某用户编辑"以实现**锁定机制**，Redis 的 `SET` + 自动过期非常适合这种场景。

## 四、`JWT` 配置



| 字段                         | 说明                                                         |
| ---------------------------- | ------------------------------------------------------------ |
| `JWT_ACCESS_TOKEN_LIFETIME`  | **访问令牌**有效期。`120` 分钟 = 2 小时。用户每次请求 `API` 都需要携带此 token，过期后请求会被拒绝。 |
| `JWT_REFRESH_TOKEN_LIFETIME` | **刷新令牌**有效期。`10080` 分钟 = 7 天。在 7 天内，前端可以用 refresh token 换取新的 access token，**用户无感知**。超过 7 天则必须重新登录。 |

### 为什么要设计双 Token？

```
┌─────────────┐     ┌──────────────────────┐     ┌──────────────────┐
│   用户登录    │ ──→ │ 返回 Access Token    │ ──→ │ 携带 Token 请求  │
│             │     │ + Refresh Token      │     │ 后端 API        │
└─────────────┘     └──────────────────────┘     └──────────────────┘
                                                    │
                                              Access Token 过期？
                                                   │
                                    ┌──────────────┤
                                    ▼              ▼
                                    是              否
                                    │              │
                           用 Refresh Token       正常响应
                           换取新 Access Token
```

### 在代码中如何使用（配合 `djangorestframework-simplejwt`）

```
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.getenv('JWT_ACCESS_TOKEN_LIFETIME', '120'))),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=int(os.getenv('JWT_REFRESH_TOKEN_LIFETIME', '10080'))),
    'ROTATE_REFRESH_TOKENS': True,   # 每次刷新时也轮换 refresh token，更安全
    'BLACKLIST_AFTER_ROTATION': True, # 旧的 refresh token 加入黑名单
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
```

> **EFMS 场景：** 用户上传大文件时可能耗时很长，2 小时的 access token 通常足够；若文件操作特别久，前端可在请求返回 401 时自动调用刷新接口。

## 五、邮件配置（SMTP）



| 字段                  | 说明                                                         |
| --------------------- | ------------------------------------------------------------ |
| `EMAIL_HOST`          | SMTP 服务器地址。QQ 邮箱为 `smtp.qq.com`，163 为 `smtp.163.com`，Gmail 为 `smtp.gmail.com`。 |
| `EMAIL_PORT`          | 端口。`587` = STARTTLS（先明文再加密），`465` = SSL（直接加密），`25` = 纯明文（不推荐）。 |
| `EMAIL_USE_TLS`       | 是否启用 TLS 加密传输，`True` 表示使用 `STARTTLS`。          |
| `EMAIL_HOST_USER`     | 发件邮箱地址。比如系统通知、密码重置邮件都从这个邮箱发出。   |
| `EMAIL_HOST_PASSWORD` | 邮箱**授权码**（不是登录密码！）。QQ/163 邮箱需要在设置中单独生成授权码。 |

### 在代码中如何使用

```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'False') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # 默认发件人
```

### 在 EFMS 中的实际应用场景

```
from django.core.mail import send_mail
from django.template.loader import render_to_string

# 场景1：密码重置
send_mail(
    subject='EFMS 文件管理系统 - 密码重置',
    message='点击以下链接重置密码...',
    from_email=settings.DEFAULT_FROM_EMAIL,
    recipient_list=[user.email],
    fail_silently=False,
)

# 场景2：文件分享通知
# "用户A与你分享了3个文件，请登录查看"

# 场景3：系统异常告警（给管理员发邮件）
```

## 六、短信配置



| 字段             | 说明                                                         |
| ---------------- | ------------------------------------------------------------ |
| `SMS_ACCESS_KEY` | 短信服务商的 API 访问密钥（如阿里云 SMS 的 AccessKey ID）。  |
| `SMS_SECRET_KEY` | 对应的密钥，与 AccessKey 配对使用。                          |
| `SMS_SIGN_NAME`  | 短信签名，如 `【XX公司文件系统】`，需要在短信平台审核通过才能使用。 |

### 在代码中如何使用（以阿里云 SMS 为例）

```
from alibabacloud_dysmsapi20170525.client import Client
from alibabacloud_tea_openapi.models import Config

config = Config(
    access_key_id=os.getenv('SMS_ACCESS_KEY'),
    access_key_secret=os.getenv('SMS_SECRET_KEY'),
    endpoint='dysmsapi.aliyuncs.com',
)
sms_client = Client(config)

def send_verification_code(phone: str, code: str):
    """发送短信验证码"""
    sms_client.send_sms(
        phone_numbers=phone,
        sign_name=os.getenv('SMS_SIGN_NAME'),
        template_code='SMS_123456789',  # 模板编号
        template_param=json.dumps({'code': code}),
    )
```

### 在 EFMS 中的应用场景

```
用户注册  →  发送短信验证码验证手机号
用户登录  →  手机号 + 验证码登录（双因素认证）
文件分享  →  短信通知接收者"有人给你分享了文件"
重要操作  →  删除大量文件时的二次验证
```

## 七、文件存储配置



| 字段                | 说明                                                         |
| ------------------- | ------------------------------------------------------------ |
| `FILE_STORAGE_ROOT` | 文件在磁盘上的存储根目录。所有用户上传的文件都存在这个目录下（通常按用户/日期分子目录）。 |
| `MAX_FILE_SIZE`     | 单个文件最大允许体积。`5368709120` 字节 = **5 GB**。上传超过此大小的文件时应在后端拒绝。 |

### 在代码中如何使用

```
from django.conf import settings
import os

# settings.py 中
MEDIA_ROOT = os.getenv('FILE_STORAGE_ROOT', os.path.join(BASE_DIR, 'uploads'))
MEDIA_URL = '/media/'  # URL 访问前缀

# 自定义文件存储路径（按用户分目录）
def user_directory_path(instance, filename):
    """文件上传路径：uploads/user_{id}/2024/01/filename.pdf"""
    from django.utils import timezone
    date_path = timezone.now().strftime('%Y/%m')
    return f'user_{instance.uploaded_by.id}/{date_path}/{filename}'

# models.py
class Document(models.Model):
    file = models.FileField(upload_to=user_directory_path)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

# 视图中进行文件大小校验
def validate_file_size(file):
    max_size = int(os.getenv('MAX_FILE_SIZE', 5368709120))
    if file.size > max_size:
        raise ValidationError(f'文件大小不能超过 {max_size // 1024 // 1024} MB')
```

### 目录结构示例

```
E:\Documents\EFMS_ROOT\
├── user_1\
│   ├── 2024\
│   │   ├── 01\
│   │   │   ├── 项目报告.pdf          (3.2 MB)
│   │   │   └── 设计稿.psd           (45 MB)
│   │   └── 02\
│   │       └── 季度总结.docx        (1.5 MB)
├── user_2\
│   └── ...
```

> **生产环境建议：** 大规模文件系统建议使用**云存储**（如阿里云 OSS、AWS S3），可通过 `django-storages` 库无缝切换，只需修改 Storage Backend 配置，代码逻辑不变。

## 整体架构关系图

```
┌───────────────────────────────────────────────────────────────┐
│                       .env 配置文件                            │
│  (所有敏感信息集中管理，不进入版本控制)                           │
└──────┬────────┬────────┬────────┬────────┬──────────┬─────────┘
       │        │        │        │        │          │
       ▼        ▼        ▼        ▼        ▼          ▼
   Django     DB      Redis     JWT      邮件SMTP    短信API
   Core      (PG)    (缓存/    (认证)   (通知/      (验证码/
   Config             队列)              密码重置)    分享通知)
       │        │        │                                    │
       ▼        ▼        ▼                                    ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                    settings.py                              │
  │           load_dotenv() → os.getenv('KEY')                  │
  │           将环境变量注入 Django 配置                          │
  └─────────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                  Django 应用程序                              │
  │  views.py │ models.py │ serializers.py │ urls.py │ ...       │
  └─────────────────────────────────────────────────────────────┘
```

## 关键安全清单 ✅



| 检查项                           | 说明                                     |
| -------------------------------- | ---------------------------------------- |
| ✅ `.env` 在 `.gitignore` 中      | 防止敏感信息提交到仓库                   |
| ✅ 生产环境 `DEBUG=False`         | 防止泄露源码和堆栈                       |
| ✅ `SECRET_KEY` 足够复杂          | 至少 50 位随机字符                       |
| ✅ `REDIS_PASSWORD` 已设置        | 生产环境 Redis 必须有密码                |
| ✅ `DB_PASSWORD` 强密码           | 数据库使用独立账号，最小权限             |
| ✅ `EMAIL_HOST_PASSWORD` 是授权码 | 不是邮箱登录密码                         |
| ✅ `SMS_*` Key 权限最小化         | 只授予发送短信的权限                     |
| ✅ 准备 `.env.example` 模板       | 提交到 Git，方便新同事配置（只含占位符） |

如果你对某个模块想深入了解（比如 JWT 双 Token 的完整实现流程、文件上传的安全防护等），随时可以继续问我！

# 2. IMPORTANT!!! **每个字段的详细补充**

## 2.1 `DJANGO_SECRET_KEY`

### 2.1.1 怎么生成

- `DJANGO_SECRET_KEY`: **不需要手动编写, 由 Django 自动生成**

- 当你第一次运行 `django-admin startproject myproject` 时，

  - `Django` 会自动调用内部的随机函数生成一个 50 个字符左右的字符串，写死在你的 `settings.py` 里，大概长这样：
  - `SECRET_KEY = 'django-insecure-^@1u8k=zj9%^*#lbf0+x@&p3!i8(q5hw2iy%7c0h*e(x$r58=8'`

- 但是, 使用 `.env` 管理配置的标准企业级开发模式下, 需要自己生成一个新的放到 .env 文件中

  1. 方式1: 使用 `django` 提供的生成函数(推荐)
     打开 terminal, 输入

     ```
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```

     它会直接输出一个完美的随机字符串，你把它复制粘贴到 `.env` 的 `DJANGO_SECRET_KEY=` 后面即可。

  2. 方式2: 使用 Python 内置的加密安全模块
     ```
     python -c "import secrets; print(secrets.token_urlsafe(50))"
     ```

**千万不要做!**

- ❌ 自己随手敲一串比如 `"mysecretkey123"`（几秒钟就能被暴力破解）
- ❌ 把 `settings.py` 里默认那个带 `django-insecure-` 前缀的用到生产环境（那只是开发用的）
- ❌ 把生成的这个真实字符串提交到 `GitHub/Gitee`

### 2.1.2 怎么使用

`SECRET_KEY` 在 `Django `中扮演的角色是**“签名印章”**。

你要理解一个核心概念：**它是用来“签名”的，不是用来“加密”的。**

- **加密**：把明文变成密文，别人看不懂（`Django `的密码存储用的是` bcrypt/hash` 算法，**不是** SECRET_KEY）。
- **签名**：数据依然是明文，但附带了一个“防伪标签”。一旦数据被篡改，标签就对不上了。

`Django `底层使用的是 `HMAC`（散列消息认证码）算法，<u>把 `SECRET_KEY` 作为密钥，对数据进行计算，得出一段独一无二的签名。</u>

#### 2.1.2.1 具体的 4 个应用场景：

##### 1. 保护 Session Cookie（最核心的用途）

`Django `默认把用户的登录状态（Session ID）存在浏览器的 Cookie 里。它发出的 Cookie 不是简简单单的 `sessionid=abc123`，而是：

```
sessionid=abc123:签名哈希值
```

- **如果没有 SECRET_KEY**：黑客可以把 Cookie 里的 `abc123` 改成别人的 ID `xyz789`，直接冒充别人登录。
- **有了 SECRET_KEY**：黑客改了 `abc123`，但因为他不知道你的 `SECRET_KEY`，他算不出对应的签名，`Django `一校验发现签名对不上，直接拒绝请求。

##### 2. 生成 `CSRF Token`（防跨站请求伪造）

当你在模板里写 `{% csrf_token %}` 时，`Django `会生成一个隐藏的 input 框。这个 Token 的值就是用 `SECRET_KEY` 签名算出来的。服务器收到表单时，用同样的 `SECRET_KEY` 验证 Token 是否是自己发出去的，防止恶意网站伪造表单提交（比如恶意网站伪装成你的系统让用户转账）。

##### 3. 密码重置链接

当用户点“忘记密码”时，`Django `会发一封带链接的邮件：`https://yoursite.com/reset/abc123xyz/` 。
这个 `abc123xyz` 里面包含了**用户ID + 时间戳**，并用 `SECRET_KEY` 进行了签名。

- 防止别人猜出链接篡改别人密码。
- `Django `一看签名，就知道这个链接是 10 分钟前发的，如果超过设定时间，签名过期，链接作废。

##### 4. 数据签名工具（开发者常用）

在视图代码里，你有时会直接用它来生成安全的数据传递令牌：

```
from django.core.signing import Signer

signer = Signer() # 底层自动读取 SECRET_KEY
# 把一个数字 56 签名
signed_value = signer.sign(56) 
# 输出类似：'56:abcdefghijklmnopqrstuvwxyz'
# 你可以把这个字符串发给前端，前端再传回来
original_value = signer.unsign(signed_value) # 自动校验并还原出 56
```

### 2.1.3、如果 SECRET_KEY 泄露了会怎样？

如果你的 `.env` 文件不小心传到了 GitHub，攻击者拿到了你的 `SECRET_KEY`，他就能：

1. **伪造任意用户的 Session**，直接以管理员身份登录你的系统。
2. **绕过所有 CSRF 防护**，构造恶意请求。
3. **伪造有效的密码重置链接**，直接重置管理员密码。

**一旦怀疑泄露，唯一的补救措施：立即重新生成一个全新的替换掉，这会导致所有用户的旧 Session 立即失效（全部被踢下线重新登录），但这是必须付出的安全代价。**

### 2.1.4 总结

| 问题       | 答案                                                         |
| ---------- | ------------------------------------------------------------ |
| 谁来写？   | **机器生成**。用终端命令生成一串随机字符。                   |
| 放在哪？   | 开发环境放 `.env`，生产环境放服务器环境变量或密钥管理服务（如阿里云 `KMS`）。 |
| 怎么用？   | 作为 **`HMAC 签名的密钥`**，给 Cookie、Token、链接打防伪标签，防篡改。 |
| 是加密吗？ | **不是**。数据本身没被加密，只是加上了不可伪造的签名。       |

## 2.2 `DJANGO_DEBUG ` 和 `DJANGO_ALLOWED_HOSTS`

这两个配置是 Django 开发者在**日常开发**和**项目部署**时，接触最频繁、也最容易踩坑的两个开关。

作为开发者，你需要建立一种**"双面人格"**的思维：**本地写代码时**怎么配，**代码上线后**怎么配。

下面我从**代码实现**和**实际工作流**两个角度教你如何使用它们。

### 一、DJANGO_DEBUG：开发者的"透视眼" vs 生产环境的"铁布衫"

#### 1. 在 `settings.py` 中如何正确读取？

因为 `.env` 文件读出来都是**字符串**（比如 `"True"`），而 Django 需要的是**布尔值**（`True`），所以你不能直接 `=`，需要做个转换：

```
import os
from dotenv import load_dotenv

load_dotenv()

# 推荐写法：兼容各种可能的写法（true, True, 1）
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() in ('true', '1', 't')
```

#### 2. 开发者如何利用 `DEBUG = True`？

当它是 `True` 时，Django 会为你开启以下"超能力"（这也是为什么它叫 Debug 模式）：

- **代码热重载：** 你修改了 `.py` 文件，保存的瞬间，服务器自动重启。不用手动 `Ctrl+C` 再 `python manage.py runserver`。
- **详细的错误追踪页：** 你的代码报错了（比如除以零、数据库字段写错），Django 不会返回一个干瘪的 500 错误，而是返回一个**极其漂亮的黄色/白色页面**，精确到第几行代码报错，甚至把上下文变量都打印出来。
- **静态文件自动服务：** Django 会自动帮你处理 CSS、JS、图片等静态文件，不需要额外配置 Nginx。
- **SQL 查询日志：** 如果你在模板里开启 `{% debug %}`，页面底部会显示当前页面执行了哪些 SQL 语句，耗时多少，这对优化数据库查询极其有用。

#### 3. 为什么生产环境必须是 `DEBUG = False`？

如果生产环境保持 `True`，一旦你的 EFMS 系统报错，**任何访问该网址的人，都能看到你服务器的完整目录结构、数据库配置、源代码片段**，这就相当于把家门钥匙贴在了门上。

当设为 `False` 时：

- 所有错误都会变成标准的 `500 Internal Server Error` 或 `400 Bad Request` 白色页面，不泄露任何信息。
- 静态文件服务失效（必须由 Nginx 等Web服务器代理）。
- 代码热重载失效。

**💡 开发者最佳实践：**
自己写一个 `views.py` 来处理 `DEBUG=False` 时的 404 和 500 页面，提升用户体验：

```
# 在你的主应用的 views.py 中
def page_not_found(request, exception):
    return render(request, '404.html', status=404)

def server_error(request):
    return render(request, '500.html', status=500)
```

### 二、DJANGO_ALLOWED_HOSTS：Django 的"门卫"

#### 1. 在 `settings.py` 中如何正确读取？

`.env` 里写的是用逗号分隔的字符串（`localhost,127.0.0.1`），Django 需要的是一个**列表**（`['localhost', '127.0.0.1']`），所以需要 `split(',')`：

```
# 从 .env 读取并转换为列表
hosts_str = os.getenv('DJANGO_ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [host.strip() for host in hosts_str.split(',') if host.strip()]
```

#### 2. 它到底在防什么？（HTTP Host 头攻击）

当用户在浏览器输入 `http://www.efms.com/login` 时，浏览器会向服务器发送一个请求头：`Host: www.efms.com`。

Django 会拿着这个 `Host` 值，去和 `ALLOWED_HOSTS` 列表比对。如果不在列表里，直接拒绝并返回 **400 Bad Request**。

**为什么不能随便放行？**
假设你不设限，攻击者可以伪造一个请求，把 `Host` 改成 `恶意钓鱼网站.com`。Django 在生成密码重置链接时，可能会拼上这个恶意的 Host，变成：`http://恶意钓鱼网站.com/reset/xxx`。用户收到邮件点进去，密码就被盗了 。

#### 3. 开发者的实际配置场景

#### 场景 A：纯本地开发

```
# .env
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

#### 场景 B：用手机测试（局域网联调）

你电脑跑着 Django，想用手机访问测试你的 EFMS 文件上传界面。

1. 查看你电脑的局域网 IP，比如是 `192.168.1.100`。
2. 启动服务时：`python manage.py runserver 0.0.0.0:8000`（监听所有网卡）。
3. **必须修改 `.env`**，否则手机访问会报 400：

```
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,192.168.1.100
```

#### 场景 C：使用内网穿透工具（如 Ngrok）

你用 Ngrok 生成了一个临时域名 `https://abc123.ngrok.io` 给产品经理看。
**必须修改 `.env`**：

```
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,abc123.ngrok.io
```

#### 场景 D：部署到生产服务器

你的域名是 `file.yourcompany.com`，服务器 IP 是 `120.xx.xx.xx`。

```
# 生产环境的 .env
DJANGO_ALLOWED_HOSTS=file.yourcompany.com,120.xx.xx.xx
```

*(注：有些人图省事写 `ALLOWED_HOSTS = ["\*"]`，这等于撤掉门卫，强烈不建议在正式项目里这么干)*

### 三、⚠️ 新手最容易踩的坑：两者的"隐秘联动"

Django 内部有一条**隐藏规则**，如果不了解，会让你怀疑人生：

> **当 `DEBUG = True` 时，Django 会自动把 `['localhost', '127.0.0.1', '[::1]']` 加到 `ALLOWED_HOSTS` 里。**

**这意味着什么？**

你在本地开发时，`.env` 里就算把 `DJANGO_ALLOWED_HOSTS` 留空，代码也不会报错，因为 `DEBUG=True` 在背后偷偷帮你兜底了。

**灾难发生的过程：**

1. 你在本地开发了一周，一切正常（`DEBUG=True`，`ALLOWED_HOSTS` 为空）。
2. 你把代码部署到服务器，把 `DEBUG` 改成了 `False`。
3. 你忘记配置 `ALLOWED_HOSTS`（或者列表里没写服务器的域名/IP）。
4. **结果：** 用户一访问网站，立刻报 **400 Bad Request**，整个网站无法访问，连后台都进不去！

### 总结：开发者的标准操作流程



| 阶段                      | DJANGO_DEBUG | DJANGO_ALLOWED_HOSTS             | 备注                           |
| :------------------------ | :----------- | :------------------------------- | :----------------------------- |
| **刚拉取代码初始化**      | `True`       | `localhost,127.0.0.1`            | 建立规范，不留空，养成习惯     |
| **手机/局域网测试**       | `True`       | 加上局域网IP，如 `192.168.1.100` | 忘了加就会报 400               |
| **提交代码前**            | 保持 `True`  | 保持不变                         | **确保 `.env` 没被提交到 Git** |
| **部署到测试/生产服务器** | **`False`**  | **改成真实域名或公网IP**         | **上线前最后检查的两件事！**   |

## 2.3 数据库配置相关

```
DB_NAME=efms_db
DB_USER=efms_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
```

这五个配置是 Django 与数据库之间的**"连接参数"**。你的 EFMS 项目跑起来后，每次执行任何数据库操作（用户登录、上传文件记录、查询文件列表），Django 都是靠这五个值找到并连接到 PostgreSQL 的。

下面我从**整条链路**教你如何使用。

### 一、先理解它们的角色

把这五个值想象成"去酒店开房"的过程：

```
DB_HOST  = 酒店的地址（哪栋楼？）         →  localhost / 120.xx.xx.xx
DB_PORT  = 酒店的大门（走哪个门进？）      →  5432
DB_USER  = 你的身份证（你是谁？）          →  efms_user
DB_PASSWORD = 你的房卡密码（证明是你本人）   →  xxxxxxxx
DB_NAME  = 房间号（你要进哪个房间？）       →  efms_db
```

**五个缺一不可，有一个错就连不上。**

### 二、在 settings.py 中如何使用

```
import os
from dotenv import load_dotenv

load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',   # 告诉 Django：用的是 PostgreSQL
        'NAME': os.getenv('DB_NAME'),                # 数据库名
        'USER': os.getenv('DB_USER'),                # 用户名
        'PASSWORD': os.getenv('DB_PASSWORD'),        # 密码
        'HOST': os.getenv('DB_HOST', 'localhost'),   # 地址，默认 localhost
        'PORT': os.getenv('DB_PORT', '5432'),        # 端口，默认 5432
    }
}
```

就这么简单，Django 剩下的所有事情（建表、查询、写入）都自动完成。

### 三、从零开始的完整操作流程（本地开发）

你拿到这个项目后，**不能直接 `python manage.py runserver`**，因为数据库还没准备好。正确的顺序是：

#### 第一步：安装 PostgreSQL

去 [postgresql.org](https://www.postgresql.org/download/) 下载安装，装完后它会在后台跑一个服务。

#### 第二步：连接数据库并创建库和用户

打开 **pgAdmin**（PostgreSQL 自带的图形界面）或者终端命令行 `psql`，执行：

```
-- 1. 创建一个专门给 EFMS 项目用的用户
CREATE USER efms_user WITH PASSWORD '你的真实密码';

-- 2. 创建数据库（编码必须是 UTF-8）
CREATE DATABASE efms_db
    WITH ENCODING 'UTF8'
    OWNER = efms_user;
```

> **为什么要创建专用用户，不用默认的 `postgres`？**
> 因为 `postgres` 是超级管理员，拥有所有数据库的完整权限。如果 Django 被注入恶意 SQL，攻击者可以删掉你电脑上所有数据库。用专用用户 + 最小权限，即使被攻破，损失也仅限于 `efms_db` 这一个库。

#### 第三步：填写 `.env` 文件

```
DB_NAME=efms_db
DB_USER=efms_user
DB_PASSWORD=你的真实密码        # 和上面 CREATE USER 时一致
DB_HOST=localhost               # 本地开发就是 localhost
DB_PORT=5432                    # PostgreSQL 默认端口，一般不用改
```

#### 第四步：验证 Django 能否连上数据库

```
python manage.py check
```

- 如果输出 `System check identified no issues.`，恭喜，连接成功 ✅
- 如果报错 `django.db.utils.OperationalError`，说明五个参数中至少有一个不对，需要排查（见下文的排错指南）。

#### 第五步：让 Django 自动建表

```
python manage.py makemigrations   # 分析 models.py 的变化，生成迁移文件
python manage.py migrate          # 执行迁移，在数据库中实际建表
```

这一步跑完后，你用 pgAdmin 打开 `efms_db`，会看到 Django 自动创建了一大堆表：

```
efms_db
├── auth_group                  ← Django 内置的用户组表
├── auth_user                   ← 用户表
├── django_migrations           ← 迁移记录表
├── django_session              ← 会话表
├── ...                         ← 你自己 app 的表（如 documents、folders 等）
```

#### 第六步：创建超级管理员（可选）

```
python manage.py createsuperuser
```

Django 会问你用户名、邮箱、密码，这些信息就是通过这五个配置写入 `efms_db` 的 `auth_user` 表中的。

### 四、不同环境的配置差异

#### 场景 A：本地开发

```
DB_NAME=efms_db
DB_USER=efms_user
DB_PASSWORD=mylocalpassword123
DB_HOST=localhost
DB_PORT=5432
```

#### 场景 B：团队协作（每个人用自己的本地数据库）

每个开发者在自己的电脑上都要执行上面的第一~四步，创建自己的 `efms_db`。

```
# 开发者A 的 .env
DB_PASSWORD=alice_local_pass

# 开发者B 的 .env
DB_PASSWORD=bob_local_pass
```

> **`.env` 不提交到 Git，所以每个人可以有不同的密码，互不影响。**

#### 场景 C：部署到生产服务器

生产环境通常在另一台服务器上（比如阿里云 ECS），PostgreSQL 也装在那台服务器上。

```
# 生产服务器的 .env
DB_NAME=efms_db
DB_USER=efms_user
DB_PASSWORD=Kj8$mN2!pL9#qR     # 必须是强密码！
DB_HOST=localhost               # 如果数据库和应用在同一台服务器
DB_PORT=5432
```

如果数据库和应用**分别部署在不同服务器**上：

```
# 应用服务器的 .env
DB_HOST=10.0.0.5                # 数据库服务器的内网 IP
```

> **注意：** 此时必须在数据库服务器的 `postgresql.conf` 中配置 `listen_addresses = '*'` 并在 `pg_hba.conf` 中允许该 IP 连接，否则会被拒绝。

### 五、在代码中的使用方式（日常开发基本不需要手动写 SQL）

配置好之后，你**几乎不需要直接接触这五个值**，Django 的 ORM 会帮你处理一切：

```
# 你写的代码长这样（完全不需要写 SQL）
class Document(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# 查询所有文件
Document.objects.all()

# 查询某用户上传的文件
Document.objects.filter(uploaded_by=request.user)

# 创建一条记录（自动写入数据库）
Document.objects.create(name="年度报告.pdf", uploaded_by=request.user)
```

Django ORM 在底层会自动把这五个配置读出来，用 `psycopg2` 库连接 PostgreSQL，把上面的 Python 代码翻译成 SQL 去执行。

### 六、连接失败怎么排查？（最常见的问题）

当你运行项目时报 `OperationalError: could not connect to server` 时，按这个顺序排查：

```
排查顺序
  │
  ├── 1. PostgreSQL 服务有没有启动？
  │      Windows: 服务 → 找 "postgresql-x64-xx" → 确认是"正在运行"
  │      Linux:   sudo systemctl status postgresql
  │
  ├── 2. DB_HOST 和 DB_PORT 对不对？
  │      用 pgAdmin 能连上，说明地址和端口没问题
  │
  ├── 3. DB_USER 和 DB_PASSWORD 对不对？
  │      用这个用户名密码在 pgAdmin 里手动登录试试
  │
  ├── 4. DB_NAME 对不对？数据库真的叫 efms_db 吗？
  │      在 pgAdmin 左侧面板看一眼
  │
  └── 5. 权限问题？
         确认 efms_user 确实是 efms_db 的 OWNER
         SQL: ALTER DATABASE efms_db OWNER TO efms_user;
```

### 总结：开发者需要记住的事

| 事项                     | 要点                                                         |
| ------------------------ | ------------------------------------------------------------ |
| **谁创建数据库？**       | 你手动用 `CREATE DATABASE` 创建，Django 不会自动帮你建库     |
| **谁创建表？**           | Django 通过 `migrate` 命令自动建表，你不需要手写 `CREATE TABLE` |
| **密码从哪来？**         | 你自己定，和 `CREATE USER` 时的密码保持一致                  |
| **需要记住这五个值吗？** | 不需要，写好 `.env` 之后，它们就被 settings.py 自动读取了    |
| **日常开发怎么用？**     | 写 Django ORM 代码，完全不需要写 SQL，Django 底层自动用这五个值连接数据库 |
| **团队协作怎么管？**     | 每个人本地创建自己的数据库，各自的 `.env` 互不干扰           |

2.4 































































































