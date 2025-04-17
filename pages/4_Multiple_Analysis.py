import streamlit as st
import pandas as pd
from pysentimiento import create_analyzer
from analizer_functions import sentiment_analisys, hate_analisys

@st.cache_resource
def load_analizers():
    sentiment_analyzer = create_analyzer(task="sentiment", lang="es")
    hate_analizer = create_analyzer(task="hate_speech", lang="es")
    return sentiment_analyzer, hate_analizer

def main():
    st.title("Análisis Múltiple de Textos")
    
    # Inicializar DataFrame en session_state si no existe
    if 'analysis_df' not in st.session_state:
        st.session_state.analysis_df = pd.DataFrame(columns=[
            'Texto', 
            'Análisis de Sentimiento',
            'Odio',
            'Agresividad',
            'Objetivismo'
        ])
    
    # Inicializar resultados del análisis si no existen
    if 'last_analysis_results' not in st.session_state:
        st.session_state.last_analysis_results = None
    
    # Mostrar toast si existe en session_state
    if 'show_toast' in st.session_state:
        st.toast(st.session_state.show_toast)
        del st.session_state.show_toast
    
    # Mostrar resultados del último análisis si existen
    if st.session_state.last_analysis_results:
        sentiment_result, hate_result = st.session_state.last_analysis_results
        st.write(sentiment_result, unsafe_allow_html=True)
        st.write(hate_result, unsafe_allow_html=True)
    
    # Cargar analizadores
    sentiment_analyzer, hate_analizer = load_analizers()
    
    # Entrada de texto
    st.subheader("Añadir Nuevo Texto")
    new_text = st.text_area("Ingrese el texto a analizar 🔍")
    
    if st.button("Analizar y Añadir"):
        if new_text:
            # Realizar análisis
            sentiment, prob_sentiment, fig_sentiment = sentiment_analisys(new_text, sentiment_analyzer)
            hate, probs_hate, fig_hate = hate_analisys(new_text, hate_analizer)
            
            # Declarar color del sentimiento
            if sentiment == 'NEG':
                sentiment='Negativo'
                sentiment_response="**<font color='red'>Negativo</font>**"
            elif sentiment == 'POS':
                sentiment='Positivo'
                sentiment_response="**<font color='green'>Positivo</font>**"
            else:
                sentiment='Neutro'
                sentiment_response="**<font color='grey'>Neutro</font>**"
            
            # Declarar color del Odio
            resp=''
            hateful = False
            aggressive = False
            targeted = False
            
            for clasification in hate:
                if clasification == 'hateful':
                    hateful = True
                    hate_response = "**<font color='red'>Odioso</font>**"
                elif clasification == 'aggressive':
                    aggressive = True
                    hate_response = "**<font color='orange'>Agresivo</font>**"
                elif clasification == 'targeted':
                    targeted = True
                    hate_response = "**<font color='yellow'>Dirigido</font>**"
                elif clasification == 'none':
                    hate_response = "**<font color='green'>No odioso</font>**"
                resp+=f"El texto es: {hate_response} con un rating de {probs_hate[clasification]*100:.2f}%. <br>"
            if resp=='':
                resp=f"El texto es: **<font color='green'>No odioso</font>**"

            # Guardar resultados para mostrar después del rerun
            sentiment_result = f"El sentimiento es {sentiment_response} con una intensidad de {prob_sentiment:.2f}"
            st.session_state.last_analysis_results = (sentiment_result, resp)
                
            # Añadir al DataFrame
            new_row = pd.DataFrame({
                'Texto': [new_text],
                'Análisis de Sentimiento': [sentiment],
                'Odio': [hateful],
                'Agresividad': [aggressive],
                'Objetivismo': [targeted]
            })
            st.session_state.analysis_df = pd.concat([st.session_state.analysis_df, new_row], ignore_index=True)
            st.session_state.show_toast = "Texto analizado y añadido correctamente 👍"
            st.rerun()
        else:
            st.warning("Por favor, ingrese un texto para analizar")
            
    # Mostrar DataFrame existente
    if not st.session_state.analysis_df.empty:
        st.subheader("Resultados del Análisis")
        st.write(st.session_state.analysis_df)
        
    # Opciones para importar
    st.subheader("Importar Datos")
    uploaded_file = st.file_uploader("Sube un archivo CSV", type=['csv'])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            required_columns = ['Texto', 'Análisis de Sentimiento', 'Odio (hateful)', 'Agresividad (aggressive)', 'Objetivismo (targeted)']
            if all(col in df.columns for col in required_columns):
                st.session_state.analysis_df = df
                st.session_state.show_toast = "Archivo importado correctamente 👍"
                st.rerun()
            else:
                st.error(f"El archivo debe contener las columnas: {', '.join(required_columns)}")
        except Exception as e:
            st.error(f"Error al importar el archivo: {str(e)}")

    # Opción para limpiar el DataFrame
    if st.button("Limpiar Todos los Resultados :wastebasket:"):
        st.session_state.analysis_df = pd.DataFrame(columns=[
            'Texto', 
            'Análisis de Sentimiento',
            'Odio',
            'Agresividad',
            'Objetivismo'
        ])
        st.session_state.last_analysis_results = None
        st.session_state.show_toast = "Resultados limpiados correctamente"
        st.rerun()


main() 