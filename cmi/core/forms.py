from django import forms
from .models import TipperDataModel, Project, DataInstance, Task, Tipper, Collector, TipperCycle

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
        