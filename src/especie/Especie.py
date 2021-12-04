from color.Color import *
from tipo.Tipo import Tipo


class Especie:
    def __init__(self, id: int, nombre_especie: str):
        self.id = id
        self.nombre_especie = nombre_especie
        self.tipo_1: Tipo = None
        self.tipo_2: Tipo = None

    def __str__(self):
        if self.tipo_2 == None and self.tipo_1 != None:
            return WBLUE +'Nombre: ' + self.nombre_especie + ENDC + YELLOW + '\nTipo Primario: ' + self.tipo_1.nombre + ENDC
        if self.tipo_2 != None and self.tipo_1 != None:
            return WBLUE + 'Nombre: ' + self.nombre_especie + ENDC + YELLOW + '\nTipo Primario: ' + self.tipo_1.nombre + '\nTipo Secundario: ' + self.tipo_2.nombre + ENDC