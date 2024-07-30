from django.db import models

from django.db import models
from onboarding.models import CustomUser

# Create your models here.
class Subuser(models.Model):
    base_user= models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sub_users")

    #remove this default in production
    subuser_name= models.CharField(max_length=40 )
    subuser_email= models.EmailField( unique=True)
    subuser_password= models.CharField(max_length=25)


    def __str__(self):
        return self.subuser_email


# models.py
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
import binascii
import os
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='custom_auth_token', on_delete=models.CASCADE, blank=True, null=True
    )
    subuser = models.ForeignKey(
        'Subuser', related_name='custom_auth_token', on_delete=models.CASCADE, blank=True, null=True
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'subuser'),)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()



