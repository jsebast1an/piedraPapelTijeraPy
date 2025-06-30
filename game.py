# Juego Piedra, Papel o Tijeras con lógica de comparación
# Importación de librerías necesarias
import sys # Proporciona acceso a funciones y variables del sistema, como la entrada estándar
import random  # Para la elección aleatoria de la computadora
import getpass  # Para ocultar la entrada en modo multijugador
import threading  # Para implementar el temporizador
import time  # Para manejar las pausas del temporizador

# Variables para estadísticas
estadisticas = {
    "total_partidas": 0, # Número total de partidas jugadas
    "jugador_1_ganadas": 0, # Veces que ha ganado el jugador 1
    "jugador_2_ganadas": 0, # Veces que ha ganado el jugador 2
    "computadora_ganadas": 0, # Veces que ha ganado la computadora esto para cuando se juega en modo solo
    "empates": 0, #número de empates
    "historico": [] # Lista que almacena el historial de todas las partidas jugadas
}

def mostrar_menu(): # Esta función se creó para que el usuario pueda ver la primera interacción y decidir que hacer. Esta sería la función principal.
    """Muestra el menú principal del juego y captura la elección del usuario"""
    while True: # Se mantiene el bucle hasta que el jugador escoja la opción 5 y pueda salir
        print("\n🎮 Bienvenido al Juego: Piedra, Papel o Tijeras 🎮")
        print("1. Jugar solo (contra la computadora)")
        print("2. Modo multijugador (2 jugadores)")
        print("3. Reglas")
        print("4. Ver estadísticas")
        print("5. Salir")

        opcion = input("Seleccione una opción (1-5): ") # Se utilizó input para que el usuario pueda seleccionar una opción.
# Se dirige a la función correspondiente, dependiendo de que opción se escoja
        if opcion == "1":
            mostrar_reglas() # Se muestran las reglas antes de comenzar el juego
            jugar_contra_pc()
        elif opcion == "2":
            mostrar_reglas()
            jugar_multijugador()
        elif opcion == "3":
            mostrar_reglas()
        elif opcion == "4":
            ver_estadisticas()
        elif opcion == "5":
            print("Gracias por jugar Piedra, Papel y Tijeras. ¡Hasta la próxima! 🎉")
            break #Termina el bucle y finaliza el juego
        else:
            print("Opción inválida. Intente nuevamente.")

def mostrar_reglas(): # Esta función muestra las reglas. Se creó para que los jugadores puedan ver las reglas antes de jugar o incluso al inicio de la partida.
    """Muestra las reglas del juego antes de empezar"""
    # Print se usa basntante en el código porque es fácil de usar y mayormente la usó para mostrar el texto o lo que se desea mostrar al usuario
    print("\n📜 REGLAS DEL JUEGO 📜") 
    print("1️⃣ Piedra vence a Tijeras, Tijeras vence a Papel, y Papel vence a Piedra.")
    print("2️⃣ Si ambos jugadores eligen la misma opción, es un empate.")
    print("3️⃣ En modo multijugador, cada jugador elige en secreto su opción.")
    print("4️⃣ El juego continúa hasta que decidas salir.\n")

