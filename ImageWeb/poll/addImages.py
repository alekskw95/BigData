from django.shortcuts import render, redirect
from flask import request
from .forms import *
from .connectDB import *


def add_images(request):
    if request.method == 'POST':
        images_db = server['imagesdb']
        images_doc = images_db['image']
        multiple_img = request.FILES.getlist('photos_multiple')
        count = len(multiple_img)
        for i in range(count):
            images_db.put_attachment(images_doc, multiple_img[i], 'image' + str(i), 'image/png')
            images_db.commit()
        return redirect('uploadImages')
    else:
        form = ImageForm()
    return render(request, 'uploadImages.html', {'form': form})
