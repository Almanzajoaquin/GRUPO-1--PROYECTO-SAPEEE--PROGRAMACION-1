import funciones

def mostrar_menu():
    print("\n--- SISTEMA DE GESTIÓN DE ESTACIONAMIENTO ---")
    print("1. Ingreso de vehículo")
    print("2. Egreso de vehículo")
    print("3. Ver mapa del estacionamiento (Disponibilidad)")
    print("4. Buscar vehículo por patente")
    print("5. Reporte de recaudación")
    print("6. Salir")
    return input("Seleccione una opción: ")

def main():
    n, m = funciones.ingresotamañomatriz()
    matriz = funciones.matrizestacionamiento(n, m)
    
    vehiculos_activos = []
    
    historial_tickets = [] 

    while True:
        opcion = mostrar_menu()

        if opcion == '1':
            if funciones.lugareslibres(matriz):
                patente = input("Ingrese la patente en mayusculas: ")
                if funciones.es_patente_valida(patente):
                    if not funciones.patente_registrada(vehiculos_activos, patente):
                        tipo = int(input("Tipo de vehículo Auto(1), Camioneta(2) o Moto(3)): "))
                        while tipo not in (1, 2, 3):
                            print("Tipo inválido. Debe ser 1, 2 o 3.")
                            tipo = int(input("Tipo de vehículo Auto(1), Camioneta(2) o Moto(3)): "))
                        
                        h_in = int(input("Ingrese la hora de entrada (0-23): "))
                        while h_in > 23 or h_in < 0:
                            print("Horario incorrecto. Ingrese un horario valido (0-23hs)")
                            h_in = int(input("Ingrese la hora de entrada (0-23): "))
                        m_in = int(input("Ingrese los minutos de entrada (0-59): "))
                        while m_in > 59 or m_in < 0:
                            print("Minutos incorrecto. Ingrese un minuto valido (0-59)")
                            m_in = int(input("Ingrese los minutos de entrada (0-59): "))
                        
                        x, y = funciones.buscarespaciodisponible(matriz)
                        matriz[x][y] = patente 
                        
                        vehiculos_activos.append([patente, tipo, h_in, m_in, x, y])
                        print(f"Vehículo ingresado en posición [{x}][{y}]")
                    else:
                        print("El vehículo ya se encuentra en el estacionamiento.")
                else:
                    print("Patente inválida. Verifique el formato.")
            else:
                print("No hay lugares disponibles.")

        elif opcion == '2':
            patente = input("Ingrese la patente a retirar: ").upper()
            datos_vehiculo = funciones.buscar_vehiculo(vehiculos_activos, patente)
            if datos_vehiculo is not None:
                
                h_out = int(input("Ingrese la hora de salida (0-23): "))
                while h_out > 23 or h_out < 0:
                    print("Horario incorrecto. Ingrese un horario valido (0-23hs)")
                    h_out = int(input("Ingrese la hora de salida (0-23): "))
                m_out = int(input("Ingrese los minutos de salida (0-59): "))
                while m_out > 59 or m_out < 0:
                    print("Horario incorrecto. Ingrese un horario valido (0-59)")
                    m_out = int(input("Ingrese los minutos de salida (0-59): "))
                
                horas, total = funciones.calcular_importe(
                    datos_vehiculo[1],   # tipo
                    datos_vehiculo[2],   # hora_ingreso
                    datos_vehiculo[3],   # minuto_ingreso
                    h_out,
                    m_out
                )
                
                x = datos_vehiculo[4]
                y = datos_vehiculo[5]
                matriz[x][y] = 'libre'
                
                historial_tickets.append([patente, total, datos_vehiculo[1]])
                
                funciones.eliminar_vehiculo(vehiculos_activos, patente)
                
                print(f"Vehículo retirado. Horas cobradas: {horas}. Total a pagar: ${total}")
            else:
                print("El vehículo no se encuentra registrado.")

        elif opcion == '3':
            print("\nMapa actual:")
            for fila in matriz:
                print(fila)

        elif opcion == '4':
            patente_buscar = input("Ingrese la patente a buscar: ")
            datos_vehiculo = funciones.buscar_vehiculo(vehiculos_activos, patente_buscar)
            if datos_vehiculo is not None:
                x = datos_vehiculo[4]
                y = datos_vehiculo[5]
                print(f"El vehículo está en la fila {x}, columna {y}")
            else:
                print("Vehículo no encontrado.")

        elif opcion == '5':
            total = funciones.reporte_recaudacion_total(historial_tickets)
            cantidad = funciones.cantidad_vehiculos_atendidos(historial_tickets)
            print(f"Total recaudado históricamente: ${total}")
            print(f"Cantidad total de vehículos atendidos: {cantidad}")

        elif opcion == '6':
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()