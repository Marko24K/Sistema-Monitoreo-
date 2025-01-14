# serializers.py
from rest_framework import serializers
from .models import Sensor, RegistroSensor
# Serializador para el modelo Sensor# Serializador para el modelo Sensor
class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id_sensor', 'id_arduino', 'id_modelo_sensor', 'estado']  # Puedes agregar más campos si es necesario


# Serializador para el modelo Datos_sensores# Serializador para el modelo RegistroSensor
class RegistroSensorSerializer(serializers.ModelSerializer):
    # Representa el ID y el nombre del sensor asociado
    sensor_id = serializers.IntegerField(source='id_sensor.id_sensor')  # ID del sensor
    sensor_name = serializers.CharField(source='id_sensor.id_modelo_sensor.nombre_sensor')  # Nombre del sensor
    
    # Representa el nombre del tipo de dato
    tipo_dato_name = serializers.CharField(source='id_tipo_dato.nombre_dato')  # Nombre del tipo de dato
    
    class Meta:
        model = RegistroSensor
        fields = ['valor', 'fecha_registro', 'sensor_id', 'sensor_name', 'tipo_dato_name']  # Campos a incluir en la respuesta