from django.db import models
from RapportApp.models import Rapport 


class Archive(models.Model):
    lien_archive = models.URLField()
    date_archive = models.DateTimeField(auto_now_add=True)
    rapport = models.ForeignKey(Rapport, on_delete=models.CASCADE)

    def __str__(self):
        return f"Archive for {self.rapport.titre}"
        return f"Validation for {self.rapport.titre}"