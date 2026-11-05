import funciones

def imprimir_resultado(nombre_func, datos, esperado, obtenido):
    print("-" * 50)
    print(f"1. Función probada: {nombre_func}")
    print(f"2. Datos utilizados: {datos}")
    print(f"3. Resultado esperado: {esperado}")
    print(f"4. Resultado obtenido: {obtenido}")
    if esperado == obtenido:
        print("5. Estado de la prueba: APROBADA")
    else:
        print("5. Estado de la prueba: NO APROBADA")
    print("-" * 50)

# ── PARTE 1: Validación de patentes ────────────────────────────
def prueba_patente_1():
    patente = "ABC123"
    esperado = True
    obtenido = funciones.es_patente_valida(patente)
    imprimir_resultado("es_patente_valida", f"'{patente}' (tradicional)", esperado, obtenido)

def prueba_patente_nueva():
    patente = "AA123BB"
    esperado = True
    obtenido = funciones.es_patente_valida(patente)
    imprimir_resultado("es_patente_valida", f"'{patente}' (nueva)", esperado, obtenido)

def prueba_patente_2():
    patente = "ABCD123"
    esperado = False
    obtenido = funciones.es_patente_valida(patente)
    imprimir_resultado("es_patente_valida", f"'{patente}' (inválida)", esperado, obtenido)

# ── PARTE 2: Patente registrada ────────────────────────────────
def prueba_registrada_1():
    vehiculos = {"AB123CD": {"tipo": 1}}
    pat = "AB123CD"
    esperado = True
    obtenido = funciones.patente_registrada(vehiculos, pat)
    imprimir_resultado("patente_registrada", f"Diccionario y patente '{pat}'", esperado, obtenido)

def prueba_registrada_2():
    vehiculos = {"AB123CD": {"tipo": 1}}
    pat = "ZZ999ZZ"
    esperado = False
    obtenido = funciones.patente_registrada(vehiculos, pat)
    imprimir_resultado("patente_registrada", f"Diccionario y patente '{pat}'", esperado, obtenido)

# ── PARTE 3: Buscar vehículo ───────────────────────────────────
def prueba_buscar_1():
    vehiculos = {"AA111BB": {"tipo": 2, "h_entrada": 10}}
    pat = "AA111BB"
    esperado = {"tipo": 2, "h_entrada": 10}
    obtenido = funciones.buscar_vehiculo(vehiculos, pat)
    imprimir_resultado("buscar_vehiculo", f"Diccionario y patente '{pat}'", esperado, obtenido)

def prueba_buscar_2():
    vehiculos = {"AA111BB": {"tipo": 2, "h_entrada": 10}}
    pat = "XX999YY"
    esperado = None  # Corregido: .get() devuelve None si no existe
    obtenido = funciones.buscar_vehiculo(vehiculos, pat)
    imprimir_resultado("buscar_vehiculo", f"Diccionario y patente '{pat}'", esperado, obtenido)

# ── PARTE 4: Cantidad de vehículos atendidos ───────────────────
def prueba_cantidad_1():
    historial = [{"patente": "A"}, {"patente": "B"}, {"patente": "C"}]
    esperado = 3
    obtenido = funciones.cantidad_vehiculos_atendidos(historial)
    imprimir_resultado("cantidad_vehiculos_atendidos", "Historial de 3 elementos", esperado, obtenido)

def prueba_cantidad_2():
    historial = []
    esperado = 0
    obtenido = funciones.cantidad_vehiculos_atendidos(historial)
    imprimir_resultado("cantidad_vehiculos_atendidos", "Historial vacío []", esperado, obtenido)

# ── PARTE 5: Filtrar por tipo ──────────────────────────────────
def prueba_filtrar_1():
    lista = [{"tipo": 1, "patente": "A"}, {"tipo": 2, "patente": "B"}, {"tipo": 1, "patente": "C"}]
    tipo_buscado = 1
    esperado = [{"tipo": 1, "patente": "A"}, {"tipo": 1, "patente": "C"}]
    obtenido = funciones.filtrar_por_tipo(lista, tipo_buscado)
    imprimir_resultado("filtrar_por_tipo", f"Lista con elementos y tipo {tipo_buscado}", esperado, obtenido)

def prueba_filtrar_2():
    lista = [{"tipo": 1, "patente": "A"}, {"tipo": 2, "patente": "B"}]
    tipo_buscado = 3
    esperado = []
    obtenido = funciones.filtrar_por_tipo(lista, tipo_buscado)
    imprimir_resultado("filtrar_por_tipo", f"Lista sin tipo {tipo_buscado}", esperado, obtenido)

# ── PARTE 6: Recaudación total (reduce) ────────────────────────
def prueba_recaudacion_total():
    historial = [{"patente": "A", "total": 3500.0}, {"patente": "B", "total": 4000.0}]
    esperado = 7500.0
    obtenido = funciones.reporte_recaudacion_total(historial)
    imprimir_resultado("reporte_recaudacion_total", "Historial con $3500 y $4000", esperado, obtenido)


def ejecutar_todas_las_pruebas():
    print("\n========== INICIO DE PRUEBAS UNITARIAS ==========")
    prueba_patente_1()
    prueba_patente_nueva()
    prueba_patente_2()
    prueba_registrada_1()
    prueba_registrada_2()
    prueba_buscar_1()
    prueba_buscar_2()
    prueba_cantidad_1()
    prueba_cantidad_2()
    prueba_filtrar_1()
    prueba_filtrar_2()
    prueba_recaudacion_total()
    print("==================================================\n")


if __name__ == "__main__":
    ejecutar_todas_las_pruebas()