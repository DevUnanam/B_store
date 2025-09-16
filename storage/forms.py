# storage/forms.py
from django import forms
from .models import StorageUnit

class StorageUnitForm(forms.ModelForm):
    class Meta:
        model = StorageUnit
        fields = ["name", "size", "location", "status"]
