from django.urls import path
from . import views

urlpatterns = [
    path('tipo_equipo/', views.TipoEquipoListView.as_view(), name='tipo_equipo_list'),
    path('tipo_equipo/create/', views.TipoEquipoCreateView.as_view(), name='tipo_equipo_create'),
    path('tipo_equipo/<int:pk>/update/', views.TipoEquipoUpdateView.as_view(), name='tipo_equipo_update'),
    path('tipo_equipo/<int:pk>/delete/', views.TipoEquipoDeleteView.as_view(), name='tipo_equipo_delete'),

    path('marca_equipo/', views.MarcaEquipoListView.as_view(), name='marca_equipo_list'),
    path('marca_equipo/create/', views.MarcaEquipoCreateView.as_view(), name='marca_equipo_create'),
    path('marca_equipo/<int:pk>/update/', views.MarcaEquipoUpdateView.as_view(), name='marca_equipo_update'),
    path('marca_equipo/<int:pk>/delete/', views.MarcaEquipoDeleteView.as_view(), name='marca_equipo_delete'),

    path('modelo_equipo/', views.ModeloEquipoListView.as_view(), name='modelo_equipo_list'),
    path('modelo_equipo/create/', views.ModeloEquipoCreateView.as_view(), name='modelo_equipo_create'),
    path('modelo_equipo/<int:pk>/update/', views.ModeloEquipoUpdateView.as_view(), name='modelo_equipo_update'),
    path('modelo_equipo/<int:pk>/delete/', views.ModeloEquipoDeleteView.as_view(), name='modelo_equipo_delete'),

    path('ajax/marcas_por_tipo/', views.marcas_por_tipo, name='marcas_por_tipo'),
    
    # URLs para fichas técnicas
    path('ficha_tecnica/', views.FichaTecnicaListView.as_view(), name='ficha_tecnica_list'),
    path('ficha_tecnica/create/', views.FichaTecnicaCreateView.as_view(), name='ficha_tecnica_create'),
    path('ficha_tecnica/<int:pk>/update/', views.FichaTecnicaUpdateView.as_view(), name='ficha_tecnica_update'),
    path('ficha_tecnica/<int:pk>/delete/', views.FichaTecnicaDeleteView.as_view(), name='ficha_tecnica_delete'),
    
    # URLs para AJAX
    path('ajax/unidades_por_tipo_dato/', views.unidades_por_tipo_dato, name='unidades_por_tipo_dato'),
    path('ajax/agregar_seccion_formset/', views.agregar_seccion_formset, name='agregar_seccion_formset'),
    path('ajax/agregar_especificacion_formset/', views.agregar_especificacion_formset, name='agregar_especificacion_formset'),
] 