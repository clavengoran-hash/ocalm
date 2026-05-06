import uuid
from django.db import models
from django.utils import timezone


class PromoCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller_name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)
    discount = models.IntegerField()  # Pourcentage
    used_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.discount}%"


class SocialAccount(models.Model):
    PLATFORM_CHOICES = (
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'),
        ('twitter', 'Twitter'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller_name = models.CharField(max_length=150)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    access_token = models.TextField(blank=True, null=True)
    page_id = models.CharField(max_length=100, blank=True, null=True)
    page_name = models.CharField(max_length=200, blank=True, null=True)
    is_connected = models.BooleanField(default=False)
    connected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seller_name} - {self.platform}"


class LiveStream(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Brouillon'),
        ('scheduled', 'Programmé'),
        ('live', 'En direct'),
        ('ended', 'Terminé'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller_name = models.CharField(max_length=150)
    title = models.CharField(max_length=200)
    description = models.TextField()
    platform = models.CharField(max_length=20, choices=SocialAccount.PLATFORM_CHOICES)
    live_url = models.URLField(blank=True, null=True)
    scheduled_time = models.DateTimeField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    viewers_count = models.IntegerField(default=0)
    whatsapp_group_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.status}"


class LiveComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    live = models.ForeignKey(LiveStream, on_delete=models.CASCADE, related_name='comments')
    user_name = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name}: {self.message[:50]}"


class SocialPost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller_name = models.CharField(max_length=150)
    listing_id = models.CharField(max_length=100)
    platform = models.CharField(max_length=20, choices=SocialAccount.PLATFORM_CHOICES)
    post_id = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    likes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seller_name} - {self.platform}"