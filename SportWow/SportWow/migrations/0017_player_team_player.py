# Generated by Django 4.0.3 on 2022-03-10 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SportWow_app', '0016_teamplayer_appearances_teamplayer_assists_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='team_player',
            field=models.ManyToManyField(through='SportWow_app.TeamPlayer', to='SportWow_app.team'),
        ),
    ]
