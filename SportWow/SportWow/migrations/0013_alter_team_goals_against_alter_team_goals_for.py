# Generated by Django 4.0.3 on 2022-03-02 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SportWow_app', '0012_team_goals_against_team_goals_for'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='goals_against',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='goals_for',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
