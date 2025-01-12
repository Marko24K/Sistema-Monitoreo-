# Generated by Django 5.1.4 on 2025-01-10 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Datos', '0009_delete_parcela'),
    ]

    operations = [
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
                ('UUID_parcela', models.IntegerField()),
                ('imagen_parcela', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'parcela',
            },
        ),
    ]
