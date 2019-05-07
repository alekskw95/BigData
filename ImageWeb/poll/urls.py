from django.urls import path
from .views import *
from .addImages import *
from .addBigImage import *
from .addKafelek import *

urlpatterns = [
    path('', home, name='home'),
    path('uploadImages/', add_images, name='uploadImages'),
    path('upload_Big_Image/', add_big_image, name='upload_Big_Image'),
    path('show_big_image/', show_image, name='show_big_image'),
    path('set_kafelek/', myView, name='set_kafelek'),
]
