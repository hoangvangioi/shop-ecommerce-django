# Generated by Django 4.0.2 on 2022-03-17 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donate', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bank',
            name='image_bank',
        ),
    ]