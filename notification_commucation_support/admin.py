from django.contrib import admin
from .models import Notification, Message, SupportTicket


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "type", "is_read", "created_at")
    list_filter = ("type", "is_read", "created_at")
    search_fields = ("title", "message", "user__email")
    readonly_fields = ("slug", "created_at")
    ordering = ("-created_at",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "sender", "receiver", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("subject", "body", "sender__email", "receiver__email")
    readonly_fields = ("slug", "created_at")
    ordering = ("-created_at",)


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ("subject", "user", "status", "priority", "created_at", "updated_at")
    list_filter = ("status", "priority", "created_at")
    search_fields = ("subject", "description", "user__email")
    readonly_fields = ("slug", "created_at", "updated_at")
    ordering = ("-created_at",)
