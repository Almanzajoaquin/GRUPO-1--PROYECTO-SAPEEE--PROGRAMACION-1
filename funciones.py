import re
import json
from functools import reduce

TARIFAS = {
    1: 3500,
    2: 4000,
    3: 3000
}

ARCHIVO_ESTADO = "estacionamiento.json"

def pedir_entero_en_rango(mensaje, minimo, maximo):
    while True:
        try:
            valor = int(input(mensaje + " "))
        except ValueError:
            print("Debe ingresar un número entero.")
        else:
            if valor >= minimo and valor <= maximo:
                return valor
            print("Número fuera de rango.")

def es_patente_valida(patente):
    '''Se confirma si lo ingresado coincide con el patron de patente
    nueva (AB123CD) o patente antigua (ABC123) y devuelve True si coincide
    o False si no coincide.'''
    if re.match(r"^[A-Z]{2}\d{3}[A-Z]{2}$", patente):
        return True
    elif re.match(r"^[A-Z]{3}\d{3}$", patente):
        return True
    else:
        return False

def matrizestacionamiento(n, m):
    '''La funcion recibe dos numeros en forma de parametros (n y m) para crear
    una matriz de tamaño nxm. Se llena la matriz con casillas llamadas "libre"
    que representan los espacios sin usar del estacionamiento.'''
    matriz = []
    for i in range(n):
        fila_nueva = []
        for j in range(m):
            fila_nueva.append('libre')
        matriz.append(fila_nueva)
    return matriz

def numeropositivo(x):
    '''La funcion recibe un numero y en caso de que sea negativo o 0 le pide
    al usuario que ingrese un valor positivo.'''
    while x <= 0:
        x = int(input("Ingrese un valor positivo: "))
    return x

def ingresotamañomatriz():
    '''La funcion pide los parametros para la creacion de la matriz y tras
    verificar que sean positivos los devuelve.'''
    print("Ingrese el tamaño de la matriz (mxn)")
    x = pedir_entero_en_rango("Ingrese el parametro m: ", 1, 1000)
    y = pedir_entero_en_rango("Ingrese el parametro n: ", 1, 1000)
    return x, y

def buscarespaciodisponible(matriz):
    '''La funcion registra la matriz desde el principio y cuando encuentra un
    espacio "libre" devuelve su ubicacion en la matriz.'''
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == 'libre':
                return i, j

def lugareslibres(matriz):
    '''La funcion registra la matriz hasta encontrar un espacio "libre". En caso
    de haberlo devuelve True, de lo contrario devuelve False.'''
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == 'libre':
                return True
    return False

def patente_registrada(vehiculos_activos, patente):
    '''La funcion recibe el diccionario de vehiculos activos y una patente, y
    devuelve True si la patente ya se encuentra registrada como clave, o False
    en caso contrario.'''
    if patente in vehiculos_activos:
        return True
    return False

def buscar_vehiculo(vehiculos_activos, patente):
    '''La funcion recibe el diccionario de vehiculos activos y una patente, y
    devuelve el diccionario de datos del vehiculo si lo encuentra, o None si
    no esta registrado.'''
    return vehiculos_activos.get(patente)

def eliminar_vehiculo(vehiculos_activos, patente):
    '''La funcion recibe el diccionario de vehiculos activos y una patente, y
    elimina del diccionario el vehiculo que coincida con esa patente.'''
    if patente in vehiculos_activos:
        del vehiculos_activos[patente]

def reporte_recaudacion_total(historial):
    '''La funcion recibe el historial de tickets y calcula la suma total
    de todos los importes registrados. En caso de que el historial este
    vacio devuelve 0. Cada ticket es un diccionario {"patente", "total", "tipo"}.'''
    if len(historial) == 0:
        return 0
    total = reduce(lambda acumulador, ticket: acumulador + ticket["total"], historial, 0.0)
    return total

def cantidad_vehiculos_atendidos(historial):
    '''La funcion recibe el historial de tickets y devuelve la cantidad
    total de vehiculos atendidos extrayendo las patentes registradas.
    En caso de que el historial este vacio devuelve 0.'''
    if len(historial) == 0:
        return 0
    lista_patentes = list(map(lambda ticket: ticket["patente"], historial))
    return len(lista_patentes)

