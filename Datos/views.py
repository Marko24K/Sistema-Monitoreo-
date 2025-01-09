import datetime
import os
from django.db import connections
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from Sistema.settings import BACKUP_DIR
from .models import Sensor, Tipo_dato, Datos_sensores
from django.http import Http404, JsonResponse
from django.db.models import Avg, Max, Min
import json
from rest_framework.decorators import api_view

from django.conf import settings
from .serializer import DatosSensoresSerializer
from rest_framework.response import Response

def home(request):
    # Obtener los datos más recientes de temperatura y humedad
    temp_data = Datos_sensores.objects.filter(tipo_dato__nombre_tipo_dato='Temperatura').order_by('-fecha_registro')[:10]
    humidity_data = Datos_sensores.objects.filter(tipo_dato__nombre_tipo_dato='Humedad').order_by('-fecha_registro')[:10]

    # Obtener las estadísticas para temperatura
    temp_stats = Datos_sensores.objects.filter(tipo_dato__nombre_tipo_dato='Temperatura').aggregate(
        max_value=Max('valor'),
        min_value=Min('valor'),
        avg_value=Avg('valor')
    )

    # Obtener las estadísticas para humedad
    hum_stats = Datos_sensores.objects.filter(tipo_dato__nombre_tipo_dato='Humedad').aggregate(
        max_value=Max('valor'),
        min_value=Min('valor'),
        avg_value=Avg('valor')
    )

    # Obtener los datos recientes de temperatura y humedad

    temp_recent = Datos_sensores.objects.filter(tipo_dato__nombre_tipo_dato='Temperatura').order_by('-fecha_registro')[:5]
    hum_recent = Datos_sensores.objects.filter(tipo_dato__nombre_tipo_dato='Humedad').order_by('-fecha_registro')[:5]

    return render(request, 'home.html', {
        'temp_data': temp_data,
        'humidity_data': humidity_data,
        'temp_max': temp_stats['max_value'],
        'temp_min': temp_stats['min_value'],
        'temp_avg': temp_stats['avg_value'],
        'hum_max': hum_stats['max_value'],
        'hum_min': hum_stats['min_value'],
        'hum_avg': hum_stats['avg_value'],
        'temp_recent': temp_recent,
        'hum_recent': hum_recent
    })


