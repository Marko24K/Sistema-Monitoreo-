# Generated by Django 5.1.4 on 2025-01-10 13:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Datos', '0003_modelo_sensor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parcela',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('localidad_parcela', models.CharField(max_length=50)),
                ('nombre_parcela', models.CharField(max_length=50)),
                ('direccion_parcela', models.CharField(max_length=50)),
                ('zona', models.PositiveIntegerField()),
                ('hemisferio', models.CharField(choices=[('N', 'Norte'), ('S', 'Sur')], max_length=1)),
                ('easting', models.DecimalField(decimal_places=2, max_digits=10)),
                ('northing', models.DecimalField(decimal_places=2, max_digits=10)),
                ('UUID_parcela', models.IntegerField()),
                ('imagen_parcela', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Planta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion_planta', models.TextField()),
                ('observaciones_planta', models.TextField()),
                ('fecha_siembra', models.DateTimeField(auto_now_add=True)),
                ('fecha_extraccion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_planta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_comun', models.CharField(max_length=50)),
                ('nombre_cientifico', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
                ('UUID_tipo_planta', models.IntegerField()),
                ('imagen_tipo_planta', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Division_parcela',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_division', models.PositiveIntegerField()),
                ('identificador', models.PositiveIntegerField()),
                ('codigoQR', models.CharField(max_length=50)),
                ('parcela', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.parcela')),
            ],
        ),
        migrations.CreateModel(
            name='Arduino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo_arduino', models.CharField(max_length=50)),
                ('UUID_arduino', models.IntegerField()),
                ('estado', models.PositiveIntegerField()),
                ('parcela', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.parcela')),
            ],
        ),
        migrations.CreateModel(
            name='Registro_planta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_planta', models.PositiveIntegerField()),
                ('altura', models.FloatField()),
                ('largo', models.FloatField()),
                ('ancho', models.FloatField()),
                ('grosor', models.FloatField()),
                ('vigor', models.CharField(max_length=50)),
                ('turgencia', models.CharField(max_length=50)),
                ('vitalidad', models.CharField(max_length=50)),
                ('plaga_enfermedad', models.BooleanField(default=False)),
                ('descripcion_plaga_enfermedad', models.TextField(blank=True, null=True)),
                ('observaciones_Registro', models.TextField(blank=True, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('division_parcela', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.division_parcela')),
                ('planta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.planta')),
            ],
        ),
        migrations.AddField(
            model_name='planta',
            name='tipo_planta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.tipo_planta'),
        ),
    ]