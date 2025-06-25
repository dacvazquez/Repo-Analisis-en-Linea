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

# Añadir CSS personalizado para la barra lateral
st.markdown("""
    <style>
    .stRadio > div {
        margin-left: 20px;
    }
    
    /*Bajar un poco el header del sidebar*/
    div[data-testid="stSidebarHeader"]{
    margin-top: 20px;
    }
    
    /*Subir un poco el titulo*/
    #deteccion-de-comportamiento-transgresivo-en-redes-sociales{
    padding-top:0;    
    }
    
    button[kind="borderlessIconActive"]{
        margin: 5px 15px;
        margin-bottom: 10px;
    }
    button[kind="borderlessIcon"]{
        margin: 0px 15px;
    }
    /* CSS de la columna derecha */
    div[data-testid="column"]:nth-child(2) {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: #888 #f0f2f6;
    }
    
    /* Estilo para la barra de desplazamiento */
    div[data-testid="column"]:nth-child(2)::-webkit-scrollbar {
        width: 8px;
    }
    
    div[data-testid="column"]:nth-child(2)::-webkit-scrollbar-track {
        background: #f0f2f6;
        border-radius: 4px;
    }
    
    div[data-testid="column"]:nth-child(2)::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }
    
    div[data-testid="column"]:nth-child(2)::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    
    /*Fixear l*/
    div.stColumn.st-emotion-cache-1862nrq.eu6p4el2{
         margin-left: 12px;
         display: inline-block;
         height: 400px;
         width: ;
    }
    div[data-testid="column"]:nth-child(2) h3 {
        color: #1f77b4;
        margin-bottom: 20px;
    }
    /*Css para los metric*/
    div[data-testid="column"]:nth-child(2) .stMetric {
        background-color: white;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    /*CSS para los separadores*/
    div[data-testid="column"]:nth-child(2) hr {
        margin: 20px 0;
    }
    /*Css para las listas*/
    div[data-testid="column"]:nth-child(2) ul {
        list-style-type: none;
        padding-left: 20px;
    }
    /*Css para los items de las listas*/
    div[data-testid="column"]:nth-child(2) ul li {
        margin: 10px 0;
        position: relative;
    }
    /*Css para el icono de la lista*/
    div[data-testid="column"]:nth-child(2) ul li:before {
        content: "•";
        color: #1f77b4;
        font-weight: bold;
        position: absolute;
        left: -15px;
    }
    </style>
""", unsafe_allow_html=True)


with st.sidebar:
        if 'analysis_df' not in st.session_state or st.session_state.analysis_df.empty:
            st.image("Icons/eye.svg", use_container_width=True)
        if 'analysis_df' in st.session_state and not st.session_state.analysis_df.empty:
            df = st.session_state.analysis_df
            
            # Métricas básicas
            st.metric(label="### Total de textos analizados", value=len(df))
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
# Verificar si existen datos almacenados
has_data = 'analysis_df' in st.session_state and not st.session_state.analysis_df.empty

pg = st.navigation([
    st.Page("app_pages/Home.py", title="Inicio", icon="🏠"),
    # st.Page("app_pages/1_Individual_Analysis.py", title="Detección de Comportamiento", icon="🔍"),
    st.Page("app_pages/2_Tweets.py", title="Extracción de Tweets", icon="🐦"),
    #st.Page("app_pages/3_Social_Media_Scraper.py", title="Extracción de Comentarios", icon="📱"),
    st.Page("app_pages/4_Multiple_Analysis.py", title="Análisis de Texto", icon="🌐"),
    *([st.Page("app_pages/5_Dashboard.py", title="Estadísticas del Análisis", icon="📊"),
       st.Page("app_pages/6_Word_Analysis.py", title="Importancia de Palabras", icon="🔤"),
       st.Page("app_pages/7_Tabla_Resultados.py", title="Tabla de Resultados", icon="🔍")] if has_data else [])
])

pg.run()