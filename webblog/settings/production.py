from .base import *

DEBUG = False

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'ali-d-akbar'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# AWS_DEFAULT_ACL = None

AWS_LOCATION = 'static'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

DEFAULT_FILE_STORAGE = 'webblog.storage_backends.MediaStorage'  # <-- here is where we reference it

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd4dbcnipet05um',
        'USER': 'xasomvaxhajhxx',
        'PASSWORD': '53a76fedcc3fe275e79d3be481f883db62fa00f2e0a3963869fcb6f4843e61d3',
        'HOST': 'ec2-174-129-227-146.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}
