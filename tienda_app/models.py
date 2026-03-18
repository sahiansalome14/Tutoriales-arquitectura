from django.db import models
from django.contrib.auth.models import User

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.titulo

class Inventario(models.Model):
    libro = models.OneToOneField(Libro, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()


class Orden(models.Model):
    usuario = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )  
    
    libros = models.ManyToManyField(Libro, related_name='ordenes')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    direccion_envio = models.CharField(max_length=255)  
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orden #{self.id} - {self.libro.titulo}"