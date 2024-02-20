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


class Category(models.Model):
    name = models.CharField(max_length=100)
    subcategory = models.ForeignKey("self", on_delete=models.PROTECT)
    icon = models.ImageField(upload_to="path/")
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=4, unique=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    short_name = models.CharField(max_length=4)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class FieldTypes(models.TextChoices):
    string = ("string", "string")
    integer = ("integer", "integer")
    boolean = ("boolean", "boolean")
    date = ("date", "date")
    time = ("time", "time")
    datetime = ("datetime", "datetime")
    float = ("float", "float")
    image = ("image", "image")
    file = ("file", "file")


class OptionalField(models.Model):
    FieldTypes = FieldTypes
    name = models.CharField(max_length=30)
    key = models.CharField(max_length=12)
    type = models.CharField(max_length=30, choices=FieldTypes.choices, default=FieldTypes.string)
    is_required = models.BooleanField(default=False)
    default = models.TextField(null=True, blank=True)
    max_length = models.IntegerField(null=True, blank=True)
    min_length = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class OptionalFieldThrough(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    optional_field = models.ForeignKey(OptionalField, on_delete=models.CASCADE)
    value = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="path/")
    file = models.FileField(null=True, blank=True, upload_to="path/")

    def __str__(self):
        return self.value


class JobStatusChoices(models.TextChoices):
    published = "published", "Published"
    under_review = "under_review", "Under Review"
    approved = "approved", "Approved"
    draft = "draft", "Draft"
    rejected = "rejected", "Rejected"
    archived = "archived", "Archived"
    blocked = "blocked", "Blocked"


class Job(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    description = models.TextField(default="")
    contact_number = models.CharField(max_length=18)
    email = models.EmailField()
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(max_length=30)
    photo = models.ImageField(upload_to="path/")
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    is_vip = models.BooleanField(default=False)
    is_top = models.BooleanField(default=False)
    # rate future

    optional_field = models.ManyToManyField(
        OptionalField,
        through=OptionalFieldThrough,
        through_fields=('job', 'optional_field')
    )


class Review(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(default="")
    first_name = models.CharField(max_length=200)
    email = models.EmailField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name


class TeamRole(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="")
    photo = models.ImageField(upload_to="path/")
    role = models.ForeignKey(TeamRole, on_delete=models.PROTECT)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name