from django.db import models
from django.conf import settings
from PIL import Image
from .jobs import UploadToPathAndRename


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(
        default="avatars/avatar-default.jpg", upload_to=UploadToPathAndRename("avatars")
    )
    avatar = models.ImageField(
        default="avatars/avatar-default.jpg", upload_to=UploadToPathAndRename("avatars")
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        path = self.avatar.path  # pylint: disable=no-member
        path = self.avatar.path  # pylint: disable=no-member
        img = Image.open(path)
        if img.height != 700 or img.width != 700:
            output_size = (700, 700)
            img = img.resize(output_size)
            img.save(path)
