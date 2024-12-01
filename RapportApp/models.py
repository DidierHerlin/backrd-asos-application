from django.db import models
from django.contrib.auth.models import User
from ProjetApp.models import Projet

class Rapport(models.Model):
    STATUT_CHOICES = [
        (0, 'Rejeté'),
        (1, 'Validé'),
        (2, 'En attente'),  # Statut par défaut
    ]

    titre = models.CharField(max_length=255)
    contenue = models.FileField(upload_to='rapports/')
    date_creation = models.DateTimeField(auto_now_add=True)
    statut = models.PositiveSmallIntegerField(choices=STATUT_CHOICES, default=2)  # Définit "En attente" comme statut par défaut
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre

    @property
    def statut_display(self):
        """Renvoie la version lisible du statut."""
        return dict(self.STATUT_CHOICES).get(self.statut, 'Inconnu')


