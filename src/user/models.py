from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField()

    # TODO: Instalar Pillow para manejo de imagenes. Implementar con el perfil del usuario.
    # avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