def jugar_contra_pc():
    """Modo de juego contra la computadora"""
    opciones = ["Piedra", "Papel", "Tijeras"] # Lista de opciones disponibles

    print("\n🔹 Modo: Jugador vs Computadora")
    nombre_jugador = input("Ingrese su nombre: ")
    #Solicita la cantidad de rondas que desea jugar el usuario
    while True:
        try:
            rondas = int(input(f"{nombre_jugador}, ¿cuántas rondas deseas jugar? (Ingrese un número): "))
            if rondas <= 0:
                print("Debe ingresar un número mayor a 0.")
                continue
            break
        except ValueError:
            print("Entrada inválida. Ingrese un número válido.")
    #Bucle para jugar la cantidad de rondas escogidas.
    while True:
        for ronda in range(rondas):
            print(f"\n🔄 Ronda {ronda + 1} de {rondas}")
            print("\nOpciones: 1) Piedra  2) Papel  3) Tijeras")

            while True: #Se obtiene la elección del usuario con un tiempo límite
                eleccion_usuario = obtener_eleccion_tiempo(f"{nombre_jugador}, elija una opción (1-3): ")
                # Si el tiempo se agotó, el usuario pierde automáticamente la ronda
                if not eleccion_usuario:
                    print(f"⏳ Se acabó el tiempo, {nombre_jugador} pierde esta ronda automáticamente.")
                    estadisticas["computadora_ganadas"] += 1
                    estadisticas["total_partidas"] += 1
                    estadisticas["historico"].append(f"Partida {estadisticas['total_partidas']}: {nombre_jugador} perdió - Computadora ganó")
                    break  # Se termina la ronda y pasa a la siguiente
                # Validación de la entrada del usuario
                if eleccion_usuario not in ["1", "2", "3"]:
                    print("❌ Opción inválida. Por favor, elige 1, 2 o 3.")
                    continue  # Permite que el usuario reingrese una opción correcta en la misma ronda
                # Convierte la opción ingresada en su equivalente en texto
                eleccion_usuario = opciones[int(eleccion_usuario) - 1]
                eleccion_pc = random.choice(opciones) # La computadora elige aleatoriamente
                # Se muestran las elecciones realizadas
                print(f"\n{nombre_jugador} eligió: {eleccion_usuario}")
                print(f"Computadora eligió: {eleccion_pc}")
                # Determina el resultado de la ronda
                resultado = determinar_ganador(eleccion_usuario, eleccion_pc)
                # Se registran las estadísticas de la partida
                if resultado == "jugador1":
                    print(f"\n🏆 ¡{nombre_jugador} gana esta ronda! 🎉")
                    estadisticas["jugador_1_ganadas"] += 1
                elif resultado == "empate":
                    print("\n🤝 ¡Empate!")
                    estadisticas["empates"] += 1
                else:
                    print("\n💻 ¡La computadora gana esta ronda! 😞")
                    estadisticas["computadora_ganadas"] += 1

                estadisticas["total_partidas"] += 1
                if resultado == "jugador1":
                    estadisticas["historico"].append(f"Partida {estadisticas['total_partidas']}: {nombre_jugador} ganó - Computadora perdió")
                elif resultado == "empate":
                    estadisticas["historico"].append(f"Partida {estadisticas['total_partidas']}: {nombre_jugador} empató - Computadora empató")
                else:
                    estadisticas["historico"].append(f"Partida {estadisticas['total_partidas']}: {nombre_jugador} perdió - Computadora ganó")

                break  # Termina la ronda correctamente y pasa a la siguiente

        if not jugar_otra_vez():
            break  # Si el jugador no quiere jugar de nuevo, regresa al menú principal



def jugar_multijugador():
    """Modo de juego entre dos jugadores"""
    opciones = ["Piedra", "Papel", "Tijeras"]

    print("\n🔹 Modo: Jugador 1 vs Jugador 2")
    jugador_1 = input("Nombre del Jugador 1: ")
    jugador_2 = input("Nombre del Jugador 2: ")

    while True:
        try:
            rondas = int(input(f"{jugador_1} y {jugador_2}, ¿cuántas rondas desean jugar? (Ingrese un número): "))
            if rondas <= 0:
                print("Debe ingresar un número mayor a 0.")
                continue
            break
        except ValueError:
            print("Entrada inválida. Ingrese un número válido.")

    while True:
        for ronda in range(rondas):
            print(f"\n🔄 Ronda {ronda + 1} de {rondas}")
            print("\nOpciones: 1) Piedra  2) Papel  3) Tijeras")

            # Elección del jugador 1 con validación
            while True:
                eleccion_1 = obtener_eleccion_tiempo(f"{jugador_1}, elija una opción (1-3) en secreto: ", ocultar=True)
                if not eleccion_1:  # Si el jugador no responde a tiempo
                    print(f"⏳ Se acabó el tiempo, {jugador_1} pierde esta ronda automáticamente.")
                    actualizar_estadisticas("jugador2", jugador_1, jugador_2)
                    break  # Sale del bucle para pasar a la siguiente ronda

                if eleccion_1.isdigit() and int(eleccion_1) in [1, 2, 3]:  # Validar que la entrada esté en el rango
                    eleccion_1 = opciones[int(eleccion_1) - 1]
                    break
                else:
                    print("❌ Opción inválida. Por favor, elige 1, 2 o 3.")

            if not eleccion_1:  # Si el jugador 1 perdió la ronda, no se pregunta al jugador 2
                continue

            # Elección del jugador 2 con validación
            while True:
                eleccion_2 = obtener_eleccion_tiempo(f"{jugador_2}, elija una opción (1-3) en secreto: ", ocultar=True)
                if not eleccion_2:  # Si el jugador no responde a tiempo
                    print(f"⏳ Se acabó el tiempo, {jugador_2} pierde esta ronda automáticamente.")
                    actualizar_estadisticas("jugador1", jugador_1, jugador_2)
                    break  # Sale del bucle para pasar a la siguiente ronda

                if eleccion_2.isdigit() and int(eleccion_2) in [1, 2, 3]:  # Validar que la entrada esté en el rango
                    eleccion_2 = opciones[int(eleccion_2) - 1]
                    break
                else:
                    print("❌ Opción inválida. Por favor, elige 1, 2 o 3.")

            if not eleccion_2:  # Si el jugador 2 perdió la ronda, no se evalúa el resultado
                continue

            # Mostrar elecciones y determinar el ganador
            print(f"\n{jugador_1} eligió: {eleccion_1}")
            print(f"{jugador_2} eligió: {eleccion_2}")

            resultado = determinar_ganador(eleccion_1, eleccion_2)
            if resultado == "empate":
                print("\n🤝 ¡Empate!")
            elif resultado == "jugador1":
                print(f"\n🏆 ¡{jugador_1} gana esta ronda! 🎉")
            else:
                print(f"\n🏆 ¡{jugador_2} gana esta ronda! 🎉")

            actualizar_estadisticas(resultado, jugador_1, jugador_2)

        if not jugar_otra_vez():
            break  # Si no quiere repetir, se sale del bucle y vuelve al menú principal


