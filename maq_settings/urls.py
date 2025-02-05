from django.urls import path
from .views import TipoEquipoListView, TipoEquipoUpdateView, TipoEquipoDeleteView, MarcaEquipoListView, MarcaEquipoUpdateView, MarcaEquipoDeleteView, ModeloEquipoListView, ModeloEquipoCreateView, ModeloEquipoUpdateView, ModeloEquipoDeleteView

urlpatterns = [
     # URLs para TipoEquipo
    path('tipoequipo/', TipoEquipoListView.as_view(), name="tipoequipo_list"),
    path('tipoequipo/<int:pk>/editar/', TipoEquipoUpdateView.as_view(), name="tipoequipo_update"),
    path('tipoequipo/<int:pk>/eliminar/', TipoEquipoDeleteView.as_view(), name='tipoequipo_delete'),

    # URLs para MarcaEquipo
    path('marcaequipo/', MarcaEquipoListView.as_view(), name="marcaequipo_list"),
    path('marcaequipo/<int:pk>/editar/', MarcaEquipoUpdateView.as_view(), name="marcaequipo_update"),
    path('marcaequipo/<int:pk>/eliminar/', MarcaEquipoDeleteView.as_view(), name="marcaequipo_delete"),

    # URLs para ModeloEquipo
    path('modeloequipo/', ModeloEquipoListView.as_view(), name="modeloequipo_list"),
    path('modeloequipo/nuevo/', ModeloEquipoCreateView.as_view(), name="modeloequipo_create"),
    path('modeloequipo/<int:pk>/editar/', ModeloEquipoUpdateView.as_view(), name="modeloequipo_update"),
    path('modeloequipo/<int:pk>/eliminar/', ModeloEquipoDeleteView.as_view(), name="modeloequipo_delete"),
]