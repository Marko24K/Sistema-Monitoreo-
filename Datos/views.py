from datetime import datetime
import os
#import qrcode
from django.core.files.storage import FileSystemStorage
from io import BytesIO
from django.core.files.base import ContentFile
from django.contrib import messages
import traceback
from django.shortcuts import  redirect, render, get_object_or_404
from Sistema.settings import BACKUP_DIR
from .models import Arduino, RegistroSensor, Sensor, TipoDato, Parcela, TipoPlanta, ModeloSensor,RegistroPlanta, DivisionParcela
from django.http import Http404, HttpResponse, JsonResponse
from django.db.models import Avg, Max, Min
import json
from rest_framework.decorators import api_view
from django.conf import settings
from .serializer import RegistroSensorSerializer

def home2(request):
    return render(request, 'home2.html')

def vista_division_parcela(request):
    return render(request, 'vistas_datos/vista_parcela.html')

def vista_parcelas(request):
    return render(request, 'vistas_datos/vista_parcelas.html')


#------------forms------------------------


def registro_planta(request):
    if request.method == 'POST':
        RegistroPlanta.objects.create(
            numero_planta = request.POST['numero_planta'],
            altura = request.POST['altura'],
            largo = request.POST['largo '],
            ancho = request.POST['ancho'],
            grosor = request.POST['grosor'],
            vigor = request.POST['vigor'],
            turgencia = request.POST['turgencia'],
            vitalidad = request.POST['vitalidad'],
            plaga_enfermedad = request.POST['plaga_enfermedad'],
            descripcion_plaga_enfermedad = request.POST['descripcion_plaga_enfermedad'],
            observaciones_Registro = request.POST['observaciones_Registro'],
        )
    return render(request, 'forms/registro_planta.html')

def modal_view(request):
    form_type = request.GET.get('form_type', '')  # Obtener el tipo de formulario de la URL

    if not form_type:
        return Http404("Formulario no especificado")

    # Ruta de la plantilla correspondiente
    template_path = f'mini_forms/{form_type}.html'

    context = {}

    if form_type == 'division_parcela':
        parcelas = Parcela.objects.all()  # Obtener las parcelas
        context['parcelas'] = parcelas

        if request.method == 'POST':
            id_parcela = request.POST.get('id_parcela')
            tipo_division = request.POST.get('tipo_division')  # Asegúrate de que sea texto
            identificador_division = request.POST.get('identificador_division')

            # Verificar si el identificador ya existe
            existe = DivisionParcela.objects.filter(id_parcela=id_parcela, identificador=identificador_division).exists()

            if existe:
                messages.error(request, 'Este número identificador ya existe para la parcela seleccionada.')
            else:
                DivisionParcela.objects.create(
                    id_parcela_id=id_parcela,
                    tipo_division=tipo_division,  # Almacena el texto aquí
                    identificador=identificador_division,
                )
                messages.success(request, 'La división se ha creado exitosamente.')

            return redirect('bt_varios')  
    elif form_type == 'modelo_sensor':
        # Obtener la lista de Arduinos disponibles
        arduino_list = Arduino.objects.all()
        context['arduino_list'] = arduino_list  # Pasar los Arduinos al contexto

        if request.method == 'POST':
            id_arduino = request.POST.get('id_arduino')  # Obtener el Arduino seleccionado
            nombre_sensor = request.POST.get('nombre_sensor')
            descripcion_sensor = request.POST.get('Descripcion_sensor')

            # Crear el modelo de sensor
            ModeloSensor.objects.create(
                nombre_sensor=nombre_sensor,
                descripcion=descripcion_sensor,
            )
            
            return redirect('bt_varios') 
        
    elif form_type == 'arduino':
        parcelas = Parcela.objects.all()  
        context['parcelas'] = parcelas
        
        if request.method == 'POST':
            return redirect('bt_varios') 
        
    elif form_type == 'planta':
        if request.method == 'POST':
            return redirect('bt_varios')
        
    elif form_type == 'sensor':
        if request.method == 'POST':
            return redirect('bt_varios') 


    try:
        return render(request, template_path, context)
    except Exception as e:
        print(f"Error al cargar la plantilla {template_path}: {e}")
        return render(request, 'mini_forms/arduino.html')

