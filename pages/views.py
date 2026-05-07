from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'pages/home.html')

def login_view(request):
    return render(request, 'pages/login.html')

def register_view(request):
    return render(request, 'pages/register.html')

def logout_view(request):
    return redirect('pages:home')

def dashboard(request):
    return render(request, 'pages/dashboard.html')

def listings_view(request):
    return render(request, 'pages/listings.html')

def listing_detail_view(request, listing_id):
    return render(request, 'pages/listing_detail.html')

def wallet_view(request):
    return render(request, 'pages/wallet.html')
