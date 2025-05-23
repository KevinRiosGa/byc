from django import forms
from django.forms import inlineformset_factory
from .models import (
    TipoEquipo, SeccionFicha, EspecificacionSeccion,
    PlantillaFichaTecnica, SeccionPlantilla
    )

class SeccionFichaForm(forms.ModelForm):
    tipoeq = forms.ModelMultipleChoiceField(
        queryset=TipoEquipo.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Tipos de Equipo"
    )

    class Meta:
        model = SeccionFicha
        fields = ['seccion', 'tipoeq']
        widgets = {
            'seccion': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '150',
                'required': True
            })
        }

class EspecificacionSeccionForm(forms.ModelForm):
    seccion = forms.ModelMultipleChoiceField(
        queryset=SeccionFicha.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Secciones"
    )
    orden = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'style': 'width: 70px;', 'min': 1, 'required': True}),
        label="Orden"
    )
    
    class Meta:
        model = EspecificacionSeccion
        fields = ['orden', 'seccion', 'especificacion', 'tipodato', 'unidadmedida']
        widgets = {
            'especificacion': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '150', 'required': True}),
            'tipodato': forms.Select(attrs={'class': 'form-control form-control-sm', 'required': True}),
            'unidadmedida': forms.Select(attrs={'class': 'form-control form-control-sm', 'required': True}),
        }

# Formset para las especificaciones
EspecificacionFormSet = inlineformset_factory(
    SeccionFicha,
    EspecificacionSeccion,
    form=EspecificacionSeccionForm,
    extra=0,
    can_delete=True,
    min_num=1,
    validate_min=True
)

class PlantillaFichaTecnicaForm(forms.ModelForm):
    class Meta:
        model = PlantillaFichaTecnica
        fields = ['nombre', 'tipoeq']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'maxlength': '200',
                'required': True
            }),
            'tipoeq': forms.Select(attrs={
                'class': 'form-control form-control-sm',
                'required': True
            })
        }

class SeccionPlantillaForm(forms.ModelForm):
    class Meta:
        model = SeccionPlantilla
        fields = ['seccion', 'orden']
        widgets = {
            'seccion': forms.Select(attrs={
                'class': 'form-control form-control-sm',
                'required': True
            }),
            'orden': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm',
                'min': 1,
                'required': True
            })
        }

# Formset para las secciones de la plantilla
SeccionPlantillaFormSet = inlineformset_factory(
    PlantillaFichaTecnica,
    SeccionPlantilla,
    form=SeccionPlantillaForm,
    extra=0,
    can_delete=True,
    min_num=1,
    validate_min=True
)



