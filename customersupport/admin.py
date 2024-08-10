from django.contrib import admin

from .models import SupportRequest

class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'message', 'created_at', 'attended_to')
    search_fields = ('user__username', 'subject')
    list_filter = ('created_at',)

admin.site.register(SupportRequest, SupportRequestAdmin)
# Register your models here.
