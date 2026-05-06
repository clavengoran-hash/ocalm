import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocalm.settings')
django.setup()

from accounts.models import User
from wallet.models import Wallet

# Ajouter 10000 FCFA à tous les vendeurs
print("=== AJOUT D'ARGENT AUX PORTEFEUILLES ===")
for user in User.objects.all():
    wallet, created = Wallet.objects.get_or_create(user_name=user.username, defaults={'balance': 0})
    if wallet.balance < 5000:
        wallet.balance = 10000
        wallet.save()
        print(f"✅ {user.username} - Nouveau solde: {wallet.balance} FCFA")
    else:
        print(f"📌 {user.username} - Solde actuel: {wallet.balance} FCFA")

print("\n🎉 Tous les portefeuilles ont été crédités de 10000 FCFA !")