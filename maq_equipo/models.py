from django.db import models
from gen_settings.models import Empresa

# Create your models here.
class TipoEquipo(models.Model):
    prefixeq = models.CharField(max_length=2, unique=True, null=False, blank=False)
    tipoeq = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"{self.tipoeq}"

    class Meta:
        ordering = ['tipoeq']
        verbose_name = 'Tipo equipo'
        verbose_name_plural = 'Tipo equipos'

class MarcaEquipo(models.Model):
    tipoeq = models.ManyToManyField(TipoEquipo)
    marcaeq = models.CharField(max_length=150, unique=True, null=False, blank=False)
    
    def __str__(self):
        return f"{self.marcaeq}"
    
    class Meta:
        ordering = ['marcaeq']
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
    
class ModeloEquipo(models.Model):
    tipoeq = models.ForeignKey(TipoEquipo, on_delete=models.CASCADE, null=False, blank=False)
    marcaeq = models.ForeignKey(MarcaEquipo, on_delete=models.CASCADE, null=False, blank=False)
    modeloeq = models.CharField(max_length=150, null=False,blank=False)

    def __str__(self):
        return f"{self.modeloeq} - {self.marcaeq}"
    
    class Meta:
        ordering = ['modeloeq']
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'

class Equipo(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    tipoeq = models.ForeignKey(TipoEquipo, on_delete=models.CASCADE)
    marcaeq = models.ForeignKey(MarcaEquipo, on_delete=models.CASCADE)
    modeloeq = models.ForeignKey(ModeloEquipo, on_delete=models.CASCADE)
    codinterno = models.CharField(max_length=4, null=False, blank=False)
    nombreeq = models.CharField(max_length=100, null=False, blank=False)
    patente = models.CharField(max_length=10, null=False, blank=True)
    anioeq = models.CharField(max_length=4, null=False, blank=False)
    fechacompra = models.DateField(null=False, blank=False)