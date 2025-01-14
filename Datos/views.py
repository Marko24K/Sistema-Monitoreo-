from datetime import datetime
import os
import traceback
from django.shortcuts import  render, get_object_or_404
from django.utils import timezone
from Sistema.settings import BACKUP_DIR
from .models import RegistroSensor, Sensor, TipoDato, Parcela, TipoPlanta, ModeloSensor
from django.http import JsonResponse
from django.db.models import Avg, Max, Min
import json
from rest_framework.decorators import api_view
from django.conf import settings
from .serializer import RegistroSensorSerializer
from rest_framework.response import Response
#-----------------------------------------------
def bt_varios(request):
    return render(request, 'bt_varios.html')

def registro_planta(request):
    return render(request, 'registro_planta.html')

def modal_view(request):
    form_type = request.GET.get('form_type', '')  # Obtener el tipo de formulario de la URL
    template_path = f'mini_forms/{form_type}.html'  # Solo usar la ruta relativa a la carpeta 'templates'
    
    try:
        return render(request, template_path)
    except:
        # Si no encuentra el archivo, cargar un formulario predeterminado
        return render(request, 'mini_forms/arduino.html')  # Cargar un formulario predeterminado

#--------------agregado por felipe-------------
def registro_parcela(request):
    if request.method == 'POST':
        # procesamiento de los datos del formulario y crear una nueva instancia
        parcela = Parcela.objects.create(
            localidad_parcela=request.POST['val_localidad_p'],
            nombre_parcela=request.POST['val_nombre_p'],
            direccion_parcela=request.POST['val_direccion_p'],
            zona=request.POST['numero_zona'],
            hemisferio=request.POST['hemisferio'],
            easting=request.POST['falso_este'],
            northing=request.POST['falso_norte'],
            imagen_parcela=request.FILES['input-imagen'],  # Si la imagen está en el formulario
        )
    return render(request, 'registro_parcela.html')


def tipo_planta(request):
    if request.method == 'POST':
        planta = TipoPlanta.objects.create(
            nombre_comun = request.POST['nombre_comun'],
            nombre_cientifico = request.POST['nombre_cientifico'],
            descripcion = request.POST['descripcion_planta'],
            imagen_tipo_planta = request.POST['input-imagen'],
        )
    return render(request, 'tipo_planta.html')

def home(request):
    # Obtener los datos más recientes de temperatura y humedad
    temp_data = RegistroSensor.objects.filter(id_tipo_dato__nombre_dato='Temperatura').order_by('-fecha_registro')[:1]
    humidity_data = RegistroSensor.objects.filter(id_tipo_dato__nombre_dato='Humedad').order_by('-fecha_registro')[:1]

    # Obtener las estadísticas para temperatura
    temp_stats = RegistroSensor.objects.filter(id_tipo_dato__nombre_dato='Temperatura').aggregate(
        max_value=Max('valor'),
        min_value=Min('valor'),
        avg_value=Avg('valor')
    )

    # Obtener las estadísticas para humedad
    hum_stats = RegistroSensor.objects.filter(id_tipo_dato__nombre_dato='Humedad').aggregate(
        max_value=Max('valor'),
        min_value=Min('valor'),
        avg_value=Avg('valor')
    )

    # Obtener los datos recientes de temperatura y humedad (últimos 5)
    temp_recent = RegistroSensor.objects.filter(id_tipo_dato__nombre_dato='Temperatura').order_by('-fecha_registro')[:5]
    hum_recent = RegistroSensor.objects.filter(id_tipo_dato__nombre_dato='Humedad').order_by('-fecha_registro')[:5]

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

