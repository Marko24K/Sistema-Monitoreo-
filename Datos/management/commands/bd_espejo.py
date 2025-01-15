from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
    
        bd_original = 'Humedal' 
        bd_espejo = 'Humedal_espejo' 


        conexion_original = connections['Humedal']

  
        with conexion_original.cursor() as cursor:
            try:
                cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{'Humedal_espejo'}';")
                if cursor.fetchone():
                    self.stdout.write(self.style.WARNING('La base de datos espejo ya existe. Eliminándola...'))
                    cursor.execute(f"DROP DATABASE {'Humedal_espejo'};")
            except OperationalError:
                self.stdout.write(self.style.ERROR('Error al verificar la base de datos.'))


        self.stdout.write(self.style.NOTICE('Creando base de datos espejo...'))
        with conexion_original.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE {'Humedal_espejo'};")

       
        conexion_espejo = connections['Humedal_espejo']

       
        with conexion_espejo.cursor() as cursor:
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
            tables = cursor.fetchall()

            for table in tables:
                table_name = table[0]
                self.stdout.write(f'Copiando tabla {table_name}...')
                cursor.execute(f"CREATE TABLE {table_name} (LIKE {'Humedal' }.{table_name} INCLUDING ALL);")
                cursor.execute(f"INSERT INTO {table_name} SELECT * FROM {'Humedal' }.{table_name};")

        self.stdout.write(self.style.SUCCESS('Base de datos espejo creada con éxito.'))
