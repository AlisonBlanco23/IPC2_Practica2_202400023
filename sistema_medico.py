from cola_turnos import ColaTurnos
from paciente import Paciente

class SistemaMedico:
    def __init__(self):
        self.cola = ColaTurnos()

    def registrar_paciente(self, nombre: str, edad: int, especialidad: str) -> bool:
        try:
            paciente = Paciente(nombre, edad, especialidad)
            self.cola.encolar(paciente)
            return True
        except Exception:
            return False

    def atender_siguiente(self) -> dict:
        paciente = self.cola.desencolar()
        if paciente is None:
            return {"error": "No hay pacientes en espera."}
        return {
            "paciente": paciente,
            "mensaje": f"Atendiendo a {paciente.nombre}. Tiempo de atención: {paciente.obtener_tiempo_atencion()} minutos."
        }

    def obtener_frente_cola(self):
        return self.cola.obtener_frente()

    def obtener_tamano_cola(self) -> int:
        return self.cola.tamano_actual()

    def obtener_paciente_en_posicion(self, indice: int):
        return self.cola.obtener_paciente_en_posicion(indice)

    def obtener_tiempo_espera_paciente(self, indice: int) -> int:
        return self.cola.calcular_tiempo_espera_hasta_posicion(indice)

    def esta_vacia(self) -> bool:
        return self.cola.esta_vacia()