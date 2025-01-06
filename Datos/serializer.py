# serializers.py
from rest_framework import serializers
from .models import Sensor, Datos_sensores

# Serializador para el modelo Sensor
class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['nombre_sensor']  # Solo el campo 'nombre_sensor'

# Serializador para el modelo Datos_sensores
class DatosSensoresSerializer(serializers.ModelSerializer):
    sensor = SensorSerializer()  # Relación con el serializador del Sensor

    class Meta:
        model = Datos_sensores
        fields = ['valor', 'fecha_registro', 'sensor']  # Incluye la información de 'sensor' con 'nombre_sensor'
