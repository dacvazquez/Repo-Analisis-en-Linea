import streamlit as st
from pysentimiento import create_analyzer
import torch
import os
import shutil
from huggingface_hub import HfFolder, snapshot_download
from pathlib import Path

def clear_huggingface_cache():
    """Limpia la caché de Hugging Face para forzar la re-descarga de modelos corruptos"""
    try:
        # Obtener el directorio de caché de Hugging Face
        cache_dir = Path.home() / ".cache" / "huggingface"
        
        if cache_dir.exists():
            # Buscar directorios de modelos de pysentimiento
            for model_dir in cache_dir.rglob("*pysentimiento*"):
                if model_dir.is_dir():
                    shutil.rmtree(model_dir, ignore_errors=True)
            
            # También limpiar archivos de tokenizer corruptos
            for tokenizer_file in cache_dir.rglob("tokenizer.json"):
                if tokenizer_file.exists():
                    # Verificar si el archivo parece corrupto (muy grande o muy pequeño)
                    file_size = tokenizer_file.stat().st_size
                    if file_size > 5000000 or file_size < 1000000:  # El tamaño esperado ~1.3MB
                        tokenizer_file.unlink(missing_ok=True)
        
        return True
    except Exception as e:
        return False

def load_models(force_redownload=False):
    """
    Carga los modelos de análisis de sentimiento y detección de odio.
    
    Args:
        force_redownload (bool): Si True, fuerza la re-descarga de los modelos
    """
    try:
        # Verificar si hay GPU disponible
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Configurar el token de Hugging Face si está disponible
        hf_token = os.getenv("HUGGINGFACE_TOKEN")
        if hf_token:
            HfFolder.save_token(hf_token)
        
        # Si se solicita re-descarga forzada, limpiar caché primero
        if force_redownload:
            with st.spinner("Limpiando caché corrupta..."):
                clear_huggingface_cache()
        
        # Cargar modelos 
        with st.spinner("Descargando y cargando modelos de análisis..."):
            sentiment_analyzer = create_analyzer(
                task="sentiment", 
                lang="es",
                force_download=force_redownload 
            )
            
            hate_analyzer = create_analyzer(
                task="hate_speech", 
                lang="es",
                force_download=force_redownload
            )
            
            # Mover modelos a la GPU si está disponible
            if device == "cuda":
                sentiment_analyzer.model = sentiment_analyzer.model.to(device)
                hate_analyzer.model = hate_analyzer.model.to(device)
        
        # Guardar modelos en el estado de la sesión
        st.session_state.sentiment_analyzer = sentiment_analyzer
        st.session_state.hate_analyzer = hate_analyzer
        
        return sentiment_analyzer, hate_analyzer
            
    except Exception as e:
        error_msg = str(e)
        
        # Detectar errores específicos de los archivos problemáticos >:(
        if "Consistency check failed" in error_msg or "tokenizer.json" in error_msg:
            st.error("""
                Error detectado: Archivos de modelo corruptos detectados.
                
                Esto suele ocurrir por interrupciones en la descarga o problemas de red.
            """)
            
            # Mostrar botón para intentar re-descarga forzada
            if st.button("Intentar re-descarga forzada", type="primary"):
                st.rerun()
            
            # Limpiar caché automáticamente
            with st.spinner("Limpiando caché corrupta..."):
                clear_huggingface_cache()
            
            # Intentar cargar con re-descarga forzada
            try:
                with st.spinner("Reintentando con descarga forzada..."):
                    result = load_models(force_redownload=True)
                return result
            except Exception as retry_error:
                st.error(f"Error persistente: {retry_error}")
                st.stop()
                return None, None
        else:
            # Sino lanzar el error genérico, si te pasa esto rézale al de arriba 
            st.error("""
                Error al cargar los modelos. Esto puede ocurrir por varias razones:
                
                1. No hay conexión a internet
                2. Los servidores de Hugging Face están temporalmente fuera de servicio
                3. No se tienen los permisos necesarios para descargar los modelos
                
                Por favor, intenta lo siguiente:
                
                1. Verifica tu conexión a internet
                2. Espera unos minutos y recarga la página
                3. Si el problema persiste, contacta al administrador
            """)
            st.error(f"Detalles del error: {error_msg}")
            st.stop()
            return None, None 