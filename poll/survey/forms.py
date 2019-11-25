from django import forms
from .models import *




class userform(forms.Form):
    CHOICES = [('М', 'М'), ('Ж', 'Ж')]
    fullname = forms.CharField(max_length=200)
    age = forms.DateField()
    pol = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
        choices=CHOICES)
    specialite = forms.CharField(max_length=100)
    language = forms.CharField(max_length=100)
    survey = forms.ModelChoiceField(queryset=vibor_test.objects.all(),empty_label="танлаш")
