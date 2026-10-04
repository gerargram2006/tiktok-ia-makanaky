# TikTok Live AI Bot - Edicion Makanaky

Este repositorio contiene un bot interactivo desarrollado en Python, diseñado para conectarse a transmisiones de TikTok Live. Procesa eventos en tiempo real como comentarios y regalos, y genera respuestas de audio dinamicas y contextuales utilizando un Modelo de Lenguaje Grande (LLM) ejecutado en local y una herramienta de Texto a Voz (TTS).

El bot esta configurado con una personalidad especifica (Makanaky), demostrando capacidades de ingenieria de prompts e interaccion en vivo.

## Arquitectura y Caracteristicas

* Escucha de Eventos en Tiempo Real: Utiliza la libreria TikTokLive para capturar comentarios, donaciones y nuevos espectadores de forma asincrona.

* Integracion de LLM Local: Usa Ollama (modelo Llama 3) para generar respuestas localmente. Esto garantiza cero costos por consumo de API y total privacidad de los datos.

* Cola de Audio Asincrona: Implementa asyncio.Queue para gestionar el alto volumen de interacciones. Esto previene que los audios se superpongan o que el sistema colapse cuando entran muchos mensajes al mismo tiempo.

* Texto a Voz (TTS): Emplea la libreria pyttsx3 para sintetizar y reproducir de forma inmediata el texto generado por la inteligencia artificial.

* Seguridad del Entorno: Usa python-dotenv para aislar el usuario objetivo y mantener el entorno seguro frente a filtraciones en repositorios publicos.

## Requisitos Previos

* Python 3.8 o superior

* Git

* Ollama instalado en tu sistema

## Instalacion y Configuracion

1. Clona el repositorio:

```
git clone https://github.com/gerargram2006/tiktok-ia-makanaky.git
cd tiktok-ia-makanaky

```

2. Crea y activa un entorno virtual:

```
python -m venv venv

# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate

```

3. Instala las dependencias requeridas:

```
pip install -r requirements.txt

```

4. Configura las variables de entorno:
   Crea un archivo llamado `.env` en la raiz del proyecto y añade el usuario de TikTok que deseas monitorear:

```
TIKTOK_USERNAME=@usuario_objetivo

```

## Uso

1. Inicia el motor de Ollama en una terminal separada con el modelo Llama 3:

```
ollama run llama3

```

2. Ejecuta el bot en tu terminal principal:

```
python main.py

```

La consola registrara las conexiones exitosas, los comentarios detectados y la respuesta generada por el LLM. El audio se emitira por la salida predeterminada de tu computadora.

## Advertencia de Seguridad

Como este repositorio es publico, verifica siempre que el archivo `.env` este declarado dentro de tu archivo `.gitignore`. Nunca realices commits de credenciales, nombres de usuario reales en produccion o claves de API de servicios de voz a este repositorio.