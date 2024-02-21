from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, email=None, **extra_fields):
        if not phone:
            raise ValueError("The Phone field must be set")
        phone = self.normalize_email(phone)
        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone, password, **extra_fields)


class SocialMedia(models.Model):
    title = models.CharField(max_length=50)
    icon = models.ImageField(upload_to="path/")
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SocialThrough(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    social = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    url = models.URLField()
    date_update = models.DateTimeField(auto_now=True)
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=18, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    username = None
    is_agree_terms = models.BooleanField(default=False)
    photo = models.ImageField(upload_to="path/")
    about = models.TextField(default="", null=True, blank=True)
    update_about = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    social_media = models.ManyToManyField(
        SocialMedia,
        through=SocialThrough,
        through_fields=('user', 'social'),
        related_name='socialLinks'
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    def __str__(self):
        return self.phone

    class Meta:
        db_table = "user_table"
        verbose_name = "CustomUser"
        verbose_name_plural = "CustomUsers"
