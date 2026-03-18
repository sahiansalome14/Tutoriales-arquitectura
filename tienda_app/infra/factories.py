import os
from .gateways import BancoNacionalProcesador

#Implementación ligera para pruebas (Mocking)
class MockPaymentProcessor:
    def pagar(self, monto):
        print(f"[DEBUG] Mock payment: Procesando pago de ${monto} sin cargo real.")
        return True
class PaymentFactory:
    @staticmethod
    def get_processor():
        provider= os.getenv('PAYMENT_PROVIDER', 'BANCO')
        if provider == 'MOCK':
            return MockPaymentProcessor()
        
        #Por defecto usamos la infraestructura real
        return BancoNacionalProcesador()