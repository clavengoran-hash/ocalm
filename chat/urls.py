from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('rooms/', views.chat_rooms, name='chat_rooms'),
    path('room/<str:room_id>/', views.chat_room, name='chat_room'),
    path('send/<str:room_id>/', views.send_message, name='send_message'),
    path('unread-count/', views.unread_count, name='unread_count'),
]