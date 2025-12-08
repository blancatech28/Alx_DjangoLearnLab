from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer

def create_notification(actor, recipient, verb, target=None):
    if actor != recipient:  # avoid notifying self
        Notification.objects.create(actor=actor, recipient=recipient, verb=verb, target=target)

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')
