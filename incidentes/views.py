from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Incidente
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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
