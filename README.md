# TikTok Live AI Bot - Edicion Makanaky

Este repositorio contiene un bot interactivo desarrollado en Python para transmisiones de TikTok Live. Procesa eventos en tiempo real (comentarios y regalos) y genera respuestas de voz utilizando un modelo de lenguaje local en Ollama y un motor de Texto a Voz (TTS).

El bot cuenta con un panel web interactivo en 3D desarrollado con Three.js que permite visualizar al personaje, sincronizar el movimiento de la boca con el microfono o audio y controlar el encendido/apagado del bot.

## Caracteristicas Principales

* Escucha de Eventos en Tiempo Real: Captura comentarios y regalos de TikTok Live de forma asincrona mediante TikTokLive v7.
* Reintento Automatico de Conexion: Si el usuario configurado esta desconectado (offline), el sistema no se cierra; mantiene el servidor web activo y reintenta conectarse cada 15 segundos hasta que inicie el directo.
* Modelo de Lenguaje Local: Genera respuestas personalizadas con Ollama utilizando el modelo Llama 3.1 sin costos de API y con privacidad local.
* Sintesis de Voz Asincrona: Utiliza pyttsx3 gestionado mediante una cola asyncio.Queue para evitar colisiones y superposicion de audio.
* Panel de Control 3D Web: Interfaz construida con Three.js que incluye un avatar animado, plancha de cocina con efectos, sincronizacion de movimiento de boca por nivel de audio y botones de control vinculados al backend.
* Servidor API Local: Construido con aiohttp en el puerto 5000 con soporte CORS para la comunicacion fluida entre el archivo HTML y Python.
* Atajo Global de Teclado: Permite activar o pausar el bot en cualquier momento pulsando la tecla F9.
* Compatibilidad con Windows: Salida de consola configurada con vaciado inmediato y codificacion UTF-8 para evitar errores de caracteres.

## Requisitos Previos

* Python 3.8 o superior (compatible con Python 3.10, 3.11, 3.12, 3.13 y 3.14)
* Git
* Ollama instalado en el sistema

## Instalacion y Configuracion

1. Clonar el repositorio:

```bash
git clone https://github.com/gerargram2006/tiktok-ia-makanaky.git
cd tiktok-ia-makanaky
```

2. Crear y activar el entorno virtual:

En Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

En Windows (CMD):
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

En Linux o macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instalar las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

4. Configurar las variables de entorno:
Crear un archivo llamado `.env` en la raiz del proyecto con el nombre de usuario de TikTok que se desea monitorear (no es obligatorio incluir el simbolo @):

```env
TIKTOK_USERNAME=tu_usuario_de_tiktok
```

## Guia de Uso

1. Iniciar Ollama con el modelo Llama 3.1:
En una terminal independiente, iniciar el modelo ejecutando:

```bash
ollama run llama3.1
```

2. Ejecutar el script principal:
En tu terminal con el entorno virtual activado (o como Administrador en Windows para permitir que la tecla F9 funcione globalmente):

```bash
py main.py
```
O bien:
```bash
python main.py
```

Al iniciar, la consola mostrara:
* El estado del servidor web en http://localhost:5000
* El intento de conexion al Live de TikTok. Si el usuario esta offline, la consola indicara el estado y continuara reintentando cada 15 segundos sin cerrar el programa.

3. Abrir el panel de control 3D:
Hacer doble clic en el archivo `index.html` para abrirlo en cualquier navegador web.

Desde el panel se puede:
* Pulsar "PRENDER MAKANAKY" para activar o pausar las respuestas de la IA.
* Pulsar "PROBAR ¡GAAAA!" para reproducir la animacion de habla de prueba en 3D.
* Pulsar "VINCULAR VOZ CON BOCA 3D" para permitir que el microfono module la boca del avatar en tiempo real.
* Usar el mouse para rotar la camara (clic izquierdo) y hacer zoom (rueda del mouse).
* Integrar la interfaz en OBS Studio como "Fuente de Navegador" para mostrar al personaje animado en directos.

## Control por Teclado

* Tecla F9: Alterna entre el estado ACTIVADO y SILENCIADO del bot en cualquier momento mientras el script este ejecutandose.