from django.db import models
import uuid


class DeliveryTracking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_id = models.CharField(max_length=100)
    driver_name = models.CharField(max_length=150, blank=True, null=True)
    customer_name = models.CharField(max_length=150, blank=True, null=True)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    pickup_city = models.CharField(max_length=100, blank=True, null=True)
    delivery_city = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default='pending')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Delivery {self.transaction_id} - {self.status}"