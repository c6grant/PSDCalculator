from django.db import models

# Create your models here.
class DeliverableType(models.Model):
    delivtype = models.CharField(max_length=50)
    mlModel = models.IntegerField()

class Priority(models.Model):
    priority = models.CharField(max_length=30)
    mlModel = models.IntegerField()

class ProductionPipeline(models.Model):
    pipeline = models.CharField(max_length=30)
    mlModel = models.IntegerField()


class ProjectType(models.Model):
    projtype = models.CharField(max_length=30)
    mlModel = models.IntegerField()


class Task(models.Model):
    task = models.CharField(max_length=400)
    group = models.IntegerField()

class StoredTask(models.Model):
    task = models.CharField(max_length=400)
    group = models.IntegerField()