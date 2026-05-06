from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import ChatRoom, ChatMessage
import json


@login_required
def chat_rooms(request):
    """Liste des conversations du vendeur ou de l'acheteur"""
    rooms = ChatRoom.objects.filter(
        buyer_name=request.user.username
    ) | ChatRoom.objects.filter(
        seller_name=request.user.username
    )

    # Compter les messages non lus
    for room in rooms:
        room.unread_count = ChatMessage.objects.filter(
            room=room, is_read=False
        ).exclude(sender_name=request.user.username).count()

    return render(request, 'chat/rooms.html', {'rooms': rooms})


@login_required
def chat_room(request, room_id):
    """Page de chat avec un interlocuteur"""
    room = get_object_or_404(ChatRoom, id=room_id)

    # Vérifier que l'utilisateur est dans la conversation
    if request.user.username not in [room.buyer_name, room.seller_name]:
        messages.error(request, 'Accès non autorisé')
        return redirect('pages:dashboard')

    # Marquer les messages comme lus
    ChatMessage.objects.filter(room=room, is_read=False).exclude(
        sender_name=request.user.username
    ).update(is_read=True)

    # Déterminer l'autre personne
    other_user = room.buyer_name if room.seller_name == request.user.username else room.seller_name
    other_role = "acheteur" if other_user == room.buyer_name else "vendeur"

    context = {
        'room': room,
        'messages': room.messages.all(),
        'other_user': other_user,
        'other_role': other_role,
    }

    return render(request, 'chat/room.html', context)


@login_required
@require_http_methods(["POST"])
def send_message(request, room_id):
    """Envoyer un message"""
    try:
        room = get_object_or_404(ChatRoom, id=room_id)

        # Vérifier l'accès
        if request.user.username not in [room.buyer_name, room.seller_name]:
            return JsonResponse({'success': False, 'error': 'Non autorisé'})

        data = json.loads(request.body)
        message = data.get('message', '').strip()

        if not message:
            return JsonResponse({'success': False, 'error': 'Message vide'})

        # Créer le message
        chat_message = ChatMessage.objects.create(
            room=room,
            sender_name=request.user.username,
            message=message
        )

        return JsonResponse({
            'success': True,
            'message': {
                'id': str(chat_message.id),
                'sender': chat_message.sender_name,
                'text': chat_message.message,
                'time': chat_message.created_at.strftime('%H:%M'),
                'is_mine': True
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def unread_count(request):
    """Compter les messages non lus"""
    rooms = ChatRoom.objects.filter(
        buyer_name=request.user.username
    ) | ChatRoom.objects.filter(
        seller_name=request.user.username
    )

    total_unread = 0
    for room in rooms:
        unread = ChatMessage.objects.filter(
            room=room, is_read=False
        ).exclude(sender_name=request.user.username).count()
        total_unread += unread

    return JsonResponse({'unread_count': total_unread})