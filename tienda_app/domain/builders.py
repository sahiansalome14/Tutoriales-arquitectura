from ..models import Orden
from decimal import Decimal

class OrdenBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self._usuario= None
        self._items= []
        self._direccion=""

    def con_usuario(self, usuario):
        self._usuario = usuario
        return self #Permite Fluent Interface

    def con_productos(self, productos):
        self._items = productos
        return self

    def para_envio(self, direccion):
        self._direccion = direccion
        return self
    
    def build(self)-> Orden:
        if not self._usuario or not self._items or not self._direccion:
            raise ValueError("Faltan datos para construir la orden.")
        
        #Encapsulamos la lógica de cálculo
        subtotal = sum(p.precio for p in self._items)
        total_con_iva= subtotal * Decimal(1.19)

        orden=Orden.objects.create(
            usuario=self._usuario,
            total=total_con_iva,
            direccion_envio=self._direccion)
        
        orden.libros.set(self._items)
        
        self.reset() #Limpiamos el builder para reutilizarlo
        return orden
