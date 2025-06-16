from datetime import datetime

class Juego:
    def __init__(self, nombre, categorias, jugadores_min=1, jugadores_max=4, duracion_minutos=30):
        self.nombre = nombre
        self.categorias = categorias
        self.jugadores_min = jugadores_min
        self.jugadores_max = jugadores_max
        self.duracion_minutos = duracion_minutos
        self.creado = datetime.now().isoformat()

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "categorias": self.categorias,
            "jugadores_min": self.jugadores_min,
            "jugadores_max": self.jugadores_max,
            "duracion_minutos": self.duracion_minutos,
            "creado": self.creado
        }

    @staticmethod
    def from_dict(data):
        return Juego(
            data["nombre"],
            data["categorias"],
            data.get("jugadores_min", 1),
            data.get("jugadores_max", 4),
            data.get("duracion_minutos", 30)
        )

    def __str__(self):
        return f"{self.nombre} ({', '.join(self.categorias)}) - Jugadores: {self.jugadores_min}-{self.jugadores_max}, Duración: {self.duracion_minutos} mins"


class SesionJuego:
    def __init__(self, fecha_hora, juego, participantes=None):
        self.fecha_hora = fecha_hora
        self.juego = juego
        self.participantes = participantes or []

    def to_dict(self):
        return {
            "fecha_hora": self.fecha_hora,
            "juego": self.juego.to_dict(),
            "participantes": self.participantes
        }

    @staticmethod
    def from_dict(data):
        return SesionJuego(
            data["fecha_hora"],
            Juego.from_dict(data["juego"]),
            data.get("participantes", [])
        )

    def __str__(self):
        return f"{self.fecha_hora}: {self.juego.nombre} con {len(self.participantes)} participantes"


class AgendaJuegos:
    def __init__(self):
        self.sesiones = []

    def agregar_sesion(self, sesion):
        self.sesiones.append(sesion)

    def to_dict(self):
        return {"sesiones": [s.to_dict() for s in self.sesiones]}

    @staticmethod
    def from_dict(data):
        agenda = AgendaJuegos()
        agenda.sesiones = [SesionJuego.from_dict(s) for s in data.get("sesiones", [])]
        return agenda

    def __str__(self):
        return "\n".join(str(s) for s in self.sesiones)