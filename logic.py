from random import sample

def generar_torneo(juegos, num_rondas=5):
    if len(juegos) < num_rondas:
        raise ValueError("No hay suficientes juegos para el torneo.")
    return sample(juegos, num_rondas)

def buscar_juegos_por_categoria(juegos, categoria):
    return [j for j in juegos if categoria.lower() in [c.lower() for c in j.categorias]]

def recomendar_juego(juegos, num_jugadores):
    return [j for j in juegos if j.jugadores_min <= num_jugadores <= j.jugadores_max]

def eliminar_juego(juegos, indice):
    if 0 <= indice < len(juegos):
        return juegos.pop(indice)
    raise IndexError("Índice de juego inválido.")

def editar_juego(juego, **kwargs):
    for key, value in kwargs.items():
        if hasattr(juego, key):
            setattr(juego, key, value)