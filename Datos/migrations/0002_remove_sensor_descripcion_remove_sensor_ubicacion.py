# Generated by Django 5.1.4 on 2025-01-10 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Datos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensor',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='ubicacion',
        ),
    ]