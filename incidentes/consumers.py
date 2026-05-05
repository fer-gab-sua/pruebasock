import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Incidente

class IncidenteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'incidentes_updates'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Enviar estado inicial
        incidentes = await self.get_incidentes()
        await self.send(text_data=json.dumps({
            'type': 'initial_data',
            'incidentes': incidentes
        }))
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from WebSocket
    async def receive(self, text_data):
        pass
    
    # Receive message from room group
    async def incidente_update(self, event):
        incidentes = event['incidentes']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'update',
            'incidentes': incidentes
        }))
    
    @database_sync_to_async
    def get_incidentes(self):
        incidentes = Incidente.objects.all().order_by('-fecha_creacion')
        return [
            {
                'id': inc.id,
                'numero_incidente': inc.numero_incidente,
                'estado': inc.estado,
                'fecha_creacion': inc.fecha_creacion.isoformat(),
                'fecha_actualizacion': inc.fecha_actualizacion.isoformat()
            }
            for inc in incidentes
        ]
