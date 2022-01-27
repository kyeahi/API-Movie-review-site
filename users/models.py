from django.db import models

# Create your models here.
class Mail(models.Model):
    tokens = models.CharField(max_length=100)