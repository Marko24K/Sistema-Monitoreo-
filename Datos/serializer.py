from rest_framework import serializers
from .models import ModeloSensor, Sensor, RegistroSensor, Arduino, TipoDato

# Serializador para el modelo Arduino
class ArduinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arduino
        fields = ['id_arduino', 'modelo_arduino', 'estado', 'UUID_arduino']

# Serializador para el modelo ModeloSensor
class ModeloSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeloSensor
        fields = ['id_modelo_sensor', 'nombre_sensor', 'descripcion']

# Serializador para el modelo Sensor
class SensorSerializer(serializers.ModelSerializer):
    id_arduino = ArduinoSerializer()
    id_modelo_sensor = ModeloSensorSerializer()

    class Meta:
        model = Sensor
        fields = ['id_sensor', 'id_arduino', 'id_modelo_sensor', 'estado']

# Serializador para el modelo RegistroSensor
class RegistroSensorSerializer(serializers.ModelSerializer):
    # Obtener el ID del sensor
    sensor_model_id = serializers.IntegerField(source='id_sensor.id_modelo_sensor.id_modelo_sensor')  # ID del modelo del sensor

    # Obtener el nombre del sensor relacionado
    sensor_name = serializers.CharField(source='id_sensor.id_modelo_sensor.nombre_sensor')  # Nombre del modelo de sensor

    # Obtener el nombre del tipo de dato
    tipo_dato_name = serializers.CharField(source='id_tipo_dato.nombre_dato')  # Nombre del tipo de dato

     # Incluir fecha_registro en el serializador
    fecha_registro = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')  # Formato de fecha que desees

    class Meta:
        model = RegistroSensor
        fields = ['valor', 'fecha_registro', 'sensor_model_id', 'sensor_name', 'tipo_dato_name']
