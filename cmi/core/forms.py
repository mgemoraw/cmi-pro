from django import forms
from .models import TipperDataModel, Project, DataInstance, Task, Tipper, Collector, Engineer

class TipperDataModelForm(forms.ModelForm):
    class Meta:
        model = TipperDataModel
        fields = '__all__'
        labels = {
            'project': 'Project',
            'date': 'Date',
            'number_of_equipment_types': 'Number of Equipment Types',
            'task': 'Task',
            'collector': 'Collector',
            'tipper': 'Tipper',
            'cyles': 'Cycle',
        }
        widgets = {
            'project': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'number_of_equipment_types': forms.NumberInput(attrs={'class': 'form-control'}),
            'task': forms.Select(attrs={'class': 'form-select'}),
            'collector': forms.Select(attrs={'class': 'form-select'}),
            'tipper': forms.Select(attrs={'class': 'form-select'}),
            'cyles': forms.Select(attrs={'class': 'form-select'}),
        }


# class TipperDataModelForm(forms.ModelForm):
#     class Meta:
#         model = TipperDataModel
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super(TipperDataModelForm, self).__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             if isinstance(field.widget, forms.Select):
#                 field.widget.attrs['class'] = 'form-select'
#             else:
#                 field.widget.attrs['class'] = 'form-control'


class EngineerForm(forms.ModelForm):
    class Meta:
        model = Engineer
        fields = '__all__'
        labels = {
            'projects': 'Projects',
            'fname': 'First Name',
            'mname': 'Middle Name',
            'lname': 'Last Name', 
            'phone': 'Phone Number',
            'email': 'Email Address',
        }
        widgets = {
            'projects': forms.CheckboxSelectMultiple(attrs={'class': 'form-check'}),
            'fname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'mname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle Name'}),
            'lname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

        labels = {
            'name': 'Name',
            'description': 'Description',
            'code': 'Project Code',
            'start_date': 'Project Started Date',
            'end_date': 'Project End Date',

            'region': 'Region',
            'zone': 'Zone',
            'woreda': 'Woreda',
            'kebele': 'Kebele',
            'town': 'Town',

            'longitude': 'Longitude',
            'latitude': 'Latitude',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Project Description'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Code'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'zone': forms.TextInput(attrs={'class': 'form-control'}),
            'woreda': forms.TextInput(attrs={'class': 'form-control'}),
            'kebele': forms.TextInput(attrs={'class': 'form-control'}),
            'town': forms.TextInput(attrs={'class': 'form-control'}),

            'latitude': forms.TextInput(attrs={'class': 'form-control'}),
            'longitude': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    # def __init__(self, args, **kwargs):
    #     super(ProjectForm, self).__init__(*args, **kwargs)
    #     for field_name, field, in self.fields.items():
    #         if isinstance(field.widget, forms.Select):
    #             field.widget.attrs['class'] = 'form-select'
    #         else:
    #             field.widget.attrs['class'] = 'form-control'


class DataInstanceForm(forms.ModelForm):
   
    class Meta:
        model = DataInstance
        fields = "__all__"

        labels = {
            'project': 'Project',
            'collector': 'Data Collector',
            # 'task': 'Task',
            # 'element': 'Element',
            'particular': 'Particular',
            'status': 'Status',
            'encoded': 'Encoded',
            # 'encoder': 'Data Encoder',
            'encoded_by': 'Encoded By',
            'reviewed_by': 'Reviewed By',
            'raw_file': 'Raw Data File',
            'encoded_file': 'Encoded Data File',
        }

        widgets = {
            'project': forms.Select(attrs={'class': 'form-select'}),
            'collector': forms.Select(attrs={'class': 'form-select'}),
            'particular': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.RadioSelect(attrs={'class': 'form-check-inline'}),
            'encoded': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            # 'encoder': forms.Select(attrs={'class': 'form-select'}),
            'encoded_by': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Encoded By'}),
            'review_comments': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Review Comments'}),
            'reviewed_by': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Reviewed By'}),
            'raw_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'encoded_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    

class DataCollectorForm(forms.ModelForm):
    class Meta:
        model = Collector
        fields = '__all__'
        labels = {
            'projects': 'Projects',
            'engineer': 'Engineer',
            'fname': 'First Name',
            'mname': 'Middle Name',
            'lname': 'Last Name',
            'phone': 'Phone Number',
        }
        widgets = {
            'projects': forms.CheckboxSelectMultiple(attrs={'class': 'form-check'}),
            'engineer': forms.Select(attrs={'class': 'form-select'}),
            'fname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'mname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle Name'}),
            'lname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }

