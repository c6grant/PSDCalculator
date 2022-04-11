from django.contrib import admin
from .models import DeliverableType, Priority, ProductionPipeline, ProjectType, Task, StoredTask

# Register your models here.
admin.site.register(DeliverableType)
admin.site.register(Priority)
admin.site.register(ProductionPipeline)
admin.site.register(ProjectType)
admin.site.register(Task)
admin.site.register(StoredTask)