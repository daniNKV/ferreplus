import os
import hashlib
from django.utils.deconstruct import deconstructible

@deconstructible
class UploadToPathAndRename(object):
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        extension = filename.split('.')[-1]
        filename = '{}.{}'.format(hashlib.md5(filename.encode()).hexdigest(), extension)
        return os.path.join(self.path, filename)
