from decimal import Decimal

class CalculadorImpuestos:
    """
    S: Responsabilidad única - Solo calcula impuestos.
    O: Abierto a extensión - Podríamos heredar para diferentes países.
    """
    @staticmethod
    def obtener_total_con_iva(precio_base) -> Decimal:
        """
        Devuelve el precio con IVA.
        Acepta precio_base como Decimal (recomendado con Django)
        """
        IVA = Decimal("1.19")  # 19% de IVA
        return precio_base * IVA
