# Generated by Django 5.1.4 on 2025-01-17 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Datos', '0005_alter_divisionparcela_identificador'),
    ]

    operations = [
        migrations.AlterField(
            model_name='divisionparcela',
            name='identificador',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='divisionparcela',
            name='tipo_division',
            field=models.CharField(max_length=50),
        ),
    ]