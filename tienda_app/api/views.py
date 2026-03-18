from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrdenInputSerializer
from tienda_app.services import CompraService
from ..models import Libro
from django.shortcuts import render
from tienda_app.infra.factories import PaymentFactory

class CompraAPIView(APIView):
    """
    Endpoint para procesar compras via JSON.
    POST /api/comprar/
    Payload: {"libro_id": 1, "direccion_envio": "Calle 123"}
    """

    def post(self, request):
        # 1. Validacion de datos de entrada (Adapter)
        serializer = OrdenInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        datos = serializer.validated_data

        try:
            # 2. Inyeccion de Dependencias (Factory)
            gateway = PaymentFactory.get_processor()

            # 3. Ejecucion de Logica de Negocio (Service Layer)
            servicio = CompraService(procesador_pago=gateway)

            # El ID se convierte en un objeto que tiene el atributo 'precio'
            detalle = servicio.obtener_detalle_producto(datos['libro_id'])
            libro_objeto = detalle['libro']

            # Ahora pasamos el objeto dentro de la lista, no el ID numérico
            resultado = servicio.ejecutar_compra(
                usuario=request.user,
                lista_productos=[libro_objeto], 
                direccion=datos['direccion_envio']
            )

            return Response({
                "estado": "exito",
                "mensaje": f"Orden creada. {resultado}"
            }, status=status.HTTP_201_CREATED)

        except ValueError as e:
            # Errores de negocio (ej: Sin stock)
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        
        except Exception as e:
            # Mantenemos error_tecnico para depurar si algo más falla
            return Response({"error_tecnico": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def inventario_view(request):
    libros = Libro.objects.all()
    return render(request, "tienda_app/inventario.html", {"libros": libros})