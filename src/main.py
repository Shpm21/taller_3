from color.Color import *
from combate.Combate import Combate
from creatura.Creatura import Creatura
from especie.Especie import Especie
from estadistica.Estadistica import Estadistica
from funciones.Funciones import *
from sql.Connection import Connection
from usuario.Usuario import Usuario

from random import randint


connect = Connection()

def combate_jugadores(creatura_usuario: Creatura, creatura_oponente: Creatura) -> bool:
    print(f'{WBLUE}Creaturas en combate: {creatura_usuario.especie.nombre_especie} PS: {creatura_usuario.salud} vs {creatura_oponente.especie.nombre_especie} PS: {creatura_oponente.salud}{ENDC}')
    comienza = 1 if creatura_usuario.velocidad > creatura_oponente.velocidad else 2
    while True:
        if creatura_usuario.k_o():
            print(f'{YELLOW}{creatura_oponente.especie.nombre_especie} Ha ganado{ENDC}')
            return False
        if creatura_oponente.k_o():
            print(f'{YELLOW}{creatura_usuario.especie.nombre_especie} Ha ganado{ENDC}')
            return True
        if comienza == 1:
            creatura_usuario.atacar(creatura_oponente)
            comienza = 2
        elif comienza == 2:
            creatura_oponente.atacar(creatura_usuario)
            comienza = 1

def definir_ganador(cantidad_ganadas_jugador: int, cantidad_ganadas_oponente: int, usuario: Usuario, oponente: Usuario, combate: Combate):
    estadistica_usuario = None
    estadistica_oponente = None
    if cantidad_ganadas_jugador > cantidad_ganadas_oponente:
        print(f'{YELLOW}Felicidades {usuario.nombre_usuario} has ganado la batalla{ENDC}')
        estadistica_usuario = Estadistica(generar_id(), usuario, combate, True)
        estadistica_oponente = Estadistica(generar_id(), oponente, combate, False)
    else:
        print(f'{YELLOW}{oponente.nombre_usuario} ha ganado la batalla{ENDC}')
        estadistica_usuario = Estadistica(generar_id(), usuario, combate, False)
        estadistica_oponente = Estadistica(generar_id(), oponente, combate, True)
    if estadistica_usuario and estadistica_oponente:
        while not connect.insertar_estadistica(estadistica_usuario):
            estadistica_usuario.id = generar_id()
        while not connect.insertar_estadistica(estadistica_oponente):
            estadistica_oponente.id = generar_id()

def lucha(usuario: Usuario):
    equipo = connect.obtener_equipo(usuario.nombre_usuario)
    oponente: Usuario = connect.obtener_oponente(usuario.nombre_usuario)
    equipo_oponente = connect.obtener_equipo(oponente.nombre_usuario)
    cantidad_c_u = len(equipo)
    cantidad_c_o = len(equipo_oponente)
    cantidad_ganadas_jugador = 0
    cantidad_ganadas_oponente = 0
    if not equipo or not equipo_oponente:
        raise Exception(YELLOW + 'No se ha podido llevar a cabo la batalla debido a que uno de los jugadores no tiene creaturas capturadas' + ENDC)
    combate = Combate(generar_id, usuario, oponente)
    while not connect.insertar_combate(combate):
        combate.id = generar_id()
    print(f'{BLUE}Jugadores: {usuario.nombre_usuario} vs {oponente.nombre_usuario}{ENDC}')
    for i in range(cantidad_minima(cantidad_c_u, cantidad_c_o)):
        if combate_jugadores(equipo[i], equipo_oponente[i]):
            cantidad_ganadas_jugador += 1
        else:
            cantidad_ganadas_oponente += 1  
    definir_ganador(cantidad_ganadas_jugador, cantidad_ganadas_oponente, usuario, oponente, combate)

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
    usuario = Usuario(nombre_usuario, nombre, apellido, contrasena, fecha_de_nacimiento, edad)
    while not connect.insertar_usuario(usuario):
        nombre_usuario = input('Ingresa un nuevo nombre de usuario\nPara salir del menu de registro ingresa ''Fin''\nNombre de usuario: ')
        if nombre_usuario == 'Fin':
            return False
        usuario.nombre_usuario = nombre_usuario
    return True

