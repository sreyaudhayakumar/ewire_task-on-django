# Generated by Django 5.0.6 on 2024-06-16 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='otp',
        ),
    ]