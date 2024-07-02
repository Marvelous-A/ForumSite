# Generated by Django 5.0.4 on 2024-06-30 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_chat_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='chapter',
            new_name='chapter_model',
        ),
        migrations.AddField(
            model_name='chapter',
            name='topics',
            field=models.ManyToManyField(to='forum.topic'),
        ),
    ]