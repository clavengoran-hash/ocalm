from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home_view(request):
    """Page d'accueil"""
    return render(request, 'pages/home.html')

def about_view(request):
    """Page À propos"""
    return render(request, 'pages/about.html')

def contact_view(request):
    """Page Contact"""
    return render(request, 'pages/contact.html')

def terms_view(request):
    """Page Conditions Générales"""
    return render(request, 'pages/terms.html')

def listings_view(request):
    """Page de la boutique"""
    return render(request, 'pages/listings.html')

def login_view(request):
    """Page de connexion"""
    return render(request, 'pages/login.html')

def register_view(request):
    """Page d'inscription"""
    return render(request, 'pages/register.html')

def logout_view(request):
    """Déconnexion"""
    from django.contrib.auth import logout
    from django.shortcuts import redirect
    logout(request)
    return redirect('home')

@login_required
def dashboard_view(request):
    """Tableau de bord utilisateur"""
    return render(request, 'pages/dashboard.html')

@login_required
def listing_detail_view(request, listing_id):
    """Détail d'une annonce"""
    context = {'listing_id': listing_id}
    return render(request, 'listings/detail.html', context)

@login_required
def wallet_view(request):
    """Portefeuille utilisateur"""
    return render(request, 'wallet/index.html')
