# Generated by Django 5.1.4 on 2025-01-27 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Datos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='espacio',
            name='codigoqr',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='espacio',
            name='direccion_espacio',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='espacio',
            name='nombre_espacio',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='espacio',
            name='utm',
            field=models.CharField(max_length=100),
        ),
    ]
