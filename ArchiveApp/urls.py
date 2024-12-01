from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArchiveViewSet

# Créer une instance de DefaultRouter
router = DefaultRouter()
# Enregistrer le viewset pour les archives avec un basename
router.register(r'archives', ArchiveViewSet, basename='archive')

# Définir les URL patterns
urlpatterns = [
    path('', include(router.urls)),  # Inclure les URL générées par le router
]
