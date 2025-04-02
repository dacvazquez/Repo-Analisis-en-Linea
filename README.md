# Análisis de Comportamiento Transgresivo en Redes Sociales

Esta aplicación permite analizar el sentimiento y detectar discurso de odio en textos de comentarios de Twiter utilizando modelos LLM que trabajan con transformers preentrenados con mensajes de twitter para su propósito, esta en desarrollo y es mi proyecto de tesis

## Características

- Análisis de sentimiento de textos
- Detección de discurso de odio
- Análisis múltiple de textos
- Visualización de datos y métricas
- Generación de nubes de palabras

## Instalación

1. Clona el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso Local

Para ejecutar la aplicación localmente:

```bash
streamlit run streamlit_app.py
```

## Desplegado en Streamlit Cloud en https://nve6d8nvuzrys5box6uvav.streamlit.app/
## https://share.streamlit.io

## Estructura del Proyecto

- `streamlit_app.py`: Aplicación principal de Streamlit
- `analizer_functions.py`: Funciones de análisis de texto
- `x_scraper.py`: Funciones para obtener tweets
- `requirements.txt`: Dependencias del proyecto
- `README.md`: Este archivo

## Requisitos

- Python 3.12 o superior
- Conexión a internet para descargar modelos y datos
