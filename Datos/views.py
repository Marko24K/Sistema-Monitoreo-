from django.db.models import Q
from django.utils import timezone
from datetime import datetime

import os
from PIL import Image
import qrcode
from django.contrib import messages
import traceback
from django.shortcuts import  redirect, render, get_object_or_404
from Sistema.settings import BACKUP_DIR
from .models import Arduino, RegistroSensor, Sensor, TipoDato, Espacio, TipoPlanta,Planta, ModeloSensor,RegistroPlanta, DivisionEspacio, Localidad,TipoEspacio
from django.http import Http404, HttpResponse, JsonResponse
from django.db.models import Avg, Max, Min
import json
from rest_framework.decorators import api_view
from django.conf import settings
from .serializer import RegistroSensorSerializer

#-----------------------mini forms-----------------------
def arduino(request,id_espacio,id_arduino = None):
    espacio = get_object_or_404(Espacio, id_espacio=id_espacio)
    arduino = None

    if id_arduino:
        arduino = get_object_or_404(Arduino, id_arduino=id_arduino)

    if request.method == 'POST':
        modelo_arduino = request.POST.get('modelo_arduino')
        estado = request.POST.get('options')  # 1 o 0
        if estado is None:
            return HttpResponse("Debe seleccionar el estado del Arduino", status=400)

        estado = int(estado)

        if arduino:
            # Editar Arduino existente
            arduino.modelo_arduino = modelo_arduino
            arduino.estado = estado
            arduino.save()
        else:
            # Crear nuevo Arduino
            arduino = Arduino.objects.create(
                id_espacio=espacio,
                modelo_arduino=modelo_arduino,
                estado=estado
            )

        return redirect('detalle_espacio', id_espacio=espacio.id_espacio)

    return render(request, 'mini_forms/arduino.html', {
        'espacio': espacio,
        'arduino': arduino
    })

def division_espacio(request, id_espacio, id_division=None):
    espacio = get_object_or_404(Espacio, id_espacio=id_espacio)
    division = None
    
    if id_division:
        division = get_object_or_404(DivisionEspacio, id_division_espacio=id_division)
    
    if request.method == 'POST':
        tipo_division = request.POST.get('tipo_division')
        identificador_division = request.POST.get('identificador_division')
        
        if not tipo_division or not identificador_division:
            return HttpResponse("Todos los campos son obligatorios", status=400)
        
        identificador_division = int(identificador_division)
        
        # Validar si el identificador ya existe (excepto si es la misma división en edición)
        if DivisionEspacio.objects.filter(
            identificador=identificador_division, id_espacio=espacio
        ).exclude(id_division_espacio=id_division).exists():
            return HttpResponse("El identificador ya existe para este espacio", status=400)
        
        if division:
            # Editar división existente
            division.tipo_division = tipo_division
            division.identificador = identificador_division
            division.save()
        else:
            # Crear nueva división
            division = DivisionEspacio.objects.create(
                id_espacio=espacio,
                tipo_division=tipo_division,
                identificador=identificador_division
            )
        
        return redirect('detalle_espacio', id_espacio=espacio.id_espacio)
    
    return render(request, 'mini_forms/division_espacio.html', {
        'espacio': espacio,
        'division': division
    })


def modelo_sensor(request, id_espacio):
    espacio = get_object_or_404(Espacio, id_espacio=id_espacio)
    # Filtrar los arduinos que pertenecen a este espacio
    arduinos = Arduino.objects.filter(id_espacio=espacio)

    if request.method == 'POST':
        nombre_sensor = request.POST.get('nombre_sensor')
        descripcion = request.POST.get('Descripcion_sensor')
        estado = request.POST.get('options')
        id_arduino = request.POST.get('id_arduino')

        if not nombre_sensor or not descripcion or estado is None or not id_arduino:
            return HttpResponse("Todos los campos son obligatorios", status=400)

        estado = int(estado)
        arduino = get_object_or_404(Arduino, id_arduino=id_arduino)

        # Crear modelo de sensor
        modelo_sensor = ModeloSensor.objects.create(
            nombre_sensor=nombre_sensor,
            descripcion=descripcion
        )

        # Crear sensor y enlazarlo con Arduino
        sensor = Sensor.objects.create(
            id_arduino=arduino,
            id_modelo_sensor=modelo_sensor,
            estado=estado
        )

        return redirect('detalle_espacio', id_espacio=espacio.id_espacio)

    return render(request, 'mini_forms/modelo_sensor.html', {
        'espacio': espacio,
        'arduinos': arduinos
    })

