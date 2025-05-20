from django.shortcuts import render
from .models import TipoEquipo, MarcaEquipo, ModeloEquipo
from .forms import TipoEquipoForm, MarcaEquipoForm, ModeloEquipoForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse

# Create your views here.
class TipoEquipoListView(ListView):
    model = TipoEquipo
    template_name = 'tipo_equipo.html'
    context_object_name = 'tipos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TipoEquipoForm()
        return context

class TipoEquipoCreateView(CreateView):
    model = TipoEquipo
    form_class = TipoEquipoForm
    success_url = reverse_lazy('tipo_equipo_list')

    def form_valid(self, form):
        form.save()
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'message': 'Error al crear el tipo de equipo. Por favor, verifique los datos.'
        })

class TipoEquipoUpdateView(UpdateView):
    model = TipoEquipo
    form_class = TipoEquipoForm
    success_url = reverse_lazy('tipo_equipo_list')

    def form_valid(self, form):
        form.save()
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'message': 'Error al actualizar el tipo de equipo. Por favor, verifique los datos.'
        })

class TipoEquipoDeleteView(DeleteView):
    model = TipoEquipo
    success_url = reverse_lazy('tipo_equipo_list')

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            if self.object.marcaequipo_set.exists() or self.object.modeloequipo_set.exists():
                return JsonResponse({
                    'success': False,
                    'message': 'No se puede eliminar este tipo de equipo porque está siendo utilizado por marcas o modelos. Por favor, elimine primero las marcas o modelos asociados.'
                }, status=200)
            self.object.delete()
            return JsonResponse({'success': True}, status=200)
        except Exception as e:
            import traceback
            return JsonResponse({
                'success': False,
                'message': f'Error al eliminar el tipo de equipo: {str(e)}',
                'traceback': traceback.format_exc()
            }, status=200)

class MarcaEquipoListView(ListView):
    model = MarcaEquipo
    template_name = 'marca_equipo.html'
    context_object_name = 'marcas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MarcaEquipoForm()
        return context

class MarcaEquipoCreateView(CreateView):
    model = MarcaEquipo
    form_class = MarcaEquipoForm
    success_url = reverse_lazy('marca_equipo_list')

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'message': 'Error al crear la marca. Por favor, verifique los datos.'
        })

class MarcaEquipoUpdateView(UpdateView):
    model = MarcaEquipo
    form_class = MarcaEquipoForm
    success_url = reverse_lazy('marca_equipo_list')

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'message': 'Error al actualizar la marca. Por favor, verifique los datos.'
        })

class MarcaEquipoDeleteView(DeleteView):
    model = MarcaEquipo
    success_url = reverse_lazy('marca_equipo_list')

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.delete()
            return JsonResponse({'success': True}, status=200)
        except Exception as e:
            import traceback
            return JsonResponse({
                'success': False,
                'message': f'Error al eliminar la marca: {str(e)}',
                'traceback': traceback.format_exc()
            }, status=200)

class ModeloEquipoListView(ListView):
    model = ModeloEquipo
    template_name = 'modelo_equipo.html'
    context_object_name = 'modelos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ModeloEquipoForm()
        return context

class ModeloEquipoCreateView(CreateView):
    model = ModeloEquipo
    form_class = ModeloEquipoForm
    success_url = reverse_lazy('modelo_equipo_list')

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'message': 'Error al crear el modelo. Por favor, verifique los datos.'
        })

class ModeloEquipoUpdateView(UpdateView):
    model = ModeloEquipo
    form_class = ModeloEquipoForm
    success_url = reverse_lazy('modelo_equipo_list')

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'message': 'Error al actualizar el modelo. Por favor, verifique los datos.'
        })

class ModeloEquipoDeleteView(DeleteView):
    model = ModeloEquipo
    success_url = reverse_lazy('modelo_equipo_list')

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.delete()
            return JsonResponse({'success': True}, status=200)
        except Exception as e:
            import traceback
            return JsonResponse({
                'success': False,
                'message': f'Error al eliminar el modelo: {str(e)}',
                'traceback': traceback.format_exc()
            }, status=200)

def marcas_por_tipo(request):
    tipo_id = request.GET.get('tipo_id')
    marcas = []
    if tipo_id:
        marcas_qs = MarcaEquipo.objects.filter(tipoeq__id=tipo_id).distinct()
        marcas = [{'id': m.id, 'nombre': m.marcaeq} for m in marcas_qs]
    return JsonResponse({'marcas': marcas})