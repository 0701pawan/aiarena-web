# Generated by Django 2.1.7 on 2019-07-25 20:27
import os

from django.db import migrations

from aiarena.scripts import run_usp_generate_stats_sql


def create_generate_stats(apps, schema_editor):
    run_usp_generate_stats_sql()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_auto_20190726_0547'),
    ]

    operations = [
        migrations.RunPython(create_generate_stats),
    ]
