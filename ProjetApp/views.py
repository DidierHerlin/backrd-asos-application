from rest_framework import  viewsets
from .serializer import ProjetSerializer
from rest_framework.permissions import  IsAuthenticated
from .models import  Projet 

# Create your views here.

class ProjetViewSet(viewsets.ModelViewSet):
    queryset = Projet.objects.all()
    serializer_class = ProjetSerializer
    permission_classes = [IsAuthenticated]
