from django.db import models

# Create your models here.
class Sensor(models.Model):
    nombre_sensor = models.CharField(max_length=50)
    tipo_sensor = models.CharField(max_length=50)
    ubicacion = models.TextField()
    descripcion = models.TextField()
    fecha_registro = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.nombre_sensor
    
class Tipo_dato(models.Model):
    nombre_tipo_dato = models.CharField(max_length=50)
    unidad = models.CharField(max_length=20)
    def __str__(self):
        return self.nombre_tipo_dato

class Datos_sensores(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    tipo_dato = models.ForeignKey(Tipo_dato, on_delete=models.CASCADE,null = False)
    valor = models.FloatField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sensor.nombre_sensor} - {self.valor}"