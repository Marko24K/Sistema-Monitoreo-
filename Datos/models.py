from django.db import models
import uuid
# Create your models here.
class Parcela(models.Model):
    id_parcela = models.AutoField(primary_key=True)
    localidad_parcela = models.CharField(max_length=50)
    nombre_parcela = models.CharField(max_length=50)
    direccion_parcela = models.CharField(max_length=50)
    zona = models.PositiveSmallIntegerField()
    hemisferio = models.CharField(max_length=1, choices=[('N', 'Norte'), ('S', 'Sur')])
    easting = models.DecimalField(max_digits=10, decimal_places=2)
    northing = models.DecimalField(max_digits=10, decimal_places=2)
    UUID_parcela = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    imagen_parcela = models.ImageField(upload_to='imagenes_parcelas/', null=True, blank=True)

    class Meta:
        db_table = 'parcela'

class DivisionParcela(models.Model):
    id_division_parcela = models.AutoField(primary_key=True)
    id_parcela = models.ForeignKey(Parcela, on_delete=models.CASCADE)
    tipo_division = models.IntegerField()
    identificador = models.IntegerField()
    codigoQR = models.CharField(max_length=50)

    class Meta:
        db_table = 'division_parcela'


class TipoPlanta(models.Model):
    id_tipo_planta = models.AutoField(primary_key=True)
    nombre_comun = models.CharField(max_length=50)
    nombre_cientifico = models.CharField(max_length=50)
    descripcion = models.TextField()
    UUID_tipo_planta =  models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
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
    id_division_parcela = models.ForeignKey(DivisionParcela, on_delete=models.CASCADE)
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
    observaciones_Registro = models.TextField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'registro_planta'


class Arduino(models.Model):
    id_arduino = models.AutoField(primary_key=True)
    id_parcela = models.ForeignKey(Parcela, on_delete=models.CASCADE)
    modelo_arduino = models.CharField(max_length=50)
    estado = models.IntegerField()
    UUID_arduino=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        db_table = 'arduino'

class ModeloSensor(models.Model):
    id_modelo_sensor = models.AutoField(primary_key=True)
    nombre_sensor = models.CharField(max_length=50)
    descripcion = models.TextField()

    class Meta:
        db_table = 'modelo_sensor'

class TipoDato(models.Model):
    id_tipo_dato = models.AutoField(primary_key=True)
    nombre_dato = models.CharField(max_length=50)
    unidad_medida = models.CharField(max_length=50)

    class Meta:
        db_table = 'tipo_dato'

class Sensor(models.Model):
    id_sensor = models.AutoField(primary_key=True)
    id_arduino = models.ForeignKey(Arduino, on_delete=models.CASCADE)
    id_modelo_sensor = models.ForeignKey(ModeloSensor, on_delete=models.CASCADE)
    estado = models.IntegerField()

    class Meta:
        db_table = 'sensor'

class RegistroSensor(models.Model):
    id_registro_sensor = models.AutoField(primary_key=True)
    id_sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    id_tipo_dato = models.ForeignKey(TipoDato, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'registro_sensor'
