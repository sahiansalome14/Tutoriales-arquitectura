from django.urls import path
from .views import CompraView
from tienda_app.api.views import CompraAPIView, inventario_view

urlpatterns = [
    # Usamos .as_view() para habilitar la CBV
    path('compra/<int:libro_id>/', CompraView.as_view(), name='finalizar_compra'),
    path ( 'api/v1/comprar/' , CompraAPIView.as_view() , name='api_comprar'),
    path('inventario/', inventario_view, name='inventario')
]