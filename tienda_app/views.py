from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .api.serializers import OrdenInputSerializer
from django.http import HttpResponse
from django.shortcuts import render
from .services import CompraService
from django.contrib.auth.models import User
from .models import Libro
from .infra.factories import PaymentFactory

class CompraView(View):
    """
    CBV: Vista Basada en Clases. 
    Actúa como un "Portero": recibe la petición y delega al servicio.
    """
    template_name = 'tienda_app/compra.html'
    
    # Configuramos el servicio con su implementación de infraestructura
    def setup_service(self):
        gateway = PaymentFactory.get_processor()
        return CompraService(procesador_pago=gateway)

    def get(self, request, libro_id):
        servicio = self.setup_service()
        contexto = servicio.obtener_detalle_producto(libro_id)
        return render(request, self.template_name, contexto)

    def post(self, request, libro_id):
        servicio = self.setup_service()

        try:
            libro = servicio.obtener_detalle_producto(libro_id)['libro']
            direccion = "Cra 5 # 10-20" # Dirección fija para simplificar
            
            if not direccion:
                return render(request, self.template_name, {
                    'error': "Debe proporcionar una dirección de envío."
                }, status=400)
            
            # El servicio retorna un mensaje como "Orden 5 procesada exitosamente."
            usuario_prueba, created = User.objects.get_or_create(
                username='usuario_prueba',
                defaults={
                    'email': 'prueba@test.com',
                    'first_name': 'Usuario',
                    'last_name': 'Prueba'
                }
            )
            mensaje = servicio.ejecutar_compra(
                usuario=usuario_prueba, 
                lista_productos=[libro], 
                direccion=direccion
            )
            
            return render(request, self.template_name, {
                'mensaje_exito': mensaje
            })
        except (ValueError, Exception) as e:
            # Manejo de errores de negocio transformados a respuesta de usuario
            return render(request, self.template_name, {
                'error': str(e)
            }, status=400)
        


def inventario_view(request):
    libros = Libro.objects.all()
    return render(request, "inventario.html", {"libros": libros})
        


