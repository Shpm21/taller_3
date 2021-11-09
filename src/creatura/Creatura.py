from especie.Especie import Especie
class Creatura(Especie):
    def __init__(self, id: int, nombre_especie: str, id_creatura: int, 
        nombre_usuario: str, salud, velocidad):
        super().__init__(id, nombre_especie)
        self.id_creatura = id_creatura
        self.nombre_usuario = nombre_usuario
        self.salud = salud
        self.velocidad = velocidad
    def atacar():
        pass