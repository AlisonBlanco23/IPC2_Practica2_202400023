class Paciente:
    def __init__(self, nombre: str, edad: int, especialidad: str):
        self.nombre = nombre
        self.edad = edad
        self.especialidad = especialidad

    def obtener_tiempo_atencion(self) -> int:
        tiempos = {
            "Medicina General": 10,
            "Pediatría": 15,
            "Ginecología": 20,
            "Dermatología": 25
        }
        return tiempos.get(self.especialidad, 10)

    def __str__(self):
        return f"{self.nombre} ({self.edad} años) - {self.especialidad}"

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "edad": self.edad,
            "especialidad": self.especialidad,
            "tiempo_atencion": self.obtener_tiempo_atencion()
        }