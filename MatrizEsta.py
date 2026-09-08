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