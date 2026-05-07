from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Incidente
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from decouple import config
import requests

def administracion(request):
    if request.method == 'POST':
        numero_incidente = request.POST.get('numero_incidente')
        estado = request.POST.get('estado', 'pendiente')
        
        if numero_incidente:
            incidente, created = Incidente.objects.get_or_create(
                numero_incidente=numero_incidente,
                defaults={'estado': estado}
            )
            
            if not created:
                incidente.estado = estado
                incidente.save()
            
            # Enviar actualización por WebSocket
            notificar_actualizacion()
            
            return redirect('administracion')
    
    incidentes = Incidente.objects.all().order_by('-fecha_creacion')
    return render(request, 'incidentes/administracion.html', {'incidentes': incidentes})

def actualizar_estado(request, incidente_id):
    if request.method == 'POST':
        incidente = get_object_or_404(Incidente, id=incidente_id)
        nuevo_estado = request.POST.get('estado')
        
        if nuevo_estado in ['pendiente', 'asignada', 'cerrada']:
            incidente.estado = nuevo_estado
            incidente.save()
            
            # Enviar actualización por WebSocket
            notificar_actualizacion()
            
            return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

def eliminar_incidente(request, incidente_id):
    if request.method == 'POST':
        incidente = get_object_or_404(Incidente, id=incidente_id)
        incidente.delete()
        
        # Enviar actualización por WebSocket
        notificar_actualizacion()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

def consulta(request):
    incidentes = Incidente.objects.all().order_by('-fecha_creacion')
    return render(request, 'incidentes/consulta.html', {'incidentes': incidentes})

def notificar_actualizacion():
    """Envía notificación a todos los clientes conectados via WebSocket"""
    channel_layer = get_channel_layer()
    incidentes_qs = Incidente.objects.all().order_by('-fecha_creacion')
    incidentes = [
        {
            'id': inc.id,
            'numero_incidente': inc.numero_incidente,
            'estado': inc.estado,
            'fecha_creacion': inc.fecha_creacion.isoformat(),
            'fecha_actualizacion': inc.fecha_actualizacion.isoformat()
        }
        for inc in incidentes_qs
    ]
    
    async_to_sync(channel_layer.group_send)(
        'incidentes_updates',
        {
            'type': 'incidente_update',
            'incidentes': incidentes
        }
    )

def sincronizar_metabase(request):
    """Sincroniza incidentes desde Metabase"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'})
    
    try:
        # Configuración de Metabase desde variables de entorno
        METABASE_URL = config('METABASE_URL', default='http://157.230.229.30/')
        METABASE_USER = config('METABASE_USER')
        METABASE_PASSWORD = config('METABASE_PASSWORD')
        METABASE_CARD_ID = config('METABASE_CARD_ID', default='51', cast=int)
        
        # LOGIN
        login = requests.post(
            f"{METABASE_URL}/api/session",
            json={
                "username": METABASE_USER,
                "password": METABASE_PASSWORD
            },
            timeout=10
        )
        
        if login.status_code != 200:
            return JsonResponse({'success': False, 'error': 'Error en login de Metabase'})
        
        session_id = login.json()["id"]
        
        headers = {
            "X-Metabase-Session": session_id
        }
        
        # EJECUTAR REPORTE (card)
        response = requests.post(
            f"{METABASE_URL}/api/card/{METABASE_CARD_ID}/query/json",
            headers=headers,
            timeout=10
        )
        
        if response.status_code != 200:
            return JsonResponse({'success': False, 'error': 'Error al obtener datos del reporte'})
        
        data = response.json()
        
        # Mapeo de estados de Metabase a estados del sistema
        MAPEO_ESTADOS = {
            'Nueva': 'pendiente',
            'Asignada': 'asignada',
            'Finalizada': 'cerrada',
        }
        
        # Procesar los datos del reporte
        # Estructura: [{'IdPrestacion': 714, 'NumeroDePrestacion': 465, 'Estado': 'Nueva'}, ...]
        
        nuevos = 0
        actualizados = 0
        
        for item in data:
            # Obtener campos de Metabase
            numero_prestacion = item.get('NumeroDePrestacion')
            estado_metabase = item.get('Estado', 'Nueva')
            
            # Mapear estado de Metabase a estado del sistema
            estado = MAPEO_ESTADOS.get(estado_metabase, 'pendiente')
            
            if numero_prestacion:
                # Usar NumeroDePrestacion como número de incidente
                numero_incidente = numero_prestacion
                
                # Crear o actualizar incidente
                incidente, created = Incidente.objects.get_or_create(
                    numero_incidente=numero_incidente,
                    defaults={'estado': estado}
                )
                
                if created:
                    nuevos += 1
                else:
                    # Solo actualizar si el estado cambió
                    if incidente.estado != estado:
                        incidente.estado = estado
                        incidente.save()
                        actualizados += 1
        
        # Notificar a todos los clientes conectados
        notificar_actualizacion()
        
        return JsonResponse({
            'success': True,
            'nuevos': nuevos,
            'actualizados': actualizados,
            'total': len(data)
        })
        
    except requests.Timeout:
        return JsonResponse({'success': False, 'error': 'Timeout en conexión con Metabase'})
    except requests.RequestException as e:
        return JsonResponse({'success': False, 'error': f'Error de conexión: {str(e)}'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Error: {str(e)}'})
