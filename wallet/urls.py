from django.urls import path
from . import views

app_name = 'wallet'

urlpatterns = [
    path('', views.wallet_detail, name='wallet_detail'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
]