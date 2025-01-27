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

#--------------------Espacio -----------------------------
def vista_plantacion(request):
    return render(request, 'vistas_datos/vista_plantacion.html')

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

def eliminar_espacio(request, id_espacio):
    espacio = get_object_or_404(Espacio, id_espacio=id_espacio)
    espacio.delete()
    messages.success(request, "La Espacio ha sido eliminada exitosamente.")

    return redirect('vista_espacios')  
def detalle_espacio(request, id_espacio):
    # Obtener la parcela correspondiente a 'id_parcela'
    dato = get_object_or_404(Espacio, id_espacio=id_espacio)
    division = DivisionEspacio.objects.filter(id_espacio=dato)
    plantas = Planta.objects.filter(registroplanta__id_division_espacio__id_espacio=dato)
    arduino = Arduino.objects.filter(id_espacio=dato)

    # Pasar los detalles de la Espacio a la plantilla
    return render(request, 'vistas_datos/vista_espacio.html',
                   {'dato': dato,
                    'division': division,
                    'plantas': plantas, 
                    'arduino':arduino,
                    'id_espacio': id_espacio})



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

def eliminar_division(request, id_division_espacio, id_espacio):
    
    division = get_object_or_404(DivisionEspacio, id_division_espacio=id_division_espacio)
    division.delete()
    return redirect('detalle_espacio', id_espacio=id_espacio)  

def eliminar_arduino(request,id_arduino, id_espacio):
    # Obtener el objeto Arduino por su id_arduino
    arduino = get_object_or_404(Arduino, id_arduino=id_arduino)

    # Eliminar el Arduino
    arduino.delete()

    # Redirigir a la vista del espacio correspondiente
    return redirect('detalle_espacio', id_espacio=id_espacio)


def modal_view(request):
    form_type = request.GET.get('form_type', '')
    id_espacio = request.POST.get('id_espacio')
    context = {}  # Añadimos id_espacio al contexto

    if not form_type:
        return Http404("Formulario no especificado")

    # Ruta de la plantilla correspondiente
    template_path = f'mini_forms/{form_type}.html'

    if form_type == 'division_espacio':
        if request.method == 'POST':
            # Verificar que los campos requeridos no estén vacíos
            
            tipo_division = request.POST.get('tipo_division')
            identificador_division = request.POST.get('identificador_division')

            if not id_espacio or not tipo_division or not identificador_division:
                return HttpResponse("Todos los campos son obligatorios", status=400)

            # Verificar si el identificador ya existe en ese espacio
            if DivisionEspacio.objects.filter(identificador=identificador_division, id_espacio_id=id_espacio).exists():
                return HttpResponse("El identificador de la división ya existe para este espacio", status=400)

            try:
                espacio = Espacio.objects.get(id_espacio=id_espacio)
            except Espacio.DoesNotExist:
                return HttpResponse("Espacio no encontrado", status=404)

            # Crear la nueva división
            nueva_division = DivisionEspacio.objects.create(
                id_espacio=espacio,
                tipo_division=tipo_division,
                identificador=identificador_division
            )

            # Redirigir a la vista de detalle del espacio
            return redirect('detalle_espacio', id_espacio=espacio.id_espacio)

        # Si no es un POST, simplemente retornar el formulario vacío con el id_espacio
        id_espacio = request.GET.get('id_espacio')
        try:
            espacio = Espacio.objects.get(id_espacio=id_espacio)
        except Espacio.DoesNotExist:
            return HttpResponse("Espacio no encontrado", status=404)

        return render(request, 'mini_forms/division_espacio.html', {'espacio': espacio, 'id_espacio': id_espacio})
        
    elif form_type == 'modelo_sensor':
        if request.method == 'POST':
            nombre_sensor = request.POST['nombre_sensor']
            descripcion_sensor = request.POST['Descripcion_sensor']
            id_arduino = request.POST.get('id_arduino')  # ID del Arduino al que se va a enlazar
            estado = 1 if request.POST['options'] == '1' else 0  # 1 para activo, 0 para inactivo

            if not nombre_sensor or not descripcion_sensor or not id_arduino:
                return HttpResponse("Todos los campos son obligatorios.", status=400)

            try:
                # Obtener el Arduino al que se va a enlazar
                arduino = Arduino.objects.get(id_arduino=id_arduino)
            except Arduino.DoesNotExist:
                return HttpResponse("Arduino no encontrado.", status=404)

            # Crear el modelo de sensor y enlazarlo al Arduino
            modelo_sensor = ModeloSensor.objects.create(
                nombre_sensor=nombre_sensor,
                descripcion=descripcion_sensor
            )

            # Enlazar el sensor al Arduino (suponiendo que hay una tabla Sensor para eso)
            Sensor.objects.create(
                id_arduino=arduino,
                id_modelo_sensor=modelo_sensor,
                estado = estado
            )

            # Redirigir de vuelta a la vista de sensores
            return redirect('vista_sensores', id_arduino=arduino.id_arduino)

        # Si no es un POST, renderizar el formulario vacío
        id_arduino = request.GET.get('id_arduino')  # Obtener el ID del Arduino desde el GET
        if not id_arduino:
            return HttpResponse("ID del Arduino no proporcionado.", status=400)

        try:
            arduino = Arduino.objects.get(id_arduino=id_arduino)
        except Arduino.DoesNotExist:
            return HttpResponse("Arduino no encontrado.", status=404)

        return render(request, 'mini_forms/modelo_sensor.html', {'arduino': arduino, 'id_arduino': id_arduino})
        
    elif form_type == 'arduino':
        if request.method == 'POST':
            modelo_arduino = request.POST['modelo_arduino']
            estado = 1 if request.POST['options'] == '1' else 0  # 1 para activo, 0 para inactivo

            if not modelo_arduino or not id_espacio:
                return HttpResponse("Por favor, complete todos los campos del formulario.")
            try:
                espacio = Espacio.objects.get(id_espacio=id_espacio)
            except Espacio.DoesNotExist:
                return HttpResponse("Espacio no encontrado", status=404)
            
            Arduino.objects.create(
                modelo_arduino=modelo_arduino,
                id_espacio_id=id_espacio,
                estado=estado,
            )
            return redirect('detalle_espacio', id_espacio=espacio.id_espacio) 
        # Si no es un POST, simplemente retornar el formulario vacío con el id_espacio
        id_espacio = request.GET.get('id_espacio')
        try:
            espacio = Espacio.objects.get(id_espacio=id_espacio)
        except Espacio.DoesNotExist:
            return HttpResponse("Espacio no encontrado", status=404)

        return render(request, 'mini_forms/arduino.html', {'espacio': espacio, 'id_espacio': id_espacio})
        
    elif form_type == 'planta':
        tipo_p = TipoPlanta.objects.all()
        if request.method == 'POST':
            return redirect('vista_Espacios')
        return render(request, 'mini_forms/planta.html', {'tipo_p': tipo_p, 'id_espacio': id_espacio})
        
    elif form_type == 'sensor':
        if request.method == 'POST':
            return redirect('vista_Espacios') 


    try:
        return render(request, template_path, context)
    except Exception as e:
        print(f"Error al cargar la plantilla {template_path}: {e}")
        return render(request, 'mini_forms/arduino.html')
    

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