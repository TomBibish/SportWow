# Generated by Django 4.0.3 on 2022-03-01 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SportWow_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='picture_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='picture_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
