from django import forms
from django.forms import inlineformset_factory
from .models import (
    TipoEquipo, MarcaEquipo, ModeloEquipo,
    SeccionFicha, EspecificacionFicha
    )

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

class EspecificacionFichaForm(forms.ModelForm):
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
        model = EspecificacionFicha
        fields = ['orden', 'seccion', 'especificacion', 'tipodato', 'unidadmedida']
        widgets = {
            'especificacion': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '150', 'required': True}),
            'tipodato': forms.Select(attrs={'class': 'form-control form-control-sm', 'required': True}),
            'unidadmedida': forms.Select(attrs={'class': 'form-control form-control-sm', 'required': True}),
        }

# Formset para las especificaciones
EspecificacionFormSet = inlineformset_factory(
    SeccionFicha,
    EspecificacionFicha,
    form=EspecificacionFichaForm,
    extra=0,
    can_delete=True,
    min_num=1,
    validate_min=True
)



