from django.db import models
import uuid
class Country(models.Model):
    id_country = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    name_ascii = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    geoname_id = models.PositiveIntegerField()
    alternate_names = models.TextField(blank=True, null=True)
    code2 = models.CharField(max_length=10)
    code3 = models.CharField(max_length=10)
    continent = models.CharField(max_length=50)
    tld = models.CharField(max_length=10)  # Top Level Domain
    phone = models.CharField(max_length=20)

    class Meta:
        db_table = 'country'

class Region(models.Model):
    id_region = models.AutoField(primary_key=True)
    id_country = models.ForeignKey(Country, on_delete=models.CASCADE)  # Relación con Country
    name = models.CharField(max_length=100)
    name_ascii = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    geoname_id = models.PositiveIntegerField()
    alternate_names = models.TextField(blank=True, null=True)
    display_name = models.CharField(max_length=100)
    geoname_code = models.CharField(max_length=20)

    class Meta:
        db_table = 'region'

class SubRegion(models.Model):
    id_sub_region = models.AutoField(primary_key=True)
    id_country = models.ForeignKey(Country, on_delete=models.CASCADE)  # Relación con Country
    id_region = models.ForeignKey(Region, on_delete=models.CASCADE)    # Relación con Region
    name = models.CharField(max_length=100)
    name_ascii = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    geoname_id = models.PositiveIntegerField()
    alternate_names = models.TextField(blank=True, null=True)
    display_name = models.CharField(max_length=100)
    geoname_code = models.CharField(max_length=20)

    class Meta:
        db_table = 'sub_region'

class City(models.Model):
    id_city = models.AutoField(primary_key=True)
    id_region = models.ForeignKey(Region, on_delete=models.CASCADE)  # Relación con Region
    id_country = models.ForeignKey(Country, on_delete=models.CASCADE)  # Relación con Country
    id_sub_region = models.ForeignKey(SubRegion, on_delete=models.CASCADE)  # Relación con SubRegion
    name = models.CharField(max_length=100)
    name_ascii = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    geoname_id = models.PositiveIntegerField()
    alternate_names = models.TextField(blank=True, null=True)
    display_name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # Para almacenar latitud
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # Para almacenar longitud
    population = models.PositiveIntegerField()  # Población de la ciudad
    featured_code = models.CharField(max_length=20, blank=True, null=True)  # Código destacado
    search_names = models.TextField(blank=True, null=True)  # Nombres de búsqueda
    timezone = models.CharField(max_length=50)  # Zona horaria

    class Meta:
        db_table = 'city'

class Localidad(models.Model):
    id_localidad = models.AutoField(primary_key=True)
    id_city = models.ForeignKey(City, on_delete=models.CASCADE)  # Relación con Region
    nombre_localidad = models.CharField(max_length=100)
    estado_localidad = models.CharField(max_length=100)
    fecha_creado = models.DateTimeField(auto_now_add=True)
    fecha_editado = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'localidad'

class TipoEspacio(models.Model):
    id_tipo_espacio = models.AutoField(primary_key=True)
    nombre_tipo_espacio = models.CharField(max_length=100) #humedal, parcela o invernadero

    class Meta:
        db_table = 'tipo_espacio'

class Espacio(models.Model): #refiere a el lugar fisico donde se realizaran las mediciones 
    id_espacio = models.AutoField(primary_key=True) 
    id_localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE) 
    id_tipo_espacio = models.ForeignKey(TipoEspacio, on_delete=models.CASCADE) 
    nombre_espacio = models.CharField(max_length=100) 
    direccion_espacio = models.CharField(max_length=100) 
    utm = models.CharField(max_length=100) 
    uuid_espacio = models.UUIDField(default=uuid.uuid4 , editable=False, unique=True)
    imagen_espacio = models.ImageField(upload_to='imagenes_espacios/', null=True, blank=True)
    codigoqr = models.CharField(max_length=100, null=True, blank=True) 
    class Meta:
        db_table = 'espacio'

class DivisionEspacio(models.Model):
    id_division_espacio = models.AutoField(primary_key=True)
    id_espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)
    tipo_division = models.CharField(max_length=50)  
    identificador = models.IntegerField()
    class Meta:
        db_table = 'division_espacio'

class TipoPlanta(models.Model):
    id_tipo_planta = models.AutoField(primary_key=True)
    nombre_comun = models.CharField(max_length=50)
    nombre_cientifico = models.CharField(max_length=50)
    descripcion = models.TextField()
    uuid_tipo_planta =  models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    imagen_tipo_planta = models.ImageField(upload_to='imagenes_tipo_plantas/', null=True, blank=True)

    class Meta:
        db_table = 'tipo_planta'

class Planta(models.Model):
    id_planta = models.AutoField(primary_key=True)
    id_tipo_planta = models.ForeignKey(TipoPlanta, on_delete=models.CASCADE)
    descripcion_planta = models.TextField()
    observaciones_planta = models.TextField()
    fecha_siembra = models.DateTimeField(auto_now_add=True)
    fecha_extraccion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'planta'

class RegistroPlanta(models.Model):
    id_registro_planta = models.AutoField(primary_key=True)
    id_division_espacio = models.ForeignKey(DivisionEspacio, on_delete=models.CASCADE)
    id_planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    numero_planta = models.IntegerField()
    altura = models.FloatField()
    largo = models.FloatField()
    ancho = models.FloatField()
    grosor = models.FloatField()
    vigor = models.CharField(max_length=50)
    turgencia = models.CharField(max_length=50)
    vitalidad = models.CharField(max_length=50)
    plaga_enfermedad = models.BooleanField(default=False)
    descripcion_plaga_enfermedad = models.TextField(null=True, blank=True)
    observaciones_registro = models.TextField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    imagen_registro_planta = models.ImageField(upload_to='imagenes_registro_plantas/', null=True, blank=True)
    class Meta:
        db_table = 'registro_planta'

class Arduino(models.Model):
    id_arduino = models.AutoField(primary_key=True)
    id_espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)
    modelo_arduino = models.CharField(max_length=50)
    estado = models.IntegerField()
    uuid_arduino=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        db_table = 'arduino'

class ModeloSensor(models.Model):
    id_modelo_sensor = models.AutoField(primary_key=True)
    nombre_sensor = models.CharField(max_length=50)
    descripcion = models.TextField()

    class Meta:
        db_table = 'modelo_sensor'

class Sensor(models.Model):
    id_sensor = models.AutoField(primary_key=True)
    id_arduino = models.ForeignKey(Arduino, on_delete=models.CASCADE)
    id_modelo_sensor = models.ForeignKey(ModeloSensor, on_delete=models.CASCADE)
    estado = models.IntegerField()

    class Meta:
        db_table = 'sensor'

class TipoDato(models.Model):
    id_tipo_dato = models.AutoField(primary_key=True)
    nombre_dato = models.CharField(max_length=50)
    unidad_medida = models.CharField(max_length=50)

    class Meta:
        db_table = 'tipo_dato'

class RegistroSensor(models.Model):
    id_registro_sensor = models.AutoField(primary_key=True)
    id_sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    id_tipo_dato = models.ForeignKey(TipoDato, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'registro_sensor'