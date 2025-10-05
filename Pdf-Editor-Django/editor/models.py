# editor/models.py
from django.db import models

class PDF(models.Model):
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    canvas_data = models.TextField(blank=True, null=True)