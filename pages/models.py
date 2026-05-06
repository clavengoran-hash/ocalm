from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class PageView(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    page = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # loyalty/models.py
    class LoyaltyPoints(models.Model):
        user_name = models.CharField(max_length=150, unique=True)
        points = models.IntegerField(default=0)
        level = models.CharField(max_length=50, default='Bronze')
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def get_next_level(self):
            if self.points < 1000:
                return {'level': 'Argent', 'points_needed': 1000 - self.points}
            elif self.points < 5000:
                return {'level': 'Or', 'points_needed': 5000 - self.points}
            elif self.points < 10000:
                return {'level': 'Platine', 'points_needed': 10000 - self.points}
            return {'level': 'Diamant', 'points_needed': 0}

    # cashback/models.py
    class CashbackTransaction(models.Model):
        STATUS_CHOICES = (
            ('pending', 'En attente'),
            ('completed', 'Validé'),
            ('used', 'Utilisé'),
            ('expired', 'Expiré'),
        )

        id = models.UUIDField(primary_key=True, default=uuid.uuid4)
        user_name = models.CharField(max_length=150)
        transaction_id = models.CharField(max_length=100)
        amount = models.DecimalField(max_digits=12, decimal_places=0)
        cashback_rate = models.IntegerField(default=5)  # 5% de cashback
        cashback_amount = models.DecimalField(max_digits=12, decimal_places=0)
        status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
        expires_at = models.DateTimeField()
        created_at = models.DateTimeField(auto_now_add=True)

    # notifications/models.py
    class PriceDropNotification(models.Model):
        user_name = models.CharField(max_length=150)
        listing_id = models.CharField(max_length=100)
        old_price = models.DecimalField(max_digits=12, decimal_places=0)
        new_price = models.DecimalField(max_digits=12, decimal_places=0)
        is_read = models.BooleanField(default=False)
        created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.page} - {self.created_at}"