from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.exceptions import *

from .models import Document
from .forms import DocumentForm
from .forms import LoginForm
from .models import Login

import sys
import os, os.path
import random

from uploads.core.proj1.face_recognition import test, train


def home(request):
    documents = Document.objects.all()
    return render(request, 'core/home.html', { 'documents': documents })


def index(request):
    #with open('/home/nightingale/django_example/upload_1/simple-file-upload/uploads/core/templates/core/index.html', 'r') as myfile:
    #    data=myfile.read().replace('\n', '')
    #return HttpResponse(data)
    return render_to_response('core/index.html')

def reg(request):
    documents = Document.objects.all()
    return render(request, 'core/reg.html', { 'documents': documents }) 

def train_handler(request):
    train()
    return HttpResponseRedirect('http://127.0.0.1:8000/index/')


@csrf_exempt
def adobe_sample(request):
    if request.method == 'POST':
        img = settings.ML_ROOT + 'test/someimage.jpg'
        # save it somewhere
        f = open(settings.MEDIA_ROOT + 'someimage.jpg', 'wb')
        f.write(request.body)
        f.close()

        return HttpResponse(test('name', img))
    else:
        return HttpResponse('no data blyat')    


@csrf_exempt
def reg_handler(request):
    newpath = settings.ML_ROOT + 'train/krasavin'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    if request.method == 'POST':
        k = str(random.randint(1,1000))
        path = newpath + '/someimage_%s.jpg' % k
        # save it somewhere
        f = open(path, 'wb')
        f.write(request.body)
        f.close()

        return HttpResponse('ok!')
    else:
        return HttpResponse('no data')    

def loadlogin(request):
    if request.method == 'POST':
        get_text = request.POST["textfield"]
    return HttpResponseRedirect('http://127.0.0.1:8000/reg/')
