from django.contrib.auth.models import User
from django.db import models
from board.models import Board

# 데이터베이스에 저장될 댓글 클래스
class Comment(models.Model):
    like = models.ManyToManyField(User, related_name='comment_likes', blank=True)   # 좋아요
    title = models.CharField(max_length=200)                                        # 댓글제목
    contents = models.TextField()                                                   # 댓글내용
    writer = models.ForeignKey(User, on_delete=models.CASCADE)  # 작성자. 유저가 탈퇴하면 댓글도 삭제됨. writer_id로 호출
    board = models.ForeignKey(Board, on_delete=models.CASCADE)  # 댓글이 달린 게시글. 게시글이 사라지면 댓글도 삭제됨. board_id로 호출
    create_date = models.DateTimeField(auto_now_add=True)       # 댓글 생성일. 사용하지 않음.
