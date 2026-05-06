from django.contrib import admin
from .models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller_name', 'price', 'is_available', 'created_at')
    list_filter = ('is_available', 'created_at')
    search_fields = ('title', 'seller_name')