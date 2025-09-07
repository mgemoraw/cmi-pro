from django.contrib import admin
from .models import Project, Collector, TipperDataModel, Engineer, DataInstance


# Register your models here.
# admin.site.register(Collector)
admin.site.register(TipperDataModel)
# admin.site.register(Engineer)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'get_location')
    search_fields = ('name', )
    list_filter = ('start_date', 'end_date')

    def get_location(self, obj):
        return f"{obj.zone}, {obj.woreda}, {obj.kebele}, {obj.town}"
    get_location.short_description = "Project Location"


@admin.register(Engineer)
class EngineerAdmin(admin.ModelAdmin):
    list_display = ('fname', 'mname', 'lname', 'email', 'phone', 'get_projects')
    search_fields = ('fname', 'mname', 'lname', 'email')
    list_filter = ('projects',)
    filter_horizontal = ('projects',)  # better widget for ManyToMany fields

    def get_projects(self, obj):
        return ", ".join([p.name for p in obj.projects.all()])
    get_projects.short_description = "Projects"


@admin.register(Collector)
class CollectorAdmin(admin.ModelAdmin):
    list_display = ('fname', 'mname', 'lname', 'phone', 'get_projects', 'engineer')
    search_fields = ('fname', 'mname', 'lname', 'phone', 'engineer__fname', 'engineer__lname')
    list_filter = ('projects', 'engineer')
    filter_horizontal = ('projects',)
    def get_projects(self, obj):
        return ", ".join([p.name for p in obj.projects.all()])
    get_projects.short_description = "Projects"


@admin.register(DataInstance)
class DataInstanceAdmin(admin.ModelAdmin):
    list_display = ('particular', 'status', 'encoded', 'encoded_by', 'reviewed_by')
    search_fields = ('particular__name', 'encoded_by__username', 'reviewed_by__username')
    list_filter = ('status', 'encoded', 'encoded_by', 'reviewed_by')