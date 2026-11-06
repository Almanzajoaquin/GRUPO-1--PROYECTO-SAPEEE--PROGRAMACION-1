import funciones

# Diccionario de tipos de vehículos
NOMBRES_TIPO = {1: "Auto", 2: "Camioneta", 3: "Moto"}

def mostrar_menu():
    # Imprime las opciones disponibles y devuelve la seleccion del usuario
    print("\n--- SISTEMA DE GESTIÓN DE ESTACIONAMIENTO ---")
    print("1. Ingreso de vehículo")
    print("2. Egreso de vehículo")
    print("3. Ver mapa del estacionamiento (Disponibilidad)")
    print("4. Buscar vehículo por patente")
    print("5. Reporte de recaudación")
    print("6. Vehículos estacionados por tipo")
    print("7. Gestión de Clientes VIP / Convenios")
    print("8. Limpiar / Reiniciar estacionamiento (Vaciar cocheras)")
    print("9. Salir (Opción de borrado total / Fábrica)")
    return input("Seleccione una opción: ").strip()

def guardar_y_avisar(matriz, vehiculos_activos, historial_tickets):
    # Guarda el estado en el JSON y avisa solo si hubo un problema
    if not funciones.guardar_estado(matriz, vehiculos_activos, historial_tickets):
        print("Atención: no se pudieron guardar los datos.")

def iniciar_sistema():
    # Recupera los datos guardados o crea un estacionamiento nuevo
    estado = funciones.cargar_estado()
    if estado is None:
        m, n = funciones.ingresotamañomatriz()
        matriz = funciones.matrizestacionamiento(m, n)
        vehiculos_activos = {}
        historial_tickets = []
    else:
        matriz, vehiculos_activos, historial_tickets = estado
        print(f"Datos recuperados: {len(vehiculos_activos)} vehículo(s) estacionado(s) "
              f"y {len(historial_tickets)} ticket(s) en el historial.")

    clientes_vip = funciones.cargar_clientes_vip()
    print(f"Padrón VIP cargado: {len(clientes_vip)} patente(s) adherida(s).")
    return matriz, vehiculos_activos, historial_tickets, clientes_vip

# ── OPCION 1: Ingreso de vehiculo ──────────────────────────────────────
def opcion_ingreso(matriz, vehiculos_activos, historial_tickets, clientes_vip):
    if not funciones.lugareslibres(matriz):
        print("No hay lugares disponibles.")
        return

    patente = input("Ingrese la patente: ").strip().upper()
    if not funciones.es_patente_valida(patente):
        print("Patente inválida. Verifique el formato.")
        return
    if funciones.patente_registrada(vehiculos_activos, patente):
        print("El vehículo ya se encuentra en el estacionamiento.")
        return

    tipo = funciones.pedir_entero_en_rango("Tipo de vehículo Auto(1), Camioneta(2) o Moto(3): ", 1, 3)
    h_in = funciones.pedir_entero_en_rango("Ingrese la hora de entrada (0-23): ", 0, 23)
    m_in = funciones.pedir_entero_en_rango("Ingrese los minutos de entrada (0-59): ", 0, 59)

    x, y = funciones.registrar_ingreso(matriz, vehiculos_activos, patente, tipo, h_in, m_in)
    etiqueta_vip = " [CLIENTE VIP - 20% OFF]" if patente in clientes_vip else ""
    print(f"Vehículo ingresado en posición [{x}][{y}]{etiqueta_vip}")
    guardar_y_avisar(matriz, vehiculos_activos, historial_tickets)

# ── OPCION 2: Egreso de vehiculo ───────────────────────────────────────
def opcion_egreso(matriz, vehiculos_activos, historial_tickets, clientes_vip):
    patente = input("Ingrese la patente a retirar: ").strip().upper()
    if not funciones.patente_registrada(vehiculos_activos, patente):
        print("El vehículo no se encuentra registrado.")
        return

    h_out = funciones.pedir_entero_en_rango("Ingrese la hora de salida (0-23): ", 0, 23)
    m_out = funciones.pedir_entero_en_rango("Ingrese los minutos de salida (0-59): ", 0, 59)
    es_vip = patente in clientes_vip

    horas, total = funciones.registrar_egreso(matriz, vehiculos_activos, historial_tickets,
                                              patente, h_out, m_out, es_vip)
    if total == 0:
        print("Vehículo retirado. Estadía de una hora o menos: sin cargo.")
    else:
        if es_vip:
            print("¡Beneficio Cliente VIP aplicado (20% de descuento)!")
        print(f"Vehículo retirado. Horas cobradas: {horas}. Total a pagar: ${total:.2f}")
    guardar_y_avisar(matriz, vehiculos_activos, historial_tickets)

