from django.db import models
# from django.contrib.gis.db import models as gis_models  # Only if using GeoDjango


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Administrative location details
    region = models.CharField(max_length=100)
    zone = models.CharField(max_length=100)
    woreda = models.CharField(max_length=100)
    kebele = models.CharField(max_length=100, blank=True, null=True)  # optional
    town = models.CharField(max_length=100, blank=True, null=True)    # optional

    # For simple coordinate storage
    latitude = models.FloatField()
    longitude = models.FloatField()

    # Optional: For full GIS support
    # location = gis_models.PointField(geography=True, null=True, blank=True)
    engineer = models.ForeignKey('Engineer', null=True, on_delete=models.PROTECT, related_name='project_engieer')

    def __str__(self):
        return self.name
    
class Engineer(models.Model):
    fname = models.CharField(max_length=255)
    mname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=255)

    def __str__(self):
        return "{} {}".format(self.fname, self.mname)


class Collector(models.Model):
    project = models.ForeignKey("Project", verbose_name=("_"), on_delete=models.CASCADE)
    engineer = models.ForeignKey('Engineer', on_delete=models.PROTECT, null=True)
    fname = models.CharField(max_length=100)
    mname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    
    def __str__(self):
        return "{self.fname} {self.mname}"


class Tipper(models.Model):
    license_plate = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.license_plate

class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name


class TipperCycle(models.Model):
    cycle_number = models.IntegerField()
    manpwer = models.TextField()
    soil_type = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)
    load_cycle = models.IntegerField()
    haul_cyle = models.IntegerField()
    dump_cycle = models.IntegerField()
    return_cycle = models.IntegerField()
    total_cycle = models.IntegerField()
    q_heaped_capacity = models.FloatField()
    productivity = models.FloatField()

    def save(self):
        # Ensure total_cycle is the sum of all cycles
        if self.unit.lower().startswith('minute'):
            self.productivity = (self.q_heaped_capacity) / (self.total_cycle * 60)
        elif self.unit.lower().startswith('second'):
            self.productivity = (self.q_heaped_capacity) / (self.total_cycle)

        super().save()
    

    def __str__(self):
        return f"Cycle {self.cycle_number} - {self.soil_type} - {self.total_cycle} {self.unit}"

class TipperDataModel(models.Model):
    project  = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateField()
    number_of_equipment_types = models.IntegerField()
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    collector = models.ForeignKey('Collector', on_delete=models.CASCADE)
    tipper = models.ForeignKey('Tipper', on_delete=models.CASCADE)

    # Optional: If you want to link to TipperCycle
    cyles = models.ForeignKey('TipperCycle',on_delete=models.CASCADE, blank=True)


    def __str__(self):
        return f"{self.project.name} - {self.date} - {self.tipper.license_plate}"
    

class DataInstance(models.Model):
    from particular.models import Particular

    class InstanceChoices(models.TextChoices):
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'
        PENDING = 'pending', 'Pending'

    project = models.ForeignKey('Project', on_delete=models.PROTECT, related_name='instance_project')
    collector = models.ForeignKey('Collector', on_delete=models.CASCADE, related_name='data_collector')
    
    particular = models.ForeignKey(Particular, on_delete=models.CASCADE, related_name='instance_particular')
    date = models.DateField(auto_now_add=True)
    
    problems = models.TextField()
    status = models.CharField(max_length=15, choices=InstanceChoices, default=InstanceChoices.PENDING)
    encoded = models.BooleanField(default=False)
    encoder = models.CharField(max_length=255)
