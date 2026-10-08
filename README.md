# TikTok Live AI Bot - Edicion Makanaky

Este repositorio contiene un bot interactivo desarrollado en Python, diseñado para conectarse a transmisiones de TikTok Live. Procesa eventos en tiempo real como comentarios y regalos, y genera respuestas de audio dinamicas y contextuales utilizando un Modelo de Lenguaje Grande (LLM) ejecutado en local y una herramienta de Texto a Voz (TTS).

El bot esta configurado con una personalidad especifica (Makanaky), demostrando capacidades de ingenieria de prompts e interaccion en vivo.

## Arquitectura y Caracteristicas

* Escucha de Eventos en Tiempo Real: Utiliza la libreria TikTokLive para capturar comentarios, donaciones y nuevos espectadores de forma asincrona.

* Integracion de LLM Local: Usa Ollama (modelo Llama 3.1) para generar respuestas localmente. Esto garantiza cero costos por consumo de API y total privacidad de los datos.

* Cola de Audio Asincrona: Implementa asyncio.Queue para gestionar el alto volumen de interacciones. Esto previene que los audios se superpongan o que el sistema colapse cuando entran muchos mensajes al mismo tiempo.

* Texto a Voz (TTS): Emplea la libreria pyttsx3 para sintetizar y reproducir de forma inmediata el texto generado por la inteligencia artificial.

* Interfaz de Control Web (Frontend y Backend): Incluye un panel interactivo (HTML) que se conecta a un servidor local asincrono construido con `aiohttp`. Permite encender o apagar la IA con un simple clic a traves del puerto 5000.

* Control por Teclado Local: Soporta la activacion y desactivacion rapida de la IA desde el equipo donde se ejecuta mediante un atajo global de teclado (tecla F9).

* Seguridad del Entorno: Usa python-dotenv para aislar el usuario objetivo y mantener el entorno seguro frente a filtraciones en repositorios publicos.

## Requisitos Previos

* Python 3.8 o superior
* Git
* Ollama instalado en tu sistema

## Instalacion y Configuracion

1. Clona el repositorio:

```bash
git clone https://github.com/gerargram2006/tiktok-ia-makanaky.git
cd tiktok-ia-makanaky
```

2. Crea y activa un entorno virtual:

```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate
```

3. Instala las dependencias requeridas:

```bash
pip install -r requirements.txt
pip install aiohttp keyboard
```

4. Configura las variables de entorno:
   Crea un archivo llamado `.env` en la raiz del proyecto y añade el usuario de TikTok que deseas monitorear:

```env
TIKTOK_USERNAME=@usuario_objetivo
```

## Uso

1. Inicia el motor de Ollama en una terminal separada con el modelo Llama 3.1:

```bash
ollama run llama3.1
```

2. Ejecuta el bot en tu terminal principal (se recomienda abrirla como Administrador en Windows para que el atajo de teclado funcione correctamente):

```bash
python main.py
```

3. Abre el archivo `index.html` en tu navegador para visualizar y controlar la IA desde su interfaz web. 

La consola registrara las conexiones exitosas, los comentarios detectados y la respuesta generada por el LLM. El audio se emitira por la salida predeterminada de tu computadora. Puedes activar o desactivar al bot en cualquier momento usando el boton del panel web o presionando la tecla F9.

##  Cómo usar el Panel Web (Para Principiantes)

¡No te preocupes si no sabes programar! Para ver la interfaz visual y controlar a la IA de manera fácil, solo sigue estos pasos:

1. **Enciende el motor principal:** El servidor que conecta el panel con el bot se activa automáticamente al ejecutar tu bot con este comando:
```bash
python main.py
```

2. **Abre el panel visual:** Puedes hacer **doble clic** en el archivo `index.html` para que se abra automáticamente en tu navegador favorito (Chrome, Edge, Firefox).

*(Alternativa)* Si el doble clic no te funciona o prefieres abrirlo como una página real, abre una nueva consola y ejecuta este comando para iniciar un servidor web básico:
```bash
python -m http.server 8000
```
Luego, entra desde tu navegador a: http://localhost:8000