@api_view(['POST'])
def guardar_datos_sensor(request):
    if request.method == 'POST':
        try:
            # Obtener los datos enviados en la solicitud
            data = json.loads(request.body)
            id_modelo_sensor = data.get('id_sensor')  # id del modelo del sensor que envía los datos
            valor = data.get('valor')
            tipo = data.get('tipo')
            
            # Verificar que los datos estén completos
            if not all([id_modelo_sensor, valor, tipo]):
                return JsonResponse({'error': 'Faltan parámetros'}, status=400)

            # Paso 1: Buscar el ModeloSensor utilizando el id del modelo (id_sensor enviado por el ESP32)
            try:
                modelo_sensor = ModeloSensor.objects.get(id_modelo_sensor=id_modelo_sensor)
            except ModeloSensor.DoesNotExist:
                return JsonResponse({'error': f'Modelo de sensor con id {id_modelo_sensor} no encontrado'}, status=404)

            # Paso 2: Buscar el Sensor asociado con ese ModeloSensor
            try:
                sensor = Sensor.objects.get(id_modelo_sensor=modelo_sensor)  # Buscar el sensor por el modelo
            except Sensor.DoesNotExist:
                return JsonResponse({'error': f'Sensor relacionado con el modelo {modelo_sensor.nombre_sensor} no encontrado'}, status=404)

            # Paso 3: Buscar el TipoDato correspondiente
            try:
                tipo_dato = TipoDato.objects.get(nombre_dato=tipo)
            except TipoDato.DoesNotExist:
                return JsonResponse({'error': f'Tipo de dato "{tipo}" no encontrado'}, status=404)

            # Guardar los datos en un archivo de respaldo si ocurre un error con la base de datos
            backup_data = {
                'id_sensor': id_modelo_sensor,
                'valor': valor,
                'tipo': tipo,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            BACKUP_DIR = os.path.join(settings.BASE_DIR, 'backup')
            os.makedirs(BACKUP_DIR, exist_ok=True)
            backup_filename = os.path.join(BACKUP_DIR, 'backup_data.txt')

            # Intentar escribir en el archivo de respaldo
            try:
                # Abrir el archivo en modo append para agregar los datos sin eliminar los existentes
                with open(backup_filename, mode='a') as f:
                    # Comprobar si el archivo está vacío para escribir el encabezado
                    if f.tell() == 0:
                        # Escribimos un encabezado legible para el archivo
                        f.write("id_sensor | valor | tipo | timestamp\n")
                    
                    # Escribir los datos en el archivo con formato personalizado (usando pipe como delimitador)
                    f.write(f"{backup_data['id_sensor']} | {backup_data['valor']} | {backup_data['tipo']} | {backup_data['timestamp']}\n")

                print("Datos respaldados correctamente.")
            except Exception as e:
                return JsonResponse({'error': f'Error al escribir en el archivo de respaldo: {str(e)}'}, status=500)

            # Intentar guardar en la base de datos
            try:
                # Crear un nuevo registro de sensor en la base de datos
                RegistroSensor.objects.create(
                    id_sensor=sensor,  # Usamos el id del sensor encontrado
                    id_tipo_dato=tipo_dato,
                    valor=valor
                )
                return JsonResponse({'message': 'Datos insertados correctamente en la base de datos y respaldo actualizado'}, status=200)

            except Exception as db_error:
                # Si ocurre un error con la base de datos
                return JsonResponse({'error': f'Error al insertar en la base de datos: {str(db_error)}. Los datos se han guardado en el archivo de respaldo.'}, status=500)
        
        except Exception as e:
            traceback.print_exc()  # Imprimir la traza del error en el servidor para depuración
            return JsonResponse({'error': f'Error inesperado en el servidor: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    

@api_view(['GET'])
def datos_recientes(request): #para las tablas al final del home
    # Obtener los últimos datos de temperatura y humedad
    temperature_data = RegistroSensor.objects.filter(id_tipo_dato__nombre_dato='Temperatura') \
                                              .order_by('-fecha_registro')[:10]
    humidity_data = RegistroSensor.objects.filter(id_tipo_dato__nombre_dato='Humedad') \
                                            .order_by('-fecha_registro')[:10]

    # Serializar los datos
    temperature_serializer = RegistroSensorSerializer(temperature_data, many=True)
    humidity_serializer = RegistroSensorSerializer(humidity_data, many=True)

    # Retornar la respuesta JSON con los datos serializados
    return Response({
        'temperature': temperature_serializer.data,
        'humidity': humidity_serializer.data
    })



def detalle_dato(request): #ver_mas
    dato = request.GET.get('dato', None)
    if dato not in ['Temperatura', 'Humedad']:
        return JsonResponse({'error': 'Tipo de dato inválido.'}, status=400)

    tipo_dato = get_object_or_404(TipoDato, nombre_dato=dato)
    datos_sensores = RegistroSensor.objects.filter(id_tipo_dato=tipo_dato).order_by('-fecha_registro')[:10]

    # Recolecta los datos para el gráfico
    chart_data = []
    for data_point in datos_sensores:
        chart_data.append({
            'fecha': data_point.fecha_registro.strftime('%Y-%m-%d %H:%M:%S'),
            'valor': data_point.valor,
        })

    # Verificar si la solicitud es AJAX usando el header HTTP_X_REQUESTED_WITH
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Aquí se añaden los datos de la tabla
        table_data = []
        for data in datos_sensores[:10]:  # Solo los 10 primeros para la tabla
            table_data.append({
                'valor': f"{data.valor:.2f} {tipo_dato.unidad_medida}",
                'fecha': data.fecha_registro.strftime('%d/%m/%Y %H:%M'),
                'sensor': data.id_sensor.modelo_arduino,  # Suponiendo que quieres el nombre del sensor desde Arduino
                'tipo_sensor': data.id_sensor.id_modelo_sensor.nombre_sensor,  # El nombre del modelo de sensor
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


