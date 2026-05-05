from django.db import models

class Incidente(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('asignada', 'Asignada'),
        ('cerrada', 'Cerrada'),
    ]
    
    numero_incidente = models.CharField(max_length=100, unique=True, verbose_name='Número de Incidente')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente', verbose_name='Estado')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')
    
    class Meta:
        verbose_name = 'Incidente'
        verbose_name_plural = 'Incidentes'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f'{self.numero_incidente} - {self.get_estado_display()}'
