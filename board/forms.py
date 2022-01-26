from django import forms
from .models import Board

# 영화 게시글 작성, 수정 양식
class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields= ('title', 'opening_date', 'director', 'cast', 'cast2', 'cast3', 'cast4', 'contents', 'poster')
        # 제목, 개봉일, 감독, 배우, 배우2, 배우3, 배우4, 내용

