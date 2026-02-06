from django.forms import BaseForm, ModelForm

from core.models import DataInstance

from .models import ProjectType, Project


# Create your forms here.
class DataInstanceForm(ModelForm):
    class Meta:
        model = DataInstance  # Placeholder for future model
        fields = '__all__'