def registro_parcela(request):
    if request.method == 'POST':
        # procesamiento de los datos del formulario y crear una nueva instancia
        Parcela.objects.create(
            localidad_parcela=request.POST['val_localidad_p'],
            nombre_parcela=request.POST['val_nombre_p'],
            direccion_parcela=request.POST['val_direccion_p'],
            zona=request.POST['numero_zona'],
            hemisferio=request.POST['hemisferio'],
            easting=request.POST['falso_este'],
            northing=request.POST['falso_norte'],
            imagen_parcela=request.FILES['input-imagen'],  # Si la imagen está en el formulario
        )
    return render(request, 'forms/registro_parcela.html')


def tipo_planta(request):
    if request.method == 'POST':
        TipoPlanta.objects.create(
            nombre_comun = request.POST['nombre_comun'],
            nombre_cientifico = request.POST['nombre_cientifico'],
            descripcion = request.POST['descripcion_planta'],
            imagen_tipo_planta = request.FILES['input-imagen'],
        )
    return render(request, 'forms/tipo_planta.html')

#---------------------------------------------------------------------------------
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

            # Paso 1: Buscar el ModeloSensor utilizando el id del modelo 
            try:
                modelo_sensor = ModeloSensor.objects.get(id_modelo_sensor=id_modelo_sensor)
            except ModeloSensor.DoesNotExist:
                return JsonResponse({'error': f'Modelo de sensor con id {id_modelo_sensor} no encontrado'}, status=404)

            # Paso 2: Buscar en la tabla Sensor asociado con ese ModeloSensor
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
    
def home2(request):
    return render(request, 'forms/home2.html')
#------visualizacion en home
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
    temp_recent = RegistroSensor.objects.filter(id_tipo_dato__nombre_dato="Temperatura").order_by('-fecha_registro')[:10]
    hum_recent = RegistroSensor.objects.filter(id_tipo_dato__nombre_dato="Humedad").order_by('-fecha_registro')[:10]

    temp_serializer = RegistroSensorSerializer(temp_recent, many=True)
    hum_serializer = RegistroSensorSerializer(hum_recent , many=True)

    return render(request, 'home.html', {
        'latest_temperature': temp_data,  
        'latest_humidity': humidity_data,        
        'temp_max': temp_stats['max_value'],
        'temp_min': temp_stats['min_value'],
        'temp_avg': temp_stats['avg_value'],
        'hum_max': hum_stats['max_value'],
        'hum_min': hum_stats['min_value'],
        'hum_avg': hum_stats['avg_value'],
        'temp_recent': temp_serializer.data,
        'hum_recent': hum_serializer.data
    })

@api_view(['GET']) 
def datos_recientes(request):
    # Obtener los datos más recientes de temperatura y humedad (solo los 1 más recientes)
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

    # Obtener los datos recientes de temperatura y humedad (últimos 10)
    temp_recent = RegistroSensor.objects.filter(id_tipo_dato__nombre_dato="Temperatura").order_by('-fecha_registro')[:10]
    hum_recent = RegistroSensor.objects.filter(id_tipo_dato__nombre_dato="Humedad").order_by('-fecha_registro')[:10]

    # Serializar los datos recientes
    temp_serializer = RegistroSensorSerializer(temp_recent, many=True)
    hum_serializer = RegistroSensorSerializer(hum_recent, many=True)

    # Serializar los datos más recientes de temperatura y humedad (los 1 más recientes)
    temp_data_serializer = RegistroSensorSerializer(temp_data, many=True)
    humidity_data_serializer = RegistroSensorSerializer(humidity_data, many=True)

    # Devolver los datos en formato JSON
    return JsonResponse({
        'latest_temperature': temp_data_serializer.data,  # Datos más recientes de temperatura
        'latest_humidity': humidity_data_serializer.data,  # Datos más recientes de humedad
        'temp_max': temp_stats['max_value'],  # Máximo de temperatura
        'temp_min': temp_stats['min_value'],  # Mínimo de temperatura
        'temp_avg': temp_stats['avg_value'],  # Promedio de temperatura
        'hum_max': hum_stats['max_value'],  # Máximo de humedad
        'hum_min': hum_stats['min_value'],  # Mínimo de humedad
        'hum_avg': hum_stats['avg_value'],  # Promedio de humedad
        'temp_recent': temp_serializer.data,  # Últimos 10 datos de temperatura
        'hum_recent': hum_serializer.data  # Últimos 10 datos de humedad
    })

