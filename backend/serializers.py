from django.db import models
from django.contrib.auth.models import User  # Optional

class Report(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)  # Or use a DateField
    file = models.FileField(upload_to='reports/', blank=True)
    image = models.ImageField(upload_to='reports/images/', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)  # Optional, if user association required

    def __str__(self):
        return self.title
    