from django import forms
from django.contrib.admin.widgets import AdminDateWidget

class MyForm(forms.Form):
    my_date_field = forms.DateField(widget=AdminDateWidget)