from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # Define the root path
    path('upload/', views.upload_image, name='upload_image'),  # Correct function name
]   
