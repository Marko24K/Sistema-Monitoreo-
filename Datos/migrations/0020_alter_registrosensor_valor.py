# Generated by Django 5.1.4 on 2025-01-15 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Datos', '0019_alter_registrosensor_fecha_registro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrosensor',
            name='valor',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
