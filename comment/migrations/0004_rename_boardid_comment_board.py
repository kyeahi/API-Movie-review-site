# Generated by Django 4.0.1 on 2022-01-20 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_rename_board_comment_boardid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='boardid',
            new_name='board',
        ),
    ]
