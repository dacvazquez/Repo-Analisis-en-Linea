import streamlit as st
import pandas as pd
from pysentimiento import create_analyzer
from analizer_functions import sentiment_analisys, hate_analisys

# Añadir CSS personalizado para la barra lateral
st.markdown("""
    <style>
    .stRadio > div {
        margin-left: 20px;
    }
    /*Subir un poco el titulo*/
    #deteccion-de-comportamiento-transgresivo-en-redes-sociales{
    padding-top:0;    
    }
    #root > div:nth-child(1) > div.withScreencast > div > div > section.stSidebar.st-emotion-cache-1wqrzgl.e1tphpha0 > div.st-emotion-cache-6qob1r.e1tphpha8 > div.st-emotion-cache-a6qe2i.e1tphpha7 > div > div > div > div > div:nth-child(2) > div > label > div > p{
        font-size: 20px;
        text-align: center;
    }
    button[kind="borderlessIconActive"]{
        margin: 5px 15px;
        margin-bottom: 10px;
    }
    button[kind="borderlessIcon"]{
        margin: 0px 15px;
    }
    .stRadio label {
        font-size: 18px !important;
        padding: 5px;
        margin: 10px 0;
    }
    .stRadio > label {
        font-size: 10px !important;
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


# Inicializar session_state
if 'analysis_df' not in st.session_state:
    st.session_state.analysis_df = pd.DataFrame(columns=['Texto', 'Análisis de Sentimiento', 'Odio', 'Agresividad', 'Objetivismo'])

    
def main():

    st.title("Deteccion de :red[comportamiento transgresivo] en redes sociales")
    st.markdown("<br>", unsafe_allow_html=True)
    with open('textoIntro.txt', "r", encoding="utf-8") as file:
        contenido = file.read() 
    #with st.expander("Instrucciones"):
    #    st.write(contenido)
    with st.container(border=True):
        st.write(contenido)    

main()