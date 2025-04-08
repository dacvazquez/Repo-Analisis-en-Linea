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
        st.session_state.analysis_df = pd.DataFrame(columns=['Texto', 'Análisis de Sentimiento', 'Análisis de Odio'])
    
    # Cargar analizadores
    sentiment_analyzer, hate_analizer = load_analizers()
    
    # Entrada de texto
    st.subheader("Añadir Nuevo Texto")
    new_text = st.text_area("Ingrese el texto a analizar")
    
    if st.button("Analizar y Añadir"):
        if new_text:
            # Realizar análisis
            sentiment, prob_sentiment, fig_sentiment = sentiment_analisys(new_text, sentiment_analyzer)
            hate, probs_hate, fig_hate = hate_analisys(new_text, hate_analizer)
            
            # Declarar color del sentimiento
            if sentiment == 'NEG':
                sentiment_response="**<font color='red'>Negativo</font>**"
            elif sentiment == 'POS':
                sentiment_response="**<font color='green'>Positivo</font>**"
            else:
                sentiment_response="**<font color='grey'>Neutro</font>**"
            
            # Declarar color del Odio
            resp=''
            for clasification in hate:
                if clasification == 'hateful':
                    hate_response = "**<font color='red'>Odioso</font>**"
                elif clasification == 'aggressive':
                    hate_response = "**<font color='orange'>Agresivo</font>**"
                elif clasification == 'targeted':
                    hate_response = "**<font color='yellow'>Dirigido</font>**"
                resp+=f"El texto es: {hate_response} con un rating de {probs_hate[clasification]*100:.2f}%. <br>"
            if resp=='':
                resp=f"El texto es: **<font color='green'>No odioso</font>**"

            # Desplegar resultados
            try:
                sentiment_result =f"El sentimiento es {sentiment_response} con una intensidad de {prob_sentiment:.2f}"
                st.write(sentiment_result, unsafe_allow_html=True)
                st.write(resp, unsafe_allow_html=True)
            except Exception as e:
                st.write(e) 
                
            # Añadir al DataFrame
            new_row = pd.DataFrame({
                'Texto': [new_text],
                'Análisis de Sentimiento': [sentiment],
                'Análisis de Odio': [hate]
            })
            st.session_state.analysis_df = pd.concat([st.session_state.analysis_df, new_row], ignore_index=True)
            st.toast("Texto analizado y añadido correctamente")
        else:
            st.warning("Por favor, ingrese un texto para analizar")
            
    # Mostrar DataFrame existente
    if not st.session_state.analysis_df.empty:
        st.subheader("Resultados del Análisis")
        st.dataframe(st.session_state.analysis_df)
        
    # Opciones para importar/exportar
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Importar Datos")
        uploaded_file = st.file_uploader("Sube un archivo CSV", type=['csv'])
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                if all(col in df.columns for col in ['Texto', 'Análisis de Sentimiento', 'Análisis de Odio']):
                    st.session_state.analysis_df = df
                    st.toast("Archivo importado correctamente")
                else:
                    st.error("El archivo debe contener las columnas: Texto, Análisis de Sentimiento, Análisis de Odio")
            except Exception as e:
                st.error(f"Error al importar el archivo: {str(e)}")
    
    with col2:
        st.subheader("Exportar Datos")
        if not st.session_state.analysis_df.empty:
            csv = st.session_state.analysis_df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
            st.download_button(
                label="Descargar como CSV",
                data=csv,
                file_name="analisis_textos.csv",
                mime="text/csv"
            )
    
    # Opción para limpiar el DataFrame
    if st.button("Limpiar Todos los Resultados"):
        st.session_state.analysis_df = pd.DataFrame(columns=['Texto', 'Análisis de Sentimiento', 'Análisis de Odio'])
        st.toast("Resultados limpiados correctamente")

if __name__ == "__main__":
    main() 