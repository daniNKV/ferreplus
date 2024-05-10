from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, birth_date, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")
        if not birth_date:
            raise ValueError("User must have a birth date")
        if not password:
            raise ValueError("User must have a password")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            password=password,
        )
        user.password = make_password(user.password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, birth_date, password):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):
    first_name = models.CharField(verbose_name="First name", max_length=20)
    last_name = models.CharField(max_length=20, verbose_name="Last name")
    birth_date = models.DateField(verbose_name="Date of birth")
    email = models.EmailField(verbose_name="Email", max_length=60, unique=True)
    password = models.CharField(verbose_name="Password", max_length=100)
    date_joined = models.DateTimeField(verbose_name="Joined on date", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="user_set",
        related_query_name="user",
        to="auth.group",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="user_set",
        related_query_name="user",
        to="auth.permission",
        verbose_name="user permissions",
    )
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "birth_date"]

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def __int__(self):
        return self.pk

    def get_id(self):
        return self.pk

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    # TODO: Instalar Pillow para manejo de imagenes. Implementar con el perfil del usuario.
    # avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
