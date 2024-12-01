from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    """
    Permet l'accès uniquement si l'utilisateur est l'administrateur ou le propriétaire du compte.
    """
    def has_object_permission(self, request, view, obj):
        # Autoriser si l'utilisateur est administrateur ou s'il modifie son propre compte
        return request.user.is_superuser or obj == request.user
