from django.contrib.auth.models import User
from django.db import models
from board.models import Board

class Comment(models.Model):
    like = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    title = models.CharField(max_length=200)
    contents = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)  # 유저가 탈퇴하면 댓글도 삭제됨. writer_id로 호출
    board = models.ForeignKey(Board, on_delete=models.CASCADE)  # 게시글이 사라지면 댓글도 삭제됨. board_id로 호출
    create_date = models.DateTimeField(auto_now_add=True)
