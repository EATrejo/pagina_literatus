from django.db import models
from django.db.models.signals import pre_save
from myproject.utils import unique_slug_generator
from cloudinary_storage.storage import MediaCloudinaryStorage

# Create your models here.

class Tertulia(models.Model):
    tertulia_name = models.CharField(max_length=100)
    tertulia_banner = models.ImageField(upload_to='imagenes_admin/tertulias/',storage=MediaCloudinaryStorage())  # Fuerza Cloudinary aquí)
    tertulia_description = models.TextField(max_length=450, blank=True)
    tertulia_address = models.CharField(max_length=250, blank=True, null=True)
    tertulia_horario = models.CharField(max_length=100)
    tertulia_fecha_de_inicio = models.DateField(auto_now_add=False, auto_now=False, null=True)
    tertulia_sesiones =models.PositiveSmallIntegerField()
    tertulia_encargado_picture = models.ImageField(upload_to='imagenes_admin/tertulias/foto-encargado')
    tertulia_encargado = models.CharField(max_length=100)
    tertulia_lugares = models.PositiveIntegerField(blank=True, null=True)
    slug = models.IntegerField(default=0) 

    def __str__(self):
        return self.tertulia_name
    
def slug_generator(sender, instance, *args, **kwargs):
        if not instance.slug:
            instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Tertulia)
        
