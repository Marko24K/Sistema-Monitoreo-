# Generated by Django 5.1.4 on 2025-01-27 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Datos', '0002_alter_espacio_codigoqr_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arduino',
            name='estado',
            field=models.CharField(max_length=50),
        ),
    ]