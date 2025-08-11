from django.db import models

# Create your models here.
class ProjectType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name 


class Project(models.Model):
    name = models.CharField(max_length=255)
    project_type = models.ForeignKey('ProjectType', on_delete=models.CASCADE, related_name='project_type')
    description = models.TextField()