# ── OPCION 3: Ver mapa del estacionamiento ─────────────────────────────
def opcion_mapa(matriz):
    print("\nMapa actual:")
    for fila in matriz:
        print(fila)

# ── OPCION 4: Buscar vehiculo por patente ──────────────────────────────
def opcion_buscar(vehiculos_activos, clientes_vip):
    patente = input("Ingrese la patente a buscar: ").strip().upper()
    datos_vehiculo = funciones.buscar_vehiculo(vehiculos_activos, patente)
    if datos_vehiculo is None:
        print("Vehículo no encontrado.")
        return

    x, y = datos_vehiculo["posicion"]
    nombre_tipo = NOMBRES_TIPO[datos_vehiculo["tipo"]]
    hora = f"{datos_vehiculo['h_entrada']:02d}:{datos_vehiculo['m_entrada']:02d}"
    estado_vip = "Sí" if patente in clientes_vip else "No"
    print(f"El vehículo está en la fila {x}, columna {y}")
    print(f"Tipo: {nombre_tipo}. Hora de entrada: {hora}. Cliente VIP: {estado_vip}")

# ── OPCION 5: Reporte de recaudacion ───────────────────────────────────
def opcion_reporte(historial_tickets):
    total = funciones.reporte_recaudacion_total(historial_tickets)
    cantidad = funciones.cantidad_vehiculos_atendidos(historial_tickets)
    patentes_unicas = funciones.obtener_patentes_unicas(historial_tickets)

    print(f"Total recaudado históricamente: ${total:.2f}")
    print(f"Cantidad total de vehículos atendidos: {cantidad}")
    print(f"Cantidad de vehículos únicos (sin repetir patente): {len(patentes_unicas)}")
    print("\nDetalle por tipo:")
    for tipo, nombre in NOMBRES_TIPO.items():
        tickets_tipo = funciones.filtrar_por_tipo(historial_tickets, tipo)
        recaudado = funciones.reporte_recaudacion_total(tickets_tipo)
        print(f"  {nombre}: {len(tickets_tipo)} atendido(s), ${recaudado:.2f}")

# ── OPCION 6: Vehiculos estacionados por tipo ──────────────────────────
def opcion_por_tipo(vehiculos_activos):
    activos = list(vehiculos_activos.values())
    print("\nVehículos estacionados actualmente:")
    for tipo, nombre in NOMBRES_TIPO.items():
        cant = len(funciones.filtrar_por_tipo(activos, tipo))
        print(f"  {nombre}: {cant}")

# ── OPCION 7: Gestion de Clientes VIP (Conjuntos y .txt) ───────────────
def opcion_vip(vehiculos_activos, clientes_vip):
    print("\n--- GESTIÓN DE CLIENTES VIP (CONVENIOS) ---")
    print("1. Agregar patente al padrón VIP")
    print("2. Dar de baja patente del padrón VIP")
    print("3. Ver listado de patentes VIP registradas")
    print("4. Comparar vehículos estacionados ahora vs. Padrón VIP")
    sub_op = funciones.pedir_entero_en_rango("Seleccione una opción (1-4): ", 1, 4)

    if sub_op == 1:
        patente = input("Ingrese la patente a adherir al VIP: ").strip().upper()
        if not funciones.es_patente_valida(patente):
            print("Patente inválida. Verifique el formato.")
        elif not funciones.agregar_cliente_vip(clientes_vip, patente):
            print("Esa patente ya pertenece al padrón VIP.")
        elif funciones.guardar_clientes_vip(clientes_vip):
            print(f"Patente {patente} agregada al padrón VIP y guardada en {funciones.ARCHIVO_VIP}.")
        else:
            print("Error al guardar en el archivo de texto.")

    elif sub_op == 2:
        patente = input("Ingrese la patente a dar de baja del VIP: ").strip().upper()
        if not funciones.eliminar_cliente_vip(clientes_vip, patente):
            print("La patente no se encontraba en el padrón VIP.")
        elif funciones.guardar_clientes_vip(clientes_vip):
            print(f"Patente {patente} eliminada del padrón VIP.")
        else:
            print("Error al actualizar el archivo de texto.")

    elif sub_op == 3:
        if len(clientes_vip) == 0:
            print("No hay clientes VIP registrados actualmente.")
        else:
            print(f"Patentes VIP activas ({len(clientes_vip)}): {funciones.formatear_patentes(clientes_vip)}")

    else:
        activos_vip, activos_regulares = funciones.comparar_activos_con_vip(vehiculos_activos, clientes_vip)
        print(f"Estacionados actualmente que SON VIP (Intersección): {funciones.formatear_patentes(activos_vip)}")
        print(f"Estacionados actualmente NO VIP (Diferencia): {funciones.formatear_patentes(activos_regulares)}")

