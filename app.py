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

@st.cache_resource
def load_analizers():
    
    # Para análisis de sentimiento
    sentiment_analyzer = create_analyzer(task="sentiment", lang="es")
    
    # Para detección de discurso de odio
    hate_analizer = create_analyzer(task="hate_speech", lang="es")

    return sentiment_analyzer, hate_analizer

# Main app logic
def main():
    st.title("Procesamiento de Texto en Redes Sociales")
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
            #st.success("Buscar los demas", icon="👍")
            st.markdown(resp, unsafe_allow_html=True)
            with st.container():
                st.write("### Distribución de Sentimientos")
                st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