def login() -> Usuario:
    nombre_usuario = input(WBLUE + 'Nombre de usuario: ' + ENDC)
    if not connect.buscar_usuario(nombre_usuario):
        raise Exception(WARNING + 'Error al iniciar sesion\nEl nombre de usuario ingresado no existe en el sistema\n' + ENDC)

    contrasena = input(WBLUE + 'Contraseña: ' + ENDC)
    usuario = connect.obtener_usuario(nombre_usuario, contrasena)
    if not usuario:
        raise Exception(WARNING + 'La contraseña ingresada es incorrecta' + ENDC)
    return usuario

def reemplazar_creatura(usuario: Usuario, creatura: Creatura) -> bool:
    equipo = connect.obtener_equipo(usuario.nombre_usuario)
    if equipo:
        for i in range(len(equipo)):
            cant = i+1
            print(f'{YELLOW}[{cant}] {equipo[i].especie.nombre_especie}{ENDC}')

        eleccion = input(WBLUE + 'Ingresa el indice de la creatura a reemplazar:\n' + ENDC)

        creatura_reemplazada = equipo[int(eleccion)-1]
        return connect.reemplazar_creatura(creatura, creatura_reemplazada.id_creatura)

def obtener_ataques(creatura: Creatura, especie: Especie):
    cantidad_ataques = randint(1,2)
    if creatura.especie.tipo_2 != None:
        if cantidad_ataques == 1:
            creatura.ataque_1 = connect.obtener_ataque_creatura(especie.tipo_1.id)
        else:
            creatura.ataque_1 = connect.obtener_ataque_creatura(especie.tipo_1.id)
            creatura.ataque_2 = connect.obtener_ataque_creatura(especie.tipo_2.id)
    else:
        creatura.ataque_1 = connect.obtener_ataque_creatura(especie.tipo_1.id)

def registrar_especie_creatura(usuario: Usuario, especie: Especie, creatura: Creatura):
    id_creatudex = generar_id()
    if connect.verificar_especie_creatudex(especie.id):
        print(f'{YELLOW}Ya tienes esta creatura registrada en tu creatudex{ENDC}')
    else:
        while not connect.registrar_en_creatudex(id_creatudex, especie.id, usuario.nombre_usuario):
            id_creatudex = generar_id()
    opcion = input(WBLUE + '¿Deseas agregarlo a tu equipo?\n[1] Agregar al equipo [2] Transferir\n' + ENDC)
    if opcion == '1':
        if connect.obtener_cantidad_creaturas(usuario.nombre_usuario) < 6:
            while not connect.registrar_creatura(creatura):
                creatura.id_creatura = generar_id()
            print(f'{YELLOW}Creatura añadida con exito al equipo{ENDC}')
        else:
            if reemplazar_creatura(usuario, creatura):
                print(f'{YELLOW}Se ha realizado un cambio en el equipo{ENDC}')            
    else:
        print(f'{YELLOW}Creatura transferida{ENDC}')

def atrapar_especie(usuario: Usuario, especie: Especie) -> None: #SIMPLIFICAR ESTE METODO
    #60% de prob de atraparlo, 40% de que huya
    probabilidad = randint(1, 100)
    if 0 < probabilidad <= 60:
        salud = randint(100,150)
        velocidad = randint(30,90)

        id_creatura = generar_id()
        creatura = Creatura(id_creatura, salud, velocidad)
        creatura.especie = especie
        creatura.nombre_usuario = usuario.nombre_usuario
        obtener_ataques(creatura, especie)
        print(f'{YELLOW}Has atrapado un {especie.nombre_especie}\nPS: {salud}\nPV: {velocidad}\nAtaques:{ENDC}')
        if creatura.ataque_2 != None:
            print(f'{WBLUE}Ataque 1:\n{creatura.ataque_1.__str__()}{ENDC}')
            print(f'{WBLUE}Ataque 2:\n{creatura.ataque_2.__str__()}{ENDC}')
        else:
            print(f'{WBLUE}Ataque 1:\n{creatura.ataque_1.__str__()}{ENDC}')
        registrar_especie_creatura(usuario, especie, creatura)
    else:
        print(f'{YELLOW}La creatura ha huido{ENDC}')

