"""
URL configuration for Sistema project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from Datos import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path


urlpatterns = [
    #forms
    path('registro_espacio/', views.registro_espacio, name='registro_parcela'),
    path('registro_planta/<int:id_espacio>', views.registro_planta, name='registro_planta'),
    path('tipo_planta/', views.tipo_planta, name='tipo_planta'),
    
    #mini_forms
    path('arduino/<int:id_espacio>/', views.arduino, name='arduino'),
    path('arduino/<int:id_espacio>/<int:id_arduino>/', views.arduino, name='arduino'),
    path('division_espacio/<int:id_espacio>/', views.division_espacio, name='division_espacio'), #crear
    path('division_espacio/<int:id_espacio>/<int:id_division_espacio>', views.division_espacio, name='division_espacio'),
    path('modelo_sensor/<int:id_espacio>/', views.modelo_sensor, name='modelo_sensor'),    
    path('modelo_sensor/<int:id_espacio>/<int:id_sensor>', views.modelo_sensor, name='modelo_sensor'),

    path('planta/', views.planta, name='planta'),
    path('planta/<int:id_planta>/', views.planta, name='planta'),

    path('sensor/', views.sensor, name='sensor'),
    path('tipo_dato/', views.tipo_dato, name='tipo_dato'),

    #vistas
    path('vista_plantacion/<int:id_planta>', views.vista_plantacion, name='vista_plantacion'),
    path('vista_sensores/<int:id_arduino>/', views.vista_sensores, name='vista_sensores'),
    path('vista_espacios/', views.vista_espacios, name='vista_espacios'),
    path('detalle_espacio/<int:id_espacio>/', views.detalle_espacio, name='detalle_espacio'),
    path('editar_espacio/<int:id_espacio>/', views.editar_espacio, name='editar_espacio'),
    path('listado_arduinos_sensores/', views.listado_arduinos_sensores, name = 'listado_arduinos_sensores'),
    
    path('cambiar_estado_sensor/<int:id_sensor>/', views.cambiar_estado_sensor, name='cambiar_estado_sensor'),
    path('cambiar_estado_arduino/<int:id_arduino>/', views.cambiar_estado_arduino, name='cambiar_estado_arduino'),
    path('vista_plantacion/<int:id_planta>', views.vista_plantacion, name='vista_plantacion'),
    
    #otros
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),

    path('guardar_datos_sensor/', views.guardar_datos_sensor, name='guardar_datos_sensor'),
    path('datos_recientes/', views.datos_recientes, name='datos_recientes'),

    path('vista_humedales/', views.vista_humedales, name='vista_humedales'),
    path('registro_humedal/<int:id_humedal>/', views.editar_humedal, name='editar_humedal'),
    path('vista_un_humedal/<int:id_humedal>/', views.ver_humedal, name='ver_humedal')
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
