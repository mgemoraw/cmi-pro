from django.db import models
# from django.contrib.gis.db import models as gis_models  # Only if using GeoDjango
from django.contrib.auth.models import User

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
    projects = models.ManyToManyField("Project", related_name="engineers")
    fname = models.CharField(max_length=255)
    mname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.fname} {self.mname} {self.lname}"


class Collector(models.Model):
    projects = models.ManyToManyField("Project", related_name="collectors")
    engineer = models.ForeignKey('Engineer', on_delete=models.PROTECT, null=True)
    fname = models.CharField(max_length=100)
    mname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=False)
    
    def __str__(self):
        return f"{self.fname} {self.mname}"



class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name


class Productivity(models.Model):
    collector = models.ForeignKey("Collector", on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    particular = models.ForeignKey('particular.Particular', on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    unit = models.CharField(max_length=100, null=True, blank=True)
    instance = models.ForeignKey('DataInstance', on_delete=models.CASCADE, null=True, blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    # mpdm_delay = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    # mpdm_code = models.CharField(max_length=100, null=True, blank=True)


class BaseForm(models.Model):
    particular = models.ForeignKey('particular.Particular', on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    submitted_by = models.ForeignKey('Collector', on_delete=models.SET_NULL, null=True)
    encoded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data_count = models.PositiveIntegerField(default=0)
    number_of_equipment_types = models.PositiveIntegerField(default=0, null=True, blank=True)
    number_of_crews = models.PositiveIntegerField(default=0, null=True, blank=True)
    time_unit = models.CharField(max_length=20, null=True, blank=True)
    task_type = models.CharField(max_length=255, null=True, blank=True)
    operation = models.CharField(max_length=255, null=True, blank=True)
    equipment = models.CharField(max_length=255, null=True, blank=True)
    crew_tag = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True


class Equipment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class EquipmentBaseForm(models.Model):
    date = models.DateField(null=True, blank=True)
    particular = models.ForeignKey('particular.Particular', on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True, blank=True)
    submitted_by = models.ForeignKey('Collector', on_delete=models.SET_NULL, null=True)
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE, blank=True, null=True)
    equipment = models.CharField(max_length=255, null=True, blank=True)
    equipment_tag = models.CharField(max_length=100, null=True, blank=True)
    manpower = models.TextField(null=True, blank=True)

    encoded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data_count = models.PositiveIntegerField(default=0)
    number_of_equipment_types = models.PositiveIntegerField(default=0, null=True, blank=True)

    time_unit = models.CharField(max_length=20, null=True, blank=True)
    task_type = models.CharField(max_length=255, null=True, blank=True)
    task_description = models.TextField(null=True, blank=True)
    soil_type = models.CharField(max_length=255, null=True, blank=True)
    operation = models.CharField(max_length=255, null=True, blank=True)

    # productivity
    productivity = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    # mpdm form
    environment_delay = models.IntegerField(default=0)
    equipment_delay = models.IntegerField(default=0)
    labor_delay = models.IntegerField(default=0)
    material_delay = models.IntegerField(default=0)
    management_delay = models.IntegerField(default=0)
    other_delay = models.IntegerField(default=0)
    other_label = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True

class Excavator(EquipmentBaseForm):
    excavator_type = models.CharField(max_length=20)
    bucket_fill_factor = models.FloatField()
    swing_angle = models.FloatField()
    cut_depth = models.FloatField()
    volume_correction = models.FloatField()
    efficiency = models.FloatField(default=1)
    
    total_cycle = models.PositiveIntegerField()
    q_heaped_bucket_capacity = models.DecimalField(max_digits=6, decimal_places=2)

    def save(self, *args, **kwargs):
        # Ensure total_cycle is the sum of all cycles
        if self.time_unit.lower().startswith('minutes'):
            self.productivity = (3600 * self.total_cycle * self.bucket_fill_factor * self.efficiency) / (self.volume_correction*self.total_cycle)
        elif self.time_unit.lower().startswith('seconds'):
            # computer AS:D correction factor
            asd = 1
            self.productivity = (3600 * self.total_cycle * self.bucket_fill_factor * self.efficiency) / (self.volume_correction*self.total_cycle * 60)

        else:
            raise Exception(f"Can't compute productivity with this value of capacity: {self.q_heaped_bucket_capacity} and cycle time of {self.total_cycle} ")
        super().save(*args, **kwargs)


class Dozer(EquipmentBaseForm):
    blade_type = models.CharField(max_length=20)
        
    # blade load measurements
    blade_height = models.FloatField()
    blade_width = models.FloatField()
    blade_length = models.FloatField()
    blade_load = models.DecimalField(max_digits=6, decimal_places=2)
    total_cycle = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        # calculate blade load
        self.blade_load = self.blade_height * self.blade_width * self.blade_length
        # Ensure total_cycle is the sum of all cycles
        if self.time_unit.lower().startswith('minutes'):
            self.productivity = self.blade_load * 3600 / (self.total_cycle*0.764555*60)
        elif self.time_unit.lower().startswith('seconds'):
            # computer AS:D correction factor
            self.productivity = self.blade_load * 3600 / (self.total_cycle*0.764555*60)
        else:
            raise Exception(f"Can't compute productivity with this value of capacity: {self.blade_load} and cycle time of {self.total_cycle} ")
        
        super().save(*args, **kwargs)


class ProblemCode(models.Model):
    category = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.description}"


class LaborCrew(BaseForm):
    location = models.CharField(max_length=255, null=True)
    crew_size = models.PositiveIntegerField()
    crew_composition = models.TextField()

    # manhours
    work_hours = models.FloatField(default=8)
    ot_work_hours = models.FloatField(default=0)
    total_work_hours = models.FloatField(default=0)
    total_manhours = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=20)
    daily_units_completed = models.CharField(max_length=255)
    task_weight = models.DecimalField(max_digits=6, decimal_places=2)
    effort_level = models.DecimalField(max_digits=6, decimal_places=2)
    completed_unit = models.DecimalField(max_digits=6, decimal_places=2)
    
    problem_codes = models.ManyToManyField('ProblemCode')


    def save(self, *args, **kwargs):
        try:
            self.total_manhours = self.work_hours + self.ot_work_hours
            self.total_manhours = self.total_work_hours * self.crew_size
            self.completed_unit = self.daily_units_completed * self.task_weight*self.effort_level

            self.completed_unit = self.daily_units_completed * self.task_weight * self.effort_level
            self.productivity = self.completed_unit / self.total_manhours

        except Exception as e:
            raise e
            self.completed_unit = 0

        super().save(*args, **kwargs)


class WorkSampling(BaseForm):
    crew = models.ForeignKey('LaborCrew', on_delete=models.CASCADE)
    observation_number = models.PositiveIntegerField()
    observation_time = models.TimeField()

    # observation
    direct = models.PositiveIntegerField(default=0)
    preparatory = models.PositiveIntegerField(default=0)
    tools_and_equipment = models.PositiveIntegerField(default=0)
    material_handling = models.PositiveIntegerField(default=0)
    waiting = models.PositiveIntegerField(default=0)
    travel = models.PositiveIntegerField(default=0)
    personal = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    comments = models.TextField()

    def save(self, *args, **kwargs):
        try:
            self.total = self.direct + self.preparatory + self.tools_and_equipment + self.material_handling + self.waiting + self.travel + self.personal
        except Exception as e:
            raise e
        
        super().save(*args, **kwargs)
    

# choice varaibles for daily variables form
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

class DailyVariables(BaseForm):
    # date = models.DateField(auto_now_add=True)
    # collector = models.ForeignKey("Collector", on_delete=models.CASCADE)
    # particular = models.ForeignKey('particular.Particular', on_delete=models.CASCADE)
    # project = models.ForeignKey('Project', on_delete=models.CASCADE)

    # crew Properties
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


class MPDM(BaseForm):
    # equipment = models.ForeignKey()
    cycle_number = models.PositiveIntegerField()
    cycle_time = models.PositiveIntegerField()
    environment_delay = models.IntegerField()
    equipment_delay = models.IntegerField()
    labor_delay = models.IntegerField()
    material_delay = models.IntegerField()
    management_delay = models.IntegerField()
    other_delay = models.IntegerField()
    other_label = models.CharField(max_length=255, null=True, blank=True)

    # class Meta:
    #     abstract = True


class Tipper(EquipmentBaseForm):
    cycle_number = models.PositiveIntegerField(default=1)
    truck_license_plate = models.CharField(max_length=20, null=True, blank=True)
    load_cyle = models.PositiveIntegerField(null=True)
    haul_cyle = models.PositiveIntegerField(null=True)
    dump_cycle = models.PositiveIntegerField(null=True)
    return_cyle = models.PositiveIntegerField(null=True)
    total_cycle = models.PositiveIntegerField(default=0)
    heaped_bucket_capacity = models.DecimalField(max_digits=6, decimal_places=2, default=0)
   

    def save(self, *args, **kwargs):
        # Ensure total_cycle is the sum of all cycles
        if self.time_unit.lower().startswith('minute'):
            self.productivity = (self.heaped_bucket_capacity) / (self.total_cycle * 60)
        elif self.time_unit.lower().startswith('second'):
            self.productivity = (self.heaped_bucket_capacity) / (self.total_cycle)
        else:
            raise Exception(f"Can't compute productivity with this value of capacity: {self.heaped_bucket_capacity} and cycle time of {self.total_cycle} ")
        super().save(*args, **kwargs)
    

    def __str__(self):
        return f"Cycle {self.cycle_number} - {self.soil_type} - {self.total_cycle} {self.time_unit}"


class FormType(models.Model):
    FormTypeChoices = [
        ('dozer', 'Dozer'),
        ('excavator', 'Excavator'),
        ('tipper', 'Tipper'),
        ('mpdm', 'MPDM'),
        ('labor', 'Labor'),
        ('ws', 'Work Sampling'),
        ('dv', 'Daily Variables'),
        ('project', 'Project Details'),
    ]

    form_name = models.CharField(max_length=100, unique=True, choices=FormTypeChoices,)
    particular = models.ForeignKey('particular.Particular', on_delete=models.CASCADE, related_name='particular_forms')
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE, related_name='work_equipment_forms', null=True, blank=True)
    description = models.TextField(blank=True)
    # file = models.FileField(upload_to='particular_forms/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Form for {self.particular.pid} - {self.form_name}"
    

