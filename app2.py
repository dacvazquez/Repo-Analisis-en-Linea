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

# Main app logic
import streamlit as st

def main():
    st.title("Procesamiento de Texto en Redes Sociales")

    # Inicializar el estado de la sesión si no existe
    if 'opcion_actual' not in st.session_state:
        st.session_state['opcion_actual'] = "Analisis de Texto"  # Opción por defecto

    if 'tweets_data' not in st.session_state:
        st.session_state['tweets_data'] = None  # Almacenar los tweets obtenidos

    if 'text_input_sentimiento' not in st.session_state:
        st.session_state['text_input_sentimiento'] = ""  # Almacenar el texto para análisis de sentimiento

    if 'text_input_odio' not in st.session_state:
        st.session_state['text_input_odio'] = ""  # Almacenar el texto para detección de odio

    if 'sentiment_analysis_result' not in st.session_state:
        st.session_state['sentiment_analysis_result'] = None  # Almacenar el resultado del análisis de sentimiento

    if 'hate_analysis_result' not in st.session_state:
        st.session_state['hate_analysis_result'] = None  # Almacenar el resultado de la detección de odio

    # Sidebar para la navegación
    with st.sidebar:
        st.header("Navegación")
        opcion = st.radio(
            "Selecciona una opción:",
            ("Analisis de Texto", "Obtener Tweets"),
            key='opcion_radio'
        )

    # Actualizar el estado de la opción actual
    if opcion != st.session_state['opcion_actual']:
        st.session_state['opcion_actual'] = opcion
    
    # Lógica para cada opción
    
    if st.session_state['opcion_actual'] == "Obtener Tweets":
        st.header("Obtener Tweets de un Usuario")
        st.write("ID de usuario de la universidad: 2277112266")

        # Entrada de usuario
        if 'user_input' not in st.session_state:    
            st.session_state['user_input'] = st.text_input("Ingresa el ID de usuario o @usuario:")
            st.number_input("Cantidad de tweets a visualizar:", min_value=1, max_value=20, value=10)
        else:
            user_input=st.session_state['user_input']
            st.number_input("Cantidad de tweets a visualizar:", min_value=1, max_value=20, value=10)
            
            
        # Botón para ejecutar la búsqueda
        if st.button("Buscar Tweets"):
            if user_input:
                # Limpiar la entrada del usuario (eliminar @ si está presente)
                user_id = user_input.replace("@", "").strip()

                # Obtener los tweets y comentarios (simulado)
                st.session_state['tweets_data'] = get_tweets_and_replies(user_input, 10)

                if st.session_state['tweets_data']:
                    st.success("Datos obtenidos correctamente.")
                    #st.write("### Vista previa de los datos:")
                    #st.dataframe(st.session_state['tweets_data'])

                    # Exportar a CSV (simulado)
                    csv = "ID,Texto,Creado el,Likes\n1,Este es un tweet de ejemplo,2023-10-01,10\n2,Otro tweet de ejemplo,2023-10-02,20"
                    st.download_button(
                        label="Descargar como CSV",
                        data=csv,
                        file_name=f"tweets_{user_id}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No se encontraron tweets o comentarios.")
            else:
                st.warning("Por favor, ingresa un ID de usuario o @usuario.")

    elif st.session_state['opcion_actual'] == "Analisis de Texto":
        # Cargar analizadores (simulado)
        sentiment_analyzer, hate_analyzer = load_analizers()

        # User input
        option = st.selectbox("Elige una opción", ["Análisis de Sentimiento", "Detección de Odio"], key='option')
        st.markdown("<br>", unsafe_allow_html=True)

        if option == "Análisis de Sentimiento":
            text_input = st.text_area(
                "Escriba el texto para realizar el análisis de sentimiento",
                value=st.session_state['text_input_sentimiento'],
                key='text_input_sentimiento'
            )
            if st.button("Analizar Sentimiento"):
                resp, fig = sentiment_analisys(text_input, sentiment_analyzer)
                st.session_state['sentiment_analysis_result'] = (resp, fig)
                st.markdown(resp, unsafe_allow_html=True)
                with st.container():
                    st.write("### Distribución de Sentimientos")
                    st.plotly_chart(fig, use_container_width=True)

            # Mostrar resultado anterior si existe
            if st.session_state['sentiment_analysis_result']:
                resp, fig = st.session_state['sentiment_analysis_result']
                st.markdown(resp, unsafe_allow_html=True)
                with st.container():
                    st.write("### Distribución de Sentimientos (Anterior)")
                    st.plotly_chart(fig, use_container_width=True)

        elif option == "Detección de Odio":
            text_input = st.text_area(
                "Escriba el texto para realizar detección de Odio",
                value=st.session_state['text_input_odio'],
                key='text_input_odio'
            )
            if st.button("Analizar Odio"):
                resp, fig = hate_analisys(text_input, hate_analyzer)
                st.session_state['hate_analysis_result'] = (resp, fig)
                st.markdown(resp, unsafe_allow_html=True)
                with st.container():
                    st.write("### Distribución de Sentimientos")
                    st.plotly_chart(fig, use_container_width=True)

            # Mostrar resultado anterior si existe
            if st.session_state['hate_analysis_result']:
                resp, fig = st.session_state['hate_analysis_result']
                st.markdown(resp, unsafe_allow_html=True)
                with st.container():
                    st.write("### Distribución de Sentimientos (Anterior)")
                    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()