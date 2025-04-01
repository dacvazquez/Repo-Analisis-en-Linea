# Análisis de Comportamiento Transgresivo en Redes Sociales

Esta aplicación permite analizar el sentimiento y detectar discurso de odio en textos de redes sociales.

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
streamlit run app_new.py
```

## Despliegue en Streamlit Cloud

1. Crea una cuenta en [share.streamlit.io](https://share.streamlit.io)
2. Conecta tu repositorio de GitHub
3. Selecciona el repositorio y la rama que quieres desplegar
4. Streamlit Cloud se encargará de todo automáticamente

## Estructura del Proyecto

- `app_new.py`: Aplicación principal de Streamlit
- `analizer_functions.py`: Funciones de análisis de texto
- `testing_scraper.py`: Funciones para obtener tweets
- `requirements.txt`: Dependencias del proyecto
- `README.md`: Este archivo

## Requisitos

- Python 3.8 o superior
- Conexión a internet para descargar modelos y datos
