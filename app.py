import pandas as pd
import sys
import os
import asyncio
import torch
from model_loader import load_models as lm

# 1. Corrección PyTorch
if hasattr(torch.classes, '__path__'):
    torch.classes.__path__ = [os.path.join(torch.__path__[0], "classes")]
else:
    sys.modules['torch.classes'] = torch

# 2. Configuración asyncio para Windows/Linux
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# 2. Importar Streamlit después de las configuraciones
import streamlit as st

sentiment_analyzer, hate_analizer = lm()

# Configurar el ancho máximo de la página
st.set_page_config(
    layout="wide",
    page_title="Análisis de Comportamiento Transgresivo en Redes Sociales",
    page_icon="Icons/eye.svg",
)
with st.sidebar:
        st.image("Icons/eye.svg", use_container_width=True)
        if 'analysis_df' in st.session_state and not st.session_state.analysis_df.empty:
            df = st.session_state.analysis_df
            st.markdown("### 📊 Resumen de Datos")
            
            # Métricas básicas
            st.metric("Total de textos analizados", len(df))
            st.metric("Última Actualización", pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"))
            
            st.markdown("---")
            # Distribución de sentimientos
            st.markdown("### 😊 Distribución de Sentimientos")
            sentiment_counts = df['Análisis de Sentimiento'].value_counts()
            
            # Crear columnas para los sentimientos
            cs = st.columns(len(sentiment_counts), vertical_alignment="center")
            for c, (sentiment, count) in zip(cs, sentiment_counts.items()):
                with c:
                    st.metric(f"{sentiment}", count)
            
            # Métricas de análisis
            st.markdown("### 🤬 Distribución de Odio")
            
            hate_percentage = round((df['Odio'].sum() / len(df) * 100))
            aggressive_percentage = round((df['Agresividad'].sum() / len(df) * 100))
            objective_percentage = round((df['Objetivismo'].sum() / len(df) * 100))
            
            c1,c2,c3=st.columns(3, vertical_alignment="center")
            with c1: st.metric("Odioso", f"{hate_percentage}%")
            with c2: st.metric("Agresivo", f"{aggressive_percentage}%")
            with c3: st.metric("Objetivo", f"{objective_percentage}%")
            

# Navegación personalizada
pg = st.navigation([
    st.Page("app_pages/Home.py", title="Inicio", icon="🏠"),
    # st.Page("app_pages/1_Individual_Analysis.py", title="Análisis de Texto", icon="🔍"),
    st.Page("app_pages/2_Tweets.py", title="Extracción de Tweets", icon="🐦"),
    #st.Page("app_pages/3_Social_Media_Scraper.py", title="Extracción de Comentarios", icon="📱"),
    st.Page("app_pages/4_Multiple_Analysis.py", title="Análisis de Texto", icon="🌐"),
    st.Page("app_pages/5_Dashboard.py", title="Dashboard", icon="📊"),
    st.Page("app_pages/6_Word_Analysis.py", title="Importancia de Palabras", icon="🔤"),
    st.Page("app_pages/7_Tabla_Resultados.py", title="Tabla de Resultados", icon="⚖️"),

])

pg.run()