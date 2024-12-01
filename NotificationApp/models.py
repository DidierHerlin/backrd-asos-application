from django.db import models


# Modèle de notification
class Notification(models.Model):
    MESSAGE_CHOICES = [
        ('approved', 'Votre rapport a été bien approuvé'),
        ('rejected', 'Votre rapport a été rejeté'),
        ('En attente','votre rapport est en cours de validation')
    ]
    contenue_notification = models.CharField(max_length=255)
    
    message = models.CharField(max_length=255, choices=MESSAGE_CHOICES, default='En attente')

    def __str__(self):
        return self.get_message_display()













