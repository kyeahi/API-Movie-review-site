from django import forms
from .models import Board


class BoardForm2(forms.ModelForm):
    class Meta:
        model = Board
        fields= ('title', 'creat_date', 'director', 'cast' , 'contents')