#ver_mas.html
def detalle_dato(request):
    dato = request.GET.get('dato', None)
    if dato not in ['Temperatura', 'Humedad','Humedad_suelo','CO2','TDS']:
        return JsonResponse({'error': 'Tipo de dato inválido.'}, status=400)

    tipo_dato = get_object_or_404(TipoDato, nombre_dato=dato)
    datos_sensores = RegistroSensor.objects.filter(id_tipo_dato=tipo_dato).order_by('-fecha_registro')[:10]

    serializer = RegistroSensorSerializer(datos_sensores, many=True)
    # Recolecta los datos para el gráfico
    chart_data = []
    for data_point in datos_sensores:
        chart_data.append({
            'fecha': data_point.fecha_registro.strftime('%Y-%m-%d %H:%M:%S'),
            'valor': float(data_point.valor),  # Convertir Decimal a float
        })

    # Si la solicitud es AJAX, devolveremos los datos en formato JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'chart_data': [{
                'fecha': data['fecha_registro'],
                'valor': data['valor'],
            } for data in serializer.data],  # Usamos los datos serializados para el gráfico
            'table_data': serializer.data,  # Usamos los datos serializados para la tabla
        })



    return render(request, 'ver_mas.html', {
        'dato': dato,
        'unidad': tipo_dato.unidad_medida,
        'chart_data': json.dumps([{
            'fecha': data['fecha_registro'],
            'valor': data['valor'],
        } for data in serializer.data]),  #  datos serializados para el gráfico
        'recent_data': serializer.data,  # Enviar los datos serializados a la plantilla
    })

def mapa(request):
    return render(request, 'mapa.html')


def vista_parcela(request):
    vista = DivisionParcela.objects.all()

    return render(request, 'vistas_datos/vista_parcela.html', {'vista': vista})

"""
def generar_qr(request, data):
    # Crea un objeto QR
    qr = qrcode.QRCode(
        version=1,  # Tamaño del QR
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Nivel de corrección de errores
        box_size=10,  # Tamaño de cada cuadro
        border=4,  # Tamaño del borde
    )
    
    # Añadir datos al código QR
    qr.add_data(data)
    qr.make(fit=True)
    
    # Crear la imagen del QR
    img = qr.make_image(fill='black', back_color='white')
    
    # Define la ruta en la que quieres guardar el código QR
    folder_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes_division')
    
    # Asegúrate de que la carpeta existe
    os.makedirs(folder_path, exist_ok=True)
    
    # Generar un nombre único para el archivo, por ejemplo, basándote en el tiempo
    qr_filename = f"qr_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    
    # Ruta completa donde se guardará la imagen
    file_path = os.path.join(folder_path, qr_filename)
    
    # Guardar la imagen en la ruta especificada
    img.save(file_path)
    
    # Opcional: Retornar la URL del archivo guardado para que puedas acceder a él
    qr_url = os.path.join(settings.MEDIA_URL, 'qr_codes_division', qr_filename)
    
    return HttpResponse(f'El código QR se ha guardado en: <a href="{qr_url}">Ver QR</a>')
"""
