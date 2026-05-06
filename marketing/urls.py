from django.urls import path
from . import views

app_name = 'marketing'

urlpatterns = [
    path('dashboard/', views.marketing_dashboard, name='marketing_dashboard'),
    path('share/<str:listing_id>/', views.share_listing, name='share_listing'),
]