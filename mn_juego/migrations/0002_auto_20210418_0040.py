# Generated by Django 3.0 on 2021-04-18 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mn_juego', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidatura',
            name='facebook',
            field=models.URLField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='candidatura',
            name='instagram',
            field=models.URLField(blank=True, default=None, null=True),
        ),
    ]