from rest_framework import serializers
from .models import Notification, Message, SupportTicket


class NotificationSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id", "slug", "user", "user_email", "title", "message", "type",
            "is_read", "created_at"
        ]
        read_only_fields = ("id", "slug", "created_at")

    def validate(self, data):
        # Ensure title and message are not empty
        if not data.get("title") or not data.get("message"):
            raise serializers.ValidationError("Both title and message are required.")
        return data


class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source="sender.email", read_only=True)
    receiver_email = serializers.EmailField(source="receiver.email", read_only=True)

    class Meta:
        model = Message
        fields = [
            "id", "slug", "sender", "sender_email", "receiver", "receiver_email",
            "subject", "body", "is_read", "created_at"
        ]
        read_only_fields = ("id", "slug", "created_at")

    def validate(self, data):
        sender = data.get("sender")
        receiver = data.get("receiver")

        if sender == receiver:
            raise serializers.ValidationError("Sender and receiver cannot be the same user.")
        return data


class SupportTicketSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = SupportTicket
        fields = [
            "id", "slug", "user", "user_email", "subject", "description",
            "status", "priority", "created_at", "updated_at"
        ]
        read_only_fields = ("id", "slug", "created_at", "updated_at")

    def validate(self, data):
        if len(data.get("subject", "")) < 5:
            raise serializers.ValidationError("Subject must be at least 5 characters long.")
        if len(data.get("description", "")) < 10:
            raise serializers.ValidationError("Description must be at least 10 characters long.")
        return data
