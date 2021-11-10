from especie.Especie import Especie
from ataque.Ataque import Ataque


class Creatura():
    def __init__(self, id_creatura: str, salud: int, velocidad: int):
        self.id_creatura = id_creatura
        self.salud = salud
        self.velocidad = velocidad
        self.especie: Especie = None
        self.ataque_1: Ataque = None
        self.ataque_2: Ataque = None
        self.nombre_usuario: str = None

    def __str__(self) -> str:
        if self.especie.tipo_2 == None and self.ataque_2 == None:
            return 'Nombre: %s\nPS: %s\nPV: %s\nTipo Primario: %s\nAtaque 1: %s\nAtaque 2: NN' \
                % (self.especie.nombre_especie, self.salud, self.velocidad, 
                self.especie.tipo_1.nombre, self.ataque_1.nombre)

        elif self.especie.tipo_2 == None and self.ataque_2 != None:
            return 'Nombre: %s\nPS: %s\nPV: %s\nTipo Primario: %s\nAtaque 1: %s\nAtaque 2: %s' \
                % (self.especie.nombre_especie, self.salud, self.velocidad, 
                self.especie.tipo_1.nombre, self.ataque_1.nombre, self.ataque_2.nombre)

        elif self.especie.tipo_2 != None and self.ataque_2 == None:
            return 'Nombre: %s\nPS: %s\nPV: %s\nTipo Primario: %s\nTipo Secundario: %s\nAtaque 1: %s' \
                % (self.especie.nombre_especie, self.salud, self.velocidad, 
                self.especie.tipo_1.nombre, self.especie.tipo_2.nombre, self.ataque_1.nombre)
                
        else:
            return 'Nombre: %s\nPS: %s\nPV: %s\nTipo Primario: %s\nTipo Secundario: %s\nAtaque 1: %s\nAtaque 2: %s' \
                % (self.especie.nombre_especie, self.salud, self.velocidad, 
                self.especie.tipo_1.nombre, self.especie.tipo_2.nombre, self.ataque_1.nombre, self.ataque_2.nombre)  