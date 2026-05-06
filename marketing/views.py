from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from listings.models import Listing
from .models import SocialAccount, SocialPost


@login_required
def social_media_dashboard(request):
    """Dashboard Business Manager intégré"""

    if request.user.role != 'seller':
        messages.error(request, 'Accès réservé aux vendeurs')
        return redirect('dashboard')

    # Récupérer les annonces du vendeur
    listings = Listing.objects.filter(seller_name=request.user.username, is_available=True)

    # Récupérer les comptes connectés
    facebook_account = SocialAccount.objects.filter(
        user=request.user,
        platform='facebook',
        is_active=True
    ).first()

    instagram_account = SocialAccount.objects.filter(
        user=request.user,
        platform='instagram',
        is_active=True
    ).first()

    # Récupérer l'historique des publications
    social_posts = SocialPost.objects.filter(
        listing__seller_name=request.user.username
    ).order_by('-published_at')[:20]

    # Statistiques Facebook
    facebook_posts = SocialPost.objects.filter(
        listing__seller_name=request.user.username,
        platform='facebook'
    )
    total_facebook_posts = facebook_posts.count()
    total_facebook_likes = sum(p.likes for p in facebook_posts)
    total_facebook_views = sum(p.views for p in facebook_posts)

    # Statistiques Instagram
    instagram_posts = SocialPost.objects.filter(
        listing__seller_name=request.user.username,
        platform='instagram'
    )
    total_instagram_posts = instagram_posts.count()
    total_instagram_likes = sum(p.likes for p in instagram_posts)
    total_instagram_comments = sum(p.comments for p in instagram_posts)

    context = {
        'listings': listings,
        'facebook_account': facebook_account,
        'instagram_account': instagram_account,
        'social_posts': social_posts,
        'total_facebook_posts': total_facebook_posts,
        'total_facebook_likes': total_facebook_likes,
        'total_facebook_views': total_facebook_views,
        'total_instagram_posts': total_instagram_posts,
        'total_instagram_likes': total_instagram_likes,
        'total_instagram_comments': total_instagram_comments,
    }

    return render(request, 'pages/business_manager.html', context)


@login_required
def connect_facebook_business(request):
    """Connecter Facebook Business (simulation pour le moment)"""
    # Pour l'instant, simulation
    messages.success(request, 'Compte Facebook Business connecté avec succès !')
    return redirect('social_media_dashboard')


@login_required
def publish_to_facebook(request, listing_id):
    """Publier une annonce sur Facebook"""
    listing = Listing.objects.get(id=listing_id)

    if listing.seller_name != request.user.username:
        messages.error(request, 'Non autorisé')
        return redirect('listing_detail', listing_id=listing_id)

    # Vérifier si un compte Facebook est connecté
    facebook_account = SocialAccount.objects.filter(
        user=request.user,
        platform='facebook',
        is_active=True
    ).first()

    if not facebook_account:
        messages.error(request, 'Connectez d\'abord votre compte Facebook Business')
        return redirect('social_media_dashboard')

    # Simuler la publication
    post = SocialPost.objects.create(
        listing=listing,
        account=facebook_account,
        platform='facebook',
        status='published',
        post_url=f"https://facebook.com/post/{listing_id}",
        likes=0,
        comments=0,
        shares=0,
        views=0
    )

    messages.success(request, f'✅ Annonce "{listing.title}" publiée sur Facebook !')
    return redirect('social_media_dashboard')


@login_required
def publish_to_instagram(request, listing_id):
    """Publier une annonce sur Instagram"""
    listing = Listing.objects.get(id=listing_id)

    if listing.seller_name != request.user.username:
        messages.error(request, 'Non autorisé')
        return redirect('listing_detail', listing_id=listing_id)

    # Vérifier si un compte Instagram est connecté
    instagram_account = SocialAccount.objects.filter(
        user=request.user,
        platform='instagram',
        is_active=True
    ).first()

    if not instagram_account:
        messages.error(request, 'Connectez d\'abord votre compte Instagram Business')
        return redirect('social_media_dashboard')

    # Simuler la publication
    post = SocialPost.objects.create(
        listing=listing,
        account=instagram_account,
        platform='instagram',
        status='published',
        post_url=f"https://instagram.com/p/{listing_id}",
        likes=0,
        comments=0
    )

    messages.success(request, f'✅ Annonce "{listing.title}" publiée sur Instagram !')
    return redirect('social_media_dashboard')


@login_required
def publish_all_to_facebook(request):
    """Publier toutes les annonces sur Facebook"""
    listings = Listing.objects.filter(seller_name=request.user.username, is_available=True)

    facebook_account = SocialAccount.objects.filter(
        user=request.user,
        platform='facebook',
        is_active=True
    ).first()

    if not facebook_account:
        messages.error(request, 'Connectez d\'abord votre compte Facebook Business')
        return redirect('social_media_dashboard')

    published_count = 0
    for listing in listings:
        SocialPost.objects.get_or_create(
            listing=listing,
            account=facebook_account,
            platform='facebook',
            defaults={'status': 'published'}
        )
        published_count += 1

    messages.success(request, f'✅ {published_count} annonces publiées sur Facebook !')
    return redirect('social_media_dashboard')


from django.utils import timezone
from .models import LiveStream, LiveComment, LiveOrder


