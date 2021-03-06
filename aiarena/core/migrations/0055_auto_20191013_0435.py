# Generated by Django 2.1.7 on 2019-10-12 18:05

import aiarena.core.models
import aiarena.core.storage
from django.db import migrations, models
import django.db.models.deletion

from aiarena.core import models as core_models


def create_first_season(apps, schema_editor):
    Season = apps.get_model('core', 'Season')
    Round = apps.get_model('core', 'Round')
    if Round.objects.count() > 0:  # if there are existing rounds, create a season for them
        season = Season.objects.create()


def transfer_bot_elo(apps, schema_editor):
    Season = apps.get_model('core', 'Season')
    Bot = apps.get_model('core', 'Bot')
    SeasonElo = apps.get_model('core', 'SeasonElo')
    for bot in Bot.objects.filter(active=True):
        SeasonElo.objects.create(season_id=1, bot=bot, elo=bot.elo)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0054_auto_20191012_1606'),
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_opened', models.DateTimeField(blank=True, null=True)),
                ('date_closed', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('created', 'Created'), ('paused', 'Paused'), ('open', 'Open'), ('closed', 'Closed')], default='created', max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='SeasonElo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elo', models.SmallIntegerField(default=1600)),
            ],
        ),
        migrations.AddField(
            model_name='seasonelo',
            name='bot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Bot'),
        ),
        migrations.AddField(
            model_name='seasonelo',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Season'),
        ),
        migrations.RunPython(create_first_season),
        migrations.RunPython(transfer_bot_elo),
        migrations.RemoveField(
            model_name='bot',
            name='elo',
        ),
        migrations.AlterField(
            model_name='map',
            name='file',
            field=models.FileField(storage=aiarena.core.storage.OverwriteStorage(), upload_to=core_models.map.map_file_upload_to),
        ),
        migrations.AddField(
            model_name='round',
            name='season',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.Season'),
            preserve_default=False,
        ),
    ]
