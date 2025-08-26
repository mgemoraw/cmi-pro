# particular/forms.py

from django import forms
from .models import Particular, Division, ProjectType, WorkEquipment, Sector

# forms 
class DivisionForm(forms.ModelForm):
    """
    A model form for the divisions model
    """
    project_type = forms.ModelChoiceField(
        queryset = ProjectType.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label='-- Select Sector --',
    )

    class Meta:
        model = Division
        fields = [
            'project_type',
            'name',
            'code',
        ]

        widgets = {
            # 'sector': forms.Select(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unique Division Code'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unique Division name'}),
        }

class ParticularForm(forms.ModelForm):
    """
    A ModelForm for the Particular model, used to create and update Particular instances.
    It automatically generates form fields based on the Particular model's fields.
    """
    class Meta:
        model = Particular
        # Specify the fields to include in the form.
        # 'pid', 'division', 'project_type', 'task', 'element', 'name'
        # are required for creating a new particular.
        # 'data_collection_days' and 'collected_days' can also be included
        # if you want them to be editable upon creation, otherwise they can
        # be handled by default values or in the view.
        fields = [
            'pid',
            'project_type',
            'division',
            'task',
            'element',
            'name',
            'required_instances', # Include if you want this editable on creation
            'collected_instances',       # Include if you want this editable on creation
        ]
        # Optional: Add widgets for custom form input types or attributes
        widgets = {
            'pid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unique Particular ID'}),
            'project_type': forms.Select(attrs={'class': 'form-control'}),
            'division': forms.Select(attrs={'class': 'form-control'}),

            'task': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task description'}),
            'element': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Element description'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Particular Name'}),
            'required_instances': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'collected_instances': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }


class WorkEquipmentForm(forms.ModelForm):
    """
    A ModelForm for the Work Equipment model, used to create and update Particular instances.
    It automatically generates form fields based on the Particular model's fields.
    """
    class Meta:
        model = WorkEquipment
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'count': forms.TextInput(attrs={'class': 'form-control'}),
        }