def planta(request):
    if request.method =='POST':
        return redirect('vistas_datos/vista_espacios.html')
    return render(request, 'mini_forms/planta.html')

def sensor(request):
    return render(request, 'mini_forms/sensor.html')

def tipo_dato(request):
    return render(request, 'mini_forms/tipo_dato.html')

#--------------------Espacio -----------------------------
def vista_plantacion(request , id_planta):
    planta = Planta.objects.filter(id_planta=id_planta)
    registro = RegistroPlanta.objects.filter(id_planta=id_planta)
    return render(request, 'vistas_datos/vista_plantacion.html', {'planta':planta, 'registro':registro})

def vista_sensores(request, id_arduino):
    # Obtener el Arduino relacionado con el id_arduino
    arduinos = Arduino.objects.filter(id_arduino=id_arduino)

    # Obtener los sensores relacionados con esos arduinos
    sensores = Sensor.objects.filter(id_arduino__in=arduinos)

    # Obtener los modelos de sensores
    modelos_sensores = ModeloSensor.objects.filter(id_modelo_sensor__in=sensores.values('id_modelo_sensor'))

    # Crear un diccionario de modelos de sensores y los sensores asociados
    modelos_sensores_dict = {}
    for modelo_sensor in modelos_sensores:
        # Filtrar los sensores relacionados con este modelo de sensor
        sensores_relacionados = sensores.filter(id_modelo_sensor=modelo_sensor)
        modelos_sensores_dict[modelo_sensor] = sensores_relacionados

    return render(request, 'vistas_datos/vista_sensores.html', {'modelos_sensores_dict': modelos_sensores_dict, 'id_arduino': id_arduino })

def cambiar_estado_sensor(request, id_sensor):
    sensor = get_object_or_404(Sensor, id_sensor=id_sensor)
    sensor.estado = 0 if sensor.estado == 1 else 1  # Alternar entre activo e inactivo
    sensor.save()
    return redirect('detalle_espacio', id_espacio=sensor.id_arduino.id_espacio.id_espacio)

def listado_arduinos_sensores(request):
    arduinos = Arduino.objects.prefetch_related('sensor_set').all()
    registros = list(RegistroSensor.objects.values('valor', 'fecha_registro'))
        # Convertir fecha a string con un formato legible
    for registro in registros:
        registro['fecha_registro'] = registro['fecha_registro'].strftime('%d-%m-%Y %H:%M:%S')

    return render(request, 'vistas_datos/listado_arduino_sensores.html', {'arduinos': arduinos, 'registros': registros})

def cambiar_estado_arduino(request, id_arduino):
    arduino = get_object_or_404(Arduino, id_arduino=id_arduino)

    if arduino.estado == 1:
        arduino.estado = 0
        sensores_actualizados = Sensor.objects.filter(id_arduino=arduino.id_arduino).update(estado=0)
        arduino.save()  # Guardamos el estado del Arduino primero
    else:
        arduino.estado = 1
        sensores_actualizados = Sensor.objects.filter(id_arduino=arduino.id_arduino).update(estado=1)
        arduino.save()  # Guardamos el nuevo estado del Arduino
        messages.success(request, "El Arduino ha sido activado. Sus sensores deben activarse manualmente.")

    return redirect('detalle_espacio', id_espacio=arduino.id_espacio.id_espacio)

