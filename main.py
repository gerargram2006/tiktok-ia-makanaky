import os
import asyncio
import pyttsx3
import requests
from dotenv import load_dotenv
from aiohttp import web
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent, GiftEvent
from TikTokLive.client.errors import UserOfflineError

load_dotenv()
TIKTOK_USERNAME = os.getenv("TIKTOK_USERNAME")

# ==========================================
# CONFIGURACIÓN DEL MODELO DE OLLAMA
# ==========================================
MODELO_OLLAMA = "llama3.2:3b"  # <--- Modelo ultra veloz configurado

client = TikTokLiveClient(unique_id=TIKTOK_USERNAME)
engine = pyttsx3.init()
engine.setProperty('rate', 160)
tts_queue = asyncio.Queue()

# Estados del bot para sincronizar con index.html
bot_activo = False
esta_hablando = False
ultimo_texto = ""


# ==========================================
# CEREBRO IA (OLLAMA)
# ==========================================
def peticion_ollama(mensaje, usuario):
    url = "http://localhost:11434/api/generate"
    prompt = f"""
    Eres 'Makanaky La Realeza', un personaje cómico peruano de redes sociales.
    Hablas con mucha jerga de barrio peruano (ejemplos: 'batería', 'causa', 'choche', 'mano', 'mi king').
    Eres efusivo, gracioso y siempre rematas con tu clásico grito '¡Gaaaa!'.
    El usuario del chat ({usuario}) te dice: "{mensaje}".
    Responde en una sola frase corta y directa, sin rodeos.
    """
    payload = {
        "model": MODELO_OLLAMA,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=8)
        if response.status_code == 200:
            return response.json().get("response", "¡Gaaaa! No te escucho bien, batería.")
        return "Se me cruzaron los cables, ¡Gaaaa!"
    except Exception as e:
        print(f"Error al conectar con Ollama: {e}")
        return "¡Gaaaa! Se me fue el internet causa."

async def generar_respuesta_async(mensaje, usuario):
    return await asyncio.to_thread(peticion_ollama, mensaje, usuario)


# ==========================================
# PROCESAMIENTO DE VOZ Y SUBTÍTULOS
# ==========================================
def reproducir_audio(texto):
    global esta_hablando, ultimo_texto
    esta_hablando = True
    ultimo_texto = texto
    print(f"\n🗣️ Makanaky: {texto}\n")
    engine.say(texto)
    engine.runAndWait()
    esta_hablando = False

async def procesador_de_voz():
    while True:
        texto = await tts_queue.get()
        await asyncio.to_thread(reproducir_audio, texto)
        tts_queue.task_done()


# ==========================================
# EVENTOS DE TIKTOK LIVE
# ==========================================
@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"✅ ¡Conectado al Live de {event.unique_id}!")
    print(f"🤖 Modelo activo en Ollama: {MODELO_OLLAMA}")
    print("⏸️  El bot está en PAUSA. Actívalo desde tu panel index.html.")

@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    if not bot_activo:
        return

    print(f"💬 [{event.user.nickname}]: {event.comment}")
    # Filtro para responder si lo mencionan o llaman
    comentario = event.comment.lower()
    if any(palabra in comentario for palabra in ["makanaky", "habla", "gerson", "gaaa", "hola"]):
        respuesta = await generar_respuesta_async(event.comment, event.user.nickname)
        await tts_queue.put(respuesta)

@client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    if not bot_activo:
        return

    print(f"🎁 [{event.user.nickname}] envió: {event.gift.name}")
    if "rose" in event.gift.name.lower():
        mensaje = f"¡Gaaaa! Gracias por esa rosita {event.user.nickname}, eres de la realeza batería."
    else:
        mensaje = f"Habla causa {event.user.nickname}, tremendo regalo. ¡Gaaaa!"
    await tts_queue.put(mensaje)


# ==========================================
# SERVIDOR WEB LOCAL (COMUNICACIÓN CON INDEX.HTML)
# ==========================================
async def toggle_bot(request):
    global bot_activo
    bot_activo = not bot_activo
    estado = "ACTIVADO 🟢" if bot_activo else "PAUSADO 🔴"
    print(f"\n[WEB] Bot {estado}\n")
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }
    return web.json_response({"status": "ok", "bot_activo": bot_activo}, headers=headers)

async def status_bot(request):
    headers = {"Access-Control-Allow-Origin": "*"}
    return web.json_response({
        "bot_activo": bot_activo,
        "hablando": esta_hablando,
        "ultimo_texto": ultimo_texto
    }, headers=headers)

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
    app.router.add_get('/status', status_bot)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 5000)
    await site.start()
    print("🌐 Servidor API listo en http://localhost:5000 (sincronizado con index.html)")


# ==========================================
# ARRANQUE PRINCIPAL
# ==========================================
async def main():
    asyncio.create_task(procesador_de_voz())
    asyncio.create_task(iniciar_servidor_web())
    
    try:
        await client.start()
    except UserOfflineError:
        print("\n❌ ERROR: ¡La cuenta de TikTok está OFFLINE!")
        print("👉 Prende tu directo en TikTok primero, causa, y luego vuelve a correr el script.\n")
    except Exception as e:
        print(f"\n❌ Se cruzaron los cables: {e}\n")

if __name__ == '__main__':
    asyncio.run(main())