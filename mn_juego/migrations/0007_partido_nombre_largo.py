# Generated by Django 3.0 on 2021-05-07 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mn_juego', '0006_remove_distrito_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='partido',
            name='nombre_largo',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
