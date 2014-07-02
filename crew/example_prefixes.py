from django.core.files.storage import FileSystemStorage
from django.utils.functional import SimpleLazyObject
from django.conf import settings
from s3storage import S3BotoStorage
import os

# A helper for storing easy_thumbnails files with reduced redundancy:
S3BotoStorageReducedRedundancy = lambda: S3BotoStorage(reduced_redundancy=True) 

# Example of setting custom django-filer storage paths:

# Set your filer storage to this object to replace the "filer" path with "f":
filer_storage_s3 = SimpleLazyObject(lambda: S3BotoStorage(location='f'))

# Here is an example of a custom storage object to make file thumbnails 
# get stored in a custom path, outside of the normal filer folder:
filer_thumb_storage_s3 = SimpleLazyObject(lambda: S3BotoStorage(location='thumbs/f', reduced_redundancy=True))
