import uuid
from django.db import models


class Listing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller_name = models.CharField(max_length=150)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=0)
    delivery_fee = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    image = models.ImageField(upload_to='listings/', blank=True, null=True)
    stock_quantity = models.IntegerField(default=1)  # ← Ajouté
    is_available = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.price} FCFA"