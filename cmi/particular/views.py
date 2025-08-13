from django.shortcuts import render, redirect
from .forms import ParticularForm
from .models import Particular, DivisionModel, ProjectType # Make sure to import your models

# Create your views here.
def index(request):
    return render(request, 'particular/index.html')

def particulars_view(request):
    particulars = Particular.objects.all()

    context = {'particulars': particulars}
    

    return render(request, 'particular/index.html', context=context)

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
    return render(request, 'particular/index.html', {'form': form})

# Example of a simple list view to redirect to after creation (optional, for testing)
def particular_list(request):
    particulars = Particular.objects.all()
    return render(request, 'particular/particulars_list.html', {'particulars': particulars})

