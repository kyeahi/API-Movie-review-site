# Generated by Django 4.0.1 on 2022-01-20 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_comment_board_alter_comment_like'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='board',
            new_name='boardid',
        ),
    ]
