"""
Django settings for xiaopgg_project project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import pymysql
pymysql.install_as_MySQLdb()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)定义项目路径，用来提供给下面的路径组合用的
# 因为项目内的目录基本不会改变，但是项目的路径因人而异有的放在/usr/local有的放在/src等，用这个可以获取这个路径，比如下面的日志logs就用
# 用这个来组合的，这样不管项目放在那里logs路径都是在项目下
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9=7mwgwj7n+t%&&-sdum)qcf-e+fkiau&$mq1&kvpzx-05l-z^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# 默认只要下面这个超时时间到了，session都失效掉，然后跳转登录页
SESSION_COOKIE_AGE = 60*60*4
# 下面这个设置了以后每次请求都会记录session，这样不会出现因为上面的超时间到了操作一半给你跳转到登录页，那样太不人性化
SESSION_SAVE_EVERY_REQUEST = True
# Application definition

# 未通过认证时跳转的认证页面
LOGIN_URL = '/login/'
# 登录成功后默认跳转的页面
LOGIN_REDIRECT_URL = '/'


# django_crontab是定时任务使用的
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'xpgg_oms',
    'django_crontab',
    'guardian',
]

# django-guardian配置
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # this is default
    'guardian.backends.ObjectPermissionBackend',
)

CRONJOBS = [('*/10 * * * *', 'xpgg_oms.cron.minion_status', '>>/usr/local/django/xiaopgg_project/logs/cron.log 2>&1'),
            ('*/10 * * * *', 'xpgg_oms.cron.saltkey_list', '>>/usr/local/django/xiaopgg_project/logs/cron.log 2>&1')]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'xpgg_oms.middleware.UserAuthentication',
]

ROOT_URLCONF = 'xiaopgg_project.urls'

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
                'xpgg_oms.views.global_setting'   # 添加在这里django启动的时候就会运行，全局使用的东西都配置在这方法里
            ],
        },
    },
]

# 网站的基本信息配置，全局配置，在views的global_setting里使用，上面TEMPLATES里要添加启动django时候运行即可使用
SITE_URL = 'http://localhost:8000/'
SITE_NAME = '小胖哥哥运维系统'
SITE_DESC = '专注Python开发，欢迎和大家交流'
# salt-api地址
SITE_SALT_API_URL = 'http://192.168.68.50:8080'
# salt-api用户
SITE_SALT_API_NAME = 'saltapi'
# salt-api密码
SITE_SALT_API_PWD = '123456'
# salt服务端安装的minion的id，服务端也要安装一下minion，有很多用到的时候
SITE_SALT_MASTER = '192.168.68.50-master'
# salt服务端IP，salt-ssh等调用
SITE_SALT_MASTER_IP = '192.168.68.50'
# 发布系统中随机生成svn目录的路径和名字前缀，这里是xiaopgg作为前缀嘿嘿
# 在views.py里后面加上当前时间来组成完整的目录路径，千万别出现中文因为py2版salt中文支持不好，出现中文后同步文件时目录可以同步文件不同步过去反而全被删除！！
SITE_BASE_SVN_PATH = '/data/svn/xiaopgg'
# 在用salt同步文件过程中发如果file_roots定义的目录内文件太多会非常的慢，所以使用的软连接的方式同步完删除软连接来保持file_roots目录的整洁
SITE_BASE_SVN_SYMLINK_PATH = '/data/svn_symlink/'

###

WSGI_APPLICATION = 'xiaopgg_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xpgg_oms',    # 你的数据库名称
        'USER': 'xiaopgg',   # 你的数据库用户名
        'PASSWORD': '123456',  # 你的数据库密码
        'HOST': '',  # 你的数据库主机，留空默认为localhost
        'PORT': '3306',  # 你的数据库端口,

        'OPTIONS': {
        # 在mysql5.7以前需要加下面的来使得同步数据库时候不会出现严格模式的警告，5.7开始默认是严格模式了就可以省略
        #     'init_command': "SET sql_mode= 'STRICT_TRANS_TABLES'",
        # 如果InnoDB Strict Mode也是严格模式也需要加下面的
        #     'init_command': 'SET innodb_strict_mode=1',
        #     之前是通过utf8创建的数据库，所以下面的这个注释掉，如果用utf8mb4可以试着打开这个
        #     'charset': 'utf8mb4',
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
#静态文件配置
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


# 配置上传文件路径
MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

# 自定义用户model
AUTH_USER_MODEL = 'xpgg_oms.MyUser'

# 自定义日志输出信息
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}  # 日志格式
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
            },
        # 下面是django自带的最详细的输出
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/all.log'),     # 日志输出文件，根目录下需要手动新建
            'maxBytes': 1024*1024*5,                  # 文件大小5M
            'backupCount': 5,                         # 备份份数
            'formatter': 'standard',                   # 使用哪种formatters日志格式上面定义了standard
        },
        # 下面是django自带的控制台输出
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        # 下面是django自带的5xx或者4xx错误记录在script.log里
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/script.log'),
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter': 'standard',
            },
        # 下面是django自带的脚本错误记录
        'scprits_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR,'logs/script.log'),
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter': 'standard',
            }
    },
    # 下面是定义日志器
    'loggers': {

        'django': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },

        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False,  # 是否继承父类
            },
        'scripts': {
            'handlers': ['scprits_handler'],
            'level': 'INFO',
            'propagate': False
        },
        # 下面是给views调用使用的
        'xpgg_oms.views': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}