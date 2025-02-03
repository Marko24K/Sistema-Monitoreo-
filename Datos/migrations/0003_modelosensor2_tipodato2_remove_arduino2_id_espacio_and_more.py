# Generated by Django 5.1.4 on 2025-02-03 18:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Datos', '0002_rename_hume_tablahumedal_and_more'),
    ]

    operations = [
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
        migrations.RemoveField(
            model_name='arduino2',
            name='id_espacio',
        ),
        migrations.AddField(
            model_name='arduino2',
            name='id_humedal',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Datos.tablahumedal'),
            preserve_default=False,
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
    ]
