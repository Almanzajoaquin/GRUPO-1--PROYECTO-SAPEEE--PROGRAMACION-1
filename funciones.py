
import re
import reduce

def es_patente_valida(patente):
    '''Se confirma si lo ingresado coincide con el patron de patente
    nueva (AB123CD) o patente antigua (ABC123) y devuelve True si coincide
    o False si no coincide.'''
    if re.match(r"[A-Z]{2}+\d{3}+[A-Z]{2}", patente):
        return True
    elif re.match(r"[A-Z]{3}+\d{3}", patente):
        return True
    else:
        return False

def matrizestacionamiento(n, m):
    '''La funcion recibe dos numeros en forma de parametros (n y m) para crear
    una matriz de tamaño nxm. Se llena la matriz con casillas llamadas "libre"
    que representan los espacios sin usar del estacionamiento'''
    matriz = []
    for i in range(n):
        fila_nueva = []
        for j in range(m):
            fila_nueva.append('libre')
        matriz.append(fila_nueva)
    return matriz

def numeropositivo(x):
    '''La funcion recibe un numero y en caso de que sea negativo o 0 le pide
    al usuario que ingrese un valor positivo'''
    while x <= 0:
        x = int(input("Ingrese un valor positivo: "))
    return x

def ingresotamañomatriz():
    '''La funcion pide los parametros para la creacion de la matriz y tras
    verificar que sean positivos se devuelven.'''
    print("Ingrese el tamaño de la matriz (mxn)")
    x = int(input("Ingrese el parametro m: "))
    x = numeropositivo(x)
    y = int(input("Ingrese el parametro n: "))
    y = numeropositivo(y)
    return x, y

def buscarespaciodisponible(matriz):
    '''La funcion registra la matriz desde el principio y cuando encuentra un
    espacion "libre" devuelve su ubicacion en la matriz.'''
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == 'libre':
                return i, j

def lugareslibres(matriz):
    '''La funcion registra la matriz hasta encontrar un espacio "libre". En caso
    de haberlo devuelve True, de lo contrario devuelve False'''
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == 'libre':
                return True
    return False              

def guardarpatentes(matriz):
    '''La funcion recibe patentes hasta que el usuario ingrese "listo".
    Tras recibir la patente se revisa si hay espacio en la matriz. En caso de
    haberlo reemplaza el espacio libre por la patente y si no hay espacios 
    indica al usuario "No hay lugares disponibles".'''
    patente = input("Ingrese la patente o 'listo' para terminar: ")
    while patente != 'listo':
        if lugareslibres(matriz):
            x, y = buscarespaciodisponible(matriz)
            matriz[x][y] = patente
        else:
            print("No hay lugares disponibles")
        patente = input("Ingrese la patente o 'listo' para terminar: ")
    return matriz

def reporte_recaudacion_total(historial):
    '''La funcion recibe el historial de tickets y calcula la suma total
    de todos los importes registrados. En caso de que el historial este
    vacio devuelve 0.'''
    if len(historial) == 0:
        return 0
    total = reduce(lambda acumulador, ticket: acumulador + ticket["importe"], historial, 0.0)
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
    '''La funcion recibe el diccionario de registros y un tipo de vehiculo
    y devuelve una lista con todos los registros que coincidan con el tipo
    indicado.'''
    tipo_buscado = tipo
    resultado = list(filter(lambda item: item[1]["tipo"]== tipo_buscado, registros.items()))

    return resultado

    return resultado

def tipovehiculo(tipo):
    '''La funcion recibe un numero que representa el tipo de vehiculo y
    devuelve el precio por hora correspondiente. En caso de recibir un
    tipo invalido devuelve 0.'''
    if tipo == 1:
        return 3500
    elif tipo == 2:
        return 4000
    elif tipo == 3:
        return 3000
    else:
        return 0 

def calculartiempo(horaentrada, minutosentrada, horasalida, minutossalida):
    '''La funcion recibe la hora y minutos de entrada y salida de un vehiculo
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

def calcular_importe(tipo, hora_ingreso, hora_egreso):
    '''La funcion recibe el tipo de vehiculo y los objetos de hora de ingreso
    y egreso. Calcula el tiempo de estadia y devuelve las horas cobradas y el
    total a pagar. Si la estadia es de una hora o menos no se cobra. En caso
    de recibir un tipo invalido devuelve un mensaje de error.'''
    preciohora = tipovehiculo(tipo)
    
    if preciohora == 0:
        return "tipo de vehiculo invalido"

    horaentrada = hora_ingreso.hour
    minutosentrada = hora_ingreso.minute
    horasalida = hora_egreso.hour
    minutossalida = hora_egreso.minute

    minutos = calculartiempo(horaentrada, minutosentrada, horasalida, minutossalida)
    
    horasdeestadia = convertirhoras(minutos)

    if horasdeestadia <= 1:
        return 0, 0
    else:
        horascobradas = horasdeestadia
        totalpagar = horascobradas * preciohora
        return horascobradas, totalpagar
