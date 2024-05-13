import re
from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rolepermissions.roles import assign_role


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
        assign_role(user, 'user')
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
        assign_role(user, 'owner')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class EmployeeManager(UserManager):
    def create_employee(
        self, email, first_name, last_name, birth_date, dni, branch, password=None
    ):
        if not dni or not re.match(r"^\d{7,8}$", dni):
            raise ValueError("Employee DNI must be 7 or 8 digits")
        if not branch:
            raise ValueError("Employee must have a branch")

        user = super().create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            password=password,
        )
        assign_role(user, 'employee')
        employee = self.model(user=user, dni=dni, branch=branch)
        employee.user.is_staff = True
        employee.save()
        return employee


class User(AbstractBaseUser):
    class Meta:
        verbose_name = "Usuario"

    first_name = models.CharField(verbose_name="Nombre", max_length=20)
    last_name = models.CharField(max_length=20, verbose_name="Apellido")
    birth_date = models.DateField(verbose_name="Fecha de nacimiento")
    email = models.EmailField(verbose_name="Email", max_length=60, unique=True)
    password = models.CharField(verbose_name="Password", max_length=100)
    date_joined = models.DateTimeField(
        verbose_name="Fecha de registro", auto_now_add=True
    )
    last_login = models.DateTimeField(verbose_name="Ultima vez activo", auto_now=True)
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
    REQUIRED_FIELDS = ["first_name", "last_name", "birth_date", "password"]

    objects = UserManager()

    def get_absolute_url(self):
        return f"/users/{self.pk}/"

    def __int__(self):
        return self.pk

    def get_id(self):
        return self.pk

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.first_name + " " + self.last_name

    # TODO: Instalar Pillow para manejo de imagenes. Implementar con el perfil del usuario.
    # avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)


class Employee(models.Model):
    class Meta:
        verbose_name = "Empleado"

    user = models.OneToOneField(User, verbose_name="Usuario", on_delete=models.CASCADE)
    dni = models.CharField(
        verbose_name="Documento nacional de identidad", max_length=8, unique=True
    )
    branch = models.ForeignKey(
        "owners.Branch", verbose_name="Sucursal", on_delete=models.CASCADE
    )
    objects = EmployeeManager()

    def __str__(self):
        return self.user.__str__()
