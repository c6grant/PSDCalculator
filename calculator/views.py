from django.shortcuts import render
from django.http import HttpResponse
from .models import DeliverableType, Priority, ProductionPipeline, ProjectType, Task, StoredTask
import pickle
import pandas as pd
from keras.models import load_model




# Create your views here.
def indexPageView(request) :
    
    delivTypes = DeliverableType.objects.all()
    priorities = Priority.objects.all()
    prodPipelines = ProductionPipeline.objects.all()
    projTypes = ProjectType.objects.all()
    tasks = Task.objects.all()



    context = {
        'delivTypes': delivTypes,
        'priorities': priorities,
        'prodPipelines': prodPipelines,
        'projTypes': projTypes,
        'tasks': tasks

    }

    return render(request, 'index.html', context)


def runClusterView(request):

    if request.method == 'POST':


        delivTypeInput = request.POST.get('delivType')
        priorityInput = request.POST.get('priority')
        pipelineInput = request.POST.get('pipeline')
        projTypeInput = request.POST.get('projType')

        output = str(delivTypeInput)
        

        delivTypes = DeliverableType.objects.all()
        priorities = Priority.objects.all()
        prodPipelines = ProductionPipeline.objects.all()
        projTypes = ProjectType.objects.all()




        context = {
            'delivTypes': delivTypes,
            'priorities': priorities,
            'prodPipelines': prodPipelines,
            'projTypes': projTypes,
            'output': output

        }


    return render(request, 'output.html', context)




def runTaskView(request):

    tasks = Task.objects.all()
    storedTasks = StoredTask.objects.all()



    context = {

        'tasks': tasks,
        'storedTasks': storedTasks

    }

    return render(request, 'tasks.html', context)


def addTaskView(request):


    tasks = Task.objects.all()
    storedTasks = StoredTask.objects.all()



    taskInput = request.POST.get('task')
    newTask = Task.objects.get(task=taskInput)
    
    newStoredTask = StoredTask(task=newTask.task, group=newTask.group)
    newStoredTask.save()


    context = {

        'tasks': tasks,
        'storedTasks': storedTasks,
        'taskInput': taskInput

    }



    return render(request, 'tasks.html', context)


def deleteTaskView(request, pk):



    # taskInput = request.POST.get('storTask')

    deleteStoredTask = StoredTask(id=pk)
    deleteStoredTask.delete()




    tasks = Task.objects.all()
    storedTasks = StoredTask.objects.all()

    context = {

    'tasks': tasks,
    'storedTasks': storedTasks,

    }


    return render(request, 'tasks.html', context)


def testClusterView(request):


    # Load in model
    model = pickle.load(open('psdcalculator/static/ml/aggClust.sav', "rb"))

    # Load in DF
    X = pd.read_csv('psdcalculator/static/ml/X.csv')

    #Grab variables from form
    delivTypeInput = request.POST.get('delivType')
    delivTypeInput = DeliverableType.objects.get(delivtype=delivTypeInput).mlModel


    priorityInput = request.POST.get('priority')
    priorityInput = Priority.objects.get(priority=priorityInput).mlModel

    
    pipelineInput = request.POST.get('pipeline')
    pipelineInput = ProductionPipeline.objects.get(pipeline=pipelineInput).mlModel

    
    projTypeInput = request.POST.get('projType')
    projTypeInput = ProjectType.objects.get(projtype=projTypeInput).mlModel

    # Grab Task Count
    taskCount = StoredTask.objects.all()
    taskCount = len(taskCount)

    # Initializing Array
    clustModelInput = [delivTypeInput, priorityInput, pipelineInput, projTypeInput, taskCount]

    # Add in new data to end of DF
    X.loc[len(X.index)] = clustModelInput

    # Run model
    fitModel = model.fit_predict(X, y=None)

    # Grab last value
    clustOutput = fitModel[-1]




    ##################################################
    # EACH TASKS COUNTS


    eachTaskCount = []

    for i in range(19):
        
        x = i+1

        numTask = StoredTask.objects.filter(group=x)

        numTask = len(numTask)

        eachTaskCount.append(numTask)


    ###################################################

    # DNN

    model = load_model('psdcalculator/static/ml/nn_model_split_tasks.h5')

    inputs = [delivTypeInput, priorityInput, pipelineInput, projTypeInput]

    for i in eachTaskCount:
        inputs.append(i)

    inputs.append(clustOutput)

    result = model.predict([inputs])[0][0]




    #################################################
    delivTypes = DeliverableType.objects.all()
    priorities = Priority.objects.all()
    prodPipelines = ProductionPipeline.objects.all()
    projTypes = ProjectType.objects.all()

    context = {
        'delivTypes': delivTypes,
        'priorities': priorities,
        'prodPipelines': prodPipelines,
        'projTypes': projTypes,
        'eachTaskCount': eachTaskCount,
        # 'output': output,
        # 'output2': output2,
        'testOutput': result

    }


    return render(request, 'output.html', context)