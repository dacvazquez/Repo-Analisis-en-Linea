import streamlit as st
import pandas as pd
from analizer_functions import sentiment_analisys, hate_analisys
from model_loader import load_models as lm
import colores_resp as cr

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
    sentiment_analyzer, hate_analizer = lm()
    
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
                sentiment_response=cr.negativo
            elif sentiment == 'POS':
                sentiment='Positivo'
                sentiment_response=cr.positivo
            else:
                sentiment='Neutro'
                sentiment_response=cr.neutro
            
            # Declarar color del Odio
            resp=''
            hateful = False
            aggressive = False
            targeted = False
            
            for clasification in hate:
                if clasification == 'hateful':
                    hateful = True
                    hate_response = cr.odioso
                elif clasification == 'aggressive':
                    aggressive = True
                    hate_response = cr.agresivo
                elif clasification == 'targeted':
                    targeted = True
                    hate_response = cr.dirigido
                elif clasification == 'none':
                    hate_response = cr.no_odioso
                resp+=f"El texto es: {hate_response} con una precisión de {probs_hate[clasification]*100:.2f}%. <br>"
            if resp=='':
                resp=f"El texto es: {cr.no_odioso}"

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
            }, index=None)
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
    uploaded_file = st.file_uploader("Sube un archivo CSV", type=['csv'], help="Solo se aceptan archivos en el mismo formato que los que se descargan desde la app (descargar en el boton de la parte superior derecha de la tabla)")
    
    if uploaded_file is not None and 'last_uploaded_file' not in st.session_state:
        try:
            df = pd.read_csv(uploaded_file, index_col=False)
            # Streamlit guarda la primera columna del indice 
            df = df.drop(df.columns[0],axis=1)
            required_columns = ['Texto', 'Análisis de Sentimiento', 'Odio', 'Agresividad', 'Objetivismo']
            if all(col in df.columns for col in required_columns):
                st.session_state.analysis_df = df
                st.session_state.show_toast = "Archivo importado correctamente 👍"
                st.session_state.last_uploaded_file = uploaded_file.name
                st.rerun()
            else:
                st.error(f"El archivo debe contener las columnas: {', '.join(required_columns)}")
        except Exception as e:
            st.error(f"Error al importar el archivo: {str(e)}")
    
    # Resetear el estado del archivo cuando se limpia
    if st.button("Limpiar Todos los Resultados :wastebasket:"):
        st.session_state.analysis_df = pd.DataFrame(columns=[
            'Texto', 
            'Análisis de Sentimiento',
            'Odio',
            'Agresividad',
            'Objetivismo'
        ])
        st.session_state.last_analysis_results = None
        if 'last_uploaded_file' in st.session_state:
            del st.session_state.last_uploaded_file
        st.session_state.show_toast = "Resultados limpiados correctamente"
        st.rerun()


main() 