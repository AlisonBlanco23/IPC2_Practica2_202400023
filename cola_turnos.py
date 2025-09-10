from paciente import Paciente

class Nodo:
    def __init__(self, paciente: Paciente):
        self.paciente = paciente
        self.siguiente = None

class ColaTurnos:
    def __init__(self):
        self.frente = None
        self.final = None
        self.tamano = 0

    def esta_vacia(self) -> bool:
        return self.frente is None

    def encolar(self, paciente: Paciente):
        nuevo_nodo = Nodo(paciente)
        if self.esta_vacia():
            self.frente = nuevo_nodo
        else:
            self.final.siguiente = nuevo_nodo
        self.final = nuevo_nodo
        self.tamano += 1

    def desencolar(self) -> Paciente:
        if self.esta_vacia():
            return None
        paciente_atendido = self.frente.paciente
        self.frente = self.frente.siguiente
        if self.frente is None:
            self.final = None
        self.tamano -= 1
        return paciente_atendido

    def ver_primero(self) -> Paciente:
        if self.esta_vacia():
            return None
        return self.frente.paciente

    def obtener_paciente_en_posicion(self, indice: int):
        if indice < 0 or indice >= self.tamano:
            return None
        actual = self.frente
        for _ in range(indice):
            actual = actual.siguiente
        return actual.paciente

    def calcular_tiempo_espera_hasta_posicion(self, indice: int) -> int:
        if indice <= 0:
            return 0
        tiempo_espera = 0
        actual = self.frente
        for i in range(indice):
            if actual is None:
                break
            tiempo_espera += actual.paciente.obtener_tiempo_atencion()
            actual = actual.siguiente
        return tiempo_espera

    def tamano_actual(self) -> int:
        return self.tamano

    def obtener_frente(self):
        return self.frente