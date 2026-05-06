from django.urls import path
from . import views

app_name = 'escrow'

urlpatterns = [
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transaction/<str:transaction_id>/', views.transaction_detail, name='transaction_detail'),
    path('create/', views.create_transaction, name='create_transaction'),
]