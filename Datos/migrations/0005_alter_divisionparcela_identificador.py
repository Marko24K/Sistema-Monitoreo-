# Generated by Django 5.1.4 on 2025-01-17 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Datos', '0004_rename_observaciones_registro_registroplanta_observaciones_registro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='divisionparcela',
            name='identificador',
            field=models.CharField(max_length=50),
        ),
    ]
