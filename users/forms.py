from django import forms
from .models import Mail

class Mail(forms.ModelForm):

    class Meta:
        model = Mail
        fields = ('tokens',)