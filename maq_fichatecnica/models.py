from django.db import models
from gen_settings.models import UnidadMedida, TipoDato
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
    tipoeq = models.ForeignKey(TipoEquipo, on_delete=models.PROTECT, null=False, blank=False)
    marcaeq = models.ForeignKey(MarcaEquipo, on_delete=models.PROTECT, null=False, blank=False)
    modeloeq = models.CharField(max_length=150, null=False,blank=False)

    def __str__(self):
        return f"{self.modeloeq} - {self.marcaeq}"
    
    class Meta:
        ordering = ['modeloeq']
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'

class FichaTecnica(models.Model):
    nombre = models.CharField(max_length=200)
    tipoeq = models.ForeignKey(TipoEquipo, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Ficha: {self.nombre} - {self.tipoeq.tipoeq}"
    
    class Meta:
        verbose_name = 'Ficha Técnica'
        verbose_name_plural = 'Fichas Técnicas'

class Seccion(models.Model):
    fichaTecnica = models.ForeignKey(FichaTecnica, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    orden = models.PositiveIntegerField()
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.orden}. {self.nombre}"
    
    class Meta:
        verbose_name = 'Sección'
        verbose_name_plural = 'Secciones'
        ordering = ['orden']

class Especificacion(models.Model):
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    orden = models.PositiveIntegerField()
    tipoDato = models.ForeignKey(TipoDato, on_delete=models.CASCADE)
    unidadMedida = models.ForeignKey(UnidadMedida, on_delete=models.SET_NULL, null=True, blank=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.seccion.nombre} - {self.nombre}"
    
    class Meta:
        verbose_name = 'Especificación'
        verbose_name_plural = 'Especificaciones'
        ordering = ['seccion__orden', 'orden']