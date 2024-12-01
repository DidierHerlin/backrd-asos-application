from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # L'utilisateur qui recevra la notification
    message = models.TextField()  # Le message de la notification
    is_read = models.BooleanField(default=False)  # Statut de lecture
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création

    def __str__(self):
        return f'Notification for {self.user.username} - {self.message}'