def registro_espacio(request):
    localidad = Localidad.objects.all()
    tipo_espacio = TipoEspacio.objects.all()
    espacio = None
    if request.method == 'POST':
        localidad_obj = Localidad.objects.get(id_localidad=request.POST['val_localidad_p'])
        imagen_espacio = request.FILES.get('input-imagen', None)
        if imagen_espacio:
            espacio = Espacio.objects.create(
                id_localidad=localidad_obj,
                nombre_espacio=request.POST['val_nombre_p'],
                direccion_espacio=request.POST['val_direccion_p'],
                utm=request.POST['utm'],
                id_tipo_espacio=TipoEspacio.objects.get(id_tipo_espacio=request.POST['tipo_espacio']),
                imagen_espacio=imagen_espacio,  # solo lo agrega si existe
            )
        else:
            espacio = Espacio.objects.create(
                id_localidad=localidad_obj,
                nombre_espacio=request.POST['val_nombre_p'],
                direccion_espacio=request.POST['val_direccion_p'],
                utm=request.POST['utm'],
                id_tipo_espacio=TipoEspacio.objects.get(id_tipo_espacio=request.POST['tipo_espacio']),
                imagen_espacio=None,  # Asignar None si no se manda una imagen
            )


        data = f"#" #cambiar direccion hacia la vista_parcela con el id que se agrega
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'icon.png')

        # Crear el objeto QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Crear la imagen QR con color verde
        img = qr.make_image(fill='green', back_color='white')

        # Convertir la imagen a un objeto de Pillow
        img = img.convert('RGB')

        # Redimensionar y colocar el logo
        width, height = img.size
        for x in range(width):
            for y in range(height):
                pixel = img.getpixel((x, y))
                if pixel != (255, 255, 255):
                    img.putpixel((x, y), (123, 187, 4))

        logo = Image.open(logo_path)
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        logo_size = int(img.size[0] * 0.3)
        logo = logo.resize((logo_size, logo_size))

        # Obtener la posición para centrar el logo
        img_width, img_height = img.size
        logo_width, logo_height = logo.size
        position = ((img_width - logo_width) // 2, (img_height - logo_height) // 2)

        img.paste(logo, position, logo)

        # Guardar la imagen
        image_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes_espacios', f'Espacio_{espacio.nombre_espacio}_id_{espacio.id_espacio}.png')
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        img.save(image_path)
        espacio.codigoqr = os.path.relpath(image_path, settings.MEDIA_ROOT)
        espacio.save()

        return redirect('vista_espacios')

    return render(request, 'forms/registro_espacio.html', {'localidad': localidad
                                                           ,'tipo_espacio':tipo_espacio})

def vista_espacios(request):
    vista = Espacio.objects.all()
    return render(request, 'vistas_datos/vista_espacios.html', {'vista': vista})

def editar_espacio(request, id_espacio):
    espacio = get_object_or_404(Espacio, id_espacio=id_espacio)
    tipo_espacio = TipoEspacio.objects.all()
    localidad = Localidad.objects.all()

    if request.method == 'POST':
        espacio.id_localidad = Localidad.objects.get(id_localidad=request.POST['val_localidad_p'])
        espacio.nombre_espacio = request.POST['val_nombre_p']
        espacio.direccion_espacio = request.POST['val_direccion_p']
        espacio.utm = request.POST['utm']
        espacio.id_tipo_espacio = TipoEspacio.objects.get(id_tipo_espacio=request.POST['tipo_espacio'])

        # Verificar si se ha subido una nueva imagen
        if 'input-imagen' in request.FILES:
            # Eliminar la imagen anterior si existe
            if espacio.imagen_espacio:
                try:
                    if os.path.exists(espacio.imagen_espacio.path):
                        os.remove(espacio.imagen_espacio.path)
                except Exception as e:
                    print(f"Error al intentar eliminar la imagen anterior: {e}")
            
            # Asignar la nueva imagen
            espacio.imagen_espacio = request.FILES['input-imagen']
        espacio.save()
        messages.success(request, "La Espacio ha sido editada exitosamente.")
        return redirect('vista_espacios')

    return render(request, 'forms/registro_espacio.html', {'espacio': espacio, 'localidad': localidad ,'tipo_espacio':tipo_espacio})


def detalle_espacio(request, id_espacio):
    # Obtener el espacio correspondiente
    dato = get_object_or_404(Espacio, id_espacio=id_espacio)
    division = DivisionEspacio.objects.filter(id_espacio=dato)
    tipo_espacio = dato.id_tipo_espacio.nombre_tipo_espacio 
    plantas = Planta.objects.filter(registroplanta__id_division_espacio__id_espacio=dato).distinct()
    arduino = Arduino.objects.filter(id_espacio=dato)


    # Obtener la fecha actual con zona horaria
    fecha_actual = timezone.localtime(timezone.now())  # Fecha y hora actual con zona horaria
    fecha_actual = fecha_actual.date()  # Extraer solo la fecha para comparación

    # Filtrar plantas dependiendo del tipo de espacio
    if tipo_espacio == "Invernadero":
        # Solo mostrar plantas dentro del rango de fechas en invernaderos
        plantas = plantas.filter(
            Q(fecha_siembra__date__lte=fecha_actual) &  # Asegurar que la fecha de siembra sea antes o igual a hoy
            Q(fecha_extraccion__date__gte=fecha_actual)  # Asegurar que la fecha de extracción sea después o igual a hoy
        )
    # Estructurar los datos de los sensores por Arduino
    arduino_sensores = []
    for a in arduino:
        sensores = Sensor.objects.filter(id_arduino=a, estado=1)  # Solo sensores activos
        arduino_sensores.append({
            'arduino': a,
            'sensores': sensores
        })
    
    return render(request, 'vistas_datos/vista_espacio.html', {
        'dato': dato,
        'division': division,
        'plantas': plantas,
        'arduino_sensores': arduino_sensores,
        'id_espacio': id_espacio
    })

def editar_division(request, id_division_espacio, id_espacio):
    # Obtener la división de espacio que se desea editar
    division = get_object_or_404(DivisionEspacio, id_division_espacio=id_division_espacio)
    
    # Obtener todos los espacios disponibles
    espacios = Espacio.objects.all()

    if request.method == 'POST':
        # Recuperar los datos del formulario
        id_espacio = request.POST.get('id_espacio')  # Ahora se obtiene desde el formulario
        tipo_division = request.POST.get('tipo_division')
        identificador_division = request.POST.get('identificador_division')

        # Actualizar la instancia de la división de espacio
        division.id_espacio = Espacio.objects.get(id_espacio=id_espacio)
        division.tipo_division = tipo_division
        division.identificador = identificador_division

        # Guardar los cambios
        division.save()

        # Redirigir al detalle del espacio con el id correspondiente
        return redirect('detalle_espacio', id_espacio=id_espacio)

    # Si es un GET, mostrar el formulario con los datos de la división de espacio
    return render(request, 'mini_forms/division_espacio.html', {
        'espacios': espacios,
        'division': division,  # Pasar la instancia de la división para pre-llenar los campos
        'id_espacio': id_espacio,  # Pasar id_espacio a la plantilla
    })

def registro_planta(request, id_espacio):
    # Obtener el espacio y las divisiones asociadas
    dato = get_object_or_404(Espacio, id_espacio=id_espacio)
    division = DivisionEspacio.objects.filter(id_espacio=dato)
    plantacion = Planta.objects.all()
    
    if request.method == 'POST':
        # Obtener los valores del formulario
        id_division_espacio = request.POST.get('id_division_espacio')
        division_obj = get_object_or_404(DivisionEspacio, id_division_espacio=id_division_espacio)

        # Crear el registro de la planta
        RegistroPlanta.objects.create(
            numero_planta=request.POST.get('numero_planta'),
            altura=request.POST.get('altura'),
            largo=request.POST.get('largo'),
            ancho=request.POST.get('ancho'),
            grosor=request.POST.get('grosor'),
            vigor=request.POST.get('vigor'),
            turgencia=request.POST.get('turgencia'),
            vitalidad=request.POST.get('vitalidad'),
            plaga_enfermedad=request.POST.get('plaga_enfermedad'),
            descripcion_plaga_enfermedad=request.POST.get('descripcion_plaga_enfermedad', None),
            observaciones_registro=request.POST.get('observaciones_registro', None),
            imagen_registro_planta=request.FILES.get('input-imagen', None),
            id_division_espacio=division_obj,
            id_planta=Planta.objects.get(id_planta=request.POST.get('plantacion'))
        )

    # Renderizar la plantilla con los datos necesarios
    return render(request, 'forms/registro_planta.html', {
        'division': division,
        'plantacion': plantacion
    })





# Vista para mostrar los sensores y sus datos
def datos_por_sensor(request):
    sensores = Sensor.objects.all()  # Obtenemos todos los sensores

    context = {
        'sensores': sensores,
    }
    return render(request, 'vistas_datos/datos_por_sensor.html', context)

# Vista para obtener los datos de un sensor
def obtener_datos_sensor(request):
    sensor_id = request.GET.get('sensor_id')  # Obtener el ID del sensor seleccionado desde el GET

    if sensor_id:
        # Obtener el sensor seleccionado
        sensor = get_object_or_404(Sensor, id_sensor=sensor_id)

        # Obtener el modelo de sensor asociado
        modelo_sensor = sensor.id_modelo_sensor

        if modelo_sensor.nombre_sensor == "DHT22":
            # Sensor DHT22: obtener registros de temperatura y humedad del mismo sensor
            registro_temperatura = RegistroSensor.objects.filter(
                id_sensor=sensor, id_tipo_dato=1  # Tipo de dato 1 = Temperatura
            ).order_by('-fecha_registro').first()

            registro_humedad = RegistroSensor.objects.filter(
                id_sensor=sensor, id_tipo_dato=2  # Tipo de dato 2 = Humedad
            ).order_by('-fecha_registro').first()

            response = {
                'tipo': 'DHT22',
                'temperatura': registro_temperatura.valor if registro_temperatura else "No disponible",
                'humedad': registro_humedad.valor if registro_humedad else "No disponible",
            }
        else:
            # Otros sensores: obtener el registro más reciente (independiente del tipo de dato)
            registro_sensor = RegistroSensor.objects.filter(
                id_sensor=sensor
            ).order_by('-fecha_registro').first()

            response = {
                'tipo': 'otro',
                'valor': registro_sensor.valor if registro_sensor else "No disponible",
                'tipo_dato': registro_sensor.id_tipo_dato.nombre_dato if registro_sensor else "No disponible",
            }

        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'Sensor no válido'}, status=400)
    
