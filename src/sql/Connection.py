from usuario.Usuario import Usuario
import psycopg2

class Connection:
    def __init__(self):
        try:
            self.con = psycopg2.connect(host='localhost', database='taller_3', user='postgres', password='-V4c3x2z')
            self.cur = self.con.cursor()
        except Exception as e:
            print('No se ha podido conectar con la base de datos')

    def insertar_usuario(self, nombre_usuario: str, nombre: str, 
        apellido: str, contrasena: str, fecha_de_nacimiento: str, edad: int) -> bool:
        try:
            self.cur.execute('INSERT INTO usuario (nombre_usuario, nombre, apellido, contrasena, fecha_de_nacimiento, edad) \
                                VALUES(%s, %s, %s, %s, %s, %s)', 
                                (nombre_usuario, nombre, apellido, contrasena, fecha_de_nacimiento, edad))
            self.con.commit()
            return True
        except Exception as e:
            print('El nombre de usuario ingresado ya existe en el sistema')
            self.con.rollback()
            return False

    def buscar_usuario(self, nombre_usuario: str) -> bool:
        try:
            self.cur.execute('SELECT nombre_usuario FROM usuario us WHERE us.nombre_usuario = %s', (nombre_usuario,))
            usuario = self.cur.fetchall()
            if usuario:
                return True
            return False
        except Exception as e:
            print(e)

    def verificar_contrasena(self, nombre_usuario: str, contrasena: str) -> list:
        try:
            self.cur.execute('SELECT * FROM usuario us WHERE us.nombre_usuario = %s and us.contrasena = %s', (nombre_usuario, contrasena))
            usuario = self.cur.fetchall()
            return usuario
        except Exception as e:
            print(e)