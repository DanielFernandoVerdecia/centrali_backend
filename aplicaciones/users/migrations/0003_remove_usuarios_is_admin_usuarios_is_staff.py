# Generated by Django 5.0 on 2023-12-10 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_usuarios_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuarios',
            name='is_admin',
        ),
        migrations.AddField(
            model_name='usuarios',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
