from django.db import models

# Create your models here.

class TipoEquipo(models.Model):
    prefixeq = models.CharField(max_length=2, unique=True, blank=False, null=False)
    tipoeq = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.tipoeq

class MarcaEquipo(models.Model):
    marcaeq = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.marcaeq


