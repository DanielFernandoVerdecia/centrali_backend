# Generated by Django 5.0 on 2024-01-11 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0006_alter_ventas_fecha_actualizacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info_ventas',
            name='descripcion',
            field=models.TextField(),
        ),
    ]
