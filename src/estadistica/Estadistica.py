from combate.Combate import Combate
from usuario.Usuario import Usuario
class Estadistica:
    def __init__(self, id: int, usuario: Usuario, combate: Combate , resultado: bool) -> None:
        self.id = id
        self.usuario = usuario
        self.combate = combate
        self.resultado = resultado