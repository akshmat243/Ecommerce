from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, MessageViewSet, SupportTicketViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r"notifications", NotificationViewSet, basename="notification")
router.register(r"messages", MessageViewSet, basename="message")
router.register(r"support-tickets", SupportTicketViewSet, basename="supportticket")

urlpatterns = [
    path('api/', include(router.urls)),
]
