import streamlit as st
import pandas as pd
from pysentimiento import create_analyzer
from analizer_functions import sentiment_analisys, hate_analisys


# Inicializar session_state
if 'analysis_df' not in st.session_state:
    st.session_state.analysis_df = pd.DataFrame(columns=['Texto', 'Análisis de Sentimiento', 'Odio', 'Agresividad', 'Objetivismo'])

    
def main():

    st.title("Detección de :red[comportamiento transgresivo] en redes sociales")
    st.markdown("<br>", unsafe_allow_html=True)
    with open('textoIntro.txt', "r", encoding="utf-8") as file:
        contenido = file.read() 
    #with st.expander("Instrucciones"):
    #    st.write(contenido)
    with st.container(border=True):
        st.write(contenido)    

main()