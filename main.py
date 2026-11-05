import funciones

# Diccionario de tipos de vehículos
NOMBRES_TIPO = {1: "Auto", 2: "Camioneta", 3: "Moto"}

def mostrar_menu():
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

def main():
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

    while True:
        opcion = mostrar_menu()

        # ── OPCION 1: Ingreso de vehiculo ──────────────────────────────
        if opcion == '1':
            if funciones.lugareslibres(matriz):
                patente = input("Ingrese la patente: ").strip().upper()

                if funciones.es_patente_valida(patente):
                    if not funciones.patente_registrada(vehiculos_activos, patente):
                        tipo = funciones.pedir_entero_en_rango("Tipo de vehículo Auto(1), Camioneta(2) o Moto(3): ", 1, 3)
                        h_in = funciones.pedir_entero_en_rango("Ingrese la hora de entrada (0-23): ", 0, 23)
                        m_in = funciones.pedir_entero_en_rango("Ingrese los minutos de entrada (0-59): ", 0, 59)

                        posicion = funciones.buscarespaciodisponible(matriz)
                        x, y = posicion
                        matriz[x][y] = patente
                        vehiculos_activos[patente] = {
                            "tipo": tipo,
                            "h_entrada": h_in,
                            "m_entrada": m_in,
                            "posicion": posicion
                        }
                        es_vip = patente in clientes_vip
                        etiqueta_vip = " [CLIENTE VIP - 20% OFF]" if es_vip else ""
                        print(f"Vehículo ingresado en posición [{x}][{y}]{etiqueta_vip}")
                        if not funciones.guardar_estado(matriz, vehiculos_activos, historial_tickets):
                            print("Atención: no se pudieron guardar los datos.")
                    else:
                        print("El vehículo ya se encuentra en el estacionamiento.")
                else:
                    print("Patente inválida. Verifique el formato.")
            else:
                print("No hay lugares disponibles.")

        # ── OPCION 2: Egreso de vehiculo ───────────────────────────────
        elif opcion == '2':
            patente = input("Ingrese la patente a retirar: ").strip().upper()
            datos_vehiculo = funciones.buscar_vehiculo(vehiculos_activos, patente)

            if datos_vehiculo is not None:
                h_out = funciones.pedir_entero_en_rango("Ingrese la hora de salida (0-23): ", 0, 23)
                m_out = funciones.pedir_entero_en_rango("Ingrese los minutos de salida (0-59): ", 0, 59)

                es_vip = patente in clientes_vip

                horas, total = funciones.calcular_importe(
                    datos_vehiculo["tipo"],
                    datos_vehiculo["h_entrada"],
                    datos_vehiculo["m_entrada"],
                    h_out,
                    m_out,
                    es_vip
                )

                x, y = datos_vehiculo["posicion"]
                matriz[x][y] = 'libre'

                historial_tickets.append({
                    "patente": patente,
                    "total": total,
                    "tipo": datos_vehiculo["tipo"]
                })
                funciones.eliminar_vehiculo(vehiculos_activos, patente)

                if total == 0:
                    print("Vehículo retirado. Estadía de una hora o menos: sin cargo.")
                else:
                    if es_vip:
                        print("¡Beneficio Cliente VIP aplicado (20% de descuento)!")
                    print(f"Vehículo retirado. Horas cobradas: {horas}. Total a pagar: ${total:.2f}")
                if not funciones.guardar_estado(matriz, vehiculos_activos, historial_tickets):
                    print("Atención: no se pudieron guardar los datos.")
            else:
                print("El vehículo no se encuentra registrado.")

        # ── OPCION 3: Ver mapa del estacionamiento ─────────────────────
        elif opcion == '3':
            print("\nMapa actual:")
            for fila in matriz:
                print(fila)

        # ── OPCION 4: Buscar vehiculo por patente ──────────────────────
        elif opcion == '4':
            patente_buscar = input("Ingrese la patente a buscar: ").strip().upper()
            datos_vehiculo = funciones.buscar_vehiculo(vehiculos_activos, patente_buscar)
            if datos_vehiculo is not None:
                x, y = datos_vehiculo["posicion"]
                nombre_tipo = NOMBRES_TIPO[datos_vehiculo["tipo"]]
                hora = f"{datos_vehiculo['h_entrada']:02d}:{datos_vehiculo['m_entrada']:02d}"
                estado_vip = "Sí" if patente_buscar in clientes_vip else "No"
                print(f"El vehículo está en la fila {x}, columna {y}")
                print(f"Tipo: {nombre_tipo}. Hora de entrada: {hora}. Cliente VIP: {estado_vip}")
            else:
                print("Vehículo no encontrado.")

        # ── OPCION 5: Reporte de recaudacion ───────────────────────────
        elif opcion == '5':
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

        # ── OPCION 6: Vehiculos estacionados por tipo ──────────────────
        elif opcion == '6':
            activos = list(vehiculos_activos.values())
            print("\nVehículos estacionados actualmente:")
            for tipo, nombre in NOMBRES_TIPO.items():
                cant = len(funciones.filtrar_por_tipo(activos, tipo))
                print(f"  {nombre}: {cant}")

        # ── OPCION 7: Gestion de Clientes VIP (Conjuntos y .txt) ───────
        elif opcion == '7':
            print("\n--- GESTIÓN DE CLIENTES VIP (CONVENIOS) ---")
            print("1. Agregar patente al padrón VIP")
            print("2. Dar de baja patente del padrón VIP")
            print("3. Ver listado de patentes VIP registradas")
            print("4. Comparar vehículos estacionados ahora vs. Padrón VIP")
            sub_op = funciones.pedir_entero_en_rango("Seleccione una opción (1-4): ", 1, 4)

            if sub_op == 1:
                pat_vip = input("Ingrese la patente a adherir al VIP: ").strip().upper()
                if funciones.es_patente_valida(pat_vip):
                    if funciones.agregar_cliente_vip(clientes_vip, pat_vip):
                        if funciones.guardar_clientes_vip(clientes_vip):
                            print(f"Patente {pat_vip} agregada al padrón VIP y guardada en {funciones.ARCHIVO_VIP}.")
                        else:
                            print("Error al guardar en el archivo de texto.")
                    else:
                        print("Esa patente ya pertenece al padrón VIP.")
                else:
                    print("Patente inválida. Verifique el formato.")

            elif sub_op == 2:
                pat_vip = input("Ingrese la patente a dar de baja del VIP: ").strip().upper()
                if funciones.eliminar_cliente_vip(clientes_vip, pat_vip):
                    if funciones.guardar_clientes_vip(clientes_vip):
                        print(f"Patente {pat_vip} eliminada del padrón VIP.")
                    else:
                        print("Error al actualizar el archivo de texto.")
                else:
                    print("La patente no se encontraba en el padrón VIP.")

            elif sub_op == 3:
                if len(clientes_vip) == 0:
                    print("No hay clientes VIP registrados actualmente.")
                else:
                    print(f"Patentes VIP activas ({len(clientes_vip)}): {clientes_vip}")

            elif sub_op == 4:
                activos_vip, activos_regulares = funciones.comparar_activos_con_vip(vehiculos_activos, clientes_vip)
                print(f"Estacionados actualmente que SON VIP (Intersección): {activos_vip if activos_vip else 'Ninguno'}")
                print(f"Estacionados actualmente NO VIP (Diferencia): {activos_regulares if activos_regulares else 'Ninguno'}")

        # ── OPCION 8: Limpiar / Reiniciar estacionamiento (En memoria) ─
        elif opcion == '8':
            confirmacion = input("¿Está seguro de vaciar todo el estacionamiento? Se liberarán todas las cocheras y se borrarán los vehículos activos (S/N): ").strip().upper()
            if confirmacion == 'S':
                funciones.limpiar_matriz(matriz)
                vehiculos_activos.clear()
                if funciones.guardar_estado(matriz, vehiculos_activos, historial_tickets):
                    print("El estacionamiento ha sido limpiado y reiniciado con éxito.")
                else:
                    print("Atención: no se pudieron guardar los cambios en el archivo JSON.")
            else:
                print("Operación cancelada.")

        # ── OPCION 9: Salir con borrado total (Fábrica) ────────────────
        elif opcion == '9':
            print("\n¡ATENCIÓN! Está por salir del sistema.")
            confirmacion = input("¿Desea BORRAR TODO EL CONTENIDO (eliminar archivos JSON, TXT e historial por completo)? (S/N): ").strip().upper()
            
            if confirmacion == 'S':
                if funciones.borrar_archivos_sistema():
                    print("Se han eliminado todos los archivos del sistema correctamente.")
                else:
                    print("Atención: algunos archivos no se pudieron borrar o no existían.")
                print("Saliendo del sistema...")
                break
            else:
                guardar_normal = input("¿Desea salir guardando los datos normalmente? (S/N): ").strip().upper()
                if guardar_normal == 'S':
                    if funciones.guardar_estado(matriz, vehiculos_activos, historial_tickets):
                        print("Datos JSON guardados correctamente.")
                    if funciones.guardar_clientes_vip(clientes_vip):
                        print("Padrón VIP guardado correctamente.")
                    print("Saliendo del sistema...")
                    break
                else:
                    print("Operación cancelada. Volviendo al menú principal.")

        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()