def filtrar_por_tipo(registros, tipo):
    '''La funcion recibe la lista de registros y un tipo de vehiculo
    y devuelve una lista con todos los registros que coincidan con el tipo
    indicado. Cada registro es un diccionario con la clave "tipo".'''
    resultado = list(filter(lambda vehiculo: vehiculo["tipo"] == tipo, registros))
    return resultado

def tipovehiculo(tipo):
    '''La funcion recibe un numero que representa el tipo de vehiculo y
    devuelve el precio por hora correspondiente desde el diccionario TARIFAS.
    En caso de recibir un tipo invalido devuelve 0.'''
    return TARIFAS.get(tipo, 0)

def calculartiempo(horaentrada, minutosentrada, horasalida, minutossalida):
    '''La funcion recibe hora y minutos de entrada y salida de un vehiculo
    y devuelve la diferencia en minutos entre ambos momentos. En caso de que
    la salida sea al dia siguiente ajusta el resultado sumando 1440 minutos.'''
    minutostotalentrada = (horaentrada * 60) + minutosentrada
    minutostotalsalida = (horasalida * 60) + minutossalida
    diferencia = minutostotalsalida - minutostotalentrada
    if diferencia < 0:
        diferencia = diferencia + 1440
    return diferencia

def convertirhoras(minutostotales):
    '''La funcion recibe una cantidad de minutos y devuelve la cantidad de
    horas enteras a cobrar. En caso de que queden minutos restantes se
    redondea hacia arriba sumando una hora adicional.'''
    horasenteras = minutostotales // 60
    restominutos = minutostotales % 60
    if restominutos > 0:
        return horasenteras + 1
    else:
        return horasenteras

def calcular_importe(tipo, horaentrada, minutosentrada, horasalida, minutossalida):
    '''La funcion recibe el tipo de vehiculo y los datos de hora de ingreso
    y egreso. Calcula el tiempo de estadia y devuelve las horas cobradas y el
    total a pagar. Si la estadia es de una hora o menos no se cobra. En caso
    de recibir un tipo invalido devuelve 0, 0.'''
    preciohora = tipovehiculo(tipo)
    if preciohora == 0:
        return 0, 0
    minutos = calculartiempo(horaentrada, minutosentrada, horasalida, minutossalida)
    horasdeestadia = convertirhoras(minutos)
    if horasdeestadia <= 1:
        return 0, 0
    else:
        horascobradas = horasdeestadia
        totalpagar = horascobradas * preciohora
        return horascobradas, totalpagar


# ── Persistencia en archivo JSON ───────────────────────────────────────

def guardar_estado(matriz, vehiculos_activos, historial, ruta=ARCHIVO_ESTADO):
    '''La funcion recibe la matriz, el diccionario de vehiculos activos y el
    historial de tickets, y los guarda juntos en un archivo JSON. Devuelve
    True si se pudo guardar o False si hubo un problema con el archivo.
    Las tuplas de posicion se guardan como listas, porque JSON no tiene
    un tipo tupla.'''
    estado = {
        "matriz": matriz,
        "vehiculos_activos": vehiculos_activos,
        "historial": historial
    }
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(estado, archivo, indent=4, ensure_ascii=False)
        return True
    except OSError:
        return False

def cargar_estado(ruta=ARCHIVO_ESTADO):
    '''La funcion lee el archivo JSON y devuelve una tupla
    (matriz, vehiculos_activos, historial). Si el archivo no existe (primera
    ejecucion) o esta dañado, devuelve None para que el sistema empiece
    de cero. Al recuperar, vuelve a convertir cada posicion en tupla.'''
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            estado = json.load(archivo)
        matriz = estado["matriz"]
        vehiculos_activos = estado["vehiculos_activos"]
        historial = estado["historial"]
    except FileNotFoundError:
        return None
    except (json.JSONDecodeError, KeyError):
        print("El archivo de datos está dañado. Se iniciará un estacionamiento nuevo.")
        return None

    for datos in vehiculos_activos.values():
        datos["posicion"] = tuple(datos["posicion"])
    return matriz, vehiculos_activos, historial