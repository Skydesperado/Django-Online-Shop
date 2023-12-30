from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .managers import UserManager
from .validators import phone_number


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11,
                                    unique=True,
                                    validators=[phone_number])
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin


class OTP(models.Model):
    otp = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(10000),
                    MaxValueValidator(99999)])
    phone_number = models.CharField(max_length=11,
                                    unique=True,
                                    validators=[phone_number])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"

    def __str__(self):
        return f"{self.phone_number} - {self.otp} - {self.created_at}"
