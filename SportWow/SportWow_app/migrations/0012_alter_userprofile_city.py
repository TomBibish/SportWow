# Generated by Django 4.0.3 on 2022-03-29 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SportWow_app', '0011_alter_userprofile_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
