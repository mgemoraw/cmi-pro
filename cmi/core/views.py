from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import TipperDataModelForm

# Create your views here.

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # Change 'home' to your desired route
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("login")

def dashboard(request):
    return render(request, 'core/dashboard.html', {})

def trucks(request):
    form = TipperDataModelForm(request.POST or None)

    return render(request, 'core/truck.html', {'form':form })

def truck_create(request):
    if request.method == 'POST':
        # Get form data
        truck_id = request.POST.get('truck_id')
        productivity = request.POST.get('productivity')

        # Save to DB, handle validation, etc.
        # Truck.objects.create(...)

        return redirect('core:truck', )  # or render with success msg
