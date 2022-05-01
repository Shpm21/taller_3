from ataque.Ataque import Ataque
from combate.Combate import Combate
from creatura.Creatura import Creatura
from estadistica.Estadistica import Estadistica
from tipo.Tipo import Tipo
from usuario.Usuario import Usuario
from especie.Especie import Especie
import psycopg2


class Connection:
    def __init__(self):
        try:
            self.con = psycopg2.connect(host='localhost', database='fakemon-db', user='postgres', password='-V4c3x2z1')
            self.cur = self.con.cursor()
        except Exception:
            print('No se ha podido conectar con la base de datos')

    def insertar_usuario(self, usuario: Usuario) -> bool:
        """Inserta un usuario en la base de datos.

        Parameters
        ----------
        usuario: `Usuario`
            Usuario el cual sera insertado en la base de datos.
        Returns
        -------
        `True`
            Si el usuario fue insertado.
        `False`
            Si el nombre de usuario ya existe en la base de datos.

        """
        try:
            self.cur.execute('INSERT INTO usuario (nombre_usuario, nombre, apellido, contrasena, fecha_de_nacimiento, edad) \
                                VALUES(%s, %s, %s, %s, %s, %s)', 
                                (usuario.nombre_usuario, usuario.nombre, usuario.apellido, usuario.contrasena, usuario.fecha_de_nacimiento, usuario.edad))
            self.con.commit()
            return True
        except Exception:
            print('El nombre de usuario ingresado ya existe en el sistema')
            self.con.rollback()
            return False

    def buscar_usuario(self, nombre_usuario: str) -> bool:
        """Busca si existe un usuario en la base de datos en base a un nombre de usuario.
        
        Parameters
        ----------
        nombre_usuario: `str`
            Nombre del usuario el cual se buscara en la base de datos.
        
        Returns
        -------
        `True`
            Si el usuario existe en la base de datos.
        `False`
            Si el usuario no existe en la base de datos.
        """

        try:
            self.cur.execute('SELECT nombre_usuario FROM usuario us WHERE us.nombre_usuario = %s', (nombre_usuario,))
            usuario = self.cur.fetchall()
            if usuario:
                return True
            return False
        except Exception as e:
            print(e)

    def obtener_usuario(self, nombre_usuario: str, contrasena: str) -> Usuario:
        """Obtiene un usuario desde la base de datos asociados al nombre de usuario y contraseña.
        
        Parameters
        ----------
        nombre_usuario: `str`
            Nombre del usuario que se buscara en la base de datos.
        contrasena: `str`
            Contraseña del usuario que se buscara en la base de datos.

        Returns
        -------
        usuario: `Usuario`
            Usuario encontrado en la base de datos.

        """
        try:
            self.cur.execute('SELECT * FROM usuario us WHERE us.nombre_usuario = %s and us.contrasena = %s', (nombre_usuario, contrasena))
            datos_usuario = self.cur.fetchone()
            if not datos_usuario:
                return
            usuario = Usuario(datos_usuario[0], datos_usuario[1], datos_usuario[2], datos_usuario[3], datos_usuario[4], datos_usuario[5])
            return usuario
        except Exception as e:
            print(e)

    def buscar_especies(self, nombre_usuario: str) -> list:
        """Obtiene las especies que ha capturado el usuario en base a un nombre de usuario.
        
        Parameters
        ----------
        nombre_usuario: `str`
            Nombre del usuario al cual le pertenecen las especies.
        
        Returns
        -------
        especies: `list[Especie]`
            Lista con las especies que le pertenecen al usuario.

        """
        try:
            especies = []
            self.cur.execute('SELECT es.id as id_especie, es.nombre as nombre_especie, ti.id as id_tipo_1, \
                ti2.id as id_tipo_2 FROM creatudex cr \
                INNER JOIN especie es on cr.id_especie = es.id \
                INNER JOIN tipo ti on es.id_tipo_1 = ti.id \
                LEFT JOIN tipo ti2 on es.id_tipo_2 = ti2.id \
                where cr.nombre_usuario = %s', (nombre_usuario,))
            datos_especie = self.cur.fetchall()
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
        """Obtiene una especie desde la base de datos en base a un id.

        Parameters
        ----------
        id: `int`
            Id perteneciente a una especie que se buscara en la base de datos.
        
        Returns
        -------
        especie: `Especie`
            Especie encontrada perteneciente al id.

        """
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
        """Obtiene un tipo especifico desde la base de datos en base a un id.
        
        Parameters
        ----------
        id: `int`
            Id perteneciente a un tipo buscado.

        Returns
        -------
        tipo: `Tipo`
            Tipo encontrado perteneciente al id.
        
        """
        try:
            self.cur.execute('SELECT * FROM tipo ti WHERE ti.id = %s', (id,))
            datos_tipo = self.cur.fetchone()
            tipo = Tipo(datos_tipo[0], datos_tipo[1], datos_tipo[2], datos_tipo[3])
            return tipo
        except Exception as e:
            print(e)

    def buscar_ataque(self, id_ataque: int) -> Ataque:
        """Obtiene un ataque especifico desde la base de datos en base a un id.
        
        Parameters
        ----------
        id_ataque: `int`
            Id perteneciente a un ataque que se buscara en la base de datos.
        
        Returns
        -------
        ataque: `Ataque`
            Ataque encontrado perteneciente al id.
        
        """
        try:
            self.cur.execute('SELECT * FROM ataque at WHERE at.id_ataque = %s', (id_ataque,))
            datos_ataque = self.cur.fetchone()
            ataque = Ataque(datos_ataque[0], datos_ataque[2], datos_ataque[3])
            ataque.tipo = self.buscar_tipo(datos_ataque[1])
            return ataque
        except Exception as e:
            print(e)

    def obtener_cantidad_creaturas(self, nombre_usuario: str) -> int:
        """Obtiene la cantidad de creaturas de un usuario en base a un nombre de usuario.
        
        Parameters
        ----------
        nombre_usuario: `str`
            Nombre del usuario el cual se le buscara la cantidad de creaturas en la base de datos.
        
        Returns
        -------
        cantidad: `int`
            Cantidad de creaturas que tiene el usuario.

        """
        try:
            self.cur.execute('SELECT count(*) from creatura cr WHERE cr.nombre_usuario = %s', (nombre_usuario,))
            cantidad = self.cur.fetchone()[0]
            return cantidad
        except Exception as e:
            print(e)

    def obtener_equipo(self, nombre_usuario: str) -> list:
        """Obtiene una lista de creaturas (equipo) correspondiente a un usuario en base a un nombre de usuario.
        
        Parameters
        ----------
        nombre_usuario: `str`
            Nombre del usuario el cual se le buscara las creaturas.
        Returns
        -------
        equipo: `list[Creatura]`
            Lista de creaturas del usuario.
        
        """
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
            if creaturas:
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
        """Obtiene la cantidad de peleas totales de un usuario en base a un nombre de usuario.
        
        Parameters
        ----------
        nombre_usuario: `str`
            Nombre del usuario el cual se le buscara la cantidad de peleas totales.

        Returns
        -------
        cantidad: `int`
            Cantidad de peleas totales que tiene el usuario.

        """
        try:
            self.cur.execute('SELECT count(*) FROM estadistica WHERE nombre_usuario = %s', (nombre_usuario,))
            cantidad = self.cur.fetchone()
            return cantidad[0]
        except Exception as e:
            print(e)
    
    def cantidad_peleas_ganadas(self, nombre_usuario: str) -> int:
        """Obtiene la cantidad de peleas ganadas de un usuario en base a un nombre de usuario.
        
        Parameters
        ----------
        nombre_usuario: `str`
            Nombre del usuario el cual se le buscara la cantidad de peleas ganadas.

        Returns
        -------
        cantidad: `int`
            Cantidad de peleas ganadas que tiene el usuario.

        """
        try:
            self.cur.execute('SELECT count(*) FROM estadistica WHERE nombre_usuario = %s and gano_s_n = true', (nombre_usuario,))
            cantidad = self.cur.fetchone()[0]
            return cantidad
        except Exception as e:
            print(e)

    def cantidad_peleas_perdidas(self, nombre_usuario: str) -> int:
        """Obtiene la cantidad de peleas perdidas de un usuario en base a un nombre de usuario.
        
        Parameters
        ----------
        nombre_usuario: `str`
            Nombre del usuario el cual se le buscara la cantidad de peleas perdidas.

        Returns
        -------
        cantidad: `int`
            Cantidad de peleas perdidas que tiene el usuario.
            
        """
        try:
            self.cur.execute('SELECT count(*) FROM estadistica WHERE nombre_usuario = %s and gano_s_n = false', (nombre_usuario,))
            cantidad = self.cur.fetchone()[0]
            return cantidad
        except Exception as e:
            print(e)

    def obtener_especie_aleatoria(self) -> Especie:
        """Obtiene una especie aleatoria desde la base de datos.

        Returns
        -------
        especie: `Especie`
            Especie aleatoria.
        
        """
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
        """Obtiene un ataque aleatorio desde la base de datos en base a un tipo.

        Parameters
        ----------
        id_tipo: `int`
            Id del tipo de creatura buscada en la base de datos.
        
        Returns
        -------
        ataque: `Ataque`
            Ataque encontrado correspondiente al id.
        
        """
        try:
            self.cur.execute('SELECT id_ataque, nombre, dano_base, tipo FROM ataque \
                WHERE tipo = %s \
                ORDER BY random() limit 1 ', (id_tipo,))
            datos_ataque = self.cur.fetchone()
            ataque = Ataque(datos_ataque[0], datos_ataque[1], datos_ataque[2])
            ataque.tipo = self.buscar_tipo(datos_ataque[3])
            return ataque
        except Exception as e:
            print(e)

    def obtener_cantidad_especies(self) -> int:
        """Obtiene la cantidad total de especies registradas en la base de datos.
        
        Returns
        -------
        cantidad: `int`
            Cantidad de especies totales en la base de datos.
        
        """
        try:
            self.cur.execute('SELECT count(*) FROM especie')
            cantidad = self.cur.fetchone()[0]
            return cantidad
        except Exception as e:
            print(e)

    def obtener_cantidad_creatudex(self, usuario: Usuario) -> int:
        """Obtiene la cantidad de especies que ha descubierto un usuario.

        Parameters
        ----------
        usuario: `Usuario`
            Usuario del sistema.

        Returns
        -------
        cantidad: `int`
            Cantidad de creaturas registradas en la creatudex del usuario.

        """
        try:
            self.cur.execute('SELECT count(*) FROM creatudex WHERE nombre_usuario = %s', (usuario.nombre_usuario,))
            cantidad = self.cur.fetchone()[0]
            return cantidad
        except Exception as e:
            print(e)

    def verificar_especie_creatudex(self, id_especie: int) -> bool:
        """Verifica que una especie ya este registrada en la creatudex.
        
        Parameters
        ----------
        id_especie: `int`
            Id de la especie que se buscara en la base de datos.
        
        Returns
        -------
        `True`
            Si la especie ya esta registrada.
        `False`
            Si la especie no esta registrada
        
        """
        try:
            self.cur.execute('SELECT * FROM creatudex WHERE id_especie = %s', (id_especie,))
            datos_especie = self.cur.fetchone()
            if datos_especie:
                return True
            return False
        except Exception as e:
            print(e)

    def registrar_en_creatudex(self, id: int, id_especie: int, nombre_usuario: str) -> bool:
        """Registra una especie en la creatudex de un usuario.

        Parameters
        ----------
        id: `int`
            Id correspondiente al registro.
        id_especie: `int` 
            Id correspondiente a la especie que se registrara.
        nombre_usuario: `str` 
            Nombre del usuario al cual le pertenece la creatudex.

        Returns
        -------
        `True`
            Si la especie se registró con éxito.
        `False`
            Si la especie no se registró.
        
        """        
        try:
            self.cur.execute('INSERT INTO creatudex (id, id_especie, nombre_usuario) VALUES (%s, %s, %s)', (id, id_especie, nombre_usuario))
            self.con.commit()
            return True
        except Exception:
            self.con.rollback()
            return False

    def registrar_creatura(self, creatura: Creatura) -> bool:
        """Registra una creatura en la base de datos.

        Parameters
        ----------
        creatura: `Creatura`
            Creatura que sera registrada en la base de datos.

        Returns
        -------
        `True`
            Si la creatura se registró.
        `False`
            Si la creatura no se registró.
        
        """

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
        """Reemplaza una creatura capturada por otra.
        
        Parameters
        ----------
        creatura: `Creatura`
            Creatura la cual reemplazara a otra.
        id_creatura: `int`
            Id de la creatura que será reemplazada.
        
        Returns
        -------
        `True`
            Si la creatura se reemplazo con éxito.
        `False`
            Si la cretura no se remplazo con éxito.
        
        """
        try:
            if creatura.ataque_2 != None:
                self.cur.execute('UPDATE creatura SET id_especie = %s, id_ataque_1 = %s, id_ataque_2 = %s, salud = %s, velocidad = %s \
                    WHERE id_creatura = %s', (creatura.especie.id, creatura.ataque_1.id_ataque,
                    creatura.ataque_2.id_ataque, creatura.salud, creatura.velocidad, id_creatura))
                return True
            else:
                self.cur.execute('UPDATE creatura SET id_especie = %s, id_ataque_1 = %s, salud = %s, velocidad = %s \
                    WHERE id_creatura = %s', (creatura.especie.id, creatura.ataque_1.id_ataque, creatura.salud, creatura.velocidad, id_creatura))
                return True
        except Exception:
            return False
        
    def obtener_oponente(self, nombre_usuario: str):
        """Obtiene un oponente aleatorio desde la base de datos.
        
        Parameters
        ----------
        nombre_usuario: `str`
            Usuario que ya esta jugando, por lo tanto no se puede obtener el.

        Returns
        -------
        usuario: `Usuario`
            Oponente desde la base de datos.

        """
        try:
            self.cur.execute('SELECT * FROM usuario \
                WHERE nombre_usuario != %s \
                ORDER BY random() limit 1 ', (nombre_usuario,))
            datos_usuario = self.cur.fetchone()
            if not datos_usuario:
                return
            usuario = Usuario(datos_usuario[0], datos_usuario[1], datos_usuario[2], datos_usuario[3], datos_usuario[4], datos_usuario[5])
            return usuario
        except Exception as e:
            print(e)

    def insertar_combate(self, combate: Combate) -> bool:
        """Inserta un combate a la base de datos.
        
        Parameters
        ----------
        combate: `Combate`
            Combate que se registrará en la base de datos.

        Returns
        -------
        `True`
            Si el combate se registro con éxito.
        `False`
            Si el combate no se registro.

        """
        try:
            self.cur.execute('INSERT INTO combate (id_combate, nombre_usuario_1, nombre_usuario_2) VALUES (%s, %s, %s)', (combate.id, combate.usuario1.nombre_usuario, combate.usuario2.nombre_usuario))
            self.con.commit()
            return True
        except Exception:
            self.con.rollback()
            return False

    def insertar_estadistica(self, estadistica: Estadistica) -> bool:
        """Insera la estadística de un combate a la base de datos.
        
        Parameters
        ----------
        estadistica: `Estadística`
            Estadistica de un combate.
            
        Returns
        -------
        `True`
            Si la estadística se registro con éxito.
        `False`
            Si la estadística no se registro.

        """
        try:
            self.cur.execute('INSERT INTO estadistica (id_estadistica, nombre_usuario, id_combate, gano_s_n) \
            VALUES (%s, %s, %s, %s)', (estadistica.id, estadistica.usuario.nombre_usuario, estadistica.combate.id, estadistica.resultado))
            self.con.commit()
            return True
        except Exception:
            self.con.rollback()
            return False

    def terminar_conexion(self):
        """Termina la conexión con la base de datos."""
        self.con.close()
