# Generated by Django 4.0.3 on 2022-03-01 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SportWow_app', '0004_team_league'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='points',
            field=models.CharField(blank=True, default=0, max_length=3, null=True),
        ),
    ]