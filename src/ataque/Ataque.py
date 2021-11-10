from tipo.Tipo import Tipo


class Ataque:
    def __init__(self, id_ataque: int, nombre: str, dano_base: int):
        self.id_ataque = id_ataque
        self.nombre = nombre
        self.dano_base = dano_base
        self.tipo: Tipo = None

    def __str__(self):
        if self.tipo != None:
            return 'Nombre: %s\nDaño base: %s' % (self.nombre, self.dano_base)
