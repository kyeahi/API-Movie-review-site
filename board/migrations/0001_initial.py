# Generated by Django 4.0.1 on 2022-01-21 05:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('contents', models.TextField()),
                ('director', models.CharField(max_length=50)),
                ('cast', models.CharField(blank=True, max_length=50)),
                ('cast2', models.CharField(blank=True, max_length=50)),
                ('cast3', models.CharField(blank=True, max_length=50)),
                ('cast4', models.CharField(blank=True, max_length=50)),
                ('opening_date', models.TextField(max_length=50)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('poster', models.CharField(blank=True, max_length=200)),
                ('like', models.ManyToManyField(blank=True, related_name='board_likes', to=settings.AUTH_USER_MODEL)),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]