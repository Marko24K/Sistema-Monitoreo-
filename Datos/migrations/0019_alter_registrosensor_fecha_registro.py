# Generated by Django 5.1.4 on 2025-01-14 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Datos', '0018_alter_registrosensor_fecha_registro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrosensor',
            name='fecha_registro',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
