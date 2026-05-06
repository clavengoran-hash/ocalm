from django.urls import path
from . import views

app_name = 'favorites'

urlpatterns = [
    path('', views.favorites_list, name='favorites_list'),
    path('add/<str:listing_id>/', views.add_favorite, name='add_favorite'),
    path('remove/<str:listing_id>/', views.remove_favorite, name='remove_favorite'),
]