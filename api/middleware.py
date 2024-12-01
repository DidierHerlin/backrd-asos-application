# backend/middleware/permissions_middleware.py

from django.http import JsonResponse
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin

class RoleBasedAccessMiddleware(MiddlewareMixin):
    """
    Middleware pour restreindre l'accès basé sur le rôle de l'utilisateur.
    - Si user = 0, l'utilisateur ne peut que créer des rapports.
    - Si l'utilisateur est admin (is_superuser), il peut accéder à toutes les pages et modifier les rapports.
    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        user = request.user
        
        # Si l'utilisateur n'est pas authentifié, on n'applique pas le middleware
        if not user.is_authenticated:
            return None
        
        # Récupère le nom de la vue en cours d'exécution
        current_view_name = resolve(request.path_info).url_name
        
        # Si l'utilisateur est un simple user (user = 0)
        if not user.is_superuser:
            if request.method in ['PUT', 'PATCH', 'DELETE']:
                return JsonResponse({'error': 'Permission denied: Only admin can modify or delete reports.'}, status=403)
            
            # Limiter l'accès à certaines pages spécifiques pour les utilisateurs simples
            restricted_views = ['rapport_update', 'rapport_delete']  # Liste des vues interdites
            if current_view_name in restricted_views:
                return JsonResponse({'error': 'Permission denied: Access restricted to admin users.'}, status=403)

        # Admin (is_superuser) peut tout faire
        return None
