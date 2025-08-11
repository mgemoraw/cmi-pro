from django.db import models

# Create your models here.

class Tipper(models.Model):
    license_plate = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.license_plate

class CollectorModel(models.Model):
    fname = models.CharField(max_length=100)
    mname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    phone = models.CharField(unique=True)
    
    def __str__(self):
        return self.name
    
    
class TipperModel(models.Model):
    collector = models.ForeignKey('CollectorModel', on_delete=models.CASCADE)
    tipper = models.ForeignKey('Tipper', on_delete=models.CASCADE)