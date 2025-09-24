# Análisis de Comportamiento Transgresivo en Redes Sociales

Esta aplicación permite analizar el sentimiento y detectar discurso de odio en textos de comentarios de Twitter utilizando modelos LLM que trabajan con transformers preentrenados con mensajes de Twitter para su propósito.

## Características

- **Análisis de Sentimiento**: Clasificación de textos en positivo, negativo o neutral
- **Detección de Discurso de Odio**: Identificación de contenido ofensivo o discriminatorio
- **Análisis Individual**: Análisis de texto único con visualizaciones detalladas
- **Análisis Múltiple**: Procesamiento en lote de múltiples textos
- **Dashboard Interactivo**: Visualización de métricas y estadísticas
- **Análisis de Palabras**: Identificación de términos más importantes
- **Nubes de Palabras**: Generación de visualizaciones de palabras clave
- **Scraping de Redes Sociales**: Extracción de contenido de redes sociales enfocado en Twitter
- **Manejo Automático de Errores**: Haciendo la aplicación fácil de debuguear

## Tecnologías Utilizadas

- **Streamlit**: Framework web para la interfaz de usuario
- **PySentimiento**: Modelos preentrenados para análisis de sentimiento en español
- **Transformers**: Biblioteca de Hugging Face para modelos de lenguaje
- **Plotly**: Visualizaciones interactivas
- **Pandas**: Manipulación y análisis de datos
- **Tweepy**: API de Twitter para extracción de datos 
- **Instaloader**: Scraping de Instagram (requiere planes avanzados)
- **Facebook-scraper**: Extracción de datos de Facebook (requiere planes avanzados)

## Instalación

### Requisitos Previos
- Python 3.8 o superior
- Conexión a internet para descargar modelos
- Git (opcional, para clonar el repositorio)

### Pasos de Instalación

1. **Clona el repositorio:**
```bash
git clone https://github.com/dacvazquez/Repo-Analisis-en-Linea.git
cd Repo-Analisis-en-Linea
```

2. **Crea un entorno virtual (recomendado):**
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

3. **Instala las dependencias:**
```bash
pip install -r requirements.txt
```

## Uso

### Ejecución Local
```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador

### Despliegue en la Nube
- **Streamlit Cloud**: https://transgressive-behavior-sentinel.streamlit.app/
- **Plataforma**: https://share.streamlit.io

## 🔧 Solución de Problemas

### Error de Modelos Corruptos

Ejecuta el script de limpieza:
```bash
python clear_cache.py
```

### Problemas de Conexión

- Verifica tu conexión a internet
- Los modelos se descargan desde Hugging Face Hub
- La primera ejecución puede tardar varios minutos

## Estructura del Proyecto

- `app.py`: Aplicación principal de Streamlit
- `analizer_functions.py`: Funciones de análisis de texto
- `app_pages/`: Directorio donde se encuentran implementadas las páginas de la app streamlit
- `x_scraper.py`: Funciones para obtener tweets
- `requirements.txt`: Dependencias del proyecto
- `README.md`: Este archivo