def tipo_planta(request):
    imagen_planta = request.FILES.get('input-imagen', None)
    if request.method == 'POST':
        if imagen_planta:
            TipoPlanta.objects.create(
                nombre_comun = request.POST['nombre_comun'],
                nombre_cientifico = request.POST['nombre_cientifico'],
                descripcion = request.POST['descripcion_planta'],
                imagen_tipo_planta = request.FILES['input-imagen'],
            )
        else:
            TipoPlanta.objects.create(
                nombre_comun = request.POST['nombre_comun'],
                nombre_cientifico = request.POST['nombre_cientifico'],
                descripcion = request.POST['descripcion_planta'],
                imagen_tipo_planta = None,
            )
            
    return render(request, 'forms/tipo_planta.html')

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
def datos(request):
    valores = RegistroSensor.objects.all()
    registros = RegistroSensor.objects.values('fecha_registro', 'valor')  # Obtiene solo los campos necesarios
    return render(request, '.html', {'registros': registros})
    
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
#pruebas
def obtener_estadisticas(id_tipo_dato):
    
    return RegistroSensor.objects.filter(id_tipo_dato_id=id_tipo_dato).aggregate(
        max_value=Max('valor'),
        min_value=Min('valor'),
        avg_value=Avg('valor')
    )

def visualizar_datos(request):
    # Obtener todos los tipos de datos
    tipos_dato = TipoDato.objects.all()
    estadisticas = {}

    for tipo in tipos_dato:
        registros = RegistroSensor.objects.filter(id_tipo_dato=tipo).order_by("fecha_registro")

        etiquetas = [registro.fecha_registro.strftime("%Y-%m-%d %H:%M") for registro in registros]
        valores = [float(registro.valor) for registro in registros]  # Convertir a float

        # Guardar en el diccionario con el nombre del tipo de dato
        estadisticas[tipo.nombre_dato] = {"etiquetas": etiquetas, "valores": valores}

    return render(request, "home.html", {"estadisticas": estadisticas})

