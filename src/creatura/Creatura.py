from especie.Especie import Especie
class Creatura():
    def __init__(self,nombre_creatura: str, salud: int, velocidad: int, nombre_tipo_1: str, nombre_ataque_1: str):
        self.nombre_creatura = nombre_creatura
        self.salud = salud
        self.velocidad = velocidad
        self.nombre_tipo_1 = nombre_tipo_1
        self.nombre_tipo_2 = ''
        self.nombre_ataque_1 = nombre_ataque_1
        self.nombre_ataque_2 = ''
    def __str__(self) -> str:
        if self.nombre_tipo_2 == '' and self.nombre_ataque_2 == '':
            return 'Nombre: %s\nPS: %s\nPV: %s\nTipo Primario: %s\nTipo Secundario: NN\nAtaque 1: %s\nAtaque 2: NN' \
                % (self.nombre_creatura, self.salud, self.velocidad, self.nombre_tipo_1, self.nombre_ataque_1)
        elif self.nombre_tipo_2 == '' and self.nombre_ataque_2 != '':
            return 'Nombre: %s\nPS: %s\nPV: %s\nTipo Primario: %s\nTipo Secundario: NN\nAtaque 1: %s\nAtaque 2: %s' \
                % (self.nombre_creatura, self.salud, self.velocidad, self.nombre_tipo_1, self.nombre_ataque_1, self.nombre_ataque_2)
        elif self.nombre_tipo_2 != '' and self.nombre_ataque_2 == '':
            return 'Nombre: %s\nPS: %s\nPV: %s\nTipo Primario: %s\nTipo Secundario: %s\nAtaque 1: %s\nAtaque 2: NN' \
                % (self.nombre_creatura, self.salud, self.velocidad, self.nombre_tipo_1, self.nombre_tipo_2, self.nombre_ataque_1)
        else:
            return 'Nombre: %s\nPS: %s\nPV: %s\nTipo Primario: %s\nTipo Secundario: %s\nAtaque 1: %s\nAtaque 2: %s' \
                % (self.nombre_creatura, self.salud, self.velocidad, self.nombre_tipo_1, self.nombre_tipo_2, self.nombre_ataque_1, self.nombre_ataque_2)  