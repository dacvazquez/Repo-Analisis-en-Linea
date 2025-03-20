import streamlit as st
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from scipy.special import softmax
import plotly.graph_objects as go
from lime.lime_text import LimeTextExplainer
import torch
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from pysentimiento import create_analyzer
from analizer_functions import sentiment_analisys, hate_analisys
from testing_scraper import get_tweets_and_replies


@st.cache_resource
def load_analizers():
    
    # Para análisis de sentimiento
    sentiment_analyzer = create_analyzer(task="sentiment", lang="es")
    
    # Para detección de discurso de odio
    hate_analizer = create_analyzer(task="hate_speech", lang="es")

    return sentiment_analyzer, hate_analizer


sest=st.session_state
# Main app logic
def main():
    st.title("Procesamiento de Texto en Redes Sociales")
    with st.sidebar:
        st.header("Navegación")
        opcion = st.radio(
        "Selecciona una opción:",
        ("Analisis de Texto", "Obtener Tweets")
    
    )
        
    if opcion == "Obtener Tweets":
        st.header("Obtener Tweets de un Usuario")
        st.write("ID de usuario de la universidad: 2277112266")
        
        # Entrada de usuario
        user_input = st.text_input("Ingresa el ID de usuario o @usuario:")
        max_tweets = st.number_input("Cantidad de tweets a visualizar:", min_value=1, max_value=20, value=10)
        
        # Botón para ejecutar la búsqueda
        if st.button("Buscar Tweets"):
            if user_input:
                # Limpiar la entrada del usuario (eliminar @ si está presente)
                user_id = user_input.replace("@", "").strip()
                
                # Verificar si 'tweets' ya está en session_state
                if 'tweets' not in sest:
                    sest.tweets = None
                    
                if sest.tweets:
                    st.write("Tweets almacenados:", sest.tweets)
                else:
                    # Obtener los tweets si no están en session_state
                    container = get_tweets_and_replies(user_id, max_tweets)
                    st.session_state.tweets = container
                    st.write("Tweets obtenidos:", container) 
                
                
                df=None
                if df is not None and not df.empty:
                    st.success("Datos obtenidos correctamente.")
                    st.write("### Vista previa de los datos:")
                    st.dataframe(df)

                    # Exportar a CSV
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Descargar como CSV",
                        data=csv,
                        file_name=f"tweets_{user_id}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("El Data Frame con los tweets esta vacio")
            else:
                st.warning("Por favor, ingresa un ID de usuario o @usuario.")   
 
    if opcion == "Analisis de Texto":
        # User input
        sentiment_analyzer, hate_analizer=load_analizers()
        option = st.selectbox("Elige una opción", ["Análisis de Sentimiento", "Detección de Odio"])
        st.markdown("<br>", unsafe_allow_html=True)
        if option == "Análisis de Sentimiento":
            text_input = st.text_area("Escriba el texto para realizar el analisis de sentimiento")
            if st.button("Analizar Sentimiento"):
                resp, fig=sentiment_analisys(text_input, sentiment_analyzer)
                st.markdown(resp, unsafe_allow_html=True)
                with st.container():
                    st.write("### Distribución de Sentimientos")
                    st.plotly_chart(fig, use_container_width=True)
        elif option == "Detección de Odio":             
            text_input = st.text_area("Escriba el texto para relizar detección de Odio") 
            if st.button("Analizar Odio"):
                resp, fig=hate_analisys(text_input, hate_analizer) 
                st.markdown(resp, unsafe_allow_html=True)
                with st.container():
                    st.write("### Distribución de Sentimientos")
                    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
