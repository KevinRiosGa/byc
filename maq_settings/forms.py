from django import forms
from .models import TipoEquipo, MarcaEquipo, ModeloEquipo

class TipoEquipoForm(forms.ModelForm):
    class Meta:
        model = TipoEquipo
        fields = ['prefixeq', 'tipoeq']
        labels = {
            'prefixeq': 'Prefijo',
            'tipoeq': 'Tipo de equipo',
        }
        widgets = {
            'prefixeq': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el prefijo'}),
            'tipoeq': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el tipo de equipo'}),
        }

class MarcaEquipoForm(forms.ModelForm):
    class Meta:
        model = MarcaEquipo
        fields = ['marcaeq']
        labels = {
            'marcaeq': 'Marca',
        }
        widgets = {
            'marcaeq': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la marca'}),
        }

class ModeloEquipoForm(forms.ModelForm):
    class Meta:
        model = ModeloEquipo
        fields = ['tipoeq_id', 'marcaeq_id', 'modeloeq']