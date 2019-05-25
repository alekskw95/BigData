from PIL import Image
from couchdb.client import ViewResults
from couchdb.mapping import Document

from .connectDB import *
import io
import math


def rgb_calculate(file, file_name):
    image = Image.open(file)
    width, height = image.size
    area = width * height
    r, g, b = 0, 0, 0
    rgb_image = image.convert('RGB')
    for w in range(1, width):
        for h in range(1, height):
            tr, tg, tb = rgb_image.getpixel((w, h))
            r, g, b = r + tr, g + tg, b + tb
    r, g, b = r / area, g / area, b / area
    image_in_bytes = io.BytesIO()
    image.save(image_in_bytes, format='PNG')
    return {
               'red': r,
               'green': g,
               'blue': b,
               '_id': file_name
           }, image_in_bytes.getvalue()


def resize_picture(images_doc: Document, file_name, sizeK,  is_big=True):
    old_photo = server.get_attachment(images_doc, '{0}.png'.format(file_name))
    image_in_bytes = io.BytesIO()
    image = Image.open(old_photo)
    old_photo_width, old_photo_height = image.size
    if is_big:
        new_photo_width, new_photo_height = sizeK * old_photo_width, sizeK * old_photo_height
    else:
        new_photo_width, new_photo_height = sizeK, sizeK
    image = image.resize((new_photo_width, new_photo_height))
    new_photo = Image.new('RGB', (new_photo_width, new_photo_height), 'WHITE')
    new_photo.paste(image)
    new_photo_filename = '{0}_{1}_{2}.png'.format(file_name, sizeK, sizeK)
    new_photo.save(image_in_bytes, 'PNG')
    server.put_attachment(images_doc, image_in_bytes.getvalue(), new_photo_filename, 'image/png')
    server.commit()
    return old_photo_width, old_photo_height, new_photo_filename


def big_picture_rgb(new_image, complete_image, sizeK, old_width, old_height):
    with Image.open(new_image) as image:
        image_rgb = image.convert('RGB')
        for i in range(0, old_width):
            for j in range(0, old_height):
                r, g, b, index = 0, 0, 0, 0
                for ix in range(1, sizeK):
                    for iy in range(1, sizeK):
                        tr, tg, tb = image_rgb.getpixel((sizeK * i + ix, sizeK * j + iy))
                        r, g, b = r + tr, g + tg, b + tb
                area = sizeK * sizeK
                r, g, b = r / area, g / area, b / area
                view = server.view('images_db/rgb')
                image_col_arr = view.rows
                min_compared = compare_images((r, g, b), image_col_arr[0].value)
                for ix in range(0, view.total_rows):
                    temp_min_compared = compare_images((r, g, b), image_col_arr[ix].value)
                    if temp_min_compared < min_compared:
                        min_compared = temp_min_compared
                        index = image_col_arr[ix].id
                complete_image[i][j] = index
    return complete_image


def get_images_from_view(view: ViewResults, sizeK, complete_image):
    flatten_array = [item for sublist in complete_image for item in sublist]
    temporary_list = list(dict.fromkeys(flatten_array))
    images = dict()
    rows = view.rows
    for i in range(0, view.total_rows):
        single_row_id = rows[i].id
        if single_row_id in temporary_list:
            attachment = server.get_attachment(single_row_id, 'image_{0}_{1}.png'.format(sizeK, sizeK))
            if attachment is None:
                images_doc = server[single_row_id]
                _, _, new_image_file = resize_picture(images_doc, 'image', sizeK,  False)
                attachment = server.get_attachment(images_doc, new_image_file)
            image = Image.open(attachment)
            images[str(single_row_id)] = image
    return images


def compare_images(a, b):
    return abs(a[0] - b['r']) + abs(a[1] - b['g']) + abs(a[2] + b['b'])