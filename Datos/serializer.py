# serializers.py
from rest_framework import serializers
from .models import Sensor, RegistroSensor
# Serializador para el modelo Sensor
class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['nombre_sensor']  # Solo el campo 'nombre_sensor'

# Serializador para el modelo Datos_sensores
class RegistroSensorSerializer(serializers.ModelSerializer):
    sensor_id = serializers.IntegerField(source='id_sensor.id')  # ID del sensor
    sensor_name = serializers.CharField(source='id_sensor.id_modelo_sensor.nombre_sensor')  # Nombre del sensor

    class Meta:
        model = RegistroSensor
        fields = ['valor', 'fecha_registro', 'sensor_id', 'sensor_name']  # Camp

