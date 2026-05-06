from django.contrib import admin
from .models import Favorite

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'listing_title', 'listing_price', 'created_at']
    search_fields = ['user_name', 'listing_title']
    list_filter = ['created_at']