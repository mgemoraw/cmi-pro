from django.shortcuts import render, redirect

# Create your views here.
def dashboard(request):
    return render(request, 'core/dashboard.html', {})

def trucks(request):
    return render(request, 'core/truck.html', {})

def truck_create(request):
    if request.method == 'POST':
        # Get form data
        truck_id = request.POST.get('truck_id')
        productivity = request.POST.get('productivity')

        # Save to DB, handle validation, etc.
        # Truck.objects.create(...)

        return redirect('core:truck')  # or render with success msg
