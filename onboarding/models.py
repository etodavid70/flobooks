from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

#this is to overide the username with email

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):

     # to Remove the username field
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'

    #additional fields
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    phoneNumber=models.CharField(max_length=20)
    businessName = models.CharField(max_length=255)
    businessAddress = models.CharField(max_length=255)
    start_tax = models.BooleanField(default=False)
    PACKAGE_CHOICES = [
    ('bronze', 'Bronze'),
    ('gold', 'Gold'),
    ('platinum', 'Platinum'),
    ('diamond', 'Diamond'),
            ]
    present_package = models.CharField(
    max_length=20,
    choices=PACKAGE_CHOICES,
    default='bronze',
    )

    objects = CustomUserManager()
    REQUIRED_FIELDS = []

class UserPhoto(models.Model):
    user = models.OneToOneField( CustomUser, on_delete=models.CASCADE)
    business_logo= models.ImageField(upload_to="onboarding\profile_photos", null=True, blank=True)

    def __str__(self):
        return self.user.email


