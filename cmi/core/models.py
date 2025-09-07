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
    # engineer = models.ForeignKey('Engineer', null=True, on_delete=models.PROTECT, related_name='project_engieer')

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



class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name



class Productivity(models.Model):
    collector = models.ForeignKey("Collector", on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    data_count = models.PositiveIntegerField(default=0)
    counted_date = models.DateField(auto_now_add=True)
    particular = models.ForeignKey('particular.Particular', on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    mpdm_delay = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    mpdm_code = models.CharField(max_length=100, null=True, blank=True)


class CrewCooperationChoices(models.IntegerChoices):
    VERY_DIVERSE_VERY_LOW = 1, 'Very Diverse Ability, Very Low Stake Value, Very Large Crew Size'
    DIVERSE_LOW = 2, 'Diverse Ability, Low Stake Value, Large Crew Size'
    DIVERSE_MEDIUM = 3, 'Diverse Ability, Medium Stake Value, Average Crew Size'
    SIMILAR_HIGH = 4, 'Similar Ability, High Stake Value, Small Crew Size'
    SIMILAR_VERY_HIGH = 5, 'Similar Ability, Very High Stake Value, Very Small Crew Size'


class FairnessChoices(models.IntegerChoices):
    VERY_POOR = 1, 'Inconsistent daily work, Unreasonable crew assignment, VERY POOR information'
    POOR = 2, 'Inconsistent daily work, Unreasonable crew assignment, POOR information'
    AVERAGE = 3, 'Consistent daily work, Reasonable crew assignment, AVERAGE information'
    GOOD = 4, 'Consistent daily work, Reasonable crew assignment, GOOD information'
    VERY_GOOD = 5, 'Consistent daily work, Reasonable crew assignment, VERY GOOD information'

class CrewAbilityChoices(models.IntegerChoices):
    VERY_LOW = 1, 'Below 20%'
    LOW = 2, 'Between 20% and 40%'
    AVERAGE = 3, 'Between 40% and 60%'
    HIGH = 4, 'Between 60% and 80%'
    VERY_HIGH = 5, 'Above 80%'


class CrewWillingnessChoices(models.IntegerChoices):
    VERY_LOW = 1, 'Completely Unwilling'
    LOW = 2, 'Somewhat NOT Willing'
    AVERAGE = 3, 'Somewhat Willing'
    HIGH = 4, 'Willing'
    VERY_HIGH = 5, 'Completely Willing'

class CraftsmenEducationChoices(models.IntegerChoices):
    ELEMENTARY = 1, "Elementary"
    HIGHSCHOOL = 2, "Highschool"
    TECHNICAL = 3, "Technical"
    COLLEGE = 4, "College"
    UNIVERSITY = 5, "University"

class DailyVariables(models.Model):
    # crew Properties
    date = models.DateField(auto_now_add=True)
    collector = models.ForeignKey("Collector", on_delete=models.CASCADE)
    particular = models.ForeignKey('particular.Particular', on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    crew_size = models.PositiveIntegerField()
    crew_composition = models.TextField()
    crew_cooperation = models.CharField(max_length=1, choices=CrewCooperationChoices.choices)
    level_of_interruption = models.PositiveIntegerField()
    fairness_of_work_assignment = models.CharField(max_length=1, choices=FairnessChoices.choices)

    # crew flexibility
    crew_ability = models.CharField(max_length=1, choices=CrewAbilityChoices.choices)
    crew_willingness = models.CharField(max_length=1, choices=CrewWillingnessChoices.choices)
    
    # crew characteristics
    craftsmen_education = models.CharField(max_length=1, choices=CraftsmenEducationChoices.choices)
    craftsmen_onjob_training = models.PositiveIntegerField()
    craftsmen_technical_training = models.PositiveIntegerField()
    crew_experience = models.DecimalField(max_digits=5, decimal_places=2)
    languages_spoken = models.PositiveIntegerField()
    job_security = models.DecimalField(max_digits=5, decimal_places=2)

    # availability of work equipment
    work_equiment_number = models.TextField()
    waiting_time_for_work_equipment = models.DecimalField(max_digits=5, decimal_places=2)

    # availability of transport equipment
    transport_equipment_number = models.TextField()
    waiting_time_for_transport_equipment = models.DecimalField(max_digits=5, decimal_places=2)

    misplacement_of_tools = models.DecimalField(max_digits=5, decimal_places=2)
    electric_power_availability = models.DecimalField(max_digits=5, decimal_places=2)
    extension_cord_availability = models.DecimalField(max_digits=5, decimal_places=2)

    # Environmental variables
    min_temperature = models.DecimalField(max_digits=5, decimal_places=2)
    max_temperature = models.DecimalField(max_digits=5, decimal_places=2)

    min_precipitation = models.DecimalField(max_digits=5, decimal_places=2)
    max_precipitation =  models.DecimalField(max_digits=5, decimal_places=2)

    min_humidity = models.DecimalField(max_digits=5, decimal_places=2)
    max_humidity =  models.DecimalField(max_digits=5, decimal_places=2)

    min_wind_speed = models.DecimalField(max_digits=5, decimal_places=2)
    max_wind_speed = models.DecimalField(max_digits=5, decimal_places=2)

    site_congestion = models.CharField(max_length=5)
    use_of_overtime = models.DecimalField(max_digits=10, decimal_places=2)



class MPDM(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    particular = models.ForeignKey('particular.Particular', on_delete=models.CASCADE)
    date= models.DateField()
    time_unit = models.CharField(max_length=20)
    operation = models.CharField(max_length=255)
    equipment = models.CharField(max_length=255)


class MPDMCycle(models.Model):
    mpdm = models.ForeignKey('MPDM', on_delete=models.CASCADE)
    cycle_number = models.PositiveIntegerField()
    cycle_time = models.PositiveIntegerField()
    environment_delay = models.IntegerField()
    equipment_delay = models.IntegerField()
    labor_delay = models.IntegerField()
    material_delay = models.IntegerField()
    management_delay = models.IntegerField()
    other_delay = models.IntegerField()
    other_label = models.CharField(max_length=255, null=True, blank=True)


class Tipper(models.Model):
    license_plate = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.license_plate

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
