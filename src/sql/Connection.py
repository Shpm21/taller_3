from ataque.Ataque import Ataque
from creatura.Creatura import Creatura
from tipo.Tipo import Tipo
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
            self.cur.execute('SELECT es.id as id_especie, es.nombre as nombre_especie, ti.id as id_tipo_1, \
                ti2.id as id_tipo_2 FROM creatudex cr \
                INNER JOIN especie es on cr.id_especie = es.id \
                INNER JOIN tipo ti on es.id_tipo_1 = ti.id \
                LEFT JOIN tipo ti2 on es.id_tipo_2 = ti2.id \
                where cr.nombre_usuario = %s', (nombre_usuario,))
            datos_especie = self.cur.fetchall()
            
            if not datos_especie:
                return

            for d in datos_especie:
                esp = Especie(d[0], d[1])
                esp.tipo_1 = self.buscar_tipo(d[2])
                if d[3] != None:
                    esp.tipo_2 = self.buscar_tipo(d[3])
                especies.append(esp)
            return especies
        except Exception as e:
            print(e)

    def buscar_especie(self, id: int) -> Especie:
        try:
            self.cur.execute('SELECT * FROM especie es WHERE es.id = %s', (id,))
            datos_especie = self.cur.fetchone()
            especie = Especie(datos_especie[0], datos_especie[1])
            especie.tipo_1 = self.buscar_tipo(datos_especie[2])
            if datos_especie[3] == None:
                return especie
            especie.tipo_2 = self.buscar_tipo(datos_especie[3])
            return especie
        except Exception as e:
            print(e)

    def buscar_tipo(self, id: int) -> Tipo:
        try:
            self.cur.execute('SELECT * FROM tipo ti WHERE ti.id = %s', (id,))
            datos_tipo = self.cur.fetchone()
            tipo = Tipo(datos_tipo[0], datos_tipo[1], datos_tipo[2], datos_tipo[3])
            return tipo
        except Exception as e:
            print(e)

    def buscar_ataque(self, id_ataque: int) -> Ataque:
        try:
            self.cur.execute('SELECT * FROM ataque at WHERE at.id_ataque = %s', (id_ataque,))
            datos_ataque = self.cur.fetchone()
            ataque = Ataque(datos_ataque[0], datos_ataque[2], datos_ataque[3])
            ataque.tipo = self.buscar_tipo(datos_ataque[1])
            return ataque
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
            self.cur.execute('SELECT cr.id_creatura, cr.salud, cr.velocidad, es.id, \
                ata.id_ataque, ata2.id_ataque \
                FROM creatura cr \
                INNER JOIN especie es ON cr.id_especie = es.id \
                INNER JOIN ataque ata on cr.id_ataque_1 = ata.id_ataque \
                LEFT JOIN ataque ata2 on cr.id_ataque_2 = ata2.id_ataque \
                WHERE cr.nombre_usuario = %s', (nombre_usuario,))
            equipo = []
            creaturas = self.cur.fetchall()
            if not creaturas:
                return
            for c in creaturas:
                creatura = Creatura(c[0], c[1], c[2])
                creatura.especie = self.buscar_especie(c[3])
                creatura.ataque_1 = self.buscar_ataque(c[4])
                if c[5] != None:
                    creatura.ataque_2 = self.buscar_ataque(c[5])
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
            self.cur.execute('SELECT es.id, es.nombre, es.id_tipo_1, es.id_tipo_2 FROM especie es \
                INNER JOIN tipo ti on es.id_tipo_1 = ti.id \
                LEFT JOIN tipo ti2 on es.id_tipo_2 = ti2.id \
                order by random() limit 1')
            datos_especie = self.cur.fetchone()
            especie = Especie(datos_especie[0], datos_especie[1])
            especie.tipo_1 = self.buscar_tipo(datos_especie[2])
            if datos_especie[3] != None:
                especie.tipo_2 = self.buscar_tipo(datos_especie[3])
            return especie
        except Exception as e:
            print(e)

    def obtener_ataque_creatura(self, id_tipo: int) -> Ataque:
        try:
            self.cur.execute('SELECT id_ataque, nombre, dano_base, tipo from ataque \
                where tipo = %s \
                order by random() limit 1 ', (id_tipo,))
            datos_ataque = self.cur.fetchone()
            ataque = Ataque(datos_ataque[0], datos_ataque[1], datos_ataque[2])
            ataque.tipo = self.buscar_tipo(datos_ataque[3])
            return ataque
        except Exception as e:
            print(e)

    def verificar_especie_usuario(self, nombre_usuario: str, id_especie: int) -> bool:
        try:
            self.cur.execute('SELECT * FROM creatudex WHERE id_especie = %s and nombre_usuario = %s', (id_especie, nombre_usuario))
            datos_especie = self.cur.fetchone()
            if datos_especie:
                return True
            return False
        except Exception as e:
            print(e)

    def obtener_cantidad_creatudex(self) -> int:
        try:
            self.cur.execute('SELECT count(*) FROM creatudex')
            cantidad = self.cur.fetchone()
            return cantidad[0]
        except Exception as e:
            print(e)

    def verificar_especie_creatudex(self, id_especie) -> bool:
        try:
            self.cur.execute('SELECT * FROM creatudex WHERE id_especie = %s', (id_especie,))
            datos_especie = self.cur.fetchone()
            if datos_especie:
                return True
            return False
        except Exception as e:
            print(e)
    def registrar_en_creatudex(self, id: int, id_especie: int, nombre_usuario: str) -> bool:
        try:
            self.cur.execute('INSERT INTO creatudex (id, id_especie, nombre_usuario) VALUES (%s, %s, %s)', (id, id_especie, nombre_usuario))
            self.con.commit()
            return True
        except Exception:
            self.con.rollback()
            return False

    def registrar_creatura(self, creatura: Creatura) -> bool:
        try:
            if creatura.ataque_2 == None:
                self.cur.execute('INSERT INTO creatura (id_creatura, id_especie, id_ataque_1, nombre_usuario, salud, velocidad) \
                    VALUES (%s, %s, %s, %s, %s, %s)', (creatura.id_creatura, creatura.especie.id, creatura.ataque_1.id_ataque,
                    creatura.nombre_usuario, creatura.salud, creatura.velocidad))
            else:
                self.cur.execute('INSERT INTO creatura (id_creatura, id_especie, id_ataque_1, id_ataque_2, nombre_usuario, salud, velocidad) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s)', (creatura.id_creatura, creatura.especie.id, creatura.ataque_1.id_ataque,
                    creatura.ataque_2.id_ataque, creatura.nombre_usuario, creatura.salud, creatura.velocidad))
            self.con.commit()
            return True
        except Exception:
            self.con.rollback()
            return False

    def reemplazar_creatura(self, creatura: Creatura, id_creatura: int):
        try:
            if creatura.ataque_2 != None:
                self.cur.execute('UPDATE creatura SET id_especie = %s, id_ataque_1 = %s, id_ataque_2 = %s, salud = %s, velocidad = %s \
                    WHERE id_creatura = %s', (creatura.especie.id, creatura.ataque_1.id_ataque,
                    creatura.ataque_2.id_ataque, creatura.salud, creatura.velocidad, id_creatura))
                return True
            else:
                self.cur.execute('UPDATE creatura SET id_especie = %s, id_ataque_1 = %s, id_ataque_2 = %s, salud = %s, velocidad = %s \
                    WHERE id_creatura = %s', (creatura.especie.id, creatura.ataque_1.id_ataque,
                    'NULL', creatura.salud, creatura.velocidad, id_creatura))
                return True
        except Exception:
            return False
        
    def terminar_conexion(self):
        self.con.close()
