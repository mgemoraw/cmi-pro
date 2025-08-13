from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ParticularForm, WorkEquipmentForm
from .models import Particular, DivisionModel, ProjectType # Make sure to import your models
from .services import parse_csv_file

from io import TextIOWrapper
import csv


# Create your views here.
def index(request):
    particulars = Particular.objects.all()
    context = {'particulars': particulars}

    return render(request, 'particular/particulars_list.html', context=context)

def particulars_view(request):
    particulars = Particular.objects.all()

    return render(request, 'particular/particulars_list.html',{'particulars': particulars})



def create_equipment(request):
    form = WorkEquipmentForm(request.POST)

    return render(request, 'particular/equipments.html', {'form': form})

def create_particular(request):
    """
    Handles the creation of a new Particular instance.
    - If the request method is POST, it attempts to validate and save the form data.
    - If the form is valid, it saves the new Particular and redirects to a success page (e.g., particular_list).
    - If the request method is GET, it renders an empty form for creating a new particular.
    """
    if request.method == 'POST':
        # Create a form instance from the request data
        form = ParticularForm(request.POST)
        if form.is_valid():
            # Save the new Particular instance to the database
            form.save()
            # Redirect to a list page or a detail page of the newly created particular
            # You'll need to define 'particular_list' or 'particular_detail' URL patterns
            return redirect('particular_list') # Assuming you have a URL named 'particular_list'
    else:
        # Create a new empty form
        form = ParticularForm()

    # Render the form template with the form instance
    return render(request, 'particular/create_particular.html', {'form': form})

# Example of a simple list view to redirect to after creation (optional, for testing)
def particular_list(request):
    particulars = Particular.objects.all()
    return render(request, 'particular/particulars_list.html', {'particulars': particulars})


def import_from_file(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("csv_file")

        if not uploaded_file:
            # No file uploaded
            return render(request, 'particulars/particular_list.html', {'error': 'Please select a file to upload. '})
        
        # Ensure it's a CSV file
        if not (uploaded_file.name.endswith('.csv') or uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls')):
            return render(request, 'particular/particulars_list.html', {'error': 'Invalid file type. Please upload a CSV file.'})
        
        try:
            # Read CSV file
            file_data = TextIOWrapper(uploaded_file.file, encoding='utf-8')
            
            # parse csv data and add into database
            parse_csv_file(file_data)

            messages.success(request, "CSV file imported successfully.")
            
            return redirect('particular:particulars')

        except Exception as e:
            return render(request, 'particular/particulars_list.html', {'error': f"Error reading file: {str(e)}"})


    return redirect('particular:particulars')