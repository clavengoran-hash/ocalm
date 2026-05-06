from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from decimal import Decimal
from .models import EscrowTransaction
from .serializers import (
    EscrowTransactionSerializer, 
    CreateTransactionSerializer,
    UploadShippingPhotosSerializer,
    ValidateDeliverySerializer
)

class EscrowViewSet(viewsets.ModelViewSet):
    serializer_class = EscrowTransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'buyer':
            return EscrowTransaction.objects.filter(buyer=user)
        elif user.role == 'seller':
            return EscrowTransaction.objects.filter(seller=user)
        elif user.role == 'delivery':
            return EscrowTransaction.objects.filter(delivery_person=user)
        return EscrowTransaction.objects.all()
    
    @action(detail=False, methods=['post'])
    def create_transaction(self, request):
        serializer = CreateTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        listing = serializer.validated_data['listing_id']
        
        # Vérifier la limite du vendeur
        seller_limit = listing.seller.get_seller_limit()
        if listing.price > seller_limit:
            return Response({
                'error': f'Ce vendeur ne peut pas vendre plus de {seller_limit} FCFA'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculer les frais
        escrow_fee = listing.price * Decimal('0.005')
        total_amount = listing.price + escrow_fee + listing.delivery_fee
        
        # Créer la transaction
        transaction = EscrowTransaction.objects.create(
            buyer=request.user,
            seller=listing.seller,
            amount=listing.price,
            escrow_fee=escrow_fee,
            delivery_fee=listing.delivery_fee,
            total_amount=total_amount,
            payment_method=serializer.validated_data['payment_method'],
            status='pending_payment'
        )
        
        # Générer OTP pour la livraison
        import random
        transaction.delivery_otp = f"{random.randint(100000, 999999)}"
        transaction.save()
        
        return Response({
            'transaction': EscrowTransactionSerializer(transaction).data,
            'message': 'Transaction créée avec succès',
            'payment_instructions': {
                'amount': str(total_amount),
                'phone': request.user.phone_number,
                'reference': transaction.reference
            }
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def confirm_payment(self, request, pk=None):
        transaction = self.get_object()
        
        if transaction.buyer != request.user:
            return Response({'error': 'Non autorisé'}, status=status.HTTP_403_FORBIDDEN)
        
        if transaction.status != 'pending_payment':
            return Response({'error': 'Transaction déjà traitée'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Simuler la vérification du paiement
        transaction.status = 'funds_held'
        transaction.escrow_held_at = timezone.now()
        transaction.payment_verified_at = timezone.now()
        transaction.save()
        
        return Response({
            'message': '✅ Paiement confirmé ! Fonds bloqués en toute sécurité.',
            'transaction': EscrowTransactionSerializer(transaction).data,
            'next_step': 'Le vendeur doit uploader les photos d\'expédition'
        })
    
    @action(detail=True, methods=['post'])
    def upload_shipping_photos(self, request, pk=None):
        transaction = self.get_object()
        
        if transaction.seller != request.user:
            return Response({'error': 'Seul le vendeur peut uploader les photos'},
                          status=status.HTTP_403_FORBIDDEN)
        
        if not transaction.can_upload_shipping_photos():
            return Response({'error': 'Délai de 12h dépassé !'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UploadShippingPhotosSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        photos = serializer.validated_data['photos']
        
        # Simuler l'upload des photos
        photo_urls = []
        for i, photo in enumerate(photos):
            photo_urls.append(f"/media/shipping/{transaction.reference}_{i}.jpg")
        
        transaction.shipping_photos = photo_urls
        transaction.shipping_photos_taken_at = timezone.now()
        transaction.status = 'shipping'
        transaction.save()
        
        return Response({
            'message': f'✅ {len(photos)} photos uploadées avec succès',
            'photos': photo_urls,
            'transaction': EscrowTransactionSerializer(transaction).data
        })
    
    @action(detail=True, methods=['post'])
    def confirm_delivery(self, request, pk=None):
        transaction = self.get_object()
        
        # L'acheteur ou le livreur peut confirmer
        if transaction.buyer != request.user and transaction.delivery_person != request.user:
            return Response({'error': 'Seul l\'acheteur ou le livreur peut confirmer'},
                          status=status.HTTP_403_FORBIDDEN)
        
        serializer = ValidateDeliverySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        method = serializer.validated_data['method']
        code = serializer.validated_data['code']
        
        if method == 'otp' and code == transaction.delivery_otp:
            transaction.delivery_time = timezone.now()
            transaction.validated_at = timezone.now()
            transaction.save()
            transaction.release_funds_to_seller()
            
            return Response({
                'message': '✅ Livraison confirmée ! Fonds libérés au vendeur',
                'transaction': EscrowTransactionSerializer(transaction).data
            })
        else:
            return Response({'error': 'Code OTP invalide'}, 
                          status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def tracking(self, request, pk=None):
        transaction = self.get_object()
        return Response({
            'status': transaction.status,
            'reference': transaction.reference,
            'amount': transaction.amount,
            'created_at': transaction.created_at,
            'funds_held_at': transaction.escrow_held_at,
            'shipping_photos_count': len(transaction.shipping_photos),
            'delivery_time': transaction.delivery_time,
            'delivery_otp': transaction.delivery_otp if transaction.delivery_person == request.user else None
        })
