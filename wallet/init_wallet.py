# init_wallet.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocalm.settings')
django.setup()

from wallet.models import Wallet
from accounts.models import User

# Mettre 10000 FCFA à tous les vendeurs
users = User.objects.filter(role='seller')
for user in users:
    wallet, created = Wallet.objects.get_or_create(user_name=user.username)
    wallet.balance = 10000
    wallet.save()
    print(f"✅ {user.username}: {wallet.balance} FCFA")

print("Terminé !")