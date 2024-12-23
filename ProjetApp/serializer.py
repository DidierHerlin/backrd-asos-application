from rest_framework import serializers
from .models import Projet

class ProjetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projet
        fields = ['id', 'nom_projet']