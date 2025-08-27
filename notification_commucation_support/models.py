import uuid
from django.db import models
from django.utils.text import slugify
from accounts.models import User


class Notification(models.Model):
    TYPE_ORDER = "order"
    TYPE_PROMOTION = "promotion"
    TYPE_SYSTEM = "system"
    TYPE_SUPPORT = "support"

    TYPE_CHOICES = [
        (TYPE_ORDER, "Order"),
        (TYPE_PROMOTION, "Promotion"),
        (TYPE_SYSTEM, "System"),
        (TYPE_SUPPORT, "Support"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default=TYPE_SYSTEM)
    slug = models.SlugField(unique=True, blank=True)
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.user.email}-{self.type}-{uuid.uuid4().hex[:6]}")
            slug = base_slug
            while Notification.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{uuid.uuid4().hex[:4]}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Notification: {self.title} → {self.user.email}"

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    subject = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.sender.email}-to-{self.receiver.email}-{uuid.uuid4().hex[:6]}")
            slug = base_slug
            while Message.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{uuid.uuid4().hex[:4]}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Message from {self.sender.email} to {self.receiver.email}"

class SupportTicket(models.Model):
    STATUS_OPEN = "open"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_RESOLVED = "resolved"
    STATUS_CLOSED = "closed"

    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_RESOLVED, "Resolved"),
        (STATUS_CLOSED, "Closed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="support_tickets")
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)
    slug = models.SlugField(unique=True, blank=True)
    priority = models.CharField(
        max_length=20,
        choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
        default="medium"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Support Ticket"
        verbose_name_plural = "Support Tickets"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"ticket-{self.user.email}-{uuid.uuid4().hex[:6]}")
            slug = base_slug
            while SupportTicket.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{uuid.uuid4().hex[:4]}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ticket {self.subject} ({self.status})"
