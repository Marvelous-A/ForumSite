# Generated by Django 5.0.2 on 2024-04-18 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_alter_topic_discription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='topics',
        ),
    ]