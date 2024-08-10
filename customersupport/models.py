from django.db import models
from onboarding.models import CustomUser

# Create your models here.
class SupportRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='support_requests')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    attended_to = models.BooleanField(default=False)

    def __str__(self):
        return self.subject