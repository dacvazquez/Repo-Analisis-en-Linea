import streamlit as st
from pages import Home, Tweets, Multiple_Analysis, Social_Media_Scraper, Dashboard
from model_loader import load_models

# Configurar la página
st.set_page_config(
    page_title="Análisis de Sentimiento",
    page_icon="📊",
    layout="wide"
)

# Inicializar modelos
try:
    sentiment_analyzer, hate_analyzer = load_models()
    if sentiment_analyzer is None or hate_analyzer is None:
        st.error("No se pudieron cargar los modelos necesarios. La aplicación no puede continuar.")
        st.stop()
except Exception as e:
    st.error(f"Error al inicializar la aplicación: {str(e)}")
    st.stop()

