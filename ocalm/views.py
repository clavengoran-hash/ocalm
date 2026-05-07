from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'pages/home.html')

def about_view(request):
    return render(request, 'pages/about.html')

def contact_view(request):
    return render(request, 'pages/contact.html')

def terms_view(request):
    return render(request, 'pages/terms.html')

def listings_view(request):
    return render(request, 'pages/listings.html')

def login_view(request):
    return render(request, 'pages/login.html')

def register_view(request):
    return render(request, 'pages/register.html')

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')

@login_required
def dashboard_view(request):
    return render(request, 'pages/dashboard.html')

@login_required
def listing_detail_view(request, listing_id):
    context = {'listing_id': listing_id}
    return render(request, 'listings/detail.html', context)

@login_required
def wallet_view(request):
    return render(request, 'wallet/index.html')
