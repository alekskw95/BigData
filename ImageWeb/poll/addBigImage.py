from django.shortcuts import render, redirect
from .forms import *
from .connectDB import *


def add_big_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        images_db = server['imagesdb']
        images_doc = images_db['image']
        images_db.put_attachment(images_doc, form['image'].value(), 'big_image', 'image/png')
        images_db.commit()
        return redirect('home')
    else:
        form = ImageForm()
    return render(request, 'bigImage.html', {'form': form})