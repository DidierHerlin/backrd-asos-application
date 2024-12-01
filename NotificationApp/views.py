from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializer import NotificationSerializer


class NotificationListCreateView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
