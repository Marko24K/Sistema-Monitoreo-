from django.core.management.base import BaseCommand
from django.db import connections, transaction
from django.core.management import call_command
import psycopg2
from psycopg2 import sql

class Command(BaseCommand):
    help = 'Copia datos de la base de datos default a espejo'

    def check_and_create_database(self, db_name):
        """
        Verifica si la base de datos existe y la crea si no existe.
        """
        default_db = connections['default']
        conn = psycopg2.connect(
            dbname='postgres',  # Conéctate a la base de datos por defecto
            user=default_db.settings_dict['USER'],
            password=default_db.settings_dict['PASSWORD'],
            host=default_db.settings_dict['HOST'],
            port=default_db.settings_dict['PORT']
        )
        conn.autocommit = True  
        cursor = conn.cursor()

        try:
            cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s;"), [db_name])
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(db_name)))
                self.stdout.write(self.style.SUCCESS(f'Base de datos "{db_name}" creada exitosamente.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'La base de datos "{db_name}" ya existe.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al verificar o crear la base de datos: {e}'))
        finally:
            cursor.close()
            conn.close()

    def copy_data(self, source_db, target_db, model, query):
        """
        Copia datos de una tabla específica desde la base de datos origen hacia destino.
        """
        try:
            with source_db.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

            if not rows:
                self.stdout.write(self.style.WARNING(f'No se encontraron datos para la tabla {model.__name__}'))
                return

            field_names = [field.name for field in model._meta.fields]
            for row in rows:
                data = {}
                for field, value in zip(field_names, row):
                    field_obj = model._meta.get_field(field)
                    if field_obj.is_relation and field_obj.related_model:
                        # Resolver claves foráneas
                        try:
                            data[field] = field_obj.related_model.objects.using('espejo').get(pk=value) if value is not None else None
                        except field_obj.related_model.DoesNotExist:
                            self.stdout.write(self.style.WARNING(
                                f'No se encontró el objeto relacionado para {field} con id {value} en {model.__name__}'
                            ))
                            data[field] = None
                    else:
                        data[field] = value

                # Crear el objeto en la base de datos espejo
                model.objects.using('espejo').create(**data)

            self.stdout.write(self.style.SUCCESS(f'Datos copiados para la tabla {model.__name__}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error copiando datos para la tabla {model.__name__}: {e}'))

    def handle(self, *args, **kwargs):
        from Datos.models import (
            Country, Region, SubRegion, City, Localidad,
            TipoEspacio, Espacio, DivisionEspacio, TipoPlanta, Planta,
            RegistroPlanta, Arduino, ModeloSensor, Sensor, TipoDato,
            RegistroSensor, TablaHumedal, Arduino2, ModeloSensor2, Sensor2, TipoDato2, RegistroSensor2
        )

        target_db_name = 'humedal_espejo'
        self.check_and_create_database(target_db_name)

        source_db = connections['default']
        target_db = connections['espejo']

        # Crear tablas en la base de datos destino si no existen
        try:
            call_command('migrate', database='espejo')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al aplicar migraciones: {e}'))
            return

        # Eliminar registros existentes en la base de datos destino
        with transaction.atomic(using='espejo'):
            try:
                tables = [
                    "country", "region", "sub_region", "city", "localidad",
                    "tipo_espacio", "espacio", "division_espacio", "tipo_planta", "planta",
                    "registro_planta", "arduino", "modelo_sensor", "sensor", "tipo_dato",
                    "registro_sensor", "tabla_humedal", "arduino2", "modelo_sensor2", "sensor2", "tipo_dato2", "registro_sensor2"
                ]
                for table in tables:
                    target_db.cursor().execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error truncando tablas: {e}'))
                return

        # Copiar datos
        models_and_queries = [
            (Country, "SELECT * FROM country;"),
            (Region, "SELECT id_region, id_country_id, name, name_ascii, slug, geoname_id, alternate_names, display_name, geoname_code FROM region;"),
            (SubRegion, "SELECT id_sub_region, id_country_id, id_region_id, name, name_ascii, slug, geoname_id, alternate_names, display_name, geoname_code FROM sub_region;"),
            (City, "SELECT id_city, id_region_id, id_country_id, id_sub_region_id, name, name_ascii, slug, geoname_id, alternate_names, display_name, latitude, longitude, population, featured_code, search_names, timezone FROM city;"),
            (Localidad, "SELECT id_localidad, id_city_id, nombre_localidad, estado_localidad, fecha_creado, fecha_editado FROM localidad;"),
            (TipoEspacio, "SELECT * FROM tipo_espacio;"),
            (Espacio, "SELECT id_espacio, id_localidad_id, id_tipo_espacio_id, nombre_espacio, direccion_espacio, utm, uuid_espacio, imagen_espacio, codigoqr FROM espacio;"),
            (DivisionEspacio, "SELECT id_division_espacio, id_espacio_id, tipo_division, identificador FROM division_espacio;"),
            (TipoPlanta, "SELECT * FROM tipo_planta;"),
            (Planta, "SELECT id_planta, id_tipo_planta_id, descripcion_planta, observaciones_planta, fecha_siembra, fecha_extraccion FROM planta;"),
            (RegistroPlanta, "SELECT id_registro_planta, id_division_espacio_id, id_planta_id, numero_planta, altura, largo, ancho, grosor, vigor, turgencia, vitalidad, plaga_enfermedad, descripcion_plaga_enfermedad, observaciones_registro, fecha_registro, imagen_registro_planta FROM registro_planta;"),
            (Arduino, "SELECT id_arduino, id_espacio_id, modelo_arduino, estado, uuid_arduino FROM arduino;"),
            (ModeloSensor, "SELECT * FROM modelo_sensor;"),
            (Sensor, "SELECT * FROM sensor;"),
            (TipoDato, "SELECT * FROM tipo_dato;"),
            (RegistroSensor, "SELECT id_registro_sensor, id_sensor_id, id_tipo_dato_id, valor, fecha_registro FROM registro_sensor;"),
             (TablaHumedal, "SELECT id_humedal, id_localidad_id, nombre_humedal, direccion, utm_norte, utm_este, uuid_espacio, imagen_humedal FROM tabla_humedal;"),
            (Arduino2, "SELECT id_arduino, id_humedal_id, modelo_arduino, estado, uuid_arduino FROM arduino2;"),
            (ModeloSensor2, "SELECT id_modelo_sensor, nombre_sensor, descripcion FROM modelo_sensor2;"),
            (Sensor2, "SELECT id_sensor, id_arduino_id, id_modelo_sensor_id, estado FROM sensor2;"),
            (TipoDato2, "SELECT id_tipo_dato, nombre_dato, unidad_medida FROM tipo_dato2;"),
            (RegistroSensor2, "SELECT id_registro_sensor, id_sensor_id, id_tipo_dato_id, valor, fecha_registro FROM registro_sensor2;")
        
        ]

        for model, query in models_and_queries:
            self.copy_data(source_db, target_db, model, query)

        self.stdout.write(self.style.SUCCESS('Datos copiados exitosamente.'))
