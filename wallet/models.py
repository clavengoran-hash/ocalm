from django.db import models


class Wallet(models.Model):
    user_name = models.CharField(max_length=150, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_name}: {self.balance} FCFA"