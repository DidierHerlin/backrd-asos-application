from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Rapport
from api.models import Notification
from .serializer import RapportSerializer
from django.http import FileResponse, HttpResponseNotFound, Http404
import os
from .drive_service import upload_file  # Assurez-vous d'importer votre fonction
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
import logging
from rest_framework import generics, permissions

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Rapport
from .serializer import RapportSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User  # Ajoutez cette ligne
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings


class RapportViewSet(viewsets.ModelViewSet):
    queryset = Rapport.objects.all()
    serializer_class = RapportSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rapport = serializer.save(user=request.user)

        # Récupérer tous les superutilisateurs
        admin_users = User.objects.filter(is_superuser=True)

        # Créer une notification et envoyer un e-mail à chaque administrateur
        for admin_user in admin_users:
            # Créer une notification dans la base de données
            Notification.objects.create(
                user=admin_user,
                message=f'Nouvelle notification de {request.user.username}: {rapport.titre}'
            )

            # Envoyer un e-mail de notification à l'administrateur
            send_mail(
                subject='Nouvelle notification de rapport',
                message=f'Le rapport "{rapport.titre}" a été créé par {request.user.username}.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[admin_user.email],  # E-mail de l'administrateur
                fail_silently=False,
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='user-reports')
    def user_reports(self, request):
        # L'utilisateur authentifié est accessible via request.user
        rapports = Rapport.objects.filter(user=request.user)

        if not rapports:
            return Response({'detail': 'No reports found for this user.'}, status=status.HTTP_404_NOT_FOUND)

        # Sérialisation des rapports et renvoi de la réponse
        serializer = self.get_serializer(rapports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        rapport = self.get_object()
        rapport.statut = 1
        rapport.save()

        file_path = rapport.contenue.path
        username = rapport.user.username
        try:
            upload_file(file_path, username)  # Uploader le fichier sur Google Drive
            message = 'Votre rapport a été validé et le fichier a été uploadé sur Google Drive.'
        except Exception as e:
            logging.error(f"Erreur lors de l'upload du fichier: {e}")
            message = 'Votre rapport a été validé, mais l\'upload du fichier sur Google Drive a échoué.'
        # Créer une notification pour l'utilisateur qui a soumis le rapport
        Notification.objects.create(
            user=rapport.user,
            message=message
        )
        # Envoyer un e-mail de notification à l'utilisateur
        self.send_email_notification(rapport.user.email, 'Validation de votre rapport', message)
        return Response({'message': message}, status=status.HTTP_200_OK)





    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        rapport = self.get_object()
        rapport.statut = 0
        rapport.save()

        # Message de notification
        message = 'Votre rapport a été rejeté.'

        # Créer une notification pour l'utilisateur qui a soumis le rapport
        Notification.objects.create(
            user=rapport.user,
            message=message
        )

        # Envoyer un e-mail de notification à l'utilisateur
        self.send_email_notification(rapport.user.email, 'Rejet de votre rapport', message)

        return Response({'message': message}, status=status.HTTP_200_OK)

    def send_email_notification(self, recipient_email, subject, message):
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                fail_silently=False,
            )
        except Exception as e:
            logging.error(f"Erreur lors de l'envoi de l'e-mail : {e}")


    @action(detail=True, methods=['get'])
    def visualiser(self, request, pk=None):
        rapport = self.get_object()
        file_path = rapport.contenue.path
        
        try:
            response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename={os.path.basename(file_path)}'
            return response
        except FileNotFoundError:
            return HttpResponseNotFound("File not found")
        

    @action(detail=True, methods=['get', 'put', 'patch'], url_path='afficher-et-modifier-rejet')
    def afficher_et_modifier_rapport_rejete(self, request, pk=None):
        try:
            # Récupérer le rapport par sa clé primaire (pk) pour l'utilisateur authentifié avec le statut "Rejeté"
            rapport = Rapport.objects.get(pk=pk, user=request.user, statut=0)
        except Rapport.DoesNotExist:
            return Response({'detail': 'Rapport non trouvé ou il n\'est pas rejeté.'}, status=status.HTTP_404_NOT_FOUND)

        # Gérer la requête GET : Afficher les détails du rapport rejeté
        if request.method == 'GET':
            serializer = self.get_serializer(rapport)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Gérer les requêtes PUT ou PATCH : Modifier le rapport rejeté
        serializer = self.get_serializer(rapport, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        rapport = serializer.save()

        # Créer une notification et envoyer des emails aux administrateurs après modification du rapport
        self.create_notification_for_admins(rapport)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def create_notification_for_admins(self, rapport):
        # Récupérer tous les superutilisateurs
        admin_users = User.objects.filter(is_superuser=True)

        # Créer une notification pour chaque administrateur
        for admin_user in admin_users:
            Notification.objects.create(
                user=admin_user,
                message=f'Le rapport "{rapport.titre}" a été modifié par {rapport.user.username}.',
                is_read=False,
                created_at=timezone.now()  # Optionnel, car `created_at` sera rempli automatiquement
            )



    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        user_id = request.user.id
        
        # Compte le total des rapports
        total_rapports = Rapport.objects.filter(user_id=user_id).count()
        
        # Compte les rapports validés
        validés_count = Rapport.objects.filter(user_id=user_id, statut=1).count()
        
        # Compte les rapports rejetés
        rejetés_count = Rapport.objects.filter(user_id=user_id, statut=0).count()
        
        # Compte les rapports en attente
        en_attente_count = Rapport.objects.filter(user_id=user_id, statut=2).count()
        
        # Prépare la réponse
        stats = {
            'total_rapports': total_rapports,
            'validés_count': validés_count,
            'rejetés_count': rejetés_count,
            'en_attente_count': en_attente_count,
        }

        return Response(stats, status=status.HTTP_200_OK)

      

