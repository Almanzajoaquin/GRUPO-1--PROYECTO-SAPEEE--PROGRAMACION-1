import re
import json
import os
from functools import reduce

TARIFAS = {
    1: 3500,
    2: 4000,
    3: 3000
}

ARCHIVO_ESTADO = "estacionamiento.json"
ARCHIVO_VIP = "clientes_vip.txt"
DESCUENTO_VIP = 0.20  # 20% de descuento para patentes adheridas al conjunto VIP

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

def matrizestacionamiento(m, n):
    '''La funcion recibe dos numeros en forma de parametros (m filas y n columnas)
    para crear una matriz de tamaño mxn. Se llena la matriz con casillas llamadas
    "libre" que representan los espacios sin usar del estacionamiento.'''
    matriz = []
    for i in range(m):
        fila_nueva = []
        for j in range(n):
            fila_nueva.append('libre')
        matriz.append(fila_nueva)
    return matriz

def ingresotamañomatriz():
    '''La funcion pide los parametros para la creacion de la matriz y tras
    verificar que esten en rango valido los devuelve.'''
    print("Ingrese el tamaño de la matriz (mxn)")
    m = pedir_entero_en_rango("Ingrese la cantidad de filas (m): ", 1, 1000)
    n = pedir_entero_en_rango("Ingrese la cantidad de columnas (n): ", 1, 1000)
    return m, n

def buscarespaciodisponible(matriz):
    '''La funcion registra la matriz desde el principio y cuando encuentra un
    espacio "libre" devuelve su ubicacion como tupla (fila, columna).'''
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == 'libre':
                return i, j
    return None

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
    return patente in vehiculos_activos

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
    vacio devuelve 0.0. Cada ticket es un diccionario {"patente", "total", "tipo"}.'''
    if len(historial) == 0:
        return 0.0
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

def calcular_importe(tipo, horaentrada, minutosentrada, horasalida, minutossalida, es_vip=False):
    '''La funcion recibe el tipo de vehiculo, los datos de hora de ingreso
    y egreso, y un booleano opcional es_vip. Calcula el tiempo de estadia y
    devuelve las horas cobradas y el total a pagar. Si la estadia es de una
    hora o menos no se cobra. Si es cliente VIP aplica un 20% de descuento.'''
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
        if es_vip:
            totalpagar = totalpagar * (1 - DESCUENTO_VIP)
        return horascobradas, totalpagar


# ── Persistencia en archivo JSON ───────────────────────────────────────

def guardar_estado(matriz, vehiculos_activos, historial, ruta=ARCHIVO_ESTADO):
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
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            estado = json.load(archivo)
        matriz = estado["matriz"]
        vehiculos_activos = estado["vehiculos_activos"]
        historial = estado["historial"]
    except FileNotFoundError:
        return None
    except (json.JSONDecodeError, KeyError, OSError):
        print("El archivo de datos está dañado. Se iniciará un estacionamiento nuevo.")
        return None

    for datos in vehiculos_activos.values():
        datos["posicion"] = tuple(datos["posicion"])
    return matriz, vehiculos_activos, historial


# ── Conjuntos (set) y Persistencia en Archivo de Texto (.txt) ──────────

def cargar_clientes_vip(ruta=ARCHIVO_VIP):
    clientes_vip = set()
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                patente = linea.strip().upper()
                if patente != "" and es_patente_valida(patente):
                    clientes_vip.add(patente)
    except FileNotFoundError:
        return set()
    except OSError:
        print("Error al leer el archivo de clientes VIP.")
        return set()
    return clientes_vip

def guardar_clientes_vip(clientes_vip, ruta=ARCHIVO_VIP):
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            for patente in sorted(clientes_vip):
                archivo.write(patente + "\n")
        return True
    except OSError:
        return False

def agregar_cliente_vip(clientes_vip, patente):
    if patente in clientes_vip:
        return False
    clientes_vip.add(patente)
    return True

def eliminar_cliente_vip(clientes_vip, patente):
    if patente in clientes_vip:
        clientes_vip.remove(patente)
        return True
    return False

def obtener_patentes_unicas(historial):
    return set(map(lambda ticket: ticket["patente"], historial))

def comparar_activos_con_vip(vehiculos_activos, clientes_vip):
    patentes_activas = set(vehiculos_activos.keys())
    activos_vip = patentes_activas & clientes_vip
    activos_regulares = patentes_activas - clientes_vip
    return activos_vip, activos_regulares

def limpiar_matriz(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            matriz[i][j] = 'libre'
    return matriz

def borrar_archivos_sistema(ruta_json=ARCHIVO_ESTADO, ruta_vip=ARCHIVO_VIP):
    '''Elimina por completo los archivos físicos del disco (JSON y TXT) para
    reiniciar el sistema desde cero en la próxima ejecución.'''
    exito = True
    try:
        if os.path.exists(ruta_json):
            os.remove(ruta_json)
    except OSError:
        exito = False
        
    try:
        if os.path.exists(ruta_vip):
            os.remove(ruta_vip)
    except OSError:
        exito = False
        
    return exito