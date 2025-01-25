from django.db import models
from django import forms

# Create your models here.
class imageUpload(forms.Form):
    image=forms.ImageField()
    