def instance_raw_file_path(instance, filename):
    return f"instances/{instance.particular.pid}/raw/{filename}"

def instance_encoded_file_path(instance, filename):
    return f"instances/{instance.particular.pid}/encoded/{filename}"


class DataInstance(models.Model):
    from particular.models import Particular

    class InstanceChoices(models.TextChoices):
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'
        PENDING = 'pending', 'Pending'

    project = models.ForeignKey('Project', on_delete=models.PROTECT, related_name='instance_project')
    project_type = models.ForeignKey('particular.ProjectType', on_delete=models.CASCADE, related_name="project_type", null=True)
    collector = models.ForeignKey('Collector', on_delete=models.CASCADE, related_name='data_collector')
    engineer = models.ForeignKey('Engineer', on_delete=models.CASCADE, related_name="assigned_engineer", null=True)
    particular = models.ForeignKey(Particular, on_delete=models.CASCADE, related_name='instance_particular')
    date = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=15, choices=InstanceChoices, default=InstanceChoices.PENDING)
    encoded = models.BooleanField(default=False)
    # encoder = models.CharField(max_length=255)
    encoded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='encoder')
    review_comments = models.TextField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewer')

    raw_file = models.FileField(upload_to=instance_raw_file_path, null=True, blank=True)
    encoded_file = models.FileField(upload_to=instance_encoded_file_path, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["date", "particular", "collector", "project"],
                name="unique_instance"
            )
        ]


