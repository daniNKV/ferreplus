from django.utils import timezone
from django.db import models
from user.models import User
from owners.models import Branch
from core.jobs import UploadToPathAndRename


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    creation_date = models.DateField()
    image = models.ImageField(
        upload_to=UploadToPathAndRename("item/images/"), null=False, blank=False
    )
    was_traded = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, blank=True, null=True
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:  # if the object is being created
            self.creation_date = timezone.now()
        super().save(*args, **kwargs)

    def __str(self):
        return str(self.name)
