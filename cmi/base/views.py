from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'base/home.html')

def about(request):
    return render(request, 'base/about.html')

def contact(request):
    return render(request, 'base/contact.html')

def services(request):
    return render(request, 'base/services.html')

def login(request):
    return render(request, 'base/login.html')

def logout(request):
    return render(request, 'base/logout.html')

def profile(request):
    return render(request, 'base/profile.html')

def register(request):
    return render(request, 'base/register.html')

