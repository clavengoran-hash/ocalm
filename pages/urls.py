from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('listings/', views.listings_view, name='listings'),
    path('listing/<str:listing_id>/', views.listing_detail_view, name='listing_detail'),
    path('wallet/', views.wallet_view, name='wallet'),
]
