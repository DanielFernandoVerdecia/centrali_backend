# Generated by Django 5.0 on 2023-12-15 16:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='cantidad_disponible',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='productos',
            name='creador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='productos',
            name='fecha_actualizacion',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
