from sql.Connection import Connection
from usuario.Usuario import Usuario
connect = Connection()


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

def registro_usuario() -> bool: #CAMBIAR ESTO
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

def login():
    nombre_usuario = input('Nombre de usuario: ')
    if not connect.buscar_usuario(nombre_usuario):
        raise Exception('Error al iniciar sesion\nEl nombre de usuario ingresado no existe en el sistema\n')

    contrasena = input('Contraseña: ')
    datos_usuario = connect.verificar_contrasena(nombre_usuario, contrasena)
    if datos_usuario:
        for u in datos_usuario:
            usuario = Usuario(u[0], u[1], u[2], u[3], u[4], u[5])
        return usuario

    raise Exception('Error al iniciar sesion\nLa contraseña ingresada es incorrecta\n')

def menu_inicio() -> int:
    try:
        opcion =  int(input('Bienvenido!!\nElige una de las siguientes opciones\n[1] Iniciar Sesion\n[2] Registrarse\n[3] Salir\n'))
        return opcion
    except ValueError:
        print('La opcion ingresada no es valida\n')

def main():
    while True:
        opcion = menu_inicio()
        if opcion == 3:
            break
        elif opcion == 1:
            try:
                usuario = login()
                print('Acceso correcto')
            except Exception as e:
                print(e)
        elif opcion == 2:
            if registro_usuario():
                print('Se ha registrado correctamente')
            else:
                print('No se ha podido registrar')
    
main()