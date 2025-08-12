from django.shortcuts import render, redirect
from .models import Particular

# Create your views here.
def index(request):
    return render(request, 'particular/index.html')

def particulars_view(request):
    particulars = Particular.objects.all()

    return redirect('core:dashboard')