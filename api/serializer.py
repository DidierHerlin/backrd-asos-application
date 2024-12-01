from rest_framework import serializers


from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
from RapportApp.models import Rapport
from .models import Notification

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure password is write-only
        }

    def create(self, validated_data):
        """Create a new user with the provided validated data."""
        return User.objects.create_user(**validated_data)



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# Serializer jwt token

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token serializer for JWT."""
    
    @classmethod
    def get_token(cls, user):
        """Override the method to add custom claims if needed."""
        token = super().get_token(user)

        # Add custom claims here if needed
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_superuser', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},  # Le mot de passe est facultatif
            'is_active': {'default': True},  # Activer par défaut
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)  # Extraire le mot de passe
        user = User(**validated_data)  # Créer l'utilisateur sans mot de passe pour le moment
        if password:
            user.set_password(password)  # Définir le mot de passe
        user.is_active = True  # Activer l'utilisateur
        user.save()  # Sauvegarder l'utilisateur
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)  # On extrait le mot de passe, s'il existe
        activation_token = validated_data.pop('activation_token', None)
        
        # Mettre à jour les autres attributs
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Mettre à jour le mot de passe uniquement s'il a été fourni
        if password:
            instance.set_password(password)
        
        # Gérer le token d'activation si fourni
        if activation_token:
            Token.objects.get_or_create(user=instance, key=activation_token)
        
        instance.save()  # Enregistrer les modifications
        return instance


    
# modifier mdp

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


# admin dashboard
# serializers.py



class RapportStatsSerializer(serializers.Serializer):
    statut_0 = serializers.IntegerField()
    statut_1 = serializers.IntegerField()
    statut_2 = serializers.IntegerField()
    total_count = serializers.IntegerField()
    
# mofication utilisateur








# class RapportSerializer(serializers.ModelSerializer):
#     projet = serializers.PrimaryKeyRelatedField(queryset=Projet.objects.all())

#     class Meta:
#         model = Rapport
#         fields = ['id', 'titre', 'contenue', 'date_creation', 'statut', 'user', 'projet']
#         read_only_fields = ['user', 'date_creation']

#     def validate_statut(self, value):
#         if value not in dict(Rapport.STATUT_CHOICES):
#             raise serializers.ValidationError("Statut invalide.")
#         return value

#     def create(self, validated_data):
#         rapport = Rapport.objects.create(**validated_data)
#         return rapport

#     def update(self, instance, validated_data):
#         projet_id = validated_data.pop('projet', None)
#         if projet_id:
#             instance.projet = Projet.objects.get(id=projet_id)
#         return super().update(instance, validated_data)

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['nom_projet'] = instance.projet.nom_projet if instance.projet else None
#         return representation

# class RapportSerializer(serializers.ModelSerializer):
#     projet_id = serializers.IntegerField(write_only=True)
#     projet = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = Rapport
#         fields = ['id', 'titre', 'contenue', 'date_creation', 'statut', 'user', 'projet', 'projet_id']
#         read_only_fields = ['user', 'date_creation']

#     def create(self, validated_data):
#         projet_id = validated_data.pop('projet_id')
#         rapport = Rapport.objects.create(**validated_data, projet_id=projet_id)
#         return rapport

#     def update(self, instance, validated_data):
#         projet_id = validated_data.pop('projet_id', None)
#         instance.titre = validated_data.get('titre', instance.titre)
#         instance.contenue = validated_data.get('contenue', instance.contenue)
#         instance.statut = validated_data.get('statut', instance.statut)
        
#         if projet_id is not None:
#             instance.projet_id = projet_id
        
#         instance.save()
#         return instance

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['nom_projet'] = instance.projet.nom_projet if instance.projet else None
#         return representation




class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'