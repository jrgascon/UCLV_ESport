import aiofiles
import json
import os
from models import Juego, AgendaJuegos

JUEGOS_PATH = "data/juegos.json"
AGENDA_PATH = "data/agenda.json"

async def guardar_juegos(juegos):
    os.makedirs("data", exist_ok=True)
    async with aiofiles.open(JUEGOS_PATH, mode="w") as f:
        await f.write(json.dumps([j.to_dict() for j in juegos], indent=4))

async def cargar_juegos():
    if not os.path.exists(JUEGOS_PATH):
        return []
    async with aiofiles.open(JUEGOS_PATH, mode="r") as f:
        contenido = await f.read()
        try:
            return [Juego.from_dict(j) for j in json.loads(contenido)]
        except json.JSONDecodeError:
            return []

async def guardar_agenda(agenda):
    os.makedirs("data", exist_ok=True)
    async with aiofiles.open(AGENDA_PATH, mode="w") as f:
        await f.write(json.dumps(agenda.to_dict(), indent=4))

async def cargar_agenda():
    if not os.path.exists(AGENDA_PATH):
        return AgendaJuegos()
    async with aiofiles.open(AGENDA_PATH, mode="r") as f:
        contenido = await f.read()
        try:
            return AgendaJuegos.from_dict(json.loads(contenido))
        except json.JSONDecodeError:
            return AgendaJuegos()