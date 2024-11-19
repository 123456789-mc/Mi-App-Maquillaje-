from django.db import models
from django.contrib.auth.models import User  # Importar User para la relación con el cliente
from django.db.models.fields import CharField, URLField
from django.db.models.fields.files import ImageField

# Create your models here.
class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default='Nombre')  # Valor por defecto
    descripcion = models.CharField(max_length=250, blank=True, default='Descripción por defecto')  # Valor por defecto
    image = models.ImageField(upload_to='imagenes/images', default='imagenes/default.jpg')  # Valor por defecto
    url = URLField(blank=True, null=True)  # Permitir que el URL sea vacío
    categoria = models.CharField(max_length=50, default='General')  # Campo para la categoría
    precio = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)  # Nuevo campo para el precio del producto

    def Cliente(self):
        return self


class Carrito(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el modelo User
    producto = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)  # Hacer este campo nullable
    cantidad = models.PositiveIntegerField(default=1)  # Cantidad de productos en el carrito
    fecha_agregado = models.DateTimeField(auto_now_add=True)  # Fecha de adición al carrito

    def __str__(self):
        return f"{self.producto.title} - {self.cantidad} item(s)"  # Cambiado a producto.title para mostrar el título del producto


class Compra(models.Model):  # Nuevo modelo de Compra
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el modelo User
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    metodo_pago = models.CharField(max_length=50)
    comentarios = models.TextField(blank=True, null=True)
    fecha_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compra de {self.nombre} - {self.fecha_compra}"
