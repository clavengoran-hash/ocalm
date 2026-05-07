from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from pages import views  # Assurez-vous d'importer views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Pages principales
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('terms/', views.terms_view, name='terms'),
    
    # Authentification
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard et fonctionnalités
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('listings/', views.listings_view, name='listings'),
    path('listing/<str:listing_id>/', views.listing_detail_view, name='listing_detail'),
    path('wallet/', views.wallet_view, name='wallet'),
]

# Pour les fichiers media/static en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
