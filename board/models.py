from django.db import models

# Create your models here.

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class Board(models.Model):
    like = models.ManyToManyField(User, related_name='likes',
                                  blank=True)
    director = models.CharField(max_length=200)
    title = models.CharField(max_length=500)
    contents = models.TextField()
    cast = models.TextField()
    creat_date = models.DateTimeField(auto_now_add=False)