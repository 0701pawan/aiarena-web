# Generated by Django 2.1.7 on 2019-10-01 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0046_map_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='discord_tag',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='discord_user',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