#Guardar datos de un sensor desde un esp32 
@api_view(['POST'])
def guardar_datos_sensor(request):
    if request.method == 'POST':
        # Obtener los datos enviados
        try:
            data = json.loads(request.body)
            id_sensor = data.get('id_sensor')
            valor = data.get('valor')
            tipo = data.get('tipo')
            
            # Verificar que los datos están completos
            if not all([id_sensor, valor, tipo]):
                return JsonResponse({'error': 'Faltan parámetros'}, status=400)
            
            # Verificar si el sensor existe
            try:
                sensor = Sensor.objects.get(id=id_sensor)
            except Sensor.DoesNotExist:
                return JsonResponse({'error': f'Sensor con id {id_sensor} no encontrado'}, status=404)

            # Verificar si el tipo de dato existe
            try:
                tipo_dato = Tipo_dato.objects.get(nombre_tipo_dato=tipo)
            except Tipo_dato.DoesNotExist:
                return JsonResponse({'error': f'Tipo de dato "{tipo}" no encontrado'}, status=404)

             # Guardar los datos en un archivo de texto como respaldo primero
            backup_data = {
                'id_sensor': id_sensor,
                'valor': valor,
                'tipo': tipo,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            # Definir el archivo de respaldo único
            BACKUP_DIR = os.path.join(settings.BASE_DIR, 'backup')  # Carpeta para respaldo
            os.makedirs(BACKUP_DIR, exist_ok=True)  # Crear el directorio si no existe
            backup_filename = os.path.join(BACKUP_DIR, 'backup_data.txt')  # Archivo único de respaldo

            # Escribir los datos en el archivo de respaldo (en modo 'a' para anexar)
            with open(backup_filename, 'a') as f:
                # Si es la primera vez que se guarda en el archivo, escribir el encabezado
                if f.tell() == 0:  # Si el archivo está vacío
                    f.write('id_sensor\tvalor\ttipo\ttimestamp\n')  # Encabezado con tabuladores
                # Escribir los datos de respaldo en formato de columnas
                f.write(f"{backup_data['id_sensor']}\t{backup_data['valor']}\t{backup_data['tipo']}\t{backup_data['timestamp']}\n")


            # Buscar el sensor y tipo de dato correspondiente
            sensor = Sensor.objects.get(id=id_sensor)
            tipo_dato = Tipo_dato.objects.get(nombre_tipo_dato=tipo)
            
            # Intentar insertar los datos en la base de datos
            try:
                # Verificar si el sensor existe
                sensor = Sensor.objects.get(id=id_sensor)
                
                # Verificar si el tipo de dato existe
                tipo_dato = Tipo_dato.objects.get(nombre_tipo_dato=tipo)

                # Crear el objeto de datos del sensor en la base de datos
                Datos_sensores.objects.create(
                    sensor=sensor,
                    tipo_dato=tipo_dato,
                    valor=valor
                )
                
                return JsonResponse({'message': 'Datos insertados correctamente en la base de datos y respaldo actualizado'}, status=200)
            
            except Exception as db_error:
                # Si ocurre un error con la base de datos, se maneja aquí
                return JsonResponse({'error': f'Error al insertar en la base de datos: {str(db_error)}. Los datos se han guardado en el archivo de respaldo.'}, status=500)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    

#guardar respaldo en un txt
#



@api_view(['GET'])
#mostrar actualizados
def datos_recientes(request):
    # Obtener los últimos datos de temperatura y humedad
    temperature_data = Datos_sensores.objects.filter(tipo_dato__nombre_tipo_dato='Temperatura').order_by('-fecha_registro')[:10]
    humidity_data = Datos_sensores.objects.filter(tipo_dato__nombre_tipo_dato='Humedad').order_by('-fecha_registro')[:10]

    # Serializar los datos
    temperature_serializer = DatosSensoresSerializer(temperature_data, many=True)
    humidity_serializer = DatosSensoresSerializer(humidity_data, many=True)

    # Retornar la respuesta JSON con los datos serializados
    return Response({
        'temperature': temperature_serializer.data,
        'humidity': humidity_serializer.data
    })


#mostrar los datos segun el tipo de dato que se elija
def detalle_dato(request):
    dato = request.GET.get('dato', None)
    if dato not in ['Temperatura', 'Humedad']:
        return JsonResponse({'error': 'Tipo de dato inválido.'})

    tipo_dato = get_object_or_404(Tipo_dato, nombre_tipo_dato=dato)
    datos_sensores = Datos_sensores.objects.filter(tipo_dato=tipo_dato).order_by('-fecha_registro')[:10]
     
    # Recolecta los datos para el gráfico
    chart_data = []
    for data_point in datos_sensores:
        chart_data.append({
        'fecha': data_point.fecha_registro.strftime('%Y-%m-%d %H:%M:%S%z'),
        'valor': data_point.valor,
    })

    # Verificar si la solicitud es AJAX usando el header HTTP_X_REQUESTED_WITH
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Aquí se añaden los datos de la tabla
        table_data = []
        for data in datos_sensores[:10]:  # Solo los 10 primeros para la tabla
            table_data.append({
                'valor': f"{data.valor:.2f} {tipo_dato.unidad}",
                'fecha': data.fecha_registro.strftime('%d/%m/%Y %H:%M'),
                'sensor': data.sensor.nombre_sensor,
                'tipo_sensor': data.sensor.tipo_sensor,
            })

        return JsonResponse({
            'chart_data': chart_data,
            'table_data': table_data
        })

    # Si no es AJAX, seguimos el flujo normal
    stats = datos_sensores.aggregate(
        max_value=Max('valor'),
        min_value=Min('valor'),
        avg_value=Avg('valor')
    )

    recent_data = datos_sensores[:10]

    return render(request, 'ver_mas.html', {
        'dato': dato,
        'tipo_dato': tipo_dato,
        'chart_data': json.dumps(chart_data),  # Enviar los datos para la carga inicial
        'stats': stats,
        'recent_data': recent_data,
    })