def obtener_eleccion_tiempo(mensaje, ocultar=False):
    """Función que permite ingresar una opción con un tiempo límite sin permitir múltiples entradas después del tiempo."""
    eleccion = [None]  # Se usa una lista mutable para modificar su valor dentro del temporizador
    tiempo_agotado = [False]  # Bandera para indicar si el tiempo se agotó

    def temporizador():
        time.sleep(10)  # Esperar 10 segundos
        if eleccion[0] is None:
            print("\n⏳ Se acabó el tiempo, perdiste esta ronda automáticamente. Presiona ENTER 2 veces para continuar")
            tiempo_agotado[0] = True  # Marcar que el tiempo se agotó

    # Iniciar temporizador en un hilo
    thread = threading.Thread(target=temporizador)
    thread.start()

    if ocultar:
        eleccion[0] = getpass.getpass(mensaje)  # Se usa getpass para ocultar la entrada en modo multijugador
    else:
        eleccion[0] = input(mensaje)  # Captura la entrada del usuario

    # Si el tiempo se agotó, esperar solo una tecla y avanzar sin pedir input de nuevo
    if tiempo_agotado[0]:
        sys.stdin.read(1)  # Captura una sola tecla y descarta cualquier otro input
        return None  # Retorna None para indicar que el jugador perdió la ronda

    return eleccion[0]  # Devuelve la elección válida si el usuario respondió a tiempo

def determinar_ganador(jugador1, jugador2): # Esta función es para definir la lógica para comparar las elecciones y definir un ganador
    """Determina el resultado de la partida"""
    if jugador1 == jugador2:
        return "empate"
    
    condiciones_ganadoras = {
        "Piedra": "Tijeras",
        "Papel": "Piedra",
        "Tijeras": "Papel"
    }

    return "jugador1" if condiciones_ganadoras[jugador1] == jugador2 else "jugador2"
# Se actualizan los contadores de victorias, empates y partidas jugadas.
def actualizar_estadisticas(resultado, jugador1, jugador2): # Esta función permite llevar un registro de las partidas jugadas de los jugadores
    """Actualiza las estadísticas del juego y almacena el historial de cada partida"""
    estadisticas["total_partidas"] += 1
# El historial almacena cada partida con su número y el resultado correspondiente.
    if resultado == "jugador1":
        estadisticas["jugador_1_ganadas"] += 1
        estadisticas["historico"].append(f"Partida {estadisticas['total_partidas']}: {jugador1} ganó - {jugador2} perdió")
    elif resultado == "jugador2":
        estadisticas["jugador_2_ganadas"] += 1
        estadisticas["historico"].append(f"Partida {estadisticas['total_partidas']}: {jugador1} perdió - {jugador2} ganó")
    else:
        estadisticas["empates"] += 1
        estadisticas["historico"].append(f"Partida {estadisticas['total_partidas']}: {jugador1} empató - {jugador2} empató")

def ver_estadisticas(): #Esta función se creó para ver el historial de partidas jugadas.
    """Muestra el historial de partidas jugadas"""
    print("\n📊 Estadísticas del juego:")
    print(f"Total de partidas jugadas: {estadisticas['total_partidas']}")
    print(f"Jugador 1 ganó: {estadisticas['jugador_1_ganadas']} veces")
    print(f"Jugador 2 ganó: {estadisticas['jugador_2_ganadas']} veces")
    print(f"Computador ganó:{estadisticas['computadora_ganadas']} veces")
    print(f"Empates: {estadisticas['empates']} veces")

    print("\n📜 Historial de partidas:")
    if estadisticas["historico"]:
        for partida in estadisticas["historico"]:
            print(partida)
    else:
        print("Aún no se han jugado partidas.")


def jugar_otra_vez(): # Esta función se creó para que el jugador decida si jugar nuevamente con el mismo número de rondas si no regresa al menu principal.
    """Pregunta si los jugadores quieren jugar con el mismo número de rondas"""
    return input("\n¿Quieres jugar con el mismo número de rondas otra vez? (si/no): ").lower() == "si"

if __name__ == "__main__":
    mostrar_menu()

