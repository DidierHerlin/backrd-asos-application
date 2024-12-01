from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RegisterView, UserViewSet
from .views import ChangePasswordView,RapportStatsView,UserDetailView,NotificationViewSet,RapportViewSet,MonthlyReportCountView,RapportStatutCountView

# Créez un router
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'notifications', NotificationViewSet)
router.register(r'rapports', RapportViewSet, basename='rapport')
# URLs
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('rapports/stats/', RapportStatsView.as_view(), name='rapport-stats'),
    path('users/me/', UserDetailView.as_view(), name='user-detail'),
    path('rapports/monthly-count/', MonthlyReportCountView.as_view(), name='monthly-report-count'),
    path('rapports/statut-count/', RapportStatutCountView.as_view(), name='rapport-statut-count'),
  

    
    path('', include(router.urls)),  # Utilisez le router pour les ViewSet


]

