from django.shortcuts import render

from .forms import DataInstanceForm

# Create your views here.
def home(request):
    return render(request, 'base/home.html')

def dashboard(request):
    context = {
        "truck_data": [
            {"id": "TRK-021", "productivity": 85},
            {"id": "TRK-044", "productivity": 78},
        ],
        "excavator_data": [
            {"id": "EXC-114", "productivity": 74},
        ],
        "dozer_data": [
            {"id": "DOZ-007", "productivity": 66},
        ],
        "labor_data": [
            {"id": "LAB-033", "productivity": 72},
        ]
    }
    return render(request, 'base/dashboard.html', context=context)

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


def settings(request):
    return render(request, 'base/settings.html')

def data_instance(request):
    forms = DataInstanceForm()  # Placeholder for future form handling logic
    context = {
        'forms': forms,
    }
    return render(request, 'base/data_instance.html', context=context)

