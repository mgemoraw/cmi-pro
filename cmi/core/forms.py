from django import forms
from .models import TipperDataModel, Project, Task, Tipper, CollectorModel, TipperCycle

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
