from django import forms
from .models import Comment

# 댓글 작성, 수정 양식
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('title', 'contents')
# 제목, 내용