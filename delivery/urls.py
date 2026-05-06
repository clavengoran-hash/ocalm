from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    path('dashboard/', views.delivery_dashboard, name='delivery_dashboard'),
    path('take/<int:delivery_id>/', views.take_delivery, name='take_delivery'),
    path('track/<str:transaction_id>/', views.track_delivery, name='track_delivery'),
]