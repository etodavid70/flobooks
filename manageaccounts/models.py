from django.db import models
from onboarding.models import CustomUser

# Create your models here.
class Subuser(models.Model):
    base_user= models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sub_users")

    #remove this default in production
    subuser_name= models.CharField(max_length=40, default=" "  )
    subuser_email= models.EmailField( unique=True)
    subuser_password= models.CharField(max_length=25)

    

    def __str__(self):
        return self.subuser_name
