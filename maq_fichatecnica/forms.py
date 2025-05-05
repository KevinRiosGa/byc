from django import forms
from .models import TipoEquipo, MarcaEquipo, ModeloEquipo, FichaTecnica, Seccion, Especificacion
from gen_settings.models import TipoDato, UnidadMedida

class TipoEquipoForm(forms.ModelForm):
    class Meta:
        model = TipoEquipo
        fields = ['prefixeq', 'tipoeq']
        widgets = {
            'prefixeq': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '2',
                'required': True
            }),
            'tipoeq': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '100',
                'required': True
            })
        }

class MarcaEquipoForm(forms.ModelForm):
    tipoeq = forms.ModelMultipleChoiceField(
        queryset=TipoEquipo.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Tipos de Equipo"
    )

    class Meta:
        model = MarcaEquipo
        fields = ['marcaeq', 'tipoeq']
        widgets = {
            'marcaeq': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '150',
                'required': True
            })
        }

class ModeloEquipoForm(forms.ModelForm):
    class Meta:
        model = ModeloEquipo
        fields = ['tipoeq', 'marcaeq', 'modeloeq']
        widgets = {
            'tipoeq': forms.Select(attrs={'class': 'form-control form-control-sm', 'required': True}),
            'marcaeq': forms.Select(attrs={'class': 'form-control form-control-sm', 'required': True}),
            'modeloeq': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '150', 'required': True}),
        }

# Formularios para Fichas Técnicas
class FichaTecnicaForm(forms.ModelForm):
    class Meta:
        model = FichaTecnica
        fields = ['nombre', 'tipoeq']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '200',
                'required': True
            }),
            'tipoeq': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            })
        }

class SeccionForm(forms.ModelForm):
    class Meta:
        model = Seccion
        fields = ['nombre', 'orden', 'fichaTecnica']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '100',
                'required': True,
                'placeholder': 'Nombre de la sección'
            }),
            'orden': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': True,
                'min': '1',
                'placeholder': 'Orden'
            }),
            'fichaTecnica': forms.HiddenInput()
        }

class EspecificacionForm(forms.ModelForm):
    tipoDato = forms.ModelChoiceField(
        queryset=TipoDato.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control tipo-dato-select',
            'required': True
        })
    )
    
    unidadMedida = forms.ModelChoiceField(
        queryset=UnidadMedida.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control unidad-medida-select'
        })
    )
    
    class Meta:
        model = Especificacion
        fields = ['nombre', 'orden', 'tipoDato', 'unidadMedida', 'seccion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '200',
                'required': True,
                'placeholder': 'Nombre de la especificación'
            }),
            'orden': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': True,
                'min': '1',
                'placeholder': 'Orden'
            }),
            'seccion': forms.HiddenInput()
        }

# Formsets para manejar múltiples secciones y especificaciones
SeccionFormSet = forms.inlineformset_factory(
    FichaTecnica,
    Seccion,
    form=SeccionForm,
    extra=1,
    can_delete=True,
    widgets={
        'orden': forms.NumberInput(attrs={
            'class': 'form-control seccion-orden',
            'min': '1',
        }),
        'nombre': forms.TextInput(attrs={
            'class': 'form-control seccion-nombre',
            'placeholder': 'Nombre de la sección'
        })
    }
)

# Modificamos el EspecificacionFormSet para incluir todas las especificaciones
EspecificacionFormSet = forms.inlineformset_factory(
    Seccion,
    Especificacion,
    form=EspecificacionForm,
    extra=1,
    can_delete=True,
    max_num=50,  # Permitir un alto número de especificaciones
    validate_max=False,  # No validar max_num para permitir más si es necesario
    widgets={
        'orden': forms.NumberInput(attrs={
            'class': 'form-control especificacion-orden',
            'min': '1',
        }),
        'nombre': forms.TextInput(attrs={
            'class': 'form-control especificacion-nombre',
            'placeholder': 'Nombre de la especificación'
        }),
        'tipoDato': forms.Select(attrs={
            'class': 'form-control tipo-dato-select'
        }),
        'unidadMedida': forms.Select(attrs={
            'class': 'form-control unidad-medida-select'
        })
    }
) 