from django.shortcuts import get_object_or_404
from .models import Libro, Inventario, Orden
from .domain.logic import CalculadorImpuestos
from .domain.builders import OrdenBuilder   

class CompraService:
    """
    SERVICE LAYER: Orquesta la interacción entre el dominio, 
    la infraestructura y la base de datos.
    """
    def __init__(self, procesador_pago):
        # Inyectamos la dependencia (DIP)
        self.procesador_pago = procesador_pago
        self.builder = OrdenBuilder() 

    def ejecutar_compra(self, usuario, lista_productos, direccion):
        # Uso del Builder: Semántica clara y validación interna
        orden = (self.builder
                 .con_usuario(usuario)
                 .con_productos(lista_productos)
                 .para_envio(direccion)
                 .build())
           
        for libro in lista_productos:
            inventario = libro.inventario

            if inventario.cantidad <= 0:
                raise ValueError("Sin stock disponible")

            inventario.cantidad -= 1
            inventario.save()
        
        # Uso del Factory (inyectado): Cambio de comportamiento sin cambiar código
        if self.procesador_pago.pagar(orden.total):
            return f"Orden {orden.id} procesada exitosamente."
        
        orden.delete()
        raise Exception("Error en la pasarela de pagos")
  
    def obtener_detalle_producto(self, libro_id):
        """
        Retorna un diccionario con el libro y su total con IVA
        """
        libro = get_object_or_404(Libro, id=libro_id)
        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)
        return {"libro": libro, "total": total}
