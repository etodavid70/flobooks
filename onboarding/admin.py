from django.contrib import admin

# Register your models here.
from onboarding.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display=['email', 'phoneNumber','businessName', "businessAddress","present_package" ]
    search_fields = ('email', 'phoneNumber', "businessName")



admin.site.register(CustomUser, CustomUserAdmin)