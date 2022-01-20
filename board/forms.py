from django import forms
from .models import Board

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields= ('title', 'opening_date', 'director', 'cast', 'cast2', 'cast3', 'cast4' , 'contents')