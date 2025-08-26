from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from .forms import TipperDataModelForm, ProjectForm, DataInstanceForm
from particular.forms import ParticularForm
from .models import (
    Project,
    Tipper,
    Collector,
    DataInstance,
)
from particular.models import Particular



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
    return redirect("core:user-login")

def dashboard(request):
    return render(request, 'core/dashboard.html', {})

def particular_dashboard(request):
    particulars = Particular.objects.all()
    projects = Project.objects.all()
    collectors = Collector.objects.all()
    form = ParticularForm()

    context = {'particulars': particulars, "form": form}

    return render(request, 'core/particulars.html', context)

def instance_dashboard(request):
    instances = DataInstance.objects.all()
    instance_form = DataInstanceForm()
    # active_particulars = DataInstance.objects.distinct(particular)
    context = {
        'instances': instances,
        "form": instance_form,
    }
    return render(request, 'core/instance_dashboard.html', context=context)

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

@login_required
def settings(request):
    context = {}
    return render(request, 'core/settings.html', context)

@login_required
def work_items(request):
    return redirect('core:particulars')


def dozers(request):

    context = {}
    return render(request, 'core/dozers.html', context)


def create_dozer(request):

    context = {}
    return render(request, 'core/dozers.html', context)


def excavators(request):

    context = {}
    return render(request, 'core/excavators.html', context)


def create_excavator(request):

    context = {}
    return render(request, 'core/excvators.html', context)


def labors(request):

    context = {}
    return render(request, 'core/labors.html', context)


def create_labor(request):

    context = {}
    return render(request, 'core/labors.html', context)


def work_sampling(request):

    context = {}
    return render(request, 'core/work_sampling.html', context)


def create_ws(request):

    context = {}
    return render(request, 'core/work_sampling.html', context)
