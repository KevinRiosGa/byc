from django.urls import path
from .views import (
    SeccionFichaListView, SeccionFichaCreateView, SeccionFichaUpdateView, SeccionFichaDeleteView,
    PlantillaFichaTecnicaListView, PlantillaFichaTecnicaCreateView, PlantillaFichaTecnicaUpdateView, PlantillaFichaTecnicaDeleteView,
    secciones_por_tipo, especificaciones_por_seccion
)

urlpatterns = [
    path('seccion_ficha/', SeccionFichaListView.as_view(), name='seccion_ficha_list'),
    path('seccion_ficha/crear/', SeccionFichaCreateView.as_view(), name='seccion_ficha_create'),
    path('seccion_ficha/<int:pk>/editar/', SeccionFichaUpdateView.as_view(), name='seccion_ficha_update'),
    path('seccion_ficha/<int:pk>/eliminar/', SeccionFichaDeleteView.as_view(), name='seccion_ficha_delete'),
    
    path('plantilla_ficha/', PlantillaFichaTecnicaListView.as_view(), name='plantilla_ficha_tecnica_list'),
    path('plantilla_ficha/crear/', PlantillaFichaTecnicaCreateView.as_view(), name='plantilla_ficha_tecnica_create'),
    path('plantilla_ficha/<int:pk>/editar/', PlantillaFichaTecnicaUpdateView.as_view(), name='plantilla_ficha_tecnica_update'),
    path('plantilla_ficha/<int:pk>/eliminar/', PlantillaFichaTecnicaDeleteView.as_view(), name='plantilla_ficha_tecnica_delete'),

    path('secciones-por-tipo/', secciones_por_tipo, name='secciones_por_tipo'),
    path('especificaciones-por-seccion/', especificaciones_por_seccion, name='especificaciones_por_seccion'),
] 