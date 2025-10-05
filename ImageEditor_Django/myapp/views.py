from django.shortcuts import render, redirect
from .form import ImageUploadForm, EditOptionsForm
from .models import ImageUpload
import cv2
import numpy as np
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import io

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_images')  # Adjust 'view_images' with your actual URL name
    else:
        form = ImageUploadForm()
    return render(request, 'myapp/upload_image.html', {'form': form})

def view_image(request):
    images = ImageUpload.objects.all()  # Fetching all uploaded images
    return render(request, 'myapp/view_image.html', {"images": images})

def edit_options(request):
    images = ImageUpload.objects.all()  # Fetching images to display

    if request.method == 'POST':
        form = EditOptionsForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data.get('comment')  # Optional comment

            width = form.cleaned_data.get('width')
            height = form.cleaned_data.get('height')
            scale = form.cleaned_data.get('scale')
            interpolation_method = form.cleaned_data.get('interpolation')

            # Map string choice to OpenCV interpolation constants
            interpolation_map = {
                'INTER_LINEAR': cv2.INTER_LINEAR,
                'INTER_CUBIC': cv2.INTER_CUBIC,
                'INTER_NEAREST': cv2.INTER_NEAREST,
                'INTER_LANCZOS4': cv2.INTER_LANCZOS4,
            }
            interpolation = interpolation_map[interpolation_method]

            # Get the first image (modify this to target a specific image)
            image_instance = images.first()

            if image_instance:
                # Load the image from the filesystem using OpenCV
                image_path = image_instance.image.path
                img = cv2.imread(image_path)

                if img is not None:
                    # Handle resizing
                    if scale:
                        # Resize based on scale
                        resized_image = cv2.resize(img, None, fx=scale, fy=scale, interpolation=interpolation)
                    elif width and height:
                        # Resize based on width and height
                        resized_image = cv2.resize(img, (width, height), interpolation=interpolation)
                    elif width:  # If only width is provided, calculate proportional height
                        aspect_ratio = img.shape[1] / img.shape[0]
                        height = int(width / aspect_ratio)
                        resized_image = cv2.resize(img, (width, height), interpolation=interpolation)
                    elif height:  # If only height is provided, calculate proportional width
                        aspect_ratio = img.shape[1] / img.shape[0]
                        width = int(height * aspect_ratio)
                        resized_image = cv2.resize(img, (width, height), interpolation=interpolation)

                    # Save the resized image
                    is_success, buffer = cv2.imencode(".jpg", resized_image)
                    import os

                    if is_success:
                        # Create a buffer for the new image
                        io_buf = io.BytesIO(buffer)
                        
                        # Construct the new image name
                        new_image_name = f"{image_instance.image.name.split('/')[-1].split('.')[0]}_resized.jpg"
                        print("New Name is:", new_image_name)

                        # Delete the old image file
                        old_image_path = image_instance.image.path
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)

                        # Save the new image
                        image_instance.image.save(new_image_name, ContentFile(io_buf.getvalue()))
                        
                        # Save the instance to update the database
                        image_instance.save()

                        # Clear the buffer (optional, not usually needed as it will be garbage collected)
                        io_buf.close()


                        return redirect('edit_images')  # Redirect to show modified images

    else:
        form = EditOptionsForm()  # Initialize the form for a GET request

    return render(request, 'myapp/edit_image.html', {'form': form, 'images': images})
