import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pysentimiento import create_analyzer
from analizer_functions import sentiment_analisys, hate_analisys
from testing_scraper import get_tweets_and_replies

# Inicializar session_state
if 'analysis_df' not in st.session_state:
    st.session_state.analysis_df = pd.DataFrame(columns=['Texto', 'Análisis de Sentimiento', 'Análisis de Odio'])

@st.cache_resource
def load_analizers():
    # Para análisis de sentimiento
    sentiment_analyzer = create_analyzer(task="sentiment", lang="es")
    # Para detección de discurso de odio
    hate_analizer = create_analyzer(task="hate_speech", lang="es")
    return sentiment_analyzer, hate_analizer

@st.cache_data
def analyze_text(text, sentiment_analyzer, hate_analizer):
    """Función optimizada para analizar texto y devolver los resultados"""
    resp_sentiment, _ = sentiment_analisys(text, sentiment_analyzer)
    resp_hate, _ = hate_analisys(text, hate_analizer)
    
    # Extraer resultados
    sentiment_result = resp_sentiment.split("El sentimiento es: ")[1].split("</p>")[0]
    hate_result = resp_hate.split("El texto es: ")[1].split("</p>")[0]
    
    return sentiment_result, hate_result

# Main app logic
def main():
    st.title("Procesamiento de Texto en Redes Sociales")
    
    # Cargar analizadores una sola vez
    sentiment_analyzer, hate_analizer = load_analizers()
    
    with st.sidebar:
        st.header("Navegación")
        opcion = st.radio(
            "Selecciona una opción:",
            ("Analisis de Texto", "Obtener Tweets", "Analizar Varios")
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
                if 'tweets' not in st.session_state:
                    st.session_state.tweets = None
                    
                if st.session_state.tweets:
                    st.write("Tweets almacenados:", st.session_state.tweets)
                else:
                    # Obtener los tweets si no están en session_state
                    with st.spinner('Obteniendo tweets...'):
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
        option = st.selectbox("Elige una opción", ["Análisis de Sentimiento", "Detección de Odio"])
        st.markdown("<br>", unsafe_allow_html=True)
        if option == "Análisis de Sentimiento":
            text_input = st.text_area("Escriba el texto para realizar el analisis de sentimiento")
            if st.button("Analizar Sentimiento"):
                with st.spinner('Analizando sentimiento...'):
                    resp, fig = sentiment_analisys(text_input, sentiment_analyzer)
                st.markdown(resp, unsafe_allow_html=True)
                with st.container():
                    st.write("### Distribución de Sentimientos")
                    st.plotly_chart(fig, use_container_width=True)
        elif option == "Detección de Odio":             
            text_input = st.text_area("Escriba el texto para relizar detección de Odio") 
            if st.button("Analizar Odio"):
                with st.spinner('Analizando discurso de odio...'):
                    resp, fig = hate_analisys(text_input, hate_analizer) 
                st.markdown(resp, unsafe_allow_html=True)
                with st.container():
                    st.write("### Distribución de Sentimientos")
                    st.plotly_chart(fig, use_container_width=True)

    if opcion == "Analizar Varios":
        st.header("Análisis Múltiple de Textos")
        
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
                
                #declarar color del sentimiento
                if sentiment == 'NEG':
                    sentiment_response="**<font color='red'>Negativo</font>**"
                elif sentiment == 'POS':
                    sentiment_response="**<font color='green'>Positivo</font>**"
                else:
                    sentiment_response="**<font color='grey'>Neutro</font>**"
                
                #declarar color del Odio
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
                except e:
                    st.write(e) 
                    
                # Añadir al DataFrame
                new_row = pd.DataFrame({
                    'Texto': [new_text],
                    'Análisis de Sentimiento': [sentiment],
                    #'Análisis de Odio': [hate] if hate!=[] else "No odioso"
                    'Análisis de Odio': [hate]
                })
                st.session_state.analysis_df = pd.concat([st.session_state.analysis_df, new_row], ignore_index=True)
                st.success("Texto analizado y añadido correctamente")
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
                        st.success("Archivo importado correctamente")
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
            st.success("Resultados limpiados correctamente")
if __name__ == "__main__":
    main()