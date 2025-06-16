import asyncio
from datetime import datetime
from models import Juego, SesionJuego, AgendaJuegos
from logic import (
    generar_torneo,
    buscar_juegos_por_categoria,
    recomendar_juego,
    eliminar_juego,
    editar_juego
)
from storage import cargar_juegos, guardar_juegos, cargar_agenda, guardar_agenda

# Variables globales
juegos = []
agenda = AgendaJuegos()

def validar_fecha(fecha_str):
    try:
        datetime.fromisoformat(fecha_str)
        return True
    except ValueError:
        return False

def agregar_juego():
    print("\n➕ Agregar Nuevo Juego")
    while True:
        nombre = input("Nombre del juego: ").strip()
        if nombre:
            break
        print("⚠️ Error: El nombre no puede estar vacío.")

    categorias = []
    while not categorias:
        categorias_input = input("Categorías (separadas por coma): ").strip()
        categorias = [c.strip() for c in categorias_input.split(",") if c.strip()]
        if not categorias:
            print("⚠️ Error: Debes ingresar al menos una categoría.")

    while True:
        try:
            jugadores_min = int(input("Jugadores mínimos (1-10): ") or 1)
            jugadores_max = int(input("Jugadores máximos (1-10): ") or 4)
            if 1 <= jugadores_min <= jugadores_max <= 10:
                break
            print("⚠️ Error: Jugadores máximos deben ser ≥ mínimos (rango 1-10).")
        except ValueError:
            print("⚠️ Error: Ingresa un número válido.")

    while True:
        try:
            duracion = int(input("Duración en minutos (≥15): ") or 30)
            if duracion >= 15:
                break
            print("⚠️ Error: La duración mínima es 15 minutos.")
        except ValueError:
            print("⚠️ Error: Ingresa un número válido.")

    juego = Juego(nombre, categorias, jugadores_min, jugadores_max, duracion)
    juegos.append(juego)
    print(f"✅ Juego '{nombre}' agregado!")

def ver_juegos():
    if not juegos:
        print("\nNo hay juegos registrados.")
    else:
        print("\n🎲 Lista de Juegos:")
        for i, juego in enumerate(juegos, 1):
            print(f"{i}. {juego}")

def editar_juego_menu():
    ver_juegos()
    if not juegos:
        return

    while True:
        try:
            idx = int(input("\nNúmero del juego a editar: ")) - 1
            if 0 <= idx < len(juegos):
                break
            print("⚠️ Error: Índice fuera de rango.")
        except ValueError:
            print("⚠️ Error: Ingresa un número válido.")

    juego = juegos[idx]
    print(f"\nEditando: {juego.nombre}")

    nombre = input(f"Nuevo nombre ({juego.nombre}): ").strip() or juego.nombre
    categorias_input = input(f"Categorías ({', '.join(juego.categorias)}): ").strip()
    categorias = [c.strip() for c in categorias_input.split(",") if c.strip()] or juego.categorias

    while True:
        try:
            jugadores_min = int(input(f"Jugadores mínimos ({juego.jugadores_min}): ") or juego.jugadores_min)
            jugadores_max = int(input(f"Jugadores máximos ({juego.jugadores_max}): ") or juego.jugadores_max)
            if 1 <= jugadores_min <= jugadores_max <= 10:
                break
            print("⚠️ Error: Jugadores máximos deben ser ≥ mínimos (rango 1-10).")
        except ValueError:
            print("⚠️ Error: Ingresa un número válido.")

    while True:
        try:
            duracion = int(input(f"Duración en minutos ({juego.duracion_minutos}): ") or juego.duracion_minutos)
            if duracion >= 15:
                break
            print("⚠️ Error: La duración mínima es 15 minutos.")
        except ValueError:
            print("⚠️ Error: Ingresa un número válido.")

    editar_juego(juego, nombre=nombre, categorias=categorias, jugadores_min=jugadores_min, jugadores_max=jugadores_max, duracion_minutos=duracion)
    print("✅ Juego actualizado!")

def eliminar_juego_menu():
    ver_juegos()
    if not juegos:
        return

    while True:
        try:
            idx = int(input("\nNúmero del juego a eliminar: ")) - 1
            if 0 <= idx < len(juegos):
                juego_eliminado = eliminar_juego(juegos, idx)
                print(f"✅ Juego eliminado: {juego_eliminado.nombre}")
                break
            print("⚠️ Error: Índice fuera de rango.")
        except ValueError:
            print("⚠️ Error: Ingresa un número válido.")

def ver_sesiones():
    if not agenda.sesiones:
        print("\nNo hay sesiones programadas.")
    else:
        print("\n📅 Sesiones Programadas:")
        for i, sesion in enumerate(agenda.sesiones, 1):
            print(f"{i}. {sesion.fecha_hora} - {sesion.juego.nombre} (Participantes: {', '.join(sesion.participantes)})")

def programar_sesion():
    ver_juegos()
    if not juegos:
        return

    while True:
        try:
            juego_idx = int(input("\nSelecciona un juego (número): ")) - 1
            if 0 <= juego_idx < len(juegos):
                break
            print("⚠️ Error: Índice fuera de rango.")
        except ValueError:
            print("⚠️ Error: Ingresa un número válido.")

    while True:
        fecha = input("Fecha y hora (ej: 2025-06-20T18:00): ").strip()
        if validar_fecha(fecha):
            break
        print("⚠️ Error: Formato inválido. Usa YYYY-MM-DDTHH:MM (ej: 2025-06-20T18:00).")

    participantes = []
    while not participantes:
        participantes_input = input("Participantes (separados por coma): ").strip()
        participantes = [p.strip() for p in participantes_input.split(",") if p.strip()]
        if not participantes:
            print("⚠️ Error: Debes ingresar al menos un participante.")

    sesion = SesionJuego(fecha, juegos[juego_idx], participantes)
    agenda.agregar_sesion(sesion)
    print("✅ Sesión agregada!")

