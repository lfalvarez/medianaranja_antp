# Generated by Django 3.0 on 2021-04-21 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mn_juego', '0002_auto_20210418_0040'),
    ]

    operations = [
        migrations.AddField(
            model_name='distrito',
            name='link_compromiso_inclusion',
            field=models.URLField(default='https://ahoranostocaparticipar.cl/processes/espaciocompromisos/f/128/proposals/8'),
        ),
        migrations.AddField(
            model_name='distrito',
            name='link_compromiso_participacion',
            field=models.URLField(default='https://ahoranostocaparticipar.cl/processes/espaciocompromisos/f/128/proposals/7'),
        ),
    ]
