# Generated by Django 5.1.4 on 2025-01-17 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Datos', '0002_country_registroplanta_imagen_registro_planta_city_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='arduino',
            old_name='UUID_arduino',
            new_name='uuid_arduino',
        ),
        migrations.RenameField(
            model_name='divisionparcela',
            old_name='codigoQR',
            new_name='codigoqr',
        ),
        migrations.RenameField(
            model_name='parcela',
            old_name='UUID_parcela',
            new_name='uuid_parcela',
        ),
        migrations.RenameField(
            model_name='tipoplanta',
            old_name='UUID_tipo_planta',
            new_name='uuid_tipo_planta',
        ),
    ]