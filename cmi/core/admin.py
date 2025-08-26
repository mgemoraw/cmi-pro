from django.contrib import admin
from .models import Project, Collector, TipperDataModel


# Register your models here.
admin.site.register(Project)
admin.site.register(Collector)
admin.site.register(TipperDataModel)

