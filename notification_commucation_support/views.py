from .models import Notification, Message, SupportTicket
from .serializers import NotificationSerializer, MessageSerializer, SupportTicketSerializer
from MBP.views import ProtectedModelViewSet


class NotificationViewSet(ProtectedModelViewSet):
    queryset = Notification.objects.select_related("user").all()
    serializer_class = NotificationSerializer
    model_name = "Notification"
    lookup_field = "slug"


class MessageViewSet(ProtectedModelViewSet):
    queryset = Message.objects.select_related("sender", "receiver").all()
    serializer_class = MessageSerializer
    model_name = "Message"
    lookup_field = "slug"


class SupportTicketViewSet(ProtectedModelViewSet):
    queryset = SupportTicket.objects.select_related("user").all()
    serializer_class = SupportTicketSerializer
    model_name = "SupportTicket"
    lookup_field = "slug"
