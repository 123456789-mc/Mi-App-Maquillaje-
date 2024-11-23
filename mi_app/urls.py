from django.urls import path
from .views import * 

urlpatterns = [
    path('', registro_view, name='registro'),  
    path('login/', login_view, name='login'), 
    path('inicio/', inicio, name='inicio'),  
    path('skincare/', skincare, name='skincare'),  
    path('buscar/', buscar_productos, name='buscar_productos'),  
    path('agregar-al-carrito/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),  
    path('carrito/', ver_carrito, name='ver_carrito'),  
    path('eliminar-del-carrito/<int:item_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('realizar-compra/', realizar_compra, name='realizar_compra'),  
    path('compra-exitosa/', compra_exitosa, name='compra_exitosa'),  
    #path('productos/', lista, name='lista_productos'),
]


