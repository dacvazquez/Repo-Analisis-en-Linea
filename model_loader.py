import streamlit as st
from pysentimiento import create_analyzer
import torch
import os
from huggingface_hub import HfFolder

def load_models():
    """
    Carga los modelos de análisis de manera eficiente y con manejo de errores.
    """
    try:
        # Verificar si hay GPU disponible
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Configurar el token de Hugging Face si está disponible
        hf_token = os.getenv("HUGGINGFACE_TOKEN")
        if hf_token:
            HfFolder.save_token(hf_token)
        
        # Cargar modelos
        sentiment_analyzer = create_analyzer(task="sentiment", lang="es")
        hate_analyzer = create_analyzer(task="hate_speech", lang="es")
        
        # Mover modelos a la GPU si está disponible
        if device == "cuda":
            sentiment_analyzer.model = sentiment_analyzer.model.to(device)
            hate_analyzer.model = hate_analyzer.model.to(device)
        
        # Guardar modelos en el estado de la sesión
        st.session_state.sentiment_analyzer = sentiment_analyzer
        st.session_state.hate_analyzer = hate_analyzer
            
        return sentiment_analyzer, hate_analyzer
            
    except Exception as e:
        st.error("""
            ❌ Error al cargar los modelos. Esto puede ocurrir por varias razones:
            
            1. No hay conexión a internet
            2. Los servidores de Hugging Face están temporalmente fuera de servicio
            3. No se tienen los permisos necesarios para descargar los modelos
            
            Por favor, intenta lo siguiente:
            
            1. Verifica tu conexión a internet
            2. Espera unos minutos y recarga la página
            3. Si el problema persiste, contacta al administrador
        """)
        st.error(e)
        st.stop()
        return None, None 