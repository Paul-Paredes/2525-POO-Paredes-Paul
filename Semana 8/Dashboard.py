import json

import os

ARCHIVO_TAREAS = "tareas.json"

# Crear archivo de tareas si no existe

if not os.path.exists(ARCHIVO_TAREAS):
    with open(ARCHIVO_TAREAS, "w") as f:
        json.dump([], f)


def cargar_tareas():
    with open(ARCHIVO_TAREAS, "r") as f:
        return json.load(f)


def guardar_tareas(tareas):
    with open(ARCHIVO_TAREAS, "w") as f:
        json.dump(tareas, f, indent=4)


def agregar_tarea():
    titulo = input("Título de la tarea: ")

    descripcion = input("Descripción: ")

    tarea = {"titulo": titulo, "descripcion": descripcion, "estado": "pendiente"}

    tareas = cargar_tareas()

    tareas.append(tarea)

    guardar_tareas(tareas)

    print("Tarea agregada con éxito.")


def ver_tareas(filtro="todas"):
    tareas = cargar_tareas()

    if filtro == "pendientes":

        tareas = [t for t in tareas if t["estado"] == "pendiente"]

    elif filtro == "completadas":

        tareas = [t for t in tareas if t["estado"] == "completada"]

    if not tareas:

        print("No hay tareas para mostrar.")

    else:

        for idx, tarea in enumerate(tareas, start=1):
            print(f"{idx}. {tarea['titulo']} - {tarea['estado']}")

            print(f"   {tarea['descripcion']}")


def completar_tarea():
    tareas = cargar_tareas()

    ver_tareas("pendientes")

    try:

        idx = int(input("Número de la tarea que deseas marcar como completada: ")) - 1

        if 0 <= idx < len(tareas) and tareas[idx]["estado"] == "pendiente":

            tareas[idx]["estado"] = "completada"

            guardar_tareas(tareas)

            print("Tarea marcada como completada.")

        else:

            print("Número inválido o tarea ya completada.")

    except:

        print("Entrada no válida. Intenta nuevamente.")


def mostrar_menu():
    while True:

        print("\n=== DASHBOARD DE TAREAS DE POO ===")

        print("1. Agregar nueva tarea")

        print("2. Ver todas las tareas")

        print("3. Ver tareas pendientes")

        print("4. Ver tareas completadas")

        print("5. Marcar tarea como completada")

        print("0. Salir")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == '1':

            agregar_tarea()

        elif opcion == '2':

            ver_tareas("todas")

        elif opcion == '3':

            ver_tareas("pendientes")

        elif opcion == '4':

            ver_tareas("completadas")

        elif opcion == '5':

            completar_tarea()

        elif opcion == '0':

            print("Saliendo del programa.")

            break

        else:

            print("Opción no válida. Intenta nuevamente.")


if __name__ == "__main__":
    mostrar_menu()

