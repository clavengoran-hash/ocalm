import uuid
import random
from django.db import models
from django.utils import timezone


class EscrowTransaction(models.Model):
    DELIVERY_COMPANIES = (
        ('avs', 'AVS TRANSPORT'),
        ('utb', 'UTB'),
        ('tsr', 'TSR'),
        ('sbta', 'SBTA'),
        ('ocalm', '🚴 Livreur OCALM'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=50, unique=True, editable=False)

    # Informations vendeur
    seller_name = models.CharField(max_length=150)

    # Informations acheteur
    buyer_name = models.CharField(max_length=150)
    buyer_first_name = models.CharField(max_length=100, blank=True, null=True)
    buyer_last_name = models.CharField(max_length=100, blank=True, null=True)
    buyer_phone = models.CharField(max_length=20, blank=True, null=True)
    buyer_email = models.CharField(max_length=200, blank=True, null=True)
    buyer_city = models.CharField(max_length=100, blank=True, null=True)

    # Informations produit
    listing_id = models.CharField(max_length=100)
    listing_title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    fee = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    delivery_fee = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=0)

    # Livraison
    delivery_address = models.TextField(blank=True, null=True)
    delivery_company = models.CharField(max_length=20, choices=DELIVERY_COMPANIES, blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)

    # Paiement
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    payment_verified = models.BooleanField(default=False)

    # Code OTP
    delivery_otp = models.CharField(max_length=6, blank=True, null=True)
    otp_attempts = models.IntegerField(default=0)
    otp_validated_at = models.DateTimeField(blank=True, null=True)

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    shipped_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = f"OCALM{random.randint(10000000, 99999999)}"
        if not self.delivery_otp:
            self.delivery_otp = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)

    def validate_otp(self, otp_code):
        if self.otp_attempts >= 5:
            return False, "Trop de tentatives. Contactez le support."

        self.otp_attempts += 1
        self.save()

        if self.delivery_otp == otp_code:
            self.otp_validated_at = timezone.now()
            self.completed_at = timezone.now()
            self.save()

            from wallet.models import Wallet
            wallet, _ = Wallet.objects.get_or_create(user_name=self.seller_name, defaults={'balance': 0})
            wallet.balance += float(self.amount)
            wallet.save()

            return True, "✅ Livraison confirmée ! Argent débloqué."

        return False, f"Code incorrect. Plus que {5 - self.otp_attempts} tentatives."

    def __str__(self):
        return f"{self.reference} - {self.listing_title}"