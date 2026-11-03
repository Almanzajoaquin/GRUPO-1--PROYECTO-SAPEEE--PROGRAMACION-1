import funciones

def mostrar_menu():
    # Imprime las opciones disponibles y devuelve la seleccion del usuario
    print("\n--- SISTEMA DE GESTIÓN DE ESTACIONAMIENTO ---")
    print("1. Ingreso de vehículo")
    print("2. Egreso de vehículo")
    print("3. Ver mapa del estacionamiento (Disponibilidad)")
    print("4. Buscar vehículo por patente")
    print("5. Reporte de recaudación")
    print("6. Salir")
    return input("Seleccione una opción: ")

def main():
    estado = funciones.cargar_estado()
    if estado is None:
        # Primera ejecucion (o archivo dañado): pedir tamaño y empezar de cero
        n, m = funciones.ingresotamañomatriz()
        matriz = funciones.matrizestacionamiento(n, m)
        vehiculos_activos = {}
        historial_tickets = []
    else:
        matriz, vehiculos_activos, historial_tickets = estado
        print(f"Datos recuperados: {len(vehiculos_activos)} vehículo(s) estacionado(s) "
              f"y {len(historial_tickets)} ticket(s) en el historial.")

    while True:
        opcion = mostrar_menu()

        # ── OPCION 1: Ingreso de vehiculo ──────────────────────────────
        if opcion == '1':
            if funciones.lugareslibres(matriz):
                patente = input("Ingrese la patente: ")
                patente = patente.upper()

                if funciones.es_patente_valida(patente):
                    if not funciones.patente_registrada(vehiculos_activos, patente):

                        # Validar tipo de vehiculo
                        tipo = funciones.pedir_entero_en_rango("Tipo de vehículo Auto(1), Camioneta(2) o Moto(3): ", 1, 3)
                        
                        # Validar hora de entrada
                        h_in = funciones.pedir_entero_en_rango("Ingrese la hora de entrada (0-23): ", 0, 23)

                        # Validar minutos de entrada
                        m_in = funciones.pedir_entero_en_rango("Ingrese los minutos de entrada (0-59): ", 0, 59)

                        # Asignar espacio en la matriz y registrar el vehiculo en el diccionario
                        # [Matías] La posicion se guarda como tupla (fila, columna)
                        posicion = funciones.buscarespaciodisponible(matriz)
                        x, y = posicion
                        matriz[x][y] = patente
                        vehiculos_activos[patente] = {
                            "tipo": tipo,
                            "h_entrada": h_in,
                            "m_entrada": m_in,
                            "posicion": posicion
                        }
                        print(f"Vehículo ingresado en posición [{x}][{y}]")
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
            patente = input("Ingrese la patente a retirar: ").upper()
            datos_vehiculo = funciones.buscar_vehiculo(vehiculos_activos, patente)

            if datos_vehiculo is not None:

                # Validar hora de salida
                h_out = int(input("Ingrese la hora de salida (0-23): "))
                while h_out > 23 or h_out < 0:
                    print("Horario incorrecto. Ingrese un horario valido (0-23hs)")
                    h_out = int(input("Ingrese la hora de salida (0-23): "))

                # Validar minutos de salida
                m_out = int(input("Ingrese los minutos de salida (0-59): "))
                while m_out > 59 or m_out < 0:
                    print("Horario incorrecto. Ingrese un horario valido (0-59)")
                    m_out = int(input("Ingrese los minutos de salida (0-59): "))

                # Calcular horas y total a pagar
                horas, total = funciones.calcular_importe(
                    datos_vehiculo["tipo"],       # tipo
                    datos_vehiculo["h_entrada"],  # hora entrada
                    datos_vehiculo["m_entrada"],  # minutos entrada
                    h_out,
                    m_out
                )

                # Liberar el espacio en la matriz
                x, y = datos_vehiculo["posicion"]  # [Matías]
                matriz[x][y] = 'libre'

                # Guardar diccionario en historial y eliminar de activos
                historial_tickets.append({
                    "patente": patente,
                    "total": total,
                    "tipo": datos_vehiculo["tipo"]
                })
                funciones.eliminar_vehiculo(vehiculos_activos, patente)

                print(f"Vehículo retirado. Horas cobradas: {horas}. Total a pagar: ${total}")
                if not funciones.guardar_estado(matriz, vehiculos_activos, historial_tickets):  # [Matías]
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
            patente_buscar = input("Ingrese la patente a buscar: ")
            datos_vehiculo = funciones.buscar_vehiculo(vehiculos_activos, patente_buscar)
            if datos_vehiculo is not None:
                x, y = datos_vehiculo["posicion"]  # [Matías]
                print(f"El vehículo está en la fila {x}, columna {y}")
            else:
                print("Vehículo no encontrado.")

        # ── OPCION 5: Reporte de recaudacion ───────────────────────────
        elif opcion == '5':
            total = funciones.reporte_recaudacion_total(historial_tickets)
            cantidad = funciones.cantidad_vehiculos_atendidos(historial_tickets)
            print(f"Total recaudado históricamente: ${total}")
            print(f"Cantidad total de vehículos atendidos: {cantidad}")

        # ── OPCION 6: Salir ────────────────────────────────────────────
        elif opcion == '6':
            # [Matías] Guardar todo antes de salir
            if funciones.guardar_estado(matriz, vehiculos_activos, historial_tickets):
                print("Datos guardados correctamente.")
            else:
                print("Atención: no se pudieron guardar los datos.")
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()