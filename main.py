import os
import asyncio
import pyttsx3
import requests
import keyboard 
from dotenv import load_dotenv
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent, GiftEvent

load_dotenv()
TIKTOK_USERNAME = os.getenv("TIKTOK_USERNAME")

client = TikTokLiveClient(unique_id=TIKTOK_USERNAME)
engine = pyttsx3.init()
engine.setProperty('rate', 160)
tts_queue = asyncio.Queue()

# --- VARIABLE GLOBAL PARA EL INTERRUPTOR ---
bot_activo = False  # Empieza apagado para que tú lo prendas cuando estés listo

def alternar_bot():
    global bot_activo
    bot_activo = not bot_activo
    if bot_activo:
        print("\n🟢 [BOTÓN F9] MAKANAKY ACTIVADO - ¡Que empiece el show! ¡Gaaaa!\n")
    else:
        print("\n🔴 [BOTÓN F9] MAKANAKY SILENCIADO - Bot en pausa.\n")

# Configuramos la tecla F9 para prender/apagar al bot
keyboard.add_hotkey('F9', alternar_bot)


# --- FUNCIÓN DE OLLAMA MEJORADA (Llama 3.1) ---
def peticion_ollama(mensaje, usuario):
    url = "http://localhost:11434/api/generate"
    prompt = f"""
    Eres 'Makanaky La Realeza', un personaje peruano de redes sociales. 
    Hablas con mucha jerga de barrio, eres efusivo y siempre usas tu grito '¡Gaaaa!'. 
    El usuario {usuario} dice: {mensaje}. 
    Responde en una sola frase corta. Usa palabras como 'batería', 'causa', 'choche', 'mano'.
    """
    # Usamos llama3.1 para aprovechar los 32GB de tu PC al máximo
    payload = {"model": "llama3.1", "prompt": prompt, "stream": False}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json().get("response", "¡Gaaaa! No te escucho batería.")
    except Exception:
        return "Se me fue el internet causa, ¡Gaaaa!"

async def generar_respuesta_async(mensaje, usuario):
    return await asyncio.to_thread(peticion_ollama, mensaje, usuario)

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
    print("⚠️ EL BOT ESTÁ APAGADO. PRESIONA 'F9' PARA ACTIVARLO.")

@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    # Si el bot está apagado, ignoramos el comentario
    if not bot_activo:
        return

    print(f"💬 [{event.user.nickname}]: {event.comment}")
    if "makanaky" in event.comment.lower() or "habla" in event.comment.lower():
        respuesta = await generar_respuesta_async(event.comment, event.user.nickname)
        await tts_queue.put(respuesta)

@client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    # Si el bot está apagado, ignoramos el regalo
    if not bot_activo:
        return

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
    # Nota: Si el teclado no responde en Windows, ejecuta la terminal como Administrador
    asyncio.run(main())