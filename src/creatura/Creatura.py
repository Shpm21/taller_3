from especie.Especie import Especie
from ataque.Ataque import Ataque

from random import randint


class Creatura():
    def __init__(self, id_creatura: str, salud: int,
                 velocidad: int):
        self.id_creatura = id_creatura
        self.salud = salud
        self.velocidad = velocidad
        self.especie: Especie = None
        self.ataque_1: Ataque = None
        self.ataque_2: Ataque = None
        self.nombre_usuario: str = None

    def atacar(self, enemigo):
        dano_final = 0
        if self.ataque_1 is not None and self.ataque_2 is None:
            dano_final = self.calcular_dano(self.ataque_1, enemigo)

        if self.ataque_1 is not None and self.ataque_2 is not None:
            ataque_elegido = randint(1, 2)
            if ataque_elegido == 1:
                dano_final = self.calcular_dano(self.ataque_1, enemigo)
            else:
                dano_final = self.calcular_dano(self.ataque_2, enemigo)
        enemigo.salud -= dano_final

    def calcular_dano(self, ataque: Ataque, enemigo):
        dano_final = 0
        if self.especie.tipo_1.nombre == ataque.tipo.nombre or self.especie.tipo_2.nombre == ataque.tipo.nombre:
            dano_final += ((ataque.dano_base * 15) / 100)
        if enemigo.especie is not None:
            if enemigo.especie.tipo_1 is not None and enemigo.especie.tipo_2 is None:
                if ataque.tipo.nombre == enemigo.especie.tipo_1.debilidad:
                    dano_final += ((ataque.dano_base * 20) / 100)
                if ataque.tipo.nombre == enemigo.especie.tipo_1.fortaleza:
                    dano_final -= ((ataque.dano_base * 20) / 100)
            if enemigo.especie.tipo_1 is not None and enemigo.especie.tipo_2 is not None:
                if ataque.tipo.nombre == enemigo.especie.tipo_2.debilidad:
                    dano_final += ((ataque.dano_base * 20) / 100)
                if ataque.tipo.nombre == enemigo.especie.tipo_2.fortaleza:
                    dano_final -= ((ataque.dano_base * 20) / 100)
        dano_final += ataque.dano_base
        return dano_final

    def k_o(self):
        return True if self.salud <= 0 else False

    def __str__(self) -> str:
        if self.especie.tipo_2 is None and self.ataque_2 is None:
            return 'Nombre: %s\nPS: %s\nPV: %s\nTipo Primario: %s\nAtaque 1: %s\nAtaque 2: NN' \
                % (self.especie.nombre_especie, self.salud, self.velocidad,
                   self.especie.tipo_1.nombre, self.ataque_1.nombre)

        elif self.especie.tipo_2 is None and self.ataque_2 is not None:
            return 'Nombre: %s\nPS: %s\nPV: %s\nTipo Primario: %s\nAtaque 1: %s\nAtaque 2: %s' \
                % (self.especie.nombre_especie, self.salud, self.velocidad,
                   self.especie.tipo_1.nombre, self.ataque_1.nombre, self.ataque_2.nombre)

        elif self.especie.tipo_2 is not None and self.ataque_2 is None:
            return 'Nombre: %s\nPS: %s\nPV: %s\nTipo Primario: %s\nTipo Secundario: %s\nAtaque 1: %s' \
                % (self.especie.nombre_especie, self.salud, self.velocidad,
                   self.especie.tipo_1.nombre, self.especie.tipo_2.nombre, self.ataque_1.nombre)

        else:
            return 'Nombre: %s\nPS: %s\nPV: %s\nTipo Primario: %s\nTipo Secundario: %s\nAtaque 1: %s\nAtaque 2: %s' \
                % (self.especie.nombre_especie, self.salud, self.velocidad,
                   self.especie.tipo_1.nombre, self.especie.tipo_2.nombre, self.ataque_1.nombre, self.ataque_2.nombre)
