from django.db import models
from django.db.models.signals import pre_save
from cursos.utils import unique_slug_generator
from datetime import datetime

# Create your models here.

class Curso(models.Model):
    title = models.CharField(max_length=100)
    banner = models.ImageField(default='fallback.png', blank=True)
    description = models.TextField()
    duracion_curso = models.DurationField(null=True)
    lugar_curso = models.TextField()
    fecha_de_inicio = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    costo_del_curso = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    curso_encargado_picture = models.ImageField(default='', blank=True)
    curso_encargado = models.CharField(max_length=100)
    curso_lugares = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title
   

def slug_generator(sender, instance, *args, **kwargs):
        if not instance.slug:
            instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Curso)