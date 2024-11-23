from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Cliente, Carrito, Compra  # Asegúrate de incluir Compra aquí
from .forms import CompraForm  # Importar el formulario de compra
import smtplib

smtp_server = 'smtp.gmail.com'
smtp_port = 587
username = 'camila.morelos.ieaci@gmail.com'
password = 'gztjqmoszdxfboqk'


def inicio(request):
    productos = Cliente.objects.all()
    return render(request, 'inicio.html', {'productos': productos})


def skincare(request):
    query = request.GET.get('q')  # Recuperar el valor del campo de búsqueda
    if query:
        productos_skincare = Cliente.objects.filter(categoria='Skincare', title__icontains=query)
    else:
        productos_skincare = Cliente.objects.filter(categoria='Skincare')
    
    return render(request, 'skincare.html', {'productos': productos_skincare})


def buscar_productos(request):
    query = request.GET.get('q')  # Obtener el término de búsqueda de la solicitud GET
    if query:
        resultados = Cliente.objects.filter(title__icontains=query)
    else:
        resultados = []

    return render(request, 'buscar_productos.html', {'resultados': resultados})


def registro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # Crear un formulario de registro
        if form.is_valid():
            user = form.save()  # Guardar el usuario
            login(request, user)  # Iniciar sesión automáticamente
            return redirect('login')  # Redirigir al login después del registro
    else:
        form = UserCreationForm()  # Inicializar el formulario vacío
    return render(request, 'registro.html', {'form': form})  # Renderizar la plantilla de registro


def login_view(request):
    error = None
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('inicio.html')  
            else:
                error = "Usuario o contraseña incorrectos."
        else:
            error = "Formulario inválido. Intenta nuevamente."
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form, 'error': error})


@login_required
def agregar_al_carrito(request, product_id):
    producto = get_object_or_404(Cliente, id=product_id)
    carrito, created = Carrito.objects.get_or_create(cliente=request.user, producto=producto)
    if not created:
        carrito.cantidad += 1
    carrito.save()
    return redirect('carrito')


@login_required
def ver_carrito(request):
    carrito_items = Carrito.objects.filter(cliente=request.user)
    total_carrito = sum(item.producto.precio * item.cantidad for item in carrito_items)
    total_por_producto = {item.producto.title: item.producto.precio * item.cantidad for item in carrito_items}

    return render(request, 'carrito.html', {
        'productos_carrito': carrito_items,
        'total_carrito': total_carrito,
        'total_por_producto': total_por_producto
    })


@login_required
def eliminar_del_carrito(request, item_id):
    carrito_item = get_object_or_404(Carrito, id=item_id, cliente=request.user)
    carrito_item.delete()
    return redirect('carrito')


@login_required
def realizar_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.cliente = request.user
            compra.save()
            try:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(username, password)
                    mensaje = f"Compra realizada por {compra.nombre}. Comentarios: {compra.comentarios}"
                    server.sendmail(username, compra.email, mensaje)
                print("Correo enviado con éxito")
            except Exception as e:
                print(f"Error al enviar el correo: {e}")

            return redirect('compra_exitosa')  # Corrige la redirección a la ruta correcta
    else:
        form = CompraForm()

    return render(request, 'realizar_compra.html', {'form': form})


def compra_exitosa(request):
    return render(request, 'compras_exitosa.html')
