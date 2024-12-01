from django.shortcuts import render
from rest_framework import  viewsets
from rest_framework.permissions import  IsAuthenticated
from .models import Archive
from .serializer import ArchiveSerializer

# Create your views here.
class ArchiveViewSet(viewsets.ModelViewSet):
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer
    permission_classes = [IsAuthenticated]