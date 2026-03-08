from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class AdminManager(BaseUserManager):
    def create_admin(self, phone, name, password, **extra_fields):
        if not phone:
            raise ValueError('Phone number is required')
        admin = self.model(phone=phone, name=name, **extra_fields)
        admin.set_password(password)
        admin.save(using=self._db)
        return admin


class Admin(AbstractBaseUser):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AdminManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'admins'

    def __str__(self):
        return f'{self.name} ({self.phone})'
