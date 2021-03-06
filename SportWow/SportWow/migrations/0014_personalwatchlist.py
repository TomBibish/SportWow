# Generated by Django 4.0.3 on 2022-03-08 08:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SportWow_app', '0013_alter_team_goals_against_alter_team_goals_for'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalWatchList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('League', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='SportWow_app.league')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='SportWow_app.team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
