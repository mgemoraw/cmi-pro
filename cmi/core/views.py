from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import TipperDataModelForm, ProjectForm
from .models import (
    Project,
    Tipper,
)



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


def projects(request):
    projects = Project.objects.all()
    form = ProjectForm(request.POST or None)

    return render(request, 'core/projects.html', {'projects': projects, 'form': form})

def create_project(request):
    if request.method == 'POST':
        # name = request.POST.get("name")
        # description = request.POST.get("description")
        # code = request.POST.get("code")
        # region = request.POST.get("region")
        # zone = request.POST.get("zone")
        # woreda = request.POST.get("woreda")
        # kebele = request.POST.get("kebele")
        # town = request.POST.get("town")
        # latitude = request.POST.get("latitude")
        # longitude = request.POST.get("longitude")

        # # create new project
        # new_project = Project.objects.create(
        #     name=name,
        #     code=code,
        #     description=description,
        #     region=region,
        #     zone=zone,
        #     woreda=woreda,
        #     kebele=kebele,
        #     town=town,
        #     latitude=latitude,
        #     longitude=longitude,
        # )

        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:projects')
    return redirect('core:projects')


def truck_create(request):
    if request.method == 'POST':
        # Get form data
        truck_id = request.POST.get('truck_id')
        productivity = request.POST.get('productivity')

        # Save to DB, handle validation, etc.
        # Truck.objects.create(...)

        return redirect('core:truck', )  # or render with success msg


