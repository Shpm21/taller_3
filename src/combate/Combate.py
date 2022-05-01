from usuario.Usuario import Usuario


class Combate:
    def __init__(self, id: int, usuario1: Usuario,
                 usuario2: Usuario):
        self.id = id
        self.usuario1 = usuario1
        self.usuario2 = usuario2
