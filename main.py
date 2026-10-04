import os
import asyncio
import pyttsx3
import requests
from dotenv import load_dotenv
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent, GiftEvent

load_dotenv()
TIKTOK_USERNAME = os.getenv("TIKTOK_USERNAME")

client = TikTokLiveClient(unique_id=TIKTOK_USERNAME)
engine = pyttsx3.init()
engine.setProperty('rate', 160)
tts_queue = asyncio.Queue()

def generar_respuesta(mensaje, usuario):
    url = "http://localhost:11434/api/generate"
    prompt = f"""
    Eres 'Makanaky La Realeza', un personaje peruano de redes sociales. 
    Hablas con mucha jerga de barrio, eres efusivo y siempre usas tu grito '¡Gaaaa!'. 
    El usuario {usuario} dice: {mensaje}. 
    Responde en una sola frase corta. Usa palabras como 'batería', 'causa', 'choche', 'mano'.
    """
    payload = {"model": "llama3", "prompt": prompt, "stream": False}
    try:
        response = requests.post(url, json=payload)
        return response.json().get("response", "¡Gaaaa! No te escucho batería.")
    except Exception:
        return "Se me fue el internet causa, ¡Gaaaa!"

def reproducir_audio(texto):
    print(f"Makanaky: {texto}")
    engine.say(texto)
    engine.runAndWait()

async def procesador_de_voz():
    while True:
        texto = await tts_queue.get()
        await asyncio.to_thread(reproducir_audio, texto)
        tts_queue.task_done()

@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"✅ ¡Conectado al Live de {event.unique_id}!")
    await tts_queue.put("¡Gaaaa! Ya llegó la realeza, batería seria.")

@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    print(f"💬 [{event.user.nickname}]: {event.comment}")
    if "makanaky" in event.comment.lower() or "habla" in event.comment.lower():
        respuesta = generar_respuesta(event.comment, event.user.nickname)
        await tts_queue.put(respuesta)

@client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    print(f"🎁 [{event.user.nickname}] envió {event.gift.name}")
    if event.gift.name == "Rose":
        mensaje = f"¡Gaaaa! Gracias por la rosa, {event.user.nickname}, eres de la realeza."
    else:
        mensaje = f"Habla causa {event.user.nickname}, gracias por el regalito. ¡Gaaaa!"
    await tts_queue.put(mensaje)

async def main():
    asyncio.create_task(procesador_de_voz())
    await client.start()

if __name__ == '__main__':
    asyncio.run(main())