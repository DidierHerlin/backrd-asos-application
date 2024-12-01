from django.urls import path
from .views import NotificationListCreateView  # Update the import here

urlpatterns = [
    path('notifications/', NotificationListCreateView.as_view(), name='notification-list-create'),
]
