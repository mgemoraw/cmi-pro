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

    def save(self):
        self.progress = self.collected_days / self.data_collection_days * 100
    
        super().save()

    def __str__(self):
        return f"{self.pid}-{self.element} {self.name}"
