import funciones
from datetime import datetime

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
    # Inicialización del sistema
    n, m = funciones.ingresotamañomatriz()
    matriz = funciones.matrizestacionamiento(n, m)
    
<<<<<<< HEAD
    # Diccionario para controlar los autos que están actualmente adentro
    # Formato: {"PATENTE": {"tipo": 1, "hora_ingreso": datetime.now(), "posicion": (x, y)}}
    vehiculos_activos = {} 
    
    # Lista de tickets históricos para usar reduce() y filter() en los reportes
=======
    vehiculos_activos = {} 
>>>>>>> Ajoaquin
    historial_tickets = [] 

    while True:
        opcion = mostrar_menu()

        if opcion == '1':
<<<<<<< HEAD
            # INGRESO DE VEHÍCULO
=======
>>>>>>> Ajoaquin
            if funciones.lugareslibres(matriz):
                patente = input("Ingrese la patente: ").upper()
                if funciones.es_patente_valida(patente):
                    if patente not in vehiculos_activos:
                        tipo = int(input("Tipo de vehículo (1, 2 o 3): "))
                        x, y = funciones.buscarespaciodisponible(matriz)
<<<<<<< HEAD
                        # Asignamos la patente (o un '1') a la matriz
                        matriz[x][y] = patente 
                        
                        # Guardamos el registro
=======
                        matriz[x][y] = patente 
                        
>>>>>>> Ajoaquin
                        vehiculos_activos[patente] = {
                            "tipo": tipo,
                            "hora_ingreso": datetime.now(),
                            "posicion": (x, y)
                        }
                        print(f"Vehículo ingresado en posición [{x}][{y}]")
                    else:
<<<<<<< HEAD
                        print("El vehículo ya se encuentra en el estacionamiento.")
                else:
                    print("Patente inválida. Verifique el formato.")
=======
                        print("El vehículo ya se encuentra adentro.")
                else:
                    print("Patente inválida.")
>>>>>>> Ajoaquin
            else:
                print("No hay lugares disponibles.")

        elif opcion == '2':
<<<<<<< HEAD
            # EGRESO DE VEHÍCULO
            patente = input("Ingrese la patente a retirar: ").upper()
            if patente in vehiculos_activos:
                datos_vehiculo = vehiculos_activos[patente]
                hora_egreso = datetime.now()
                
                # Calcular importe
                horas, total = funciones.calcular_importe(datos_vehiculo["tipo"], datos_vehiculo["hora_ingreso"], hora_egreso)
                
                # Liberar lugar en la matriz ('0' o 'libre')
                x, y = datos_vehiculo["posicion"]
                matriz[x][y] = 'libre'
                
                # Guardar en el historial para los reportes
                historial_tickets.append({"patente": patente, "importe": total, "tipo": datos_vehiculo["tipo"]})
                
                # Eliminar de activos
=======
            patente = input("Ingrese la patente a retirar: ").upper()
            if patente in vehiculos_activos:
                datos = vehiculos_activos[patente]
                hora_egreso = datetime.now()
                
                horas, total = funciones.calcular_importe(datos["tipo"], datos["hora_ingreso"], hora_egreso)
                
                x, y = datos["posicion"]
                matriz[x][y] = 'libre'
                historial_tickets.append({"patente": patente, "importe": total, "tipo": datos["tipo"]})
>>>>>>> Ajoaquin
                del vehiculos_activos[patente]
                
                print(f"Vehículo retirado. Horas: {horas}. Total a pagar: ${total}")
            else:
<<<<<<< HEAD
                print("El vehículo no se encuentra registrado.")

        elif opcion == '3':
            # MAPA DEL ESTACIONAMIENTO
            print("\nMapa actual:")
=======
                print("Vehículo no encontrado.")

        elif opcion == '3':
>>>>>>> Ajoaquin
            for fila in matriz:
                print(fila)

        elif opcion == '4':
<<<<<<< HEAD
            # BUSCAR POR PATENTE
=======
>>>>>>> Ajoaquin
            patente_buscar = input("Ingrese la patente a buscar: ").upper()
            if patente_buscar in vehiculos_activos:
                pos = vehiculos_activos[patente_buscar]["posicion"]
                print(f"El vehículo está en la fila {pos[0]}, columna {pos[1]}")
            else:
                print("Vehículo no encontrado.")

        elif opcion == '5':
<<<<<<< HEAD
            # REPORTE DE RECAUDACIÓN (Uso de filter y reduce)
            total = funciones.reporte_recaudacion_total(historial_tickets)
            cantidad = funciones.cantidad_vehiculos_atendidos(historial_tickets)
            print(f"Total recaudado históricamente: ${total}")
            print(f"Cantidad total de vehículos atendidos: {cantidad}")

        elif opcion == '6':
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida. Intente de nuevo.")

if _name_ == "_main_":
    main()
    
=======
            total = funciones.reporte_recaudacion_total(historial_tickets)
            cantidad = funciones.cantidad_vehiculos_atendidos(historial_tickets)
            print(f"Total recaudado: ${total}")
            print(f"Vehículos atendidos: {cantidad}")

        elif opcion == '6':
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
>>>>>>> Ajoaquin
