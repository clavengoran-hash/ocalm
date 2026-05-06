from rest_framework import serializers
from .models import EscrowTransaction
from listings.models import Listing

class EscrowTransactionSerializer(serializers.ModelSerializer):
    buyer_name = serializers.CharField(source='buyer.username', read_only=True)
    seller_name = serializers.CharField(source='seller.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = EscrowTransaction
        fields = '__all__'
        read_only_fields = ['id', 'reference', 'created_at', 'updated_at']

class CreateTransactionSerializer(serializers.Serializer):
    listing_id = serializers.UUIDField()
    payment_method = serializers.ChoiceField(choices=['wave', 'orange_money', 'mtn_momo'])
    
    def validate_listing_id(self, value):
        try:
            listing = Listing.objects.get(id=value, is_available=True)
            return listing
        except Listing.DoesNotExist:
            raise serializers.ValidationError("Annonce non trouvée ou indisponible")

class UploadShippingPhotosSerializer(serializers.Serializer):
    photos = serializers.ListField(
        child=serializers.ImageField(),
        min_length=3,
        max_length=10
    )
    gps_coordinates = serializers.CharField(required=False, allow_blank=True)

class ValidateDeliverySerializer(serializers.Serializer):
    method = serializers.ChoiceField(choices=['qr', 'otp'])
    code = serializers.CharField(max_length=10)