def home(request):
    # Obtener todos los tipos de datos
    tipos_dato = TipoDato.objects.values('id_tipo_dato', 'nombre_dato')

    # Generar estadísticas para cada tipo de dato
    estadisticas = {}
    for tipo in tipos_dato:
        id_tipo = tipo['id_tipo_dato']
        nombre = tipo['nombre_dato']

        # Obtener estadísticas y datos recientes
        stats = obtener_estadisticas(id_tipo)
        datos_recientes = RegistroSensor.objects.filter(id_tipo_dato_id=id_tipo).order_by('-fecha_registro')[:10]

        # Serializar los datos recientes
        datos_serializer = RegistroSensorSerializer(datos_recientes, many=True)

        # Guardar en el diccionario
        estadisticas[nombre] = {
            'max': stats['max_value'],
            'min': stats['min_value'],
            'avg': stats['avg_value'],
            'datos_recientes': datos_serializer.data,
        }

    return render(request, 'home.html', {'estadisticas': estadisticas})

@api_view(['GET'])
def datos_recientes(request):
    # Obtener todos los tipos de datos
    tipos_dato = TipoDato.objects.values('id_tipo_dato', 'nombre_dato')

    # Generar estadísticas para cada tipo de dato
    estadisticas = {}
    for tipo in tipos_dato:
        id_tipo = tipo['id_tipo_dato']
        nombre = tipo['nombre_dato']

        # Obtener estadísticas y datos recientes
        stats = obtener_estadisticas(id_tipo)
        datos_recientes = RegistroSensor.objects.filter(id_tipo_dato_id=id_tipo).order_by('-fecha_registro')[:10]

        # Serializar los datos recientes
        datos_serializer = RegistroSensorSerializer(datos_recientes, many=True)

        # Guardar en el diccionario
        estadisticas[nombre] = {
            'max': stats['max_value'],
            'min': stats['min_value'],
            'avg': stats['avg_value'],
            'datos_recientes': datos_serializer.data,
        }

    return JsonResponse({'estadisticas': estadisticas})