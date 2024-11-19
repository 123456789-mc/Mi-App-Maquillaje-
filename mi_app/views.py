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
    # Recuperar productos de la categoría "Skincare"
    query = request.GET.get('q')  # Recuperar el valor del campo de búsqueda
    if query:
        # Filtrar productos por el título y la categoría "Skincare"
        productos_skincare = Cliente.objects.filter(categoria='Skincare', title__icontains=query)
    else:
        productos_skincare = Cliente.objects.filter(categoria='Skincare')
    
    return render(request, 'skincare.html', {'productos': productos_skincare})  # Pasar productos a la plantilla

def buscar_productos(request):
    query = request.GET.get('q')  # Obtener el término de búsqueda de la solicitud GET
    if query:
        # Filtrar los productos que coincidan con el término de búsqueda
        resultados = Cliente.objects.filter(title__icontains=query)
    else:
        resultados = []  # Si no hay consulta, no hay resultados

    return render(request, 'buscar_productos.html', {'resultados': resultados})  # Renderizar la plantilla con los resultados

def registro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # Crear un formulario de registro
        if form.is_valid():
            user = form.save()  # Guardar el usuario
            login(request, user)  # Iniciar sesión automáticamente
            return redirect('inicio')  # Redirigir a la página de inicio
    else:
        form = UserCreationForm()  # Inicializar el formulario vacío
    return render(request, 'registro.html', {'form': form})  # Renderizar la plantilla de registro

def login_view(request):
    error = None
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Autenticar usuario
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('inicio')  # Redirigir a la página de inicio
            else:
                error = "Usuario o contraseña incorrectos."
        else:
            error = "Formulario inválido. Intenta nuevamente."
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form, 'error': error})

# Vista para agregar productos al carrito
@login_required  # Requiere que el usuario esté autenticado
def agregar_al_carrito(request, product_id):
    producto = get_object_or_404(Cliente, id=product_id)  # Obtener el producto o devolver 404
    carrito, created = Carrito.objects.get_or_create(cliente=request.user, producto=producto)  # Asociar al cliente logueado y el producto
    if not created:
        carrito.cantidad += 1  # Incrementar la cantidad si ya existe en el carrito
    carrito.save()
    return redirect('carrito')  # Redirigir a la vista del carrito después de agregar


# Vista para mostrar el carrito
@login_required  # Requiere que el usuario esté autenticado
def ver_carrito(request):
    # Asegurarse de que solo se muestren los productos del cliente actual
    carrito_items = Carrito.objects.filter(cliente=request.user)  # Obtener productos en el carrito del usuario actual

    # Calcular el total sumando el precio del producto por la cantidad en el carrito
    total_carrito = sum(item.producto.precio * item.cantidad for item in carrito_items)  # Acceder al precio del producto

    # Crear una lista de total por producto
    total_por_producto = {item.producto.title: item.producto.precio * item.cantidad for item in carrito_items}

    return render(request, 'carrito.html', {
        'productos_carrito': carrito_items,
        'total_carrito': total_carrito,  # Pasar el total del carrito a la plantilla
        'total_por_producto': total_por_producto  # Pasar el total por producto a la plantilla
    })

# Vista para eliminar un producto del carrito
@login_required  # Requiere que el usuario esté autenticado
def eliminar_del_carrito(request, item_id):
    carrito_item = get_object_or_404(Carrito, id=item_id, cliente=request.user)  # Asegurarse de que solo pueda eliminar su propio carrito
    carrito_item.delete()
    return redirect('carrito')  # Redirigir a la página del carrito

# Nueva vista para realizar la compra
@login_required  # Requiere que el usuario esté autenticado
def realizar_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.cliente = request.user  # Asignar el cliente actual
            compra.save()
            try:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()  # Establece la conexión segura
                    server.login(username, password)
                    # Formatear el mensaje adecuadamente
                    mensaje = f"Compra realizada por {compra.nombre}. Comentarios: {compra.comentarios}"
                    server.sendmail(username, compra.email, mensaje)
                print("Correo enviado con éxito")
            except Exception as e:
                print(f"Error al enviar el correo: {e}")

            return redirect('compras_exitosa')  # Redirige a una página de éxito
    else:
        form = CompraForm()

    return render(request, 'realizar_compra.html', {'form': form})

# Nueva vista para mostrar mensaje de compra exitosa
def compra_exitosa(request):
    return render(request, 'compras_exitosa.html')  # Asegúrate de que la ruta sea correcta


