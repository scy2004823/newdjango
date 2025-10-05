# editor/views.py
from django.shortcuts import render, redirect
from .forms import PDFUploadForm
from .models import PDF
import fitz  # PyMuPDF
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

def home(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'pdf_id': form.instance.id})
        else:
            return JsonResponse({'success': False})
    else:
        form = PDFUploadForm()
    return render(request, 'editor/home.html', {'form': form})


def edit_pdf(request, pdf_id):
    pdf = get_object_or_404(PDF, pk=pdf_id)
    return render(request, 'editor/edit_pdf.html', {'pdf': pdf})



def save_pdf(request, pdf_id):
    if request.method == 'POST':
        pdf = get_object_or_404(PDF, pk=pdf_id)
        canvas_data = request.POST.get('canvas')
        pdf.canvas_data = canvas_data
        pdf.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)