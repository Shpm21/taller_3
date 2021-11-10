from especie.Especie import Especie
from sql.Connection import Connection
from usuario.Usuario import Usuario
from creatura.Creatura import Creatura
from random import randint
connect = Connection()


def generar_id() -> int:
    n1 = str(randint(1,100))
    n2 = str(randint(1,100))
    n3 = str(randint(1,100))
    return int(n1+n2+n3)

def validar_fecha(fecha_de_nacimiento: str) -> bool:
    valido = True
    fecha = fecha_de_nacimiento.split('/')
    if len(fecha) == 3:
        dia = int(fecha[0])
        mes = int(fecha[1])
        if dia <= 31 and dia > 0 and mes > 0 and mes <= 12:
            valido = True
        else:
            valido = False
    else:
        valido = False
    return valido

def registro_usuario() -> bool:
    nombre_usuario = input('Para salir del menu de registro ingresa ''Fin''\nNombre de usuario: ')
    if nombre_usuario == 'Fin':
        return False
    nombre = input('Nombre: ')
    apellido = input('Apellido: ')
    contrasena = input('Contraseña: ')
    fecha_de_nacimiento = input('Fecha de nacimiento (DD/MM/AA): ')
    while not validar_fecha(fecha_de_nacimiento):
        fecha_de_nacimiento = input('La fecha ingresada es incorrecta, ingresa nuevamente\nFecha de nacimiento (DD/MM/AA): ')

    edad = int(input('Edad: '))
    while not connect.insertar_usuario(nombre_usuario, nombre, apellido, contrasena, fecha_de_nacimiento, edad):
        nombre_usuario = input('Ingresa un nuevo nombre de usuario\nPara salir del menu de registro ingresa ''Fin''\nNombre de usuario: ')
        if nombre_usuario == 'Fin':
            return False
    return True

def login() -> Usuario:
    nombre_usuario = input('Nombre de usuario: ')
    if not connect.buscar_usuario(nombre_usuario):
        raise Exception('Error al iniciar sesion\nEl nombre de usuario ingresado no existe en el sistema\n')

    contrasena = input('Contraseña: ')
    usuario = connect.obtener_usuario(nombre_usuario, contrasena)
    if not usuario:
        raise Exception('La contraseña ingresada es incorrecta')
    return usuario


def reemplazar_creatura(usuario: Usuario, creatura: Creatura) -> bool:
    equipo = connect.obtener_equipo(usuario.nombre_usuario)
    if equipo:
        #DATOS DE EQUIPO
        for i in range(len(equipo)):
            cant = i+1
            print(f'[{cant}] {equipo[i].especie.nombre_especie}')
        eleccion = input('Ingresa el indice de la creatura a reemplazar:\n')
        creatura_reemplazada = equipo[int(eleccion)-1]
        return connect.reemplazar_creatura(creatura, creatura_reemplazada.id_creatura)

def atrapar_especie(usuario: Usuario, especie: Especie) -> None: #SIMPLIFICAR ESTE METODO
    #60% de prob de atraparlo, 40% de que huya
    probabilidad = randint(1, 100)
    if 0 < probabilidad <= 60:
        salud = randint(100,150)
        velocidad = randint(30,90)
        cantidad_ataques = randint(1,2)
        id_creatura = generar_id()
        creatura = Creatura(id_creatura, salud, velocidad)
        creatura.especie = especie
        creatura.nombre_usuario = usuario.nombre_usuario
        if creatura.especie.tipo_2 != None:
            if cantidad_ataques == 1:
                creatura.ataque_1 = connect.obtener_ataque_creatura(especie.tipo_1.id)
            else:
                creatura.ataque_1 = connect.obtener_ataque_creatura(especie.tipo_1.id)
                creatura.ataque_2 = connect.obtener_ataque_creatura(especie.tipo_2.id)
        else:
            creatura.ataque_1 = connect.obtener_ataque_creatura(especie.tipo_1.id)
        #ACA QUEDE
        print(f'Has atrapado un {especie.nombre_especie}\nPS: {salud}\nPV: {velocidad}\nAtaques:')
        if creatura.ataque_2 != None:
            print(f'Ataque 1:\n{creatura.ataque_1.__str__()}')
            print(f'Ataque 2:\n{creatura.ataque_2.__str__()}')
        else:
            print(f'Ataque 1:\n{creatura.ataque_1.__str__()}')

        id_creatudex = generar_id()
        if connect.verificar_especie_creatudex(especie.id):
            print('Ya tienes esta creatura registrada en tu creatudex')
        else:
            while not connect.registrar_en_creatudex(id_creatudex, especie.id, usuario.nombre_usuario):
                id_creatudex = generar_id()
        opcion = input('¿Deseas agregarlo a tu equipo?\n[1] Agregar al equipo [2] Transferir\n')
        if opcion == '1':
            if connect.obtener_cantidad_creaturas(usuario.nombre_usuario) < 6:
                while not connect.registrar_creatura(creatura):
                    creatura.id_creatura = generar_id()
            else:
                if reemplazar_creatura(usuario, creatura):
                    print('Se ha realizado un cambio en el equipo')            
            print('Creatura añadida con exito al equipo')
        else:
            print('Creatura transferida')
    else:
        print('La creatura ha huido')

def expedicion(usuario: Usuario):
    especie = connect.obtener_especie_aleatoria()
    while True:
        print(especie.__str__())
        decision = input('[1] Atrapar especie\n[2] Escapar\n[3] Salir de la expedicion\n')
        if decision == '1':
            atrapar_especie(usuario, especie)
            especie = connect.obtener_especie_aleatoria()
        elif decision == '2':
            especie = connect.obtener_especie_aleatoria()
        elif decision == '3':
            break
        else:
            print('La opcion ingresada no es valida')

def equipo_lucha(usuario: Usuario):
    try:
        equipo = connect.obtener_equipo(usuario.nombre_usuario)
        if equipo:
            #DATOS DE EQUIPO
            for e in equipo:
                print(e.__str__() + '\n')
            #DATOS DE ESTADISTICAS
            print(f'Cantidad de peleas en las que ha participado: {connect.cantidad_peleas_totales(usuario.nombre_usuario)}')
            print(f'Cantidad de peleas en las que ha ganado: {connect.cantidad_peleas_ganadas(usuario.nombre_usuario)}')
            print(f'Cantidad de peleas en las que ha perdido: {connect.cantidad_peleas_perdidas(usuario.nombre_usuario)}')
    except Exception as e:
        print(e)

def creatudex(usuario: Usuario):
    especies = connect.buscar_especies(usuario.nombre_usuario)
    if especies:
        for e in especies:
            print(e)
    else:
        print('El usuario no tiene especies capturadas')

def menu_usuario(usuario: Usuario):
    print(f'Nombre usuario: {usuario.nombre_usuario}')
    while True:
        opcion = opciones_usuario()
        if opcion == 5:
            break
        if opcion == 1:
            creatudex(usuario)
        if opcion == 2:
            equipo_lucha(usuario)
        if opcion == 3:
            expedicion(usuario)
        if opcion == 4:
            pass

def opciones_usuario() -> int:
    try:
        opcion =  int(input('Elige una de las siguientes opciones\n[1] Creatudex\n[2] Equipo Lucha\n[3] Expedición\n[4] Lucha\n[5] Cerrar Sesión\n'))
        return opcion
    except ValueError:
        print('La opcion ingresada no es valida\n')

def opciones_inicio() -> int:
    try:
        opcion =  int(input('Bienvenido!!\nElige una de las siguientes opciones\n[1] Iniciar Sesion\n[2] Registrarse\n[3] Salir\n'))
        return opcion
    except ValueError:
        print('La opcion ingresada no es valida\n')

def main():
    while True:
        opcion = opciones_inicio()
        if opcion == 3:
            break
        elif opcion == 1:
            try:
                usuario = login()
                print('Acceso correcto\n')
                menu_usuario(usuario)
            except Exception as e:
                print(e)
        elif opcion == 2:
            if registro_usuario():
                print('Se ha registrado correctamente')
            else:
                print('No se ha podido registrar')
    connect.terminar_conexion()
    
main()
