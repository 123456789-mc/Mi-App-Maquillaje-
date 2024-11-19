# basedatosprueba/urls.py

from django.contrib import admin
from django.urls import path
from django.conf import settings  # Importar settings para las configuraciones
from django.conf.urls.static import static  # Importar para manejar archivos estáticos
from mi_app import views  # Importa las vistas de la aplicación

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta para el panel de administración
    path('login/', views.login_view, name='login'),  # Ruta para el login
    path('', views.inicio, name='inicio'),  # Ruta para la página de inicio
    path('registro/', views.registro_view, name='registro'),  # Ruta para el registro
    path('skincare/', views.skincare, name='skincare'),  # Ruta para skincare
    path('agregar-al-carrito/<int:product_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('buscar/', views.buscar_productos, name='buscar_productos'),  # Ruta para búsqueda
    path('carrito/', views.ver_carrito, name='carrito'),  # Agregar la ruta para el carrito
    path('eliminar-del-carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('realizar_compra/', views.realizar_compra, name='realizar_compra'),
    path('compras_exitosa/', views.compra_exitosa, name='compras_exitosa'),
]

# Agregar esta línea para servir archivos multimedia (como las imágenes) durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
