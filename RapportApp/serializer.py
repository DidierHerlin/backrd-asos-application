from rest_framework import serializers
from .models import Projet, Rapport

class RapportSerializer(serializers.ModelSerializer):
    projet = serializers.PrimaryKeyRelatedField(queryset=Projet.objects.all())
    nom_projet = serializers.SerializerMethodField()
    statut_display = serializers.SerializerMethodField()
    contenue_url = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)  # Inclure le nom d'utilisateur directement

    class Meta:
        model = Rapport
        fields = ['id', 'titre', 'contenue', 'contenue_url', 'date_creation', 'statut', 'statut_display', 'user', 'projet', 'nom_projet','username']
        read_only_fields = ['user']

    def get_nom_projet(self, obj):
        return obj.projet.nom_projet if obj.projet else None

    def get_statut_display(self, obj):
        return obj.get_statut_display()

    def get_contenue_url(self, obj):
        """Retourne l'URL publique pour accéder au fichier PDF"""
        if obj.contenue:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.contenue.url)
        return None

    def update(self, instance, validated_data):
        # Mise à jour des champs autorisés
        for attr in ['titre', 'contenue', 'projet']:
            if attr in validated_data:
                setattr(instance, attr, validated_data[attr])

        # Récupérer le statut actuel et le statut à valider
        current_statut = instance.statut
        new_statut = validated_data.get('statut')

        # Si le statut actuel est "0" (Rejeté), forcer la mise à jour à "2" (En attente)
        if current_statut == 0:
            instance.statut = 2
        elif new_statut in [0, 1]:
            # Si le statut est valide (0 ou 1), permettre la mise à jour
            instance.statut = new_statut

        instance.save()  # Sauvegarde l'instance
        return instance
    
    def get_username(self, obj):
        """Retourne le nom d'utilisateur associé au rapport"""
        return obj.user.username if obj.user else 'Utilisateur inconnu'



class StatutCountSerializer(serializers.Serializer):
    statut = serializers.IntegerField()
    nombre_rapports = serializers.IntegerField()