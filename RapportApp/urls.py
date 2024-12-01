from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RapportViewSet
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .drive_service import upload_file

# Initialisation du router
router = DefaultRouter()
router.register(r'rapports', RapportViewSet, basename='rapport')

# Définition des URLs
urlpatterns = [
    # Enregistrer les vues du ViewSet dans le router
    path('', include(router.urls)),
    
    # Visualisation d'un rapport spécifique
    path('api/RapportApp/rapports/<int:pk>/visualiser/', views.RapportViewSet.as_view({'get': 'visualiser'}), name='visualiser_rapport'),
    
    # Upload de fichier (si nécessaire)
    path('upload/', upload_file, name='upload_file'),
    
    # Route pour obtenir les rapports d'un utilisateur
    path('api/RapportApp/rapports/user-reports/<int:user_id>/', views.RapportViewSet.as_view({'get': 'user_reports'}), name='rapports-par-utilisateur'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
