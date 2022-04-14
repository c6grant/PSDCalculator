from django.urls import path
# from django.conf.urls import url

from .views import indexPageView, runTaskView, addTaskView, deleteTaskView, runModelView

urlpatterns = [
    path("", indexPageView, name="index"),
    path("tasks/", runTaskView, name="runTask"),
    path("addTask/", addTaskView, name='addTask'),
    path("deleteTask/<int:pk>", deleteTaskView, name='deleteTask'),
    path('runModel/', runModelView, name='runModel')
]

