from django.db import models

# Create your models here.

class Projet(models.Model):
    nom_projet = models.CharField(max_length=255)

    def __str__(self):
        return self.nom_projet

