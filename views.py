from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from .utils import process_image  # Import the updated function

def home(request):
    """
    Render the home page and pass context data from session if available.
    """
    context = {
        'uploaded_image_url': request.session.pop('uploaded_image_url', None),
        'image_text': request.session.pop('image_text', None),
        'translated_words': request.session.pop('translated_words', None),
    }
    return render(request, 'home.html', context)

def upload_image(request):
    """
    Handle image upload, process it, and redirect to the home page with results.
    """
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_image.name, uploaded_image)
        media_path = os.path.join(settings.MEDIA_ROOT, filename)

        try:
            translations = process_image(media_path)  # Process image with new function
            if "error" in translations:
                request.session['image_text'] = "Error processing the image."
                request.session['translated_words'] = {}
            else:
                request.session['uploaded_image_url'] = fs.url(filename)
                request.session['image_text'] = ' '.join(translations.keys())
                request.session['translated_words'] = translations
        except Exception as e:
            request.session['image_text'] = "Error processing the image."
            request.session['translated_words'] = {}

        return redirect('home')

    return render(request, 'home.html')
