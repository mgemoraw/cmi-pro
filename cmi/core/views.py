from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from .forms import TipperDataModelForm, ProjectForm, DataInstanceForm,DataCollectorForm, EngineerForm
from particular.forms import ParticularForm
from .models import (
    Project,
    Tipper,
    Collector,
    DataInstance,
    Engineer,
    Task,
    TipperCycle,
    TipperDataModel,
)
from particular.models import Particular
from .services import  ProjectDataParser, ProjectDataTemplateGenerator


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

def create_instance_view(request):
    return redirect('core:instances')

def trucks(request):
    form = TipperDataModelForm(request.POST or None)

    return render(request, 'core/truck.html', {'form':form })


def projects(request):
    projects = Project.objects.all()
    engineers = Engineer.objects.all()
    collectors = Collector.objects.all()
    project_form = ProjectForm()
    engineer_form = EngineerForm()
    collector_form = DataCollectorForm()
    project_form = ProjectForm()
    context = {
        "projects": projects,
        'engineers': engineers,
        'collectors': collectors,
        
    }

    if request.method == "GET":
        selected_type = request.GET.get('projectInfo')
        label = f"{selected_type}_form"
        context[label] = selected_type
    return render(request, 'core/projects.html', context=context)

def create_project(request):
    projects = Project.objects.all()
    if request.method == 'POST':
        form_type = request.POST.get('projectInfo')
        if form_type =='project':
            project_form = ProjectForm(request.POST)
            if project_form.is_valid():
                project_form.save()
                return redirect('core:projects')
            
        if form_type =='engineer':
            engineer_form = EngineerForm(request.POST)
            if engineer_form.is_valid():
                engineer_form.save()
                return redirect('core:projects')
        if form_type == 'collector':
            collector_form = DataCollectorForm(request.POST)
            if collector_form.is_valid():
                collector_form.save()
                return redirect("core:projects")
    else:
        project_form = ProjectForm()
        engineer_form = EngineerForm()
        collector_form = DataCollectorForm()
   
        context = {
            'projects': projects,
            'project_form': project_form,
            'engineer_form': engineer_form,
            'collector_form': collector_form,
        }
        return render(request, 'core/projects.html', context)

def download_template(request):
    """
    View to handle template file downloads.
    URL: /download_template/<str:data_type>/<str:file_format>/
    
    """
    if request.method == "POST":
        file_format = request.POST.get('dataFormat')
        data_type = request.POST.get('projectInfo')
        try:
            generator = ProjectDataTemplateGenerator(data_type=data_type)
            output_file = generator.create_template(file_format=file_format)
            
            file_name = f"{data_type}_template.{file_format}"
            response = HttpResponse(output_file.read(), content_type=f'application/{file_format}')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
        except ValueError as e:
            return HttpResponse(str(e), status=400)
    return redirect('core:projects')

def import_project_data(request):
    context = {}
    if request.method == "POST":
        record_type = request.POST.get("projectInfo")
        uploaded_file = request.FILES.get("data_file")
        # print(record_type)
        # print(uploaded_file)

        try:
           
            if (record_type == 'null') or (uploaded_file == None):
                messages.error(request, 'No file selected')
                return redirect('core:projects')
            
            parser = ProjectDataParser(data_file=uploaded_file, data_type=record_type)
            parsed_data = parser.parse()

            if record_type == 'collector':
                # process collector data
                messages.success(request, "Collecters Information uploaded")
                return redirect('core:projects')
                
            elif record_type == 'engineer':
                # process eingineer data
                messages.success(request, "Engineeers Information uploaded")
                return redirect('core:projects')

            elif record_type == 'project':
                # process project data
                messages.success(request, "Project Information uploaded")
                return redirect('core:projects')
        
            else:
                messages.warning(request, message="Data format Unknown")
                return redirect('core:projects')

                
            
            # Now, 'parsed_data' is a list of dictionaries. 
            # You can iterate through it to save data to your Django models.
            # Example:
            # for row in parsed_data:
            #     Project.objects.create(**row)
            
            return HttpResponse("Data imported successfully!", status=200)
        except ValueError as e:
            messages.error(request, "Please upload file")
            return HttpResponse(str(e), status=400)
        
    return render(request, 'core/projects.html', context)


def add_collector(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        mname = request.POST.get('mname')
        lname = request.POST.get('lname')
        phone = request.POST.get('phone')
        project_id = request.POST.get('project')
        engineer_id = request.POST.get('engineer')
        project = Project.objects.get(id=project_id)
        engineer = None
        if engineer_id:
            engineer = Engineer.objects.get(id=engineer_id)
        Collector.objects.create(
            fname=fname,
            mname=mname,
            lname=lname,
            phone=phone,
            project=project,
            engineer=engineer
        )
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
def settings_view(request):
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
