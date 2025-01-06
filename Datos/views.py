from django.shortcuts import render, get_object_or_404
from .models import Sensor, Tipo_dato, Datos_sensores
from django.http import Http404, JsonResponse
from django.db.models import Avg, Max, Min
import json
from rest_framework.decorators import api_view
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .serializer import DatosSensoresSerializer
from rest_framework.response import Response


# Create your views here.

def home(request):
    # Obtener los datos más recientes de temperatura y humedad
    temp_data = Datos_sensores.objects.filter(tipo_dato__nombre_tipo_dato='Temperatura').order_by('-fecha_registro')[:1]
    humidity_data = Datos_sensores.objects.filter(tipo_dato__nombre_tipo_dato='Humedad').order_by('-fecha_registro')[:1]

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

    temp_recent = Datos_sensores.objects.filter(tipo_dato__nombre_tipo_dato='Temperatura').order_by('-fecha_registro')[:5].select_related('sensor')
    hum_recent = Datos_sensores.objects.filter(tipo_dato__nombre_tipo_dato='Humedad').order_by('-fecha_registro')[:5].select_related('sensor')

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
#guardar archivos


    
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
            
            

            # Buscar el sensor y tipo de dato correspondiente
            sensor = Sensor.objects.get(id=id_sensor)
            tipo_dato = Tipo_dato.objects.get(nombre_tipo_dato=tipo)
            
            # Crear el objeto de datos del sensor
            Datos_sensores.objects.create(
                sensor=sensor,
                tipo_dato=tipo_dato,
                valor=valor
            )
            
            
            return JsonResponse({'message': 'Datos insertados correctamente'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    

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
    # valida los tipos de datos
    dato = request.GET.get('dato', None)
    if dato not in ['Temperatura', 'Humedad']:  # Verifica que sea uno de los tipos esperados
        return render(request, 'home.html', {'error': 'Tipo de dato inválido.'})
    
    # Get the Tipo_dato object based on the 'dato' parameter
    tipo_dato = get_object_or_404(Tipo_dato, nombre_tipo_dato=dato)

    try:
        # Intentar obtener el tipo de dato desde la base de datos
        tipo_dato = Tipo_dato.objects.get(nombre_tipo_dato=dato)
    except Tipo_dato.DoesNotExist:

        # Si no se encuentra el tipo de dato, muestra un mensaje de error
        return render(request, 'home.html', {'error': f'No se encontró el tipo de dato: {dato}'})

    # obtiene todos los datos de los sensores ordenados por fecha
    datos_sensores = Datos_sensores.objects.filter(tipo_dato=tipo_dato).order_by('-fecha_registro')

    # recolecta datos para el grafico
    chart_data = []
    for data_point in datos_sensores:
        chart_data.append({
            'fecha': data_point.fecha_registro.strftime('%Y-%m-%d %H:%M:%S'),
            'valor': data_point.valor,
        })
    
    # maximo, minimo , promedio
    stats = datos_sensores.aggregate(
        max_value=Max('valor'),
        min_value=Min('valor'),
        avg_value=Avg('valor')
    )

    # obtener una lista de los ultimos 10 sensores
    recent_data = datos_sensores[:10]

    return render(request, 'ver_mas.html', {
        'dato': dato,
        'tipo_dato': tipo_dato,
        'chart_data': json.dumps(chart_data),  # envia el dato de js a json
        'stats': stats,
        'recent_data': recent_data,
    })


def guardar_archivo(archivo):
    """
    Guarda el archivo recibido en la ubicación configurada.
    Retorna la URL del archivo guardado.
    """
    try:
        # Crear un almacenamiento de archivos usando FileSystemStorage
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'archivos_sensores'))
        
        # Guardar el archivo en la ubicación deseada
        archivo_guardado = fs.save(archivo.name, archivo)
        
        # Retornar la URL del archivo guardado
        return fs.url(archivo_guardado)
    
    except Exception as e:
        raise Exception(f"Error al guardar el archivo: {str(e)}")