@login_required
def live_dashboard(request):
    """Dashboard des lives pour le vendeur"""
    if request.user.role != 'seller':
        messages.error(request, 'Accès réservé aux vendeurs')
        return redirect('dashboard')

    lives = LiveStream.objects.filter(seller=request.user).order_by('-scheduled_time')

    # Statistiques
    total_lives = lives.count()
    total_viewers = sum(l.viewers for l in lives)
    total_orders = sum(l.orders_placed for l in lives)
    total_revenue = sum(l.revenue_generated for l in lives)

    context = {
        'lives': lives,
        'upcoming_lives': lives.filter(status='scheduled'),
        'past_lives': lives.filter(status='ended'),
        'total_lives': total_lives,
        'total_viewers': total_viewers,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'now': timezone.now(),
    }

    return render(request, 'marketing/live_dashboard.html', context)


@login_required
def create_live(request):
    """Créer un live stream"""
    from listings.models import Listing

    if request.user.role != 'seller':
        messages.error(request, 'Accès réservé aux vendeurs')
        return redirect('dashboard')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        scheduled_time = request.POST.get('scheduled_time')
        product_ids = request.POST.getlist('products')

        live = LiveStream.objects.create(
            seller=request.user,
            title=title,
            description=description,
            scheduled_time=scheduled_time,
            status='scheduled'
        )

        for product_id in product_ids:
            product = Listing.objects.get(id=product_id)
            live.products.add(product)

        messages.success(request, f'Live "{title}" programmé avec succès !')
        return redirect('live_dashboard')

    listings = Listing.objects.filter(seller_name=request.user.username, is_available=True)

    context = {
        'listings': listings,
    }

    return render(request, 'marketing/create_live.html', context)


@login_required
def start_live(request, live_id):
    """Démarrer un live stream (simulation)"""
    live = LiveStream.objects.get(id=live_id)

    if live.seller != request.user:
        messages.error(request, 'Non autorisé')
        return redirect('live_dashboard')

    live.status = 'live'
    live.started_at = timezone.now()
    live.save()

    messages.success(request, f'Live "{live.title}" est maintenant en direct !')
    return redirect('watch_live', live_id=live.id)


@login_required
def watch_live(request, live_id):
    """Regarder un live stream"""
    live = LiveStream.objects.get(id=live_id)

    # Incrémenter le compteur de viewers
    if request.user != live.seller:
        live.viewers += 1
        live.save()

    # Produits du live
    products = live.products.all()

    # Acheter pendant le live
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = live.products.get(id=product_id)

        # Créer la commande
        order = LiveOrder.objects.create(
            live=live,
            product=product,
            buyer=request.user,
            quantity=1,
            amount=product.price
        )

        live.orders_placed += 1
        live.revenue_generated += product.price
        live.save()

        messages.success(request, f'✅ Produit "{product.title}" ajouté au panier !')
        return redirect('watch_live', live_id=live.id)

    context = {
        'live': live,
        'products': products,
        'comments': live.comments.all().order_by('-created_at')[:50],
        'is_seller': request.user == live.seller,
    }

    return render(request, 'marketing/watch_live.html', context)


@login_required
def end_live(request, live_id):
    """Terminer le live stream"""
    live = LiveStream.objects.get(id=live_id)

    if live.seller != request.user:
        messages.error(request, 'Non autorisé')
        return redirect('live_dashboard')

    live.status = 'ended'
    live.ended_at = timezone.now()
    live.save()

    messages.success(request, f'Live "{live.title}" terminé. Félicitations !')
    return redirect('live_dashboard')


@login_required
def add_live_comment(request, live_id):
    """Ajouter un commentaire pendant le live"""
    if request.method == 'POST':
        live = LiveStream.objects.get(id=live_id)
        message = request.POST.get('message')

        if message:
            LiveComment.objects.create(
                live=live,
                user=request.user,
                message=message
            )
            live.comments_count += 1
            live.save()

    return redirect('watch_live', live_id=live_id)


@login_required
def share_live_to_whatsapp(request, live_id):
    """Partager le live sur WhatsApp"""
    live = LiveStream.objects.get(id=live_id)

    if live.seller != request.user:
        messages.error(request, 'Non autorisé')
        return redirect('live_dashboard')

    # Générer le lien WhatsApp
    message = f"🎥 LIVE OCALM - {live.title}\n\n{live.description}\n\n📅 {live.scheduled_time.strftime('%d/%m/%Y à %H:%M')}\n\n👉 Rejoignez le live : http://127.0.0.1:8000/marketing/live/watch/{live.id}/"

    whatsapp_url = f"https://wa.me/?text={message.replace(' ', '%20')}"

    # Sauvegarder le lien
    live.whatsapp_group_link = whatsapp_url
    live.save()

    return redirect(whatsapp_url)


@login_required
def create_whatsapp_group(request, live_id):
    """Créer un groupe WhatsApp pour le live"""
    live = LiveStream.objects.get(id=live_id)

    if live.seller != request.user:
        messages.error(request, 'Non autorisé')
        return redirect('live_dashboard')

    # Lien pour créer un groupe WhatsApp (simulation)
    group_link = f"https://chat.whatsapp.com/invite/generate"

    live.whatsapp_group_link = group_link
    live.save()

    messages.success(request, 'Lien du groupe WhatsApp généré !')
    return redirect('live_dashboard')