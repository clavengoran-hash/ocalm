from django.contrib import admin
from .models import PromoCode, SocialAccount, LiveStream, LiveComment, SocialPost

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'seller_name', 'discount', 'used_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'seller_name')
    search_fields = ('code', 'seller_name')

@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ('seller_name', 'platform', 'is_connected', 'connected_at')
    list_filter = ('platform', 'is_connected')

@admin.register(LiveStream)
class LiveStreamAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller_name', 'platform', 'status', 'scheduled_time')
    list_filter = ('status', 'platform')

@admin.register(LiveComment)
class LiveCommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'live', 'message', 'created_at')

@admin.register(SocialPost)
class SocialPostAdmin(admin.ModelAdmin):
    list_display = ('seller_name', 'platform', 'listing_id', 'created_at')