def expedicion(usuario: Usuario):
    especie = connect.obtener_especie_aleatoria()
    while True:
        print(especie.__str__())
        decision = input(WBLUE + '[1] Atrapar especie\n[2] Escapar\n[3] Salir de la expedicion\n' + ENDC)
        if decision == '1':
            atrapar_especie(usuario, especie)
            especie = connect.obtener_especie_aleatoria()
        elif decision == '2':
            especie = connect.obtener_especie_aleatoria()
        elif decision == '3':
            break
        else:
            print(f'{WARNING}La opcion ingresada no es valida{ENDC}')

def equipo_lucha(usuario: Usuario):
    equipo = connect.obtener_equipo(usuario.nombre_usuario)
    if equipo:
        #DATOS DE EQUIPO
        for e in equipo:
            print(f'{WBLUE}{e.__str__() }\n{ENDC}')
        #DATOS DE ESTADISTICAS
        print(f'{WBLUE}Cantidad de peleas en las que ha participado:{ENDC} {YELLOW}{connect.cantidad_peleas_totales(usuario.nombre_usuario)}{ENDC}')
        print(f'{WBLUE}Cantidad de peleas en las que ha ganado:{ENDC} {YELLOW}{connect.cantidad_peleas_ganadas(usuario.nombre_usuario)}{ENDC}')
        print(f'{WBLUE}Cantidad de peleas en las que ha perdido:{ENDC} {YELLOW}{connect.cantidad_peleas_perdidas(usuario.nombre_usuario)}{ENDC}')
    else:
        print(f'{YELLOW}El jugador no tiene creaturas capturadas{ENDC}')

def creatudex(usuario: Usuario):
    especies = connect.buscar_especies(usuario.nombre_usuario)
    if especies:
        for e in especies:
            print(e)
    else:
        print(f'{YELLOW}El usuario no tiene especies capturadas{ENDC}')
    print(f'{WBLUE}La cantidad de especies que ha capturado hasta el momento es de:{ENDC} {YELLOW}{connect.obtener_cantidad_creatudex(usuario)}{ENDC}')
    print(f'{WBLUE}La cantidad de especies que nos falta por descubrir es de:{ENDC} {YELLOW}{connect.obtener_cantidad_especies()}{ENDC}')

def menu_usuario(usuario: Usuario):
    print(f'{BLUE}Nombre usuario: {usuario.nombre_usuario}{ENDC}')
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
            try:
                lucha(usuario)
            except Exception as e:
                print(e)

def opciones_usuario() -> int:
    try:
        opcion =  int(input(HEADER + 'Elige una de las siguientes opciones\n' + WBLUE +'[1] Creatudex\n[2] Equipo Lucha\n[3] Expedición\n[4] Lucha\n[5] Cerrar Sesión\n' + ENDC + HEADER + 'Opción: ' + ENDC))
        return opcion
    except ValueError:
        print(f'{WARNING}La opción ingresada no es válida\n {ENDC}')

def opciones_inicio() -> int:
    try:
        opcion =  int(input(HEADER + 'Bienvenido!!\nElige una de las siguientes opciones\n' + WBLUE + '[1] Iniciar Sesion\n[2] Registrarse\n[3] Salir\n' + ENDC + HEADER + 'Opción: ' + ENDC))
        return opcion
    except ValueError:
        print(f'{WARNING}La opción ingresada no es válida\n {ENDC}')

def main():
    while True:
        opcion = opciones_inicio()
        if opcion == 3:
            break
        elif opcion == 1:
            try:
                usuario = login()
                print(f'{GREEN}Acceso correcto\n{ENDC}')
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
