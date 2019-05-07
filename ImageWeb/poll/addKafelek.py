from couchdb import json
from django.shortcuts import render
from flask import render_template
from django.shortcuts import render, redirect
from .forms import *
from .connectDB import *

scal2 = 40

def myFun(s):
    scal2 = s
    return scal2


# def myView(request):
#     inp_value = request.GET.get('next')
#     scal2 = request.POST.get('next')
#     return render(request, 'kafelek.html')

def myView(request):
    if request.method == 'GET':
        inp_value = request.GET.get('next')
        if inp_value is not None and inp_value != '':
            inp_value = request.GET.get('next')
            images_db = server['imagesdb']
            images_doc = images_db['image']  # { 'MyimageSize': inp_value}  #images_db['image']
            images_doc['MyimageSize'] = inp_value
            images_db.save(images_doc)
            images_db.commit()
        else:
            inp_value = 10
            images_db = server['imagesdb']
            images_doc = images_db['image'] #{ 'MyimageSize': inp_value}  #images_db['image']
            images_doc['MyimageSize'] = inp_value
            images_db.save(images_doc)
            images_db.commit()
    # else:
    #     inp_value = 10
    #     images_db = server['imagesdb']
    #     images_doc = images_db['image']
    #     images_doc['MyimageSize'] = inp_value
    #     images_db.commit()

    return render(request, 'kafelek.html')