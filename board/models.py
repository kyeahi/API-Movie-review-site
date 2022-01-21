from django.contrib.auth.models import User
from django.db import models

# 데이터베이스에 저장될 영화게시글 클래스
class Board(models.Model):
    like = models.ManyToManyField(User, related_name='board_likes', blank=True) # 좋아요
    title = models.CharField(max_length=100)                                    # 영화제목
    contents = models.TextField()                                               # 영화내용
    director = models.CharField(max_length=50)                                  # 영화감독
    cast = models.CharField(max_length=50, blank=True)                          # 배우
    cast2 = models.CharField(max_length=50, blank=True)                         # 배우2
    cast3 = models.CharField(max_length=50, blank=True)                         # 배우3
    cast4 = models.CharField(max_length=50, blank=True)                         # 배우4
    writer = models.ForeignKey(User, on_delete=models.CASCADE)                  # 작성자. 작성자가 탈퇴하면 게시글도 삭제됨
    opening_date = models.TextField(max_length=50)                              # 영화개봉일
    create_date = models.DateTimeField(auto_now_add=True)                       # 게시글 작성일. 우리는 생성만 해뒀다. 사용x
    poster = models.ImageField(null=True, upload_to="images/", blank=True)      # 포스터

    def __str__(self):
        return self.title
