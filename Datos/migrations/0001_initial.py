# Generated by Django 5.1.4 on 2025-02-07 13:37

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Arduino2',
            fields=[
                ('id_arduino', models.AutoField(primary_key=True, serialize=False)),
                ('modelo_arduino', models.CharField(max_length=50)),
                ('estado', models.IntegerField()),
                ('uuid_arduino', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
            options={
                'db_table': 'arduino2',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id_country', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('name_ascii', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('geoname_id', models.PositiveIntegerField()),
                ('alternate_names', models.TextField(blank=True, null=True)),
                ('code2', models.CharField(max_length=10)),
                ('code3', models.CharField(max_length=10)),
                ('continent', models.CharField(max_length=50)),
                ('tld', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'country',
            },
        ),
        migrations.CreateModel(
            name='Espacio',
            fields=[
                ('id_espacio', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_espacio', models.CharField(max_length=100)),
                ('direccion_espacio', models.CharField(max_length=100)),
                ('utm', models.CharField(max_length=100)),
                ('uuid_espacio', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('imagen_espacio', models.ImageField(blank=True, null=True, upload_to='imagenes_espacios/')),
                ('codigoqr', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'espacio',
            },
        ),
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
            name='ModeloSensor2',
            fields=[
                ('id_modelo_sensor', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_sensor', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
            ],
            options={
                'db_table': 'modelo_sensor2',
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
            name='TipoDato2',
            fields=[
                ('id_tipo_dato', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_dato', models.CharField(max_length=50)),
                ('unidad_medida', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'tipo_dato2',
            },
        ),
        migrations.CreateModel(
            name='TipoEspacio',
            fields=[
                ('id_tipo_espacio', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_tipo_espacio', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'tipo_espacio',
            },
        ),
        migrations.CreateModel(
            name='TipoPlanta',
            fields=[
                ('id_tipo_planta', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_comun', models.CharField(max_length=50)),
                ('nombre_cientifico', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
                ('uuid_tipo_planta', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('imagen_tipo_planta', models.ImageField(blank=True, null=True, upload_to='imagenes_tipo_plantas/')),
            ],
            options={
                'db_table': 'tipo_planta',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id_city', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('name_ascii', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('geoname_id', models.PositiveIntegerField()),
                ('alternate_names', models.TextField(blank=True, null=True)),
                ('display_name', models.CharField(max_length=100)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('population', models.PositiveIntegerField()),
                ('featured_code', models.CharField(blank=True, max_length=20, null=True)),
                ('search_names', models.TextField(blank=True, null=True)),
                ('timezone', models.CharField(max_length=50)),
                ('id_country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.country')),
            ],
            options={
                'db_table': 'city',
            },
        ),
        migrations.CreateModel(
            name='DivisionEspacio',
            fields=[
                ('id_division_espacio', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_division', models.CharField(max_length=50)),
                ('identificador', models.IntegerField()),
                ('id_espacio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.espacio')),
            ],
            options={
                'db_table': 'division_espacio',
            },
        ),
        migrations.CreateModel(
            name='Arduino',
            fields=[
                ('id_arduino', models.AutoField(primary_key=True, serialize=False)),
                ('modelo_arduino', models.CharField(max_length=50)),
                ('estado', models.IntegerField()),
                ('uuid_arduino', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('id_espacio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.espacio')),
            ],
            options={
                'db_table': 'arduino',
            },
        ),
        migrations.CreateModel(
            name='Localidad',
            fields=[
                ('id_localidad', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_localidad', models.CharField(max_length=100)),
                ('estado_localidad', models.CharField(max_length=100)),
                ('fecha_creado', models.DateTimeField(auto_now_add=True)),
                ('fecha_editado', models.DateTimeField(auto_now=True)),
                ('id_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.city')),
            ],
            options={
                'db_table': 'localidad',
            },
        ),
        migrations.AddField(
            model_name='espacio',
            name='id_localidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.localidad'),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id_region', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('name_ascii', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('geoname_id', models.PositiveIntegerField()),
                ('alternate_names', models.TextField(blank=True, null=True)),
                ('display_name', models.CharField(max_length=100)),
                ('geoname_code', models.CharField(max_length=20)),
                ('id_country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.country')),
            ],
            options={
                'db_table': 'region',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='id_region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.region'),
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
                ('observaciones_registro', models.TextField(blank=True, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('imagen_registro_planta', models.ImageField(blank=True, null=True, upload_to='imagenes_registro_plantas/')),
                ('id_division_espacio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.divisionespacio')),
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
            name='Sensor2',
            fields=[
                ('id_sensor', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.IntegerField()),
                ('id_arduino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.arduino2')),
                ('id_modelo_sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.modelosensor2')),
            ],
            options={
                'db_table': 'sensor2',
            },
        ),
        migrations.CreateModel(
            name='SubRegion',
            fields=[
                ('id_sub_region', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('name_ascii', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('geoname_id', models.PositiveIntegerField()),
                ('alternate_names', models.TextField(blank=True, null=True)),
                ('display_name', models.CharField(max_length=100)),
                ('geoname_code', models.CharField(max_length=20)),
                ('id_country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.country')),
                ('id_region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.region')),
            ],
            options={
                'db_table': 'sub_region',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='id_sub_region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.subregion'),
        ),
        migrations.CreateModel(
            name='TablaHumedal',
            fields=[
                ('id_humedal', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_humedal', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('utm_norte', models.CharField(max_length=100)),
                ('utm_este', models.CharField(max_length=100)),
                ('uuid_espacio', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('imagen_humedal', models.ImageField(blank=True, null=True, upload_to='imagenes_humedales/')),
                ('id_localidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.localidad')),
            ],
            options={
                'db_table': 'tabla_humedal',
            },
        ),
        migrations.AddField(
            model_name='arduino2',
            name='id_humedal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.tablahumedal'),
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
        migrations.CreateModel(
            name='RegistroSensor2',
            fields=[
                ('id_registro_sensor', models.AutoField(primary_key=True, serialize=False)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('id_sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.sensor2')),
                ('id_tipo_dato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.tipodato2')),
            ],
            options={
                'db_table': 'registro_sensor2',
            },
        ),
        migrations.AddField(
            model_name='espacio',
            name='id_tipo_espacio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.tipoespacio'),
        ),
        migrations.AddField(
            model_name='planta',
            name='id_tipo_planta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Datos.tipoplanta'),
        ),
    ]
