from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ParticularForm, WorkEquipmentForm, DivisionForm
from .models import Particular, Division, ProjectType # Make sure to import your models
from .services import GridDataParser

from io import TextIOWrapper
import csv


# Create your views here.
def index(request):
    particulars = Particular.objects.all()
    
    sectors = ProjectType.objects.all()
    divisions = Division.objects.all()
    particular_form = ParticularForm()
    equipment_form = WorkEquipmentForm(request.POST)
    division_form = DivisionForm()
    error = ""
    try:
        # filter particulars
        selected_division_id = request.GET.get('division', 'all')
        selected_sector_id = request.GET.get('sector', 'all')

        print("selected sector", selected_sector_id )
        print("selected division", selected_division_id)
        if selected_sector_id:
            sector_id = int(selected_sector_id)
            divisions = divisions.filter(project_type__id=sector_id)
            particulars = particulars.filter(project_type__id=sector_id)

        if (selected_division_id):
            division_id = int(selected_division_id)
            particulars = particulars.filter(division__id=division_id)
    except ValueError as e:
        error = f"{e}"
        
    context = {
        'particulars': particulars, 
        'sectors': sectors, 
        'divisions': divisions,
        'particular_form': particular_form,
        'equipment_form': equipment_form,
        'division_form': division_form,
        'error': error,
    }


    return render(request, 'particular/index.html', context=context)

def update_instances(request):
    from core.models import DataInstance
    from django.db.models import Count

    particulars = Particular.objects.annotate(
        instance_count=Count('instance_particular')
    )

    for particular in particulars:
        particular.collected_instances = particular.instance_count
        particular.progress = particular.collected_instances/80 * 100
        particular.save()


    return redirect('particular:particulars')


def particulars_view(request):
    particulars = Particular.objects.all()
    sectors = ProjectType.objects.all()
    divisions = Division.objects.all()

    context = {'particulars': particulars, 'sectors': sectors, 'divisions': divisions}

    return render(request, 'particular/particulars_list.html', context)

def create_project_sector(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")

            project = ProjectType.objects.create(
                name=name,
            )
            messages.success(request, "Sector added!")
            # Redirect to a list page or a detail page of the newly created particular
            # You'll need to define 'particular_list' or 'particular_detail' URL patterns
            return redirect('particular:particulars') # Assuming
        except Exception as e:
            messages.error(request, f"Adding Sector Failed with error: {e}")

    return redirect('particular:particulars')

def create_equipment(request):
    form = WorkEquipmentForm(request.POST)

    return render(request, 'particular/equipments.html', {'equipment_form': form})

def create_division(request):
    form = DivisionForm(request.POST)
    if form.is_valid():
        form.save()
        
    return redirect('particular:particulars')


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
        equipment_form = WorkEquipmentForm()
        # Render the form template with the form instance
        return render(request, 'particular/create_particular.html', {'form': form, 'equipment_form': equipment_form})
    messages.success(request, "Information about request")
    return redirect('particular:particulars')


# Example of a simple list view to redirect to after creation (optional, for testing)
def particular_list(request):
    particulars = Particular.objects.all()
    sectors = ProjectType.objects.all()
    divisions = Division.objects.all()

    context = {'particulars': particulars, 'sectors': sectors, 'divisions': divisions}

    return render(request, 'particular/particulars_list.html', context)


def import_from_file(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("csv_file")

        if not uploaded_file:
            messages.error(request, 'failed to import file')

            # No file uploaded
            return render(request, 'particular/particulars_list.html', {'error': 'Please select a file to upload. '})
        
        # Ensure it's a CSV file
        if not (uploaded_file.name.endswith('.csv') or uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls')):
            messages.error(request, 'failed to import file')

            return render(request, 'particular/particulars_list.html', {'error': 'Invalid file type. Please upload a CSV file.'})
        
        
        try:
            # Read CSV file
            # file_data = TextIOWrapper(uploaded_file.file, encoding='utf-8')
            
            # parse csv data and add into database
            filename = uploaded_file.name  # e.g., "data.xlsx" or "data.csv"
            extension = filename.split('.')[-1].lower()

            # if extension in ('csv',):
            #     file_format = 'csv'
            # elif extension in ('xlsx', 'xls'):
            #     file_format = 'xlsx'
            # else:
            #     raise ValueError("Unsupported file type")
            

            parser = GridDataParser(uploaded_file, extension)
            parser.parse()

            # parse_csv_file(uploaded_file)

            messages.success(request, "File imported successfully.")
            
            return redirect('particular:particulars')

        except Exception as e:
            messages.error(request, f"Failed to upload the file: {e}")
            return render(request, 'particular/particulars_list.html', {'particulars': Particular.objects.all(), 'error': f"Error reading file: {str(e)}", 'open_modal':True})


    return redirect('particular:particulars')