from django.contrib import admin
from .models import Project, CollectorModel, TipperDataModel


# Register your models here.
admin.site.register(Project)
admin.site.register(CollectorModel)
admin.site.register(TipperDataModel)

