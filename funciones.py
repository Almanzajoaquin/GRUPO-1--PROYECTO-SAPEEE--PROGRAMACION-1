<<<<<<< Updated upstream
=======
import re
import reduce

def es_patente_valida(patente):
    if re.match(r"[A-Z]{2}+\d{3}+[A-Z]{2}", patente):
        return True
    elif re.match(r"[A-Z]{3}+\d{3}", patente):
        return True
    else:
        return False


def matrizestacionamiento(n, m):
    matriz = []
    for i in range(n):
        fila_nueva = []
        for j in range(m):
            fila_nueva.append('libre')
        matriz.append(fila_nueva)
    return matriz

def numeropositivo(x):
    while x <= 0:
        x = int(input("Ingrese un valor positivo: "))
    return x

def ingresotamañomatriz():
    print("Ingrese el tamaño de la matriz (mxn)")
    x = int(input("Ingrese el parametro m: "))
    x = numeropositivo(x)
    y = int(input("Ingrese el parametro n: "))
    y = numeropositivo(y)
    return x, y

def buscarespaciodisponible(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == 'libre':
                return i, j

def lugareslibres(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == 'libre':
                return True
    return False              

def guardarpatentes(matriz):
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
    if len(historial) == 0:
        return 0
    total = reduce(lambda acumulador, ticket: acumulador + ticket["importe"], historial, 0.0)
    return total

def cantidad_vehiculos_atendidos(historial):
    if len(historial) == 0:
        return 0
    lista_patentes = list(map(lambda ticket: ticket["patente"], historial))
    return len(lista_patentes)

def filtrar_por_tipo(registros, tipo):
    tipo_buscado = tipo
    resultado = list(filter(lambda item: item[1]["tipo"]== tipo_buscado, registros.items()))

    return resultado


>>>>>>> Stashed changes
