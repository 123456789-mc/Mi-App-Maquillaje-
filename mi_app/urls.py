from django.urls import path
from .views import * 

urlpatterns = [
    path('', inicio, name='inicio'),  # Página de inicio
    path('registro/', registro_view, name='registro'),  # Ruta de registro
    path('login/', login_view, name='login'),  # Ruta de login usando login_view
    path('skincare/', skincare, name='skincare'),  # Nueva ruta para skincare
    path('buscar/', buscar_productos, name='buscar_productos'),  # Ruta para búsqueda
    path('agregar-al-carrito/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),  # Ruta para agregar al carrito
    path('carrito/', ver_carrito, name='ver_carrito'),  # Ruta para ver el carrito
    path('eliminar-del-carrito/<int:item_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('realizar-compra/', realizar_compra, name='realizar_compra'),  # Ruta para realizar compra
    path('compra-exitosa/', compra_exitosa, name='compra_exitosa'),  # Ruta para la página de compra exitosa
    path('productos/', lista_productos, name='lista_productos'),
]

