# Generated by Django 5.1.4 on 2025-01-16 12:20

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ModeloSensor',
            fields=[
                ('id_modelo_sensor', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_sensor', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
            ],
            options={
                'db_table': 'modelo_sensor',
            },
        ),
        migrations.CreateModel(
            name='Parcela',
            fields=[
                ('id_parcela', models.AutoField(primary_key=True, serialize=False)),
                ('localidad_parcela', models.CharField(max_length=50)),
                ('nombre_parcela', models.CharField(max_length=50)),
                ('direccion_parcela', models.CharField(max_length=50)),
                ('zona', models.PositiveSmallIntegerField()),
                ('hemisferio', models.CharField(choices=[('N', 'Norte'), ('S', 'Sur')], max_length=1)),
                ('easting', models.DecimalField(decimal_places=2, max_digits=10)),
                ('northing', models.DecimalField(decimal_places=2, max_digits=10)),
                ('UUID_parcela', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('imagen_parcela', models.ImageField(blank=True, null=True, upload_to='imagenes_parcelas/')),
            ],
            options={
                'db_table': 'parcela',
            },
        ),
        migrations.CreateModel(
            name='Planta',
            fields=[
                ('id_planta', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion_planta', models.TextField()),
                ('observaciones_planta', models.TextField()),
                ('fecha_siembra', models.DateTimeField(auto_now_add=True)),
                ('fecha_extraccion', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'planta',
            },
        ),
        migrations.CreateModel(
            name='TipoDato',
            fields=[
                ('id_tipo_dato', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_dato', models.CharField(max_length=50)),
                ('unidad_medida', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'tipo_dato',
            },
        ),
        migrations.CreateModel(
            name='TipoPlanta',
            fields=[
                ('id_tipo_planta', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_comun', models.CharField(max_length=50)),
                ('nombre_cientifico', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
                ('UUID_tipo_planta', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('imagen_tipo_planta', models.ImageField(blank=True, null=True, upload_to='imagenes_tipo_plantas/')),
            ],
            options={
                'db_table': 'tipo_planta',
            },
        ),
        migrations.CreateModel(
            name='DivisionParcela',
            fields=[
                ('id_division_parcela', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_division', models.IntegerField()),
                ('identificador', models.IntegerField()),
                ('codigoQR', models.CharField(max_length=50)),
                ('id_parcela', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.parcela')),
            ],
            options={
                'db_table': 'division_parcela',
            },
        ),
        migrations.CreateModel(
            name='Arduino',
            fields=[
                ('id_arduino', models.AutoField(primary_key=True, serialize=False)),
                ('modelo_arduino', models.CharField(max_length=50)),
                ('estado', models.IntegerField()),
                ('UUID_arduino', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('id_parcela', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.parcela')),
            ],
            options={
                'db_table': 'arduino',
            },
        ),
        migrations.CreateModel(
            name='RegistroPlanta',
            fields=[
                ('id_registro_planta', models.AutoField(primary_key=True, serialize=False)),
                ('numero_planta', models.IntegerField()),
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
                ('id_division_parcela', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.divisionparcela')),
                ('id_planta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.planta')),
            ],
            options={
                'db_table': 'registro_planta',
            },
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id_sensor', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.IntegerField()),
                ('id_arduino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.arduino')),
                ('id_modelo_sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.modelosensor')),
            ],
            options={
                'db_table': 'sensor',
            },
        ),
        migrations.CreateModel(
            name='RegistroSensor',
            fields=[
                ('id_registro_sensor', models.AutoField(primary_key=True, serialize=False)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('id_sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.sensor')),
                ('id_tipo_dato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.tipodato')),
            ],
            options={
                'db_table': 'registro_sensor',
            },
        ),
        migrations.AddField(
            model_name='planta',
            name='id_tipo_planta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.tipoplanta'),
        ),
    ]