# ── OPCION 8: Limpiar / Reiniciar estacionamiento ──────────────────────
def opcion_limpiar(matriz, vehiculos_activos, historial_tickets):
    confirmacion = input("¿Está seguro de vaciar todo el estacionamiento? Se liberarán todas las cocheras "
                         "y se borrarán los vehículos activos (S/N): ").strip().upper()
    if confirmacion != 'S':
        print("Operación cancelada.")
        return

    funciones.limpiar_matriz(matriz)
    vehiculos_activos.clear()
    if funciones.guardar_estado(matriz, vehiculos_activos, historial_tickets):
        print("El estacionamiento ha sido limpiado y reiniciado con éxito.")
    else:
        print("Atención: no se pudieron guardar los cambios en el archivo JSON.")

# ── OPCION 9: Salir (con borrado total opcional) ───────────────────────
def opcion_salir(matriz, vehiculos_activos, historial_tickets, clientes_vip):
    # Devuelve True si el usuario confirma la salida, o False si cancela
    print("\n¡ATENCIÓN! Está por salir del sistema.")
    confirmacion = input("¿Desea BORRAR TODO EL CONTENIDO (eliminar archivos JSON, TXT e historial "
                         "por completo)? (S/N): ").strip().upper()
    if confirmacion == 'S':
        if funciones.borrar_archivos_sistema():
            print("Se han eliminado todos los archivos del sistema correctamente.")
        else:
            print("Atención: algunos archivos no se pudieron borrar.")
        print("Saliendo del sistema...")
        return True

    guardar_normal = input("¿Desea salir guardando los datos normalmente? (S/N): ").strip().upper()
    if guardar_normal != 'S':
        print("Operación cancelada. Volviendo al menú principal.")
        return False

    if funciones.guardar_estado(matriz, vehiculos_activos, historial_tickets):
        print("Datos JSON guardados correctamente.")
    if funciones.guardar_clientes_vip(clientes_vip):
        print("Padrón VIP guardado correctamente.")
    print("Saliendo del sistema...")
    return True

def main():
    # Programa principal: carga los datos y deriva cada opcion a su funcion
    matriz, vehiculos_activos, historial_tickets, clientes_vip = iniciar_sistema()

    while True:
        opcion = mostrar_menu()
        if opcion == '1':
            opcion_ingreso(matriz, vehiculos_activos, historial_tickets, clientes_vip)
        elif opcion == '2':
            opcion_egreso(matriz, vehiculos_activos, historial_tickets, clientes_vip)
        elif opcion == '3':
            opcion_mapa(matriz)
        elif opcion == '4':
            opcion_buscar(vehiculos_activos, clientes_vip)
        elif opcion == '5':
            opcion_reporte(historial_tickets)
        elif opcion == '6':
            opcion_por_tipo(vehiculos_activos)
        elif opcion == '7':
            opcion_vip(vehiculos_activos, clientes_vip)
        elif opcion == '8':
            opcion_limpiar(matriz, vehiculos_activos, historial_tickets)
        elif opcion == '9':
            if opcion_salir(matriz, vehiculos_activos, historial_tickets, clientes_vip):
                break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C / Ctrl+D: los datos ya se guardan despues de cada operacion
        print("\nPrograma interrumpido. Los datos guardados hasta el momento se conservan.")