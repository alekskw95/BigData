from django.shortcuts import render
from .image_operations import *
from .connectDB import *
from .forms import ShowImageForm


def show_image(request):
    if request.method == 'POST':
        form = ShowImageForm(request.POST)
        if form.is_valid():
            sizeK = int(form.cleaned_data['sizeKafelek'])

            images_doc = server['big_image']
            # zmieniamy rozmiar naszego duzego obrazka
            old_width, old_height, new_image_name = resize_picture(images_doc, 'big_image', sizeK)#, height)

            complete_image = [[0 for _ in range(old_height)] for _ in range(old_width)]
            new_image = server.get_attachment(images_doc, new_image_name)

            complete_image = big_picture_rgb(new_image, complete_image, sizeK,  old_width, old_height)

            view = server.view('images_db/rgb')

            images = get_images_from_view(view, sizeK, complete_image)
            ia = Image.new('RGB', (old_width * sizeK, old_height * sizeK))
            for i in range(0, old_width):
                for j in range(0, old_height):
                    ia.paste(images[complete_image[i][j]], (i * sizeK, j * sizeK + j))

            image_io = io.BytesIO()
            ia.save(image_io, 'PNG')
            server.put_attachment(images_doc, image_io.getvalue(), 'mosaic', 'image/png')
            return render(request, 'showImage.html',
                          {'image': 'http://localhost:5984/images/big_image/mosaic', 'has_content': True})
    else:
        form = ShowImageForm()
    return render(request, 'showImage.html', {'has_content': False, 'form': form})