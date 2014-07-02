# Set up Amazon S3
AWS_ACCESS_KEY_ID = "----------------"
AWS_SECRET_ACCESS_KEY = "------------"
AWS_STORAGE_BUCKET_NAME = "s3.mysite.com"
AWS_S3_CUSTOM_DOMAIN = "s3.mysite.com"
AWS_REDUCED_REDUNDANCY = False # We enable this server-wide on our staging server's S3 buckets
AWS_PRELOAD_METADATA = True # You want this to be on!
AWS_S3_SECURE_URLS = False
AWS_HEADERS = { 'Cache-Control': 'max-age=2592000' }
AWS_QUERYSTRING_AUTH = False


MY_DEFAULT_STORAGE = 'myapp.s3storage.S3BotoStorage' # Used below
DEFAULT_FILE_STORAGE = MY_DEFAULT_STORAGE
COMPRESS_STORAGE = MY_DEFAULT_STORAGE # use with django-compressor
STATICFILES_STORAGE = MY_DEFAULT_STORAGE # use with django-staticfiles
FILER_PUBLICMEDIA_STORAGE = 'myapp.example_prefixes.filer_storage_s3' # user with django-filer
# Finally, we want to use reduced redundancy storage for all thumbnails:
FILER_PUBLICMEDIA_THUMBNAIL_STORAGE = 'myapp.example_prefixes.filer_thumb_storage_s3'
THUMBNAIL_DEFAULT_STORAGE = 'myapp.example_prefixes.S3BotoStorageReducedRedundancy'
