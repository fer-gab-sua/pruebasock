from django.urls import path
from . import views

urlpatterns = [
    path('administracion/', views.administracion, name='administracion'),
    path('consulta/', views.consulta, name='consulta'),
    path('actualizar-estado/<int:incidente_id>/', views.actualizar_estado, name='actualizar_estado'),
    path('eliminar-incidente/<int:incidente_id>/', views.eliminar_incidente, name='eliminar_incidente'),
    path('sincronizar-metabase/', views.sincronizar_metabase, name='sincronizar_metabase'),
]
