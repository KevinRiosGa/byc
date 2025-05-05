from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.forms import inlineformset_factory
from django.db import transaction
from django.contrib import messages
from .models import TipoEquipo, MarcaEquipo, ModeloEquipo, FichaTecnica, Seccion, Especificacion
from .forms import (TipoEquipoForm, MarcaEquipoForm, ModeloEquipoForm, 
                   FichaTecnicaForm, SeccionForm, EspecificacionForm,
                   SeccionFormSet, EspecificacionFormSet)
from gen_settings.models import TipoDato, UnidadMedida

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

# Nuevas vistas para fichas técnicas

class FichaTecnicaListView(ListView):
    model = FichaTecnica
    template_name = 'maq_fichatecnica/ficha_tecnica_list.html'
    context_object_name = 'fichas'

    def get_queryset(self):
        queryset = super().get_queryset()
        tipo_id = self.request.GET.get('tipo_id')
        if tipo_id:
            queryset = queryset.filter(tipoeq_id=tipo_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_equipo'] = TipoEquipo.objects.all()
        return context


class FichaTecnicaCreateView(View):
    template_name = 'maq_fichatecnica/ficha_tecnica_form.html'
    
    def get(self, request, *args, **kwargs):
        form = FichaTecnicaForm()
        seccion_formset = SeccionFormSet(prefix='secciones')
        
        # Obtener lista de tipos de datos para el template
        tipodatos_list = TipoDato.objects.all()
        
        # Obtener lista de unidades de medida para el template
        unidadesmedida_list = UnidadMedida.objects.all()
        
        context = {
            'form': form,
            'seccion_formset': seccion_formset,
            'tipodatos_list': tipodatos_list,
            'unidadesmedida_list': unidadesmedida_list,
            'is_update': False
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = FichaTecnicaForm(request.POST)
        seccion_formset = SeccionFormSet(request.POST, prefix='secciones')
        
        if form.is_valid() and seccion_formset.is_valid():
            try:
                with transaction.atomic():
                    # Guardar la ficha técnica
                    ficha = form.save()
                    
                    # Guardar secciones
                    secciones = seccion_formset.save(commit=False)
                    
                    # Asegurar que el orden de las secciones sea secuencial
                    for i, seccion in enumerate(secciones, 1):
                        seccion.orden = i
                        seccion.fichaTecnica = ficha
                        seccion.save()
                    
                    # Eliminar secciones marcadas
                    for seccion in seccion_formset.deleted_objects:
                        seccion.delete()
                    
                    # Guardar especificaciones para cada sección
                    for seccion in secciones:
                        # Crear formset para especificaciones de esta sección
                        if seccion.id:  # Si la sección ya existe
                            especificacion_prefix = f'especificaciones_{seccion.id}'
                        else:
                            # Para nuevas secciones, buscamos el prefijo basado en el índice
                            seccion_index = list(secciones).index(seccion)
                            especificacion_prefix = f'especificaciones_nueva_{seccion_index}'
                        
                        try:
                            # Intentar procesar con el prefijo calculado
                            especificacion_formset = EspecificacionFormSet(
                                request.POST, 
                                prefix=especificacion_prefix,
                                instance=seccion
                            )
                            
                            if especificacion_formset.is_valid():
                                # Guardar las especificaciones
                                especificaciones = especificacion_formset.save(commit=False)
                                print(f"  {len(especificaciones)} especificaciones a guardar")
                                
                                # Imprimir datos del formset para depuración
                                print(f"  Formset data:")
                                for form in especificacion_formset.forms:
                                    print(f"    Form cleaned_data: {form.cleaned_data if hasattr(form, 'cleaned_data') else 'No hay cleaned_data'}")
                                    if hasattr(form, 'cleaned_data') and form.cleaned_data:
                                        # Si es una especificación existente, mostramos su ID
                                        if 'id' in form.cleaned_data and form.cleaned_data['id']:
                                            print(f"      Especificación existente ID: {form.cleaned_data['id'].id}")
                                        else:
                                            print("      Nueva especificación")
                                
                                # Asegurar que el orden de las especificaciones sea secuencial
                                for i, especificacion in enumerate(especificaciones, 1):
                                    especificacion.orden = i
                                    especificacion.seccion = seccion
                                    # Asegurarse de que la especificación no sea una ficticia
                                    if especificacion.nombre != "Nueva especificación" or especificacion.id:
                                        especificacion.save()
                                        print(f"  Guardada especificación ID: {especificacion.id}, Nombre: {especificacion.nombre}")
                                    else:
                                        print(f"  Ignorando especificación ficticia: {especificacion.nombre}")
                                
                                # Eliminar especificaciones marcadas
                                for especificacion in especificacion_formset.deleted_objects:
                                    print(f"  Eliminando especificación ID: {especificacion.id}")
                                    especificacion.delete()
                            else:
                                # Para depuración
                                print(f"Errores en formset {especificacion_prefix}:", especificacion_formset.errors)
                                if len(especificacion_formset.forms) > 0:
                                    # Si no hay formularios, no es un error, solo una sección sin especificaciones
                                    raise ValueError(f"Error en el formulario de especificaciones: {especificacion_formset.errors}")
                        except Exception as e:
                            # Si hay un error en el proceso de una sección, verificamos si hay especificaciones
                            # Si no hay especificaciones para esta sección, seguimos con la siguiente
                            if "existe un campo TOTAL_FORMS" in str(e) or "This field is required" in str(e):
                                # Es probable que esta nueva sección no tenga especificaciones aún
                                print(f"  Error al procesar especificaciones: {str(e)}")
                                continue
                            else:
                                # Es un error diferente, lo propagamos
                                print(f"  Error crítico: {str(e)}")
                                raise
                
                messages.success(request, "Ficha técnica creada con éxito")
                return redirect('ficha_tecnica_list')
            
            except Exception as e:
                messages.error(request, f"Error al crear la ficha técnica: {str(e)}")
        
        context = {
            'form': form,
            'seccion_formset': seccion_formset,
            'tipodatos_list': tipodatos_list,
            'unidadesmedida_list': unidadesmedida_list,
            'is_update': False
        }
        return render(request, self.template_name, context)


class FichaTecnicaUpdateView(View):
    template_name = 'maq_fichatecnica/ficha_tecnica_form.html'
    
    def get(self, request, *args, **kwargs):
        ficha = get_object_or_404(FichaTecnica, pk=kwargs['pk'])
        form = FichaTecnicaForm(instance=ficha)
        seccion_formset = SeccionFormSet(instance=ficha, prefix='secciones')
        
        # Obtener lista de tipos de datos para el template
        tipodatos_list = TipoDato.objects.all()
        
        # Obtener lista de unidades de medida para el template
        unidadesmedida_list = UnidadMedida.objects.all()
        
        # Preparar formsets de especificaciones para cada sección
        especificacion_formsets = []
        print(f"Cargando especificaciones para ficha ID: {ficha.id}")
        
        # Consultar cuántas secciones tiene la ficha
        secciones = ficha.seccion_set.all().order_by('orden')
        print(f"La ficha tiene {secciones.count()} secciones")
        
        for seccion in secciones:
            # Consultar cuántas especificaciones tiene esta sección
            especificaciones = seccion.especificacion_set.all().order_by('orden')
            specs_count = especificaciones.count()
            print(f"Sección ID: {seccion.id}, Nombre: {seccion.nombre} tiene {specs_count} especificaciones")
            
            # Preparar el formset
            if specs_count == 0:
                print(f"  Creando especificación ficticia para la sección {seccion.id}")
                # Crear formset con una especificación ficticia
                formset = EspecificacionFormSet(
                    instance=seccion,
                    prefix=f'especificaciones_{seccion.id}',
                    initial=[{
                        'seccion': seccion.id,
                        'nombre': "Nueva especificación",
                        'orden': 1,
                        'tipoDato': TipoDato.objects.first().id if TipoDato.objects.exists() else None,
                        'unidadMedida': None
                    }]
                )
            else:
                # Listar especificaciones existentes para depuración
                for idx, spec in enumerate(especificaciones):
                    print(f"  {idx+1}. Especificación ID: {spec.id}, Nombre: {spec.nombre}, Tipo: {spec.tipoDato}, Unidad: {spec.unidadMedida}")
                
                # Crear el formset con las especificaciones existentes
                formset = EspecificacionFormSet(
                    instance=seccion,
                    prefix=f'especificaciones_{seccion.id}',
                    queryset=especificaciones
                )
                
                # Confirmar que todas las especificaciones estén presentes en el formset
                for idx, form in enumerate(formset.forms):
                    if hasattr(form, 'instance') and form.instance.id:
                        print(f"  Formulario {idx}: contiene especificación ID: {form.instance.id}, Nombre: {form.instance.nombre}")
            
            # Verificar el formset
            print(f"  Formset para sección {seccion.id} tiene {len(formset.forms)} formularios")
            
            # Añadir al conjunto de formsets
            especificacion_formsets.append((seccion, formset))
        
        context = {
            'form': form,
            'seccion_formset': seccion_formset,
            'especificacion_formsets': especificacion_formsets,
            'ficha': ficha,
            'tipodatos_list': tipodatos_list,
            'unidadesmedida_list': unidadesmedida_list,
            'is_update': True
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        ficha = get_object_or_404(FichaTecnica, pk=kwargs['pk'])
        form = FichaTecnicaForm(request.POST, instance=ficha)
        seccion_formset = SeccionFormSet(request.POST, instance=ficha, prefix='secciones')
        
        # Para depuración
        print(f"Procesando actualización de ficha técnica ID: {ficha.id}, Nombre: {ficha.nombre}")
        
        if form.is_valid() and seccion_formset.is_valid():
            try:
                with transaction.atomic():
                    # Actualizar ficha
                    ficha = form.save()
                    
                    # Actualizar secciones
                    secciones = seccion_formset.save(commit=False)
                    print(f"Procesando {len(secciones)} secciones para la ficha")
                    
                    # Asegurar que el orden de las secciones sea secuencial
                    for i, seccion in enumerate(secciones, 1):
                        seccion.orden = i
                        seccion.fichaTecnica = ficha
                        seccion.save()
                    
                    # Eliminar secciones marcadas
                    for seccion in seccion_formset.deleted_objects:
                        seccion.delete()
                    
                    # Procesar datos de especificaciones manualmente
                    for seccion in secciones:
                        print(f"Procesando especificaciones para sección ID: {seccion.id}, Nombre: {seccion.nombre}")
                        
                        if seccion.id:  # Si la sección ya existe
                            especificacion_prefix = f'especificaciones_{seccion.id}'
                        else:
                            # Para nuevas secciones, buscamos el prefijo basado en el índice
                            seccion_index = list(secciones).index(seccion)
                            especificacion_prefix = f'especificaciones_nueva_{seccion_index}'
                        
                        print(f"Usando prefijo: {especificacion_prefix}")
                        
                        # Primero, eliminar todas las especificaciones existentes que no estén marcadas para preservar
                        # Esto es más simple que tratar de determinar cuáles actualizar y cuáles crear
                        especificaciones_a_preservar = []
                        
                        # Extraer IDs de especificaciones a preservar del POST data
                        for key, value in request.POST.items():
                            if key.startswith(f"{especificacion_prefix}-") and "-id" in key and value:
                                try:
                                    form_index = key.split('-')[1]
                                    delete_key = f"{especificacion_prefix}-{form_index}-DELETE"
                                    nombre_key = f"{especificacion_prefix}-{form_index}-nombre"
                                    nombre = request.POST.get(nombre_key, "")
                                    
                                    # Solo preservar si no está marcada para eliminar y no es ficticia
                                    if delete_key not in request.POST and nombre != "Nueva especificación":
                                        try:
                                            esp_id = int(value)
                                            especificaciones_a_preservar.append(esp_id)
                                            print(f"Marcando para preservar especificación ID: {esp_id}, Nombre: {nombre}")
                                        except (ValueError, TypeError):
                                            print(f"Valor no válido para ID de especificación: {value}")
                                            continue
                                except Exception as e:
                                    print(f"Error procesando clave {key}: {str(e)}")
                                    continue
                        
                        print(f"Especificaciones a preservar para sección {seccion.id}: {especificaciones_a_preservar}")
                        
                        # Eliminar todas las que no estén en la lista
                        if seccion.id:  # Solo para secciones existentes
                            for espec in Especificacion.objects.filter(seccion=seccion).exclude(id__in=especificaciones_a_preservar):
                                print(f"Eliminando especificación ID: {espec.id}, Nombre: {espec.nombre}")
                                espec.delete()
                        
                        # Extraer datos para crear o actualizar especificaciones
                        nuevas_especificaciones = []
                        for key, value in request.POST.items():
                            if key.startswith(f"{especificacion_prefix}-") and "-nombre" in key and value:
                                try:
                                    form_index = key.split('-')[1]
                                    
                                    # Verificar si es una nueva o una existente
                                    id_key = f"{especificacion_prefix}-{form_index}-id"
                                    nombre = request.POST.get(key, "").strip()
                                    orden = request.POST.get(f"{especificacion_prefix}-{form_index}-orden", 0)
                                    tipo_dato_id = request.POST.get(f"{especificacion_prefix}-{form_index}-tipoDato", None)
                                    unidad_medida_id = request.POST.get(f"{especificacion_prefix}-{form_index}-unidadMedida", None)
                                    
                                    # Ignorar si es la especificación ficticia o está vacía
                                    if nombre == "Nueva especificación" or not nombre:
                                        print(f"Ignorando especificación ficticia o vacía en índice {form_index}")
                                        continue
                                    
                                    # Verificar si está marcada para eliminar
                                    delete_key = f"{especificacion_prefix}-{form_index}-DELETE"
                                    if delete_key in request.POST:
                                        print(f"Especificación en índice {form_index} marcada para eliminar")
                                        continue
                                    
                                    # Crear o actualizar la especificación
                                    especificacion_id = request.POST.get(id_key)
                                    if especificacion_id:
                                        try:
                                            especificacion = Especificacion.objects.get(id=especificacion_id)
                                            print(f"Actualizando especificación existente ID: {especificacion.id}, Nombre: {nombre}")
                                        except Especificacion.DoesNotExist:
                                            print(f"No se encontró la especificación con ID: {especificacion_id}, creando nueva")
                                            especificacion = Especificacion(seccion=seccion)
                                    else:
                                        print(f"Creando nueva especificación: {nombre}")
                                        especificacion = Especificacion(seccion=seccion)
                                    
                                    # Actualizar campos
                                    especificacion.nombre = nombre
                                    especificacion.orden = orden
                                    
                                    if tipo_dato_id:
                                        try:
                                            tipo_dato = TipoDato.objects.get(id=tipo_dato_id)
                                            especificacion.tipoDato = tipo_dato
                                        except TipoDato.DoesNotExist:
                                            print(f"Tipo de dato con ID {tipo_dato_id} no existe")
                                            continue
                                    else:
                                        print(f"No se proporcionó tipo de dato para la especificación")
                                        continue
                                    
                                    if unidad_medida_id and unidad_medida_id != '':
                                        try:
                                            unidad_medida = UnidadMedida.objects.get(id=unidad_medida_id)
                                            especificacion.unidadMedida = unidad_medida
                                        except UnidadMedida.DoesNotExist:
                                            print(f"Unidad de medida con ID {unidad_medida_id} no existe")
                                            especificacion.unidadMedida = None
                                    else:
                                        especificacion.unidadMedida = None
                                    
                                    # Guardar la especificación
                                    especificacion.save()
                                    print(f"Guardada especificación ID: {especificacion.id}, Nombre: {especificacion.nombre}")
                                except Exception as e:
                                    print(f"Error procesando especificación en índice {form_index}: {str(e)}")
                        
                        # Reordenar todas las especificaciones de esta sección
                        for i, especificacion in enumerate(seccion.especificacion_set.all().order_by('orden'), 1):
                            if especificacion.orden != i:
                                especificacion.orden = i
                                especificacion.save()
                                print(f"Reordenada especificación ID: {especificacion.id} a orden {i}")
                
                messages.success(request, "Ficha técnica actualizada con éxito")
                return redirect('ficha_tecnica_list')
            
            except Exception as e:
                messages.error(request, f"Error al actualizar la ficha técnica: {str(e)}")
                # Para depuración detallada
                import traceback
                traceback.print_exc()
                print(f"Error completo: {str(e)}")
        else:
            # Mostrar errores del formulario para depuración
            if not form.is_valid():
                print(f"Errores en el formulario principal: {form.errors}")
            if not seccion_formset.is_valid():
                print(f"Errores en el formset de secciones: {seccion_formset.errors}")
                for i, form_error in enumerate(seccion_formset.errors):
                    if form_error:
                        print(f"  Formulario {i} errores: {form_error}")
        
        # Recrear formsets de especificaciones para renderizar en caso de error
        especificacion_formsets = []
        for seccion in ficha.seccion_set.all():
            formset = EspecificacionFormSet(
                request.POST,
                instance=seccion,
                prefix=f'especificaciones_{seccion.id}'
            )
            especificacion_formsets.append((seccion, formset))
        
        context = {
            'form': form,
            'seccion_formset': seccion_formset,
            'especificacion_formsets': especificacion_formsets,
            'ficha': ficha,
            'tipodatos_list': tipodatos_list,
            'unidadesmedida_list': unidadesmedida_list,
            'is_update': True
        }
        return render(request, self.template_name, context)


class FichaTecnicaDeleteView(DeleteView):
    model = FichaTecnica
    success_url = reverse_lazy('ficha_tecnica_list')
    template_name = 'maq_fichatecnica/ficha_tecnica_confirm_delete.html'
    
    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al eliminar la ficha técnica: {str(e)}'
            })


# Vistas AJAX para complementar la funcionalidad
def unidades_por_tipo_dato(request):
    tipo_dato_id = request.GET.get('tipo_dato_id')
    unidades = []
    
    try:
        # Obtener todas las unidades de medida
        unidades_qs = UnidadMedida.objects.all()        
        unidades = [{'id': u.id, 'nombre': f"{u.codigo}"} for u in unidades_qs]
    except Exception as e:
        print(f"Error al buscar unidades: {str(e)}")
        unidades = []
    
    return JsonResponse({'unidades': unidades})


def agregar_seccion_formset(request):
    """Vista AJAX para añadir una nueva fila al formset de secciones"""
    if request.method == 'GET':
        index = request.GET.get('index')
        if index:
            formset = SeccionFormSet(prefix='secciones')
            form = formset.empty_form
            return render(request, 'maq_fichatecnica/partials/seccion_form.html', {
                'form': form,
                'index': index
            })
    return JsonResponse({'success': False})


def agregar_especificacion_formset(request):
    """Vista AJAX para añadir una nueva fila al formset de especificaciones"""
    if request.method == 'GET':
        index = request.GET.get('index')
        seccion_id = request.GET.get('seccion_id')
        if index and seccion_id:
            formset = EspecificacionFormSet(prefix=f'especificaciones_{seccion_id}')
            form = formset.empty_form
            return render(request, 'maq_fichatecnica/partials/especificacion_form.html', {
                'form': form,
                'index': index,
                'seccion_id': seccion_id
            })
    return JsonResponse({'success': False})
