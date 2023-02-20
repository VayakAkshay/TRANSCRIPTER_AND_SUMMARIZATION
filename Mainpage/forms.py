from django import forms
from .models import Myfiles

class FileForm(forms.ModelForm):
    class Meta:
        model = Myfiles
        fields = ["my_file"]
        labels = {"my_file": ""}