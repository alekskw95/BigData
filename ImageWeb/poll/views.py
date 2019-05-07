from .addKafelek import *
from .connectDB import *
import io
import json
from django.shortcuts import render, redirect
from PIL import Image


def home(request):
    return render(request, 'home.html')


def big_images(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def show_image(request):
    if request.method == 'GET':
        images_db = server['imagesdb']
        images_doc = images_db['image']
        attachments_db = json.dumps(images_doc['_attachments'])
        attachments_as_json = json.loads(attachments_db)
        attachments = []
        attachments2 = []
        #big_file = images_db.get_attachment(images_doc, 'big_image')
        big_file2 = images_db.get_attachment(images_doc, 'big_image')
        img_coll_arr = []
        sizekafelek = int(images_doc['MyimageSize'])

        bH = 0
        bW = 0
        wynikowyW = 0
        wynikowyH = 0
        # for (k, v) in attachments_as_json.items():
        #     if k == 'big_image':
        #         with Image.open(images_db.get_attachment(images_doc, k)) as im:
        #             bW, bH = im.size
        with Image.open(big_file2) as img:
            bW, bH = img.size
            wynikowyW = sizekafelek * bW  # sizekafelek dajemy 20 to wynikowy 1200 x 800
            wynikowyH = sizekafelek * bH
            img = img.resize((wynikowyW, wynikowyH))
            imgnew = Image.new('RGB', (wynikowyW, wynikowyH), 'WHITE')
            imgnew.paste(img)
            imagei = io.BytesIO()
            imgnew.save(imagei, 'PNG')
            images_db.put_attachment(images_doc, imagei.getvalue(), 'big2_image', 'image/png')

        for (k, v) in attachments_as_json.items():
            if k != 'big_image' and k != 'mosaic':
                attachments.append(images_db.get_attachment(images_doc, k))
                attachments2.append(images_db.get_attachment(images_doc, k))
        complete_image = [[0 for x in range(bH)] for y in range(bW)]

        for i in range(len(attachments)):
            with Image.open(attachments[i]) as img:
                width, height = img.size
                r, g, b = 0, 0, 0
                rgb_im = img.convert('RGB')
                for w in range(1, width):
                    for h in range(1, height):
                        tr, tg, tb = rgb_im.getpixel((w, h))
                        r, g, b = r + tr, g + tg, b + tb
                area = width * height
                r, g, b = r / area, g / area, b / area
                img_coll_arr.append((r, g, b))

        big_file = images_db.get_attachment(images_doc, 'big2_image')

        with Image.open(big_file) as big:
            rgb_im = big.convert('RGB')
            for i in range(bW): #sizekafelek
                for j in range(bH): #sizekafelek
                    r, g, b = 0, 0, 0
                    for ix in range(1, sizekafelek):
                        for iy in range(1, sizekafelek):
                            tr, tg, tb = rgb_im.getpixel((sizekafelek * i + ix, sizekafelek * j + iy))
                            r, g, b = r + tr, g + tg, b + tb
                    x = 1024
                    r, g, b = r / x, g / x, b / x
                    index = 0
                    minimum_from_images = big_images((r, g, b), img_coll_arr[0])
                    for ix in range(len(attachments)):
                        temp_min = big_images((r, g, b), img_coll_arr[ix])
                        if temp_min < minimum_from_images:
                            minimum_from_images = temp_min
                            index = ix
                    complete_image[i][j] = index

        images = []
        for i in range(len(attachments)):
            image = Image.open(attachments2[i])
            image.thumbnail((sizekafelek, sizekafelek)) #tworzy miniaturki obrazkow danego rozmiaru np 4x4 z dostepnych obrazkow  w bazie
            #images_db.put_attachment(images_doc, image, 'obrazek' + str(i) + '_' + str(sizekafelek),'image/png')  # obrazek1_4
            #images_db.commit()
            images.append(image)

        new_image = Image.new('RGB', (wynikowyW, wynikowyH), 'BLACK')

        for i in range(bW):
            for j in range(bH):
                new_image.paste(images[complete_image[i][j]], (i * sizekafelek, j * sizekafelek + j))

        image_io = io.BytesIO()
        new_image.save(image_io, 'PNG')
        images_db.put_attachment(images_doc, image_io.getvalue(), 'mosaic', 'image/png')
        return render(request, 'show_big_image.html', {'image': 'http://localhost:5984/imagesdb/image/mosaic'})