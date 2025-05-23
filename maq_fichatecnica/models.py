from django.db import models
from gen_settings.models import UnidadMedida, TipoDato
from maq_equipo.models import TipoEquipo
# Create your models here.

class SeccionFicha(models.Model):
    seccion = models.CharField(max_length=150, null=False, blank=False)
    tipoeq = models.ManyToManyField(TipoEquipo)

    def __str__(self):
        return f"{self.seccion}"
    
    class Meta:
        ordering = ['seccion']
        verbose_name = 'Sección'
        verbose_name_plural = 'Secciones'

class EspecificacionSeccion(models.Model):
    orden = models.IntegerField(null=False, blank=False)
    seccion = models.ForeignKey(SeccionFicha, on_delete=models.CASCADE, null=False, blank=False)
    especificacion = models.CharField(max_length=150, null=False, blank=False)
    tipodato = models.ForeignKey(TipoDato, on_delete=models.CASCADE, null=False, blank=False)
    unidadmedida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"{self.especificacion} - {self.seccion}"
    
    class Meta:
        ordering = ['especificacion']
        verbose_name = 'Especificación'
        verbose_name_plural = 'Especificaciones'

class PlantillaFichaTecnica(models.Model):
    nombre = models.CharField(max_length=200, null=False, blank=False)
    tipoeq = models.ForeignKey(TipoEquipo, on_delete=models.CASCADE, null=False, blank=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.tipoeq}"
    
    class Meta:
        ordering = ['-fecha_modificacion']
        verbose_name = 'Plantilla de Ficha Técnica'
        verbose_name_plural = 'Plantillas de Fichas Técnicas'

class SeccionPlantilla(models.Model):
    plantilla = models.ForeignKey(PlantillaFichaTecnica, on_delete=models.CASCADE, related_name='secciones')
    seccion = models.ForeignKey(SeccionFicha, on_delete=models.CASCADE)
    orden = models.IntegerField(null=False, blank=False)
    
    def __str__(self):
        return f"{self.seccion} (Orden: {self.orden})"
    
    class Meta:
        ordering = ['orden']
        verbose_name = 'Sección de Plantilla'
        verbose_name_plural = 'Secciones de Plantilla'
        unique_together = [['plantilla', 'seccion']]
