from django import forms
from .models import Product

class createform(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'features', 'category', 'seller', 'price', 'status', 'additional_info']

