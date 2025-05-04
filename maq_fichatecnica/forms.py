from django import forms
from .models import TipoEquipo, MarcaEquipo, ModeloEquipo

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