# chat/models.py
from django.db import models
from django.contrib.auth.models import User
import uuid


class Visitor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Visitor: {self.name or self.email or self.id}"


class Agent(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="agent_profile"
    )
    is_online = models.BooleanField(default=False)
    display_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Agent: {self.user.username}"

    @property
    def name(self):
        return self.display_name or self.user.get_full_name() or self.user.username


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    visitor = models.ForeignKey(
        Visitor, on_delete=models.CASCADE, related_name="conversations"
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_conversations",
    )

    # Chat state
    STATUS_CHOICES = [
        ("active", "Active"),
        ("waiting", "Waiting"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="waiting")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_message_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation: {self.visitor} with {self.assigned_to or 'Unassigned'}"

    @property
    def unread_count(self):
        """
        Count the number of unread messages from the customer in this conversation
        """
        return self.messages.filter(read=False, is_from_customer=True).count()


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )

    # Content
    content = models.TextField()

    # Sender info
    is_from_customer = models.BooleanField(default=True)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_messages",
    )

    # Message metadata
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        sender = (
            "Customer"
            if self.is_from_customer
            else self.author.get_full_name() or self.author.username
        )
        return f"{sender}: {self.content[:50]}"

    class Meta:
        ordering = ["timestamp"]
