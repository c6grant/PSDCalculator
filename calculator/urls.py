from django.urls import path
# from django.conf.urls import url

from .views import indexPageView, runClusterView, runTaskView, addTaskView, deleteTaskView, testClusterView

urlpatterns = [
    path("", indexPageView, name="index"),
    path("clustered/", runClusterView, name="runClust"),
    path("tasks/", runTaskView, name="runTask"),
    path("addTask/", addTaskView, name='addTask'),
    path("deleteTask/<int:pk>", deleteTaskView, name='deleteTask'),
    path('testCluster', testClusterView, name='testCluster')
]



    # url(r'login/$', login, name='cas-login'),
