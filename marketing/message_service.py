from datetime import datetime


class MessageService:
    """Service pour générer des messages chic"""

    @staticmethod
    def get_payment_link_message(transaction):
        """Message pour le lien de paiement"""

        message = f"""✨ OCALM - Paiement sécurisé ✨

Cher client,

Vous avez reçu une demande de paiement sécurisé via OCALM.

💎 DÉTAIL DE LA TRANSACTION :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Article      : {transaction.listing_title}
💰 Montant      : {transaction.amount:,.0f} FCFA
🔖 Frais (1%)   : {transaction.fee:,.0f} FCFA
🚚 Livraison    : {transaction.delivery_fee:,.0f} FCFA
💎 TOTAL        : {transaction.total:,.0f} FCFA
📝 Référence    : {transaction.reference}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔒 PROTECTION ESCROW
Votre paiement sera bloqué en toute sécurité.
Il ne sera débloqué qu'à la réception de votre colis.

📍 LIEN DE PAIEMENT SÉCURISÉ :
👉 {transaction.payment_link}

💬 BESOIN D'AIDE ?
Notre service conciergerie est à votre disposition :
📱 WhatsApp : +225 07 89 78 29 21
📧 Email : support@ocalm.com

✨ Paiement sécurisé - Livraison garantie ✨

L'élégance de la sécurité,
L'équipe OCALM"""

        return message

    @staticmethod
    def get_payment_confirmation_message(transaction):
        """Message après confirmation de paiement"""

        message = f"""✅ PAIEMENT CONFIRMÉ - OCALM ✅

Cher client,

Nous avons le plaisir de vous confirmer que votre paiement a été validé avec succès.

💎 RÉCAPITULATIF :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Article      : {transaction.listing_title}
💰 Montant      : {transaction.amount:,.0f} FCFA
💎 Total payé   : {transaction.total:,.0f} FCFA
📝 Référence    : {transaction.reference}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔒 SÉCURISATION ACTIVE
✓ Fonds bloqués en toute sécurité
✓ Vendeur notifié
✓ Préparation de la commande

📍 PROCHAINES ÉTAPES :
1. Le vendeur prépare votre colis
2. Vous recevrez un lien de suivi GPS
3. Validation à la livraison

💎 CODE OTP DE LIVRAISON : {transaction.delivery_otp}
(À conserver précieusement)

✨ Merci pour votre confiance ✨

L'équipe OCALM
support@ocalm.com | +225 07 89 78 29 21"""

        return message

    @staticmethod
    def get_shipping_confirmation_message(transaction):
        """Message après expédition du colis"""

        message = f"""🚚 COLIS EXPÉDIÉ - OCALM 🚚

Cher client,

Bonne nouvelle ! Votre colis a été expédié par le vendeur.

📍 SUIVI EN TEMPS RÉEL :
👉 http://127.0.0.1:8000/tracking/{transaction.id}

📦 INFORMATIONS DE LIVRAISON :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Référence    : {transaction.reference}
🚚 Transporteur : OCALM Delivery
📍 Ville        : {transaction.pickup_city}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔔 LIVRAISON PRÉVUE :
Sous 48h maximum

💎 CODE OTP : {transaction.delivery_otp}
(À donner au livreur à la réception)

📍 Suivez votre colis en direct sur la carte GPS.

✨ Votre colis arrive bientôt ! ✨

L'équipe OCALM"""

        return message

    @staticmethod
    def get_delivery_confirmation_message(transaction):
        """Message après confirmation de livraison"""

        message = f"""🎁 LIVRAISON CONFIRMÉE - OCALM 🎁

Cher client,

Félicitations ! Votre commande a été livrée avec succès.

✅ LIVRAISON COMPLÉTÉE :
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Article      : {transaction.listing_title}
💰 Montant      : {transaction.amount:,.0f} FCFA
📝 Référence    : {transaction.reference}
📅 Date livraison : {datetime.now().strftime('%d/%m/%Y à %H:%M')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⭐ NOTEZ LE VENDEUR :
Votre avis compte ! Évaluez cette transaction :
👉 http://127.0.0.1:8000/rate/{transaction.id}

💎 Merci d'avoir choisi OCALM 💎

À très bientôt pour vos prochains achats !

L'élégance de la sécurité,
L'équipe OCALM ✨"""

        return message

    @staticmethod
    def get_whatsapp_payment_link(transaction):
        """Lien WhatsApp avec message chic"""
        message = MessageService.get_payment_link_message(transaction)
        return f"https://wa.me/?text={message.replace(' ', '%20')}"

    @staticmethod
    def get_whatsapp_payment_confirmation(transaction):
        """Lien WhatsApp après paiement"""
        message = MessageService.get_payment_confirmation_message(transaction)
        return f"https://wa.me/?text={message.replace(' ', '%20')}"