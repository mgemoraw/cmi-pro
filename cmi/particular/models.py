from django.db import models

# Create your models here.

class DivisionModel(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)

    # particulars = models.ForeignKey('Particular', on_delete=models.CASCADE)

    def __str__(self):
        return f"Division {self.code} - {self.name}"
    

class ProjectType(models.Model):
    name: str = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    
class WorkEquipment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    unit = models.CharField(max_length=50, null=True)
    count = models.PositiveIntegerField(default=0)



    def save(self, *args, **kwargs):
        if self.pk is None: # only when creating a new equipment
            self.count += 1
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (Count: {self.count})"
    


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    equipments = models.ManyToManyField(
        'WorkEquipment', 
        through='TaskEquipment',
        related_name='tasks'
        )


class TaskEquipment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    equipment = models.ForeignKey(WorkEquipment, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    usage_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.equipment.name} for {self.task.name} ({self.quantity} units)"
    

class Particular(models.Model):
    pid = models.CharField(max_length=10, unique=True)
    division = models.ForeignKey('DivisionModel', on_delete=models.CASCADE)
    project_type = models.ForeignKey('ProjectType', on_delete=models.CASCADE)

    task = models.CharField(max_length=255)
    element = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    data_collection_days = models.IntegerField(default=80)
    collected_days = models.IntegerField(default=0)
    progress = models.FloatField(default=0.0)

    equipments = models.ManyToManyField('WorkEquipment', related_name='work_equipments')

    def save(self):
        self.progress = self.collected_days / self.data_collection_days * 100
    
        super().save()

    def __str__(self):
        return f"{self.pid}-{self.element} {self.name}"