def editar_sesion():
    ver_sesiones()
    if not agenda.sesiones:
        return

    while True:
        try:
            idx = int(input("\nNúmero de la sesión a editar: ")) - 1
            if 0 <= idx < len(agenda.sesiones):
                break
            print("⚠️ Error: Índice fuera de rango.")
        except ValueError:
            print("⚠️ Error: Ingresa un número válido.")

    sesion = agenda.sesiones[idx]
    print(f"\nEditando sesión: {sesion.juego.nombre} ({sesion.fecha_hora})")

    # Editar fecha/hora (opcional)
    nueva_fecha = input(f"Nueva fecha/hora (actual: {sesion.fecha_hora}, Enter para mantener): ").strip()
    if nueva_fecha:
        if validar_fecha(nueva_fecha):
            sesion.fecha_hora = nueva_fecha
        else:
            print("⚠️ Formato inválido. No se cambió la fecha.")

    nuevos_participantes = input(f"\nAgregar participantes (actuales: {', '.join(sesion.participantes)}): ").strip()
    if nuevos_participantes:
        participantes_agregados = [p.strip() for p in nuevos_participantes.split(",") if p.strip()]
        sesion.participantes.extend(participantes_agregados)
        print(f"✅ Participantes agregados: {', '.join(participantes_agregados)}")
    else:
        print("⚠️ No se agregaron nuevos participantes.")

    print("\n✅ Sesión actualizada!")

def eliminar_sesion():
    ver_sesiones()
    if not agenda.sesiones:
        return

    while True:
        try:
            idx = int(input("\nNúmero de la sesión a eliminar: ")) - 1
            if 0 <= idx < len(agenda.sesiones):
                sesion_eliminada = agenda.sesiones.pop(idx)
                print(f"✅ Sesión eliminada: {sesion_eliminada.juego.nombre}")
                break
            print("⚠️ Error: Índice fuera de rango.")
        except ValueError:
            print("⚠️ Error: Ingresa un número válido.")

# --- Menús ---
def menu_gestion_juegos():
    while True:
        print("\n📚 Gestión de Juegos")
        print("1. Agregar juego")
        print("2. Ver todos los juegos")
        print("3. Editar juego")
        print("4. Eliminar juego")
        print("5. Volver al menú principal")
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            agregar_juego()
        elif opcion == "2":
            ver_juegos()
        elif opcion == "3":
            editar_juego_menu()
        elif opcion == "4":
            eliminar_juego_menu()
        elif opcion == "5":
            break
        else:
            print("⚠️ Opción inválida.")

def menu_gestion_sesiones():
    while True:
        print("\n📅 Gestión de Sesiones")
        print("1. Programar sesión")
        print("2. Ver todas las sesiones")
        print("3. Editar sesión")
        print("4. Eliminar sesión")
        print("5. Volver al menú principal")
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            programar_sesion()
        elif opcion == "2":
            ver_sesiones()
        elif opcion == "3":
            editar_sesion()
        elif opcion == "4":
            eliminar_sesion()
        elif opcion == "5":
            break
        else:
            print("⚠️ Opción inválida.")

def mostrar_menu():
    print("\n=== 🎮 ORGANIZADOR DE JUEGOS ===")
    print("1. Gestión de Juegos")
    print("2. Gestión de Sesiones")
    print("3. Generar Torneo Aleatorio")
    print("4. Buscar Juegos por Categoría")
    print("5. Recomendar Juego por Número de Jugadores")
    print("6. Guardar y Salir")


async def inicializar():
    global juegos, agenda
    juegos = await cargar_juegos()
    agenda = await cargar_agenda()
    print("\n✅ Datos cargados exitosamente.")

async def main():
    await inicializar()
    while True:
        mostrar_menu()
        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            menu_gestion_juegos()
        elif opcion == "2":
            menu_gestion_sesiones()
        elif opcion == "3":
            try:
                num_rondas = int(input("Número de rondas del torneo: "))
                torneo = generar_torneo(juegos, num_rondas)
                print("\n🎲 Torneo Generado:")
                for i, juego in enumerate(torneo, 1):
                    print(f"{i}. {juego.nombre}")
            except ValueError as e:
                print(f"⚠️ Error: {e}")
        elif opcion == "4":
            categoria = input("Categoría a buscar: ").strip()
            resultados = buscar_juegos_por_categoria(juegos, categoria)
            print("\n🔍 Resultados:" if resultados else "No hay juegos en esta categoría.")
            for j in resultados:
                print(f"- {j}")
        elif opcion == "5":
            try:
                num_jugadores = int(input("Número de jugadores disponibles: "))
                recomendados = recomendar_juego(juegos, num_jugadores)
                print("\n🎯 Juegos Recomendados:" if recomendados else "No hay juegos para este número de jugadores.")
                for j in recomendados:
                    print(f"- {j}")
            except ValueError:
                print("⚠️ Error: Ingresa un número válido.")
        elif opcion == "6":
            await guardar_juegos(juegos)
            await guardar_agenda(agenda)
            print("\n✅ Datos guardados. ¡Hasta luego!")
            break
        else:
            print("⚠️ Opción inválida.")

if __name__ == "__main__":
    asyncio.run(main())