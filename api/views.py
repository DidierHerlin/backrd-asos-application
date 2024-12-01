# api/views.py

from rest_framework import status, generics, viewsets
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.models import User
from .models import Notification
from RapportApp.models import Rapport
from .serializer import MyTokenObtainPairSerializer, RegisterSerializer, UserSerializer,ChangePasswordSerializer,NotificationSerializer
from RapportApp.serializer import StatutCountSerializer
from RapportApp.serializer import RapportSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from django.core.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import secrets  # Pour générer un token unique
from rest_framework.decorators import action
from datetime import datetime, timedelta
from django.db.models import Count, F
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.db.models.functions import TruncMonth
from django.utils import timezone



import uuid
from django.db import models

from django.http import JsonResponse

def api_root_view(request):
    return JsonResponse({
        "message": "Bienvenue sur l'API!",
        "endpoints": {
            "token_obtain": "/api/token/",
            "token_refresh": "/api/token/refresh/",
            "notifications": "/api/notifications/",
            # Ajoutez d'autres endpoints que vous avez ici
        }
    })








User = get_user_model()

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of a profile or admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow admins to edit any user
        if request.user.is_superuser:
            return True
        # Allow users to edit their own profile
        return obj.id == request.user.id

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdmin]

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied("You do not have permission to perform this action.")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        password = request.data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)





# Ajoutez ces imports au début du fichier
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



# modifier mdp
class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(old_password):
                return Response({'detail': 'Ancien mot de passe incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Mot de passe changé avec succès.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    





# class MyTokenObtainPairView(TokenObtainPairView):
#      authentication_classes = [] 
#      serializer_class = MyTokenObtainPairSerializer

# from .models import Report, Projet ,Notification,Rapport,Validation,Archive
# from .serializer import MyTokenObtainPairSerializer, RegisterSerializer, ReportSerializer, UserSerializer, ProjetSerializer, NotificationSerializer,RapportSerializer, ValidationSerializer, NotificationSerializer, ArchiveSerializer

# import json

# ViewSet for handling User operations (Admin access only)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

@api_view(['GET'])
def getRoutes(request):
    """Get available API routes."""
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/',
        '/api/test/',
        '/api/logout/',
        '/api/reports/',
        '/api/users/',
        '/api/projets/',
        '/api/notifications/',
        '/api/notifications/<int:pk>/',
        '/api/rapports/',
        '/api/validations/',
        '/api/archives/',
    ]
    return Response(routes)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    """Test endpoint for GET and POST requests."""
    if request.method == 'GET':
        return Response({'response': f"Congratulations {request.user}, your API just responded to GET request"}, status=status.HTTP_200_OK)


    # Handling POST request
    data = request.data
    if request.method == 'POST':
        text = data.get('text')
        if text is None:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

        response_data = f'Congratulations, your API just responded to POST request with text: {text}'
        return Response({'response': response_data}, status=status.HTTP_200_OK)


    
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            text = data.get('text')
            if text is None:
                return Response({"error": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)
            response_data = f'Congratulations, your API just responded to POST request with text: {text}'
            return Response({'response': response_data}, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)


    return Response({"error": "Invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):


    refresh_token = request.data.get('refresh')
    if not refresh_token:
        return Response({"error": "No refresh token provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"detail": "Successfully logged out"}, status=status.HTTP_204_NO_CONTENT)
    except TokenError:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])

@permission_classes([IsAuthenticated])
def create_rapport(request):
    """Create a rapport associated with the authenticated user."""
    data = request.data.copy()
    data['user'] = request.user.id  # Associate the logged-in user
    serializer = RapportSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def create_rapport(request):
    if request.method == 'POST':
        data = request.data.copy()
        data['user'] = request.user.id  # Ajoute l'utilisateur connecté
        serializer = RapportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    








# dashboard admin rapport
# views.py




class RapportStatsView(APIView):
    def get(self, request, *args, **kwargs):
        # Compter les rapports pour chaque statut
        count_statut_0 = Rapport.objects.filter(statut=0).count()
        count_statut_1 = Rapport.objects.filter(statut=1).count()
        count_statut_2 = Rapport.objects.filter(statut=2).count()
        
        # Compter tous les rapports
        total_count = Rapport.objects.count()

        # Retourner les résultats sous forme de JSON
        return Response({
            'statut_0': count_statut_0,
            'statut_1': count_statut_1,
            'statut_2': count_statut_2,
            'total_count': total_count
        }, status=status.HTTP_200_OK)


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # Return the current user




# Vue pour récupérer, mettre à jour ou supprimer une notification spécifique

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtrer les notifications pour l'utilisateur connecté
        return self.queryset.filter(user=self.request.user)

    # Action pour marquer une notification comme lue
    @action(detail=True, methods=['post'], url_path='mark-as-read')
    def mark_as_read(self, request, pk=None):
        try:
            notification = self.get_object()
            notification.is_read = True
            notification.save()
            return Response({'status': 'notification marked as read'}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)







class RapportViewSet(viewsets.ModelViewSet):
    queryset = Rapport.objects.all()
    serializer_class = RapportSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='par-date')
    def par_date(self, request):
        rapports = self.queryset.filter(statut=2).order_by('-date_creation')
        serializer = self.get_serializer(rapports, many=True)
        return Response(serializer.data)
    


class MonthlyReportCountView(APIView):
       
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Calculate the date from 12 months ago
        twelve_months_ago = timezone.now() - timezone.timedelta(days=365)

        # Query to get the total reports grouped by month
        report_counts = (
            Rapport.objects.filter(date_creation__gte=twelve_months_ago)  # Filter for last 12 months
            .annotate(month=TruncMonth('date_creation'))  # Group by month
            .values('month')  # Select month
            .annotate(total_reports=Count('id'))  # Count total reports
            .order_by('month')  # Order by month
        )

        # Prepare the response data
        report_data = {
            report['month'].strftime('%Y-%m'): report['total_reports'] for report in report_counts
        }

        return JsonResponse(report_data)
    


class RapportStatutCountView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Group by statut and count the number of reports
        queryset = Rapport.objects.filter(statut__in=[0, 1, 2]).values('statut').annotate(nombre_rapports=Count('id'))

        # Serialize the data
        serializer = StatutCountSerializer(queryset, many=True)

        return Response(serializer.data)