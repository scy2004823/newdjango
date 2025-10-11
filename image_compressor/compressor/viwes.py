from django.shortcuts import render
from .forms import ImageForm
from PIL import Image
from django.conf import settings
import os
from django.http import HttpResponse

def index(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            original_path = os.path.join(settings.MEDIA_ROOT, image.name)
            with open(original_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            img = Image.open(original_path)
            compressed_name = 'compressed_' + image.name
            compressed_path = os.path.join(settings.MEDIA_ROOT, compressed_name)
            if img.format == 'JPEG':
                img.save(compressed_path, 'JPEG', quality=50)
            else:
                img.save(compressed_path)
            return render(request, 'compressor/index.html', {'form': form, 'compressed_url': '/media/' + compressed_name})
    else:
        form = ImageForm()
    return render(request, 'compressor/index.html', {'form': form})