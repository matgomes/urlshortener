from django import forms
from django.core.validators import RegexValidator

class myForm(forms.Form):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

    url = forms.URLField(widget = forms.TextInput(attrs={'class':'input'}))
    custom = forms.CharField(required  = False, widget = forms.TextInput(attrs={'class':'input'}), validators=[alphanumeric])
