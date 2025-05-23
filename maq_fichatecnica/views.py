from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.forms import modelformset_factory
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import (
    SeccionFicha, EspecificacionSeccion,
    PlantillaFichaTecnica
)
from .forms import (
    SeccionFichaForm, EspecificacionSeccionForm, EspecificacionFormSet,
    PlantillaFichaTecnicaForm, SeccionPlantillaFormSet
)


# Create your views here.

class SeccionFichaListView(ListView):
    model = SeccionFicha
    template_name = 'seccion_ficha.html'
    context_object_name = 'secciones'

class SeccionFichaCreateView(CreateView):
    model = SeccionFicha
    form_class = SeccionFichaForm
    template_name = 'seccion_ficha_form.html'
    success_url = reverse_lazy('seccion_ficha_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            formset = EspecificacionFormSet(self.request.POST)
        else:
            formset = EspecificacionFormSet()
        context['formset'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class SeccionFichaUpdateView(UpdateView):
    model = SeccionFicha
    form_class = SeccionFichaForm
    template_name = 'seccion_ficha_form.html'
    success_url = reverse_lazy('seccion_ficha_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = EspecificacionFormSet(
                self.request.POST, instance=self.object)
        else:
            context['formset'] = EspecificacionFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class SeccionFichaDeleteView(DeleteView):
    model = SeccionFicha
    success_url = reverse_lazy('seccion_ficha_list')

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.delete()
            messages.success(request, 'Sección eliminada con éxito.')
            return redirect('seccion_ficha_list')
        except Exception as e:
            import traceback
            messages.error(request, f'Error al eliminar la sección: {str(e)}')
            return redirect('seccion_ficha_list')

# Vistas para las plantillas de fichas técnicas
class PlantillaFichaTecnicaListView(ListView):
    model = PlantillaFichaTecnica
    template_name = 'plantilla_ficha_tecnica.html'
    context_object_name = 'plantillas'

class PlantillaFichaTecnicaCreateView(CreateView):
    model = PlantillaFichaTecnica
    form_class = PlantillaFichaTecnicaForm
    template_name = 'plantilla_ficha_tecnica_form.html'
    success_url = reverse_lazy('plantilla_ficha_tecnica_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = SeccionPlantillaFormSet(self.request.POST)
        else:
            context['formset'] = SeccionPlantillaFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            messages.success(self.request, 'Plantilla creada exitosamente.')
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class PlantillaFichaTecnicaUpdateView(UpdateView):
    model = PlantillaFichaTecnica
    form_class = PlantillaFichaTecnicaForm
    template_name = 'plantilla_ficha_tecnica_form.html'
    success_url = reverse_lazy('plantilla_ficha_tecnica_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = SeccionPlantillaFormSet(
                self.request.POST, instance=self.object)
        else:
            context['formset'] = SeccionPlantillaFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            messages.success(self.request, 'Plantilla actualizada exitosamente.')
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class PlantillaFichaTecnicaDeleteView(DeleteView):
    model = PlantillaFichaTecnica
    success_url = reverse_lazy('plantilla_ficha_tecnica_list')

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.delete()
            messages.success(request, 'Plantilla eliminada con éxito.')
            return redirect('plantilla_ficha_tecnica_list')
        except Exception as e:
            import traceback
            messages.error(request, f'Error al eliminar la plantilla: {str(e)}')
            return redirect('plantilla_ficha_tecnica_list')

def secciones_por_tipo(request):
    """Devuelve las secciones asociadas a un tipo de equipo específico"""
    tipo_id = request.GET.get('tipo_id')
    secciones = []
    if tipo_id:
        try:
            secciones_qs = SeccionFicha.objects.filter(tipoeq__id=tipo_id).distinct()
            secciones = [{'id': str(s.id), 'nombre': s.seccion} for s in secciones_qs]
        except Exception as e:
            import traceback
            print(f"Error al obtener secciones: {str(e)}")
            print(traceback.format_exc())
    return JsonResponse({'secciones': secciones})

def especificaciones_por_seccion(request):
    """Devuelve las especificaciones asociadas a una sección específica"""
    seccion_id = request.GET.get('seccion_id')
    especificaciones = []
    if seccion_id:
        try:
            especificaciones_qs = EspecificacionSeccion.objects.filter(seccion__id=seccion_id).order_by('orden')
            especificaciones = [
                {
                    'id': str(e.id),
                    'orden': e.orden,
                    'especificacion': e.especificacion,
                    'tipodato': e.tipodato.nombre if e.tipodato else '',
                    'unidadmedida': e.unidadmedida.codigo if e.unidadmedida else ''
                } for e in especificaciones_qs
            ]
        except Exception as e:
            import traceback
            print(f"Error al obtener especificaciones: {str(e)}")
            print(traceback.format_exc())
    return JsonResponse({'especificaciones': especificaciones})

