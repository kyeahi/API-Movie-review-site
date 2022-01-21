from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Board(models.Model):
    like = models.ManyToManyField(User, related_name='board_likes', blank=True)
    poster = models.ImageField(null=True, upload_to="images/", blank=True)
    title = models.CharField(max_length=100)
    contents = models.TextField()
    director = models.CharField(max_length=50)
    cast = models.CharField(max_length=50, blank=True)
    cast2 = models.CharField(max_length=50, blank=True)
    cast3 = models.CharField(max_length=50, blank=True)
    cast4 = models.CharField(max_length=50, blank=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)  # 유저가 탈퇴하면 댓글도 삭제됨
#    board = models.ForeignKey(Board, on_delete=models.CASCADE)  # 게시글이 사라지면 댓글도 삭제됨
    opening_date = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# class FileUpload:
#     poster = models.ImageField(null=True, upload_to="", blank=True)
