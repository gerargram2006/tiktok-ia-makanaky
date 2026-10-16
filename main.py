import os
import sys
import asyncio
import functools
import pyttsx3
import requests
import keyboard 
from dotenv import load_dotenv
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent, GiftEvent
from TikTokLive.client.errors import UserOfflineError, TikTokLiveError
from aiohttp import web

# Asegurar codificacion UTF-8 y salida inmediata en consolas de Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
print = functools.partial(print, flush=True)

load_dotenv()
TIKTOK_USERNAME = (os.getenv("TIKTOK_USERNAME") or "").strip().lstrip("@")

client = TikTokLiveClient(unique_id=TIKTOK_USERNAME)
engine = pyttsx3.init()
engine.setProperty('rate', 160)
tts_queue = asyncio.Queue()

# --- VARIABLE GLOBAL PARA EL INTERRUPTOR ---
bot_activo = False  # Empieza apagado para activarlo cuando estes listo

def alternar_bot():
    global bot_activo
    bot_activo = not bot_activo
    if bot_activo:
        print("\n[BOTON F9] MAKANAKY ACTIVADO - Que empiece el show! Gaaaa!\n")
    else:
        print("\n[BOTON F9] MAKANAKY SILENCIADO - Bot en pausa.\n")

# Configuramos la tecla F9 para prender/apagar al bot
keyboard.add_hotkey('F9', alternar_bot)


# --- FUNCION DE OLLAMA MEJORADA (Llama 3.1) ---
def peticion_ollama(mensaje, usuario):
    url = "http://localhost:11434/api/generate"
    prompt = f"""
    Eres 'Makanaky La Realeza', un personaje peruano de redes sociales. 
    Hablas con mucha jerga de barrio, eres efusivo y siempre usas tu grito '¡Gaaaa!'. 
    El usuario {usuario} dice: {mensaje}. 
    Responde en una sola frase corta. Usa palabras como 'bateria', 'causa', 'choche', 'mano'.
    """
    payload = {"model": "llama3.1", "prompt": prompt, "stream": False}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json().get("response", "Gaaaa! No te escucho bateria.")
    except Exception:
        return "Se me fue el internet causa, Gaaaa!"

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
    print(f"[CONECTADO] Conectado exitosamente al Live de {event.unique_id}!")
    print("[ESTADO] El bot esta apagado inicialmente. Presiona F9 o usa el panel web para activarlo.")

@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    # Si el bot esta apagado, ignoramos el comentario
    if not bot_activo:
        return

    nickname = event.user.nickname if event.user else "Anonimo"
    print(f"[{nickname}]: {event.comment}")
    if "makanaky" in event.comment.lower() or "habla" in event.comment.lower():
        respuesta = await generar_respuesta_async(event.comment, nickname)
        await tts_queue.put(respuesta)

@client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    # Si el bot esta apagado, ignoramos el regalo
    if not bot_activo:
        return

    nickname = event.user.nickname if event.user else "Anonimo"
    gift_name = event.gift.name if event.gift else "Regalo"
    print(f"[{nickname}] envio {gift_name}")
    if gift_name == "Rose":
        mensaje = f"Gaaaa! Gracias por la rosa, {nickname}, eres de la realeza."
    else:
        mensaje = f"Habla causa {nickname}, gracias por el regalito. Gaaaa!"
    await tts_queue.put(mensaje)

# --- API LOCAL PARA COMUNICARSE CON EL HTML ---
async def toggle_bot(request):
    global bot_activo
    bot_activo = not bot_activo
    estado = "ACTIVADO" if bot_activo else "DESACTIVADO"
    print(f"\n[PANEL WEB] MAKANAKY {estado}!\n")
    
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }
    return web.json_response({"status": "ok", "bot_activo": bot_activo}, headers=headers)

async def opciones_cors(request):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }
    return web.Response(headers=headers)

async def iniciar_servidor_web():
    app = web.Application()
    app.router.add_post('/toggle', toggle_bot)
    app.router.add_options('/toggle', opciones_cors)
    runner = web.AppRunner(app)
    await runner.setup()
    try:
        site = web.TCPSite(runner, '127.0.0.1', 5000)
        await site.start()
        print("[SERVIDOR] Panel de control web activo en http://localhost:5000")
    except OSError:
        print("[SERVIDOR] Aviso: El puerto 5000 ya esta en uso o reservado.")

async def conectar_tiktok():
    if not TIKTOK_USERNAME:
        print("\n[CONFIGURACION] No se encontro TIKTOK_USERNAME en el archivo .env.")
        print("[INFO] Agrega tu usuario en el archivo .env (ejemplo: TIKTOK_USERNAME=tu_usuario).\n")
        return

    while True:
        try:
            print(f"[TIKTOK] Intentando conectar al Live de @{TIKTOK_USERNAME}...")
            await client.start()
        except UserOfflineError:
            print(f"[TIKTOK] El usuario @{TIKTOK_USERNAME} esta OFFLINE (no esta en vivo en TikTok actualmente).")
            print("[SISTEMA] El panel web y la IA permanecen listos. Reintentando conexion en 15 segundos...\n")
            await asyncio.sleep(15)
        except TikTokLiveError as e:
            print(f"[TIKTOK] Aviso de conexion: {e}")
            print("[SISTEMA] Reintentando en 15 segundos...\n")
            await asyncio.sleep(15)
        except Exception as e:
            print(f"[TIKTOK] Excepcion ({type(e).__name__}): {e}")
            print("[SISTEMA] Reintentando en 15 segundos...\n")
            await asyncio.sleep(15)

# --- FUNCION PRINCIPAL ---
async def main():
    asyncio.create_task(procesador_de_voz())
    asyncio.create_task(iniciar_servidor_web()) # Arranca el servidor web en segundo plano
    asyncio.create_task(conectar_tiktok())      # Arranca la conexion a TikTok con reintento automatico
    
    # Mantener el proceso principal activo
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    # Nota: Si el teclado no responde en Windows, ejecuta la terminal como Administrador
    asyncio.run(main())