from creatura.Creatura import Creatura
from usuario.Usuario import Usuario
from especie.Especie import Especie
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
        except Exception:
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

    def obtener_usuario(self, nombre_usuario: str, contrasena: str) -> Usuario:
        try:
            self.cur.execute('SELECT * FROM usuario us WHERE us.nombre_usuario = %s and us.contrasena = %s', (nombre_usuario, contrasena))
            datos_usuario = self.cur.fetchone()
            if not datos_usuario:
                return
            usuario = Usuario(datos_usuario[0], datos_usuario[1], datos_usuario[2], datos_usuario[3], datos_usuario[4], datos_usuario[5])
            return usuario
        except Exception as e:
            print(e, 'a1')

    def buscar_especies(self, nombre_usuario: str) -> list:
        try:
            especies = []
            self.cur.execute('SELECT es.id as id_especie, es.nombre as nombre_especie, ti.id as id_tipo_1, ti2.id as id_tipo_2 FROM creatudex cr \
                INNER JOIN especie es on cr.id_especie = es.id \
                INNER JOIN tipo ti on es.id_tipo_1 = ti.id \
                LEFT JOIN tipo ti2 on es.id_tipo_2 = ti2.id \
                where cr.nombre_usuario = %s', (nombre_usuario,))
            datos_especie = self.cur.fetchall()
            
            if not datos_especie:
                return

            for d in datos_especie:
                esp = Especie(d[0], d[1], d[2])
                esp.nombre_tipo_1 = self.buscar_tipo(esp.id_tipo_1)
                if d[3] != None:
                    esp.id_tipo_2 = d[3]
                    esp.nombre_tipo_2 = self.buscar_tipo(esp.id_tipo_2)
                especies.append(esp)
            return especies
        except Exception as e:
            print(e)

    def buscar_tipo(self, id: int) -> str:
        try:
            self.cur.execute('SELECT ti.nombre FROM tipo ti WHERE ti.id = %s', (id,))
            tipo = self.cur.fetchone()
            nombre_tipo = tipo[0]
            return nombre_tipo
        except Exception as e:
            print(e)

    def obtener_cantidad_creaturas(self, nombre_usuario: str) -> int:
        try:
            self.cur.execute('SELECT count(*) from creatura cr WHERE cr.nombre_usuario = %s', (nombre_usuario,))
            cantidad = self.cur.fetchone()
            return cantidad[0]
        except Exception as e:
            print(e)

    def obtener_equipo(self, nombre_usuario: str) -> list:
        try:
            self.cur.execute('SELECT es.nombre, cr.salud, cr.velocidad, ti.nombre as nombre_tipo_1, \
                ti2.nombre as nombre_tipo_2, ata.nombre as nombre_ataque_1, ata2.nombre as nombre_ataque_2 \
                FROM creatura cr \
                INNER JOIN especie es ON cr.id_especie = es.id \
                INNER JOIN tipo ti ON es.id_tipo_1 = ti.id \
                LEFT JOIN tipo ti2 ON es.id_tipo_2 = ti2.id \
                INNER JOIN ataque ata on cr.id_ataque_1 = ata.id_ataque \
                LEFT JOIN ataque ata2 on cr.id_ataque_2 = ata2.id_ataque \
                WHERE cr.nombre_usuario = %s', (nombre_usuario,))
            equipo = []
            creaturas = self.cur.fetchall()
            if not creaturas:
                return
            for c in creaturas:
                creatura = Creatura(c[0], c[1], c[2], c[3], c[5])
                if c[4] != None:
                    creatura.nombre_tipo_2 = c[4]
                if c[6] != None:
                    creatura.nombre_ataque_2 = c[6]
                equipo.append(creatura)
            return equipo
        except Exception as e:
            print(e)

    def cantidad_peleas_totales(self, nombre_usuario: str) -> int:
        try:
            self.cur.execute('SELECT count(*) FROM estadistica WHERE nombre_usuario = %s', (nombre_usuario,))
            cantidad = self.cur.fetchone()
            return cantidad[0]
        except Exception as e:
            print(e)
    
    def cantidad_peleas_ganadas(self, nombre_usuario: str) -> int:
        try:
            self.cur.execute('SELECT count(*) FROM estadistica WHERE nombre_usuario = %s and gano_s_n = true', (nombre_usuario,))
            cantidad = self.cur.fetchone()
            return cantidad[0]
        except Exception as e:
            print(e)

    def cantidad_peleas_perdidas(self, nombre_usuario: str) -> int:
        try:
            self.cur.execute('SELECT count(*) FROM estadistica WHERE nombre_usuario = %s and gano_s_n = false', (nombre_usuario,))
            cantidad = self.cur.fetchone()
            return cantidad[0]
        except Exception as e:
            print(e)

    def obtener_especie_aleatoria(self) -> Especie:
        try:
            self.cur.execute('SELECT es.nombre, ti.nombre, ti2.nombre  FROM especie es \
                INNER JOIN tipo ti on es.id_tipo_1 = ti.id \
                LEFT JOIN tipo ti2 on es.id_tipo_2 = ti2.id \
                order by random() limit 1')
            datos_especie = self.cur.fetchone()
            if datos_especie[2] == None:
                return Especie(datos_especie[0], datos_especie[1])
            especie = Especie(datos_especie[0], datos_especie[1])
            especie.nombre_tipo_2 = datos_especie[2]
            return especie
        except Exception as e:
            print(e)