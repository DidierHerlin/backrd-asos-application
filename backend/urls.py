from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.views import api_root_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root_view, name='api-root'),  # Vue de racine de l'API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('api.urls')),  # Incluez vos routes d'API
    path('api/RapportApp/', include('RapportApp.urls')),
    path('api/ProjetApp/', include('ProjetApp.urls')),
    path('api/ArchiveApp/', include('ArchiveApp.urls')),
    path('api/NotificationApp/', include('NotificationApp.urls')),
    path('api/GoocleDriveApi',include('GoocleDriveApi.urls')),

    path('api/', include('api.urls')),
]

if settings.DEBUG:  # Assurez-vous que cela est activé uniquement en mode développement
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
