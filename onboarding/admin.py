from django.contrib import admin

# Register your models here.
from onboarding.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display=['email', 'first_name', 'last_name', 'phoneNumber',"present_package",'country','state','businessName', ]



admin.site.register(CustomUser, CustomUserAdmin)