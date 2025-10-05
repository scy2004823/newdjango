from django.urls import path
from .views import upload_image, view_image,edit_options

urlpatterns = [
    path('upload/', upload_image, name='upload_image'),
    path('view/', view_image, name='view_images'),  # URL for displaying uploaded images
    path('edit/', edit_options, name='edit_images'),  
]
