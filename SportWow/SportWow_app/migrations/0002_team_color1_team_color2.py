# Generated by Django 4.0.3 on 2022-03-17 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SportWow_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='color1',
            field=models.CharField(default='white', max_length=128),
        ),
        migrations.AddField(
            model_name='team',
            name='color2',
            field=models.CharField(default='black', max_length=128),
        ),
    ]
