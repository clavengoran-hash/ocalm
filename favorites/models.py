from django.db import models
import uuid


class Favorite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=150)
    listing_id = models.CharField(max_length=100)
    listing_title = models.CharField(max_length=200)
    listing_price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user_name', 'listing_id']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user_name} ❤️ {self.listing_title}"