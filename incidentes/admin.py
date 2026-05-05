from django.contrib import admin
from .models import Incidente

@admin.register(Incidente)
class IncidenteAdmin(admin.ModelAdmin):
    list_display = ('numero_incidente', 'estado', 'fecha_creacion', 'fecha_actualizacion')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('numero_incidente',)
