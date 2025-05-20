from django.urls import path
from .views import (
    TipoEquipoListView, TipoEquipoCreateView, TipoEquipoUpdateView, TipoEquipoDeleteView,
    MarcaEquipoListView, MarcaEquipoCreateView, MarcaEquipoUpdateView, MarcaEquipoDeleteView,
    ModeloEquipoListView, ModeloEquipoCreateView, ModeloEquipoUpdateView, ModeloEquipoDeleteView,
    marcas_por_tipo
)

urlpatterns = [
    path('tipo_equipo/', TipoEquipoListView.as_view(), name='tipo_equipo_list'),
    path('tipo_equipo/crear/', TipoEquipoCreateView.as_view(), name='tipo_equipo_create'),
    path('tipo_equipo/<int:pk>/editar/', TipoEquipoUpdateView.as_view(), name='tipo_equipo_update'),
    path('tipo_equipo/<int:pk>/eliminar/', TipoEquipoDeleteView.as_view(), name='tipo_equipo_delete'),

    path('marca_equipo/', MarcaEquipoListView.as_view(), name='marca_equipo_list'),
    path('marca_equipo/crear/', MarcaEquipoCreateView.as_view(), name='marca_equipo_create'),
    path('marca_equipo/<int:pk>/editar/', MarcaEquipoUpdateView.as_view(), name='marca_equipo_update'),
    path('marca_equipo/<int:pk>/eliminar/', MarcaEquipoDeleteView.as_view(), name='marca_equipo_delete'),

    path('modelo_equipo/', ModeloEquipoListView.as_view(), name='modelo_equipo_list'),
    path('modelo_equipo/crear/', ModeloEquipoCreateView.as_view(), name='modelo_equipo_create'),
    path('modelo_equipo/<int:pk>/editar/', ModeloEquipoUpdateView.as_view(), name='modelo_equipo_update'),
    path('modelo_equipo/<int:pk>/eliminar/', ModeloEquipoDeleteView.as_view(), name='modelo_equipo_delete'),

    path('ajax/marcas_por_tipo/', marcas_por_tipo, name='marcas_por_tipo'),

]