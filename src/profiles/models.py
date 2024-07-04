from PIL import Image
from django.db import models
from django.db.models import Sum
from django.conf import settings
from core.jobs import UploadToPathAndRename
from django.core.exceptions import ValidationError
from trades.models import Trade


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(
        default="avatars/avatar-default.jpg", upload_to=UploadToPathAndRename("avatars")
    )
    avatar = models.ImageField(
        default="avatars/avatar-default.jpg", upload_to=UploadToPathAndRename("avatars")
    )
    valoration = models.IntegerField(default=0)
    
    def update_rating(self):
        valorations = Valoration.objects.filter(to_user_id=self.user.id).exclude(rating=-1)
        valorations_sum = valorations.aggregate(total=Sum('rating'))['total']
        if valorations_sum is not None:
            self.valoration = int(valorations_sum / valorations.count())
        else:
            self.valoration = 0
        self.save()
        

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        path = self.avatar.path  # pylint: disable=no-member
        img = Image.open(path)
        if img.height != 700 or img.width != 700:
            output_size = (700, 700)
            img = img.resize(output_size)
            img.save(path)
            

class Valoration(models.Model):
    trade = models.ForeignKey(Trade, verbose_name=("trade"), on_delete=models.PROTECT)
    from_user = models.ForeignKey("user.User", verbose_name=(""), on_delete=models.PROTECT, related_name="Rating")
    to_user = models.ForeignKey("user.User", verbose_name=(""), on_delete=models.PROTECT, related_name="Rated")
    rating = models.IntegerField();
    
    def skipped(self):
        return self.rating == -1