import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pysentimiento import create_analyzer
from analizer_functions import sentiment_analisys, hate_analisys
from x_scraper import get_tweets_and_replies
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from nltk.corpus import stopwords
import nltk

# Download required NLTK data
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Configurar el ancho máximo de la página (debe ser la primera llamada de Streamlit)
st.set_page_config(
    layout="wide",
    page_title="Análisis de Comportamiento Transgresivo en Redes Sociales",
    page_icon="Icons/eye.svg"
    )

# Añadir CSS personalizado para la barra lateral
st.markdown("""
    <style>
    .stRadio > div {
        margin-left: 20px;
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
    
    /*Separar un poco la segunda columna de la primera*/
    div.stColumn.st-emotion-cache-1862nrq.eu6p4el2{
        margin-left: 12px;
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

captions=("Analizar el sentimiento y el odio de un texto específico", 
          "Para obtener Tweets de un usuario específico", 
          "Para analizar varios textos a la vez y visualizar los resultados en un dataframe", 
          "Para observar los análisis cuantitativos y cualitativos sobre los textos almacenados en el dataframe")

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


def main():
    # Crear el layout principal con dos columnas
    main_col, right_col = st.columns([7, 3])
    
    with main_col:
        st.title("Procesamiento de Texto en Redes Sociales")
        
        # Cargar analizadores una sola vez
        sentiment_analyzer, hate_analizer = load_analizers()
        
        with st.sidebar:
            st.write("# Navegación")
            opcion = st.radio(
                label="Selecciona una opción:",
                options=("Analisis de Texto", "Obtener Tweets", "Analizar Varios", "Análisis de Datos")
            )
            feed_level=st.feedback("faces")
            if feed_level:
                st.success("### Gracias por su feedback",icon=":material/thumb_up:")
    
    with right_col:
        st.markdown("### 📊 Panel de Información")
        
        st.image("Icons/eye.svg", width=200)
        st.markdown("""
        ---
        ### 📈 Información
        - Total de textos analizados
        - Última actualización
        - Estado del sistema
        """)
        
        if 'analysis_df' in st.session_state and not st.session_state.analysis_df.empty:
            st.markdown("### 📊 Resumen de Datos")
            st.metric("Total de textos analizados", len(st.session_state.analysis_df))
            st.metric("Última Actualización", pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"))
    
    if opcion == "Obtener Tweets":
        with main_col:
            st.header("Obtener Tweets de un Usuario")
            st.write("ID de usuario de la universidad: 2277112266")
            
            # Entrada de usuario
            user_input = st.text_input("Ingresa el ID de usuario o @usuario:")
            max_tweets = st.number_input("Cantidad de tweets a visualizar:", min_value=1, max_value=20, value=10)
            
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
                        csv = df.to_csv(index=False).encode('utf-8-sig')
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
        with main_col:
            option = st.selectbox("Elige una opción", ["Análisis de Sentimiento", "Detección de Odio"])
            st.markdown("<br>", unsafe_allow_html=True)
            if option == "Análisis de Sentimiento":
                text_input = st.text_area("Escriba el texto para realizar el analisis de sentimiento")
                if st.button("Analizar Sentimiento"):
                    with st.spinner('Analizando sentimiento...'):
                        resp, prob, fig = sentiment_analisys(text_input, sentiment_analyzer)
                    st.markdown(resp, unsafe_allow_html=True)
                    with st.container():
                        st.write("### Distribución de Sentimientos")
                        st.plotly_chart(fig, use_container_width=True)
            elif option == "Detección de Odio":             
                text_input = st.text_area("Escriba el texto para relizar detección de Odio") 
                if st.button("Analizar Odio"):
                    with st.spinner('Analizando discurso de odio...'):
                        hate, hate_probs, fig = hate_analisys(text_input, hate_analizer) 
                    st.markdown(hate, unsafe_allow_html=True)
                    with st.container():
                        st.write("### Distribución de Sentimientos")
                        st.plotly_chart(fig, use_container_width=True)

    if opcion == "Analizar Varios":
        with main_col:
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

    if opcion == "Análisis de Datos":
        with main_col:
            st.header("Dashboard de Análisis")
            
            if st.session_state.analysis_df.empty:
                st.warning("No hay datos para analizar. Por favor, ingresa algunos textos primero.")
            else:
                # Primera fila: Métricas principales
                st.divider()
                st.markdown("### Métricas Principales")
                
                # Calcular métricas adicionales
                total_texts = len(st.session_state.analysis_df)
                sentiment_counts = st.session_state.analysis_df['Análisis de Sentimiento'].value_counts()
                dominant_sentiment = sentiment_counts.index[0]
                
                # Calcular porcentajes de sentimientos
                sentiment_percentages = (sentiment_counts / total_texts * 100).apply(lambda x: round(x, 1))
                
                # Calcular métricas de odio
                hate_counts = {'hateful': 0, 'aggressive': 0, 'targeted': 0}
                total_hate = 0
                for hate_list in st.session_state.analysis_df['Análisis de Odio']:
                    for hate_type in hate_counts.keys():
                        if hate_type in hate_list:
                            hate_counts[hate_type] += 1
                            total_hate += 1
                
                # Longitud promedio de textos
                avg_text_length = round(st.session_state.analysis_df['Texto'].str.len().mean(), 1)
                
                # Tasa de odio
                hate_rate = round((total_hate / total_texts * 100), 1)
                
                # Primera fila: Métricas básicas
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("#### 📊 Total de Análisis")
                    st.metric("Total de Textos", total_texts)
                    st.metric("Longitud Promedio", f"{avg_text_length} caracteres")
                
                with col2:
                    st.markdown("#### 😊 Sentimiento")
                    st.metric("Sentimiento Dominante", dominant_sentiment)
                    st.metric("Porcentaje", f"{sentiment_percentages[dominant_sentiment]}%")
                
                with col3:
                    dominant_hate = max(hate_counts.items(), key=lambda x: x[1])[0]
                    st.markdown("#### ⚠️ Análisis de Odio")
                    st.metric("Tipo de Odio Dominante", dominant_hate)
                    # Mostrar tasas individuales para cada tipo de odio
                    for hate_type, count in hate_counts.items():
                        rate = round((count / total_texts * 100), 1)
                        st.metric(f"Tasa de {hate_type}", f"{rate}%")
                
                # Segunda fila: Métricas detalladas
                st.markdown("<br>", unsafe_allow_html=True)
                st.divider()
                st.markdown("### Métricas del Análisis")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("#### 📈 Análisis de Sentimientos")
                    for sentiment, percentage in sentiment_percentages.items():
                        st.metric(
                            f"Sentimiento {sentiment}",
                            f"{percentage}%",
                            f"{sentiment_counts[sentiment]} textos"
                        )
                
                with col2:
                    st.markdown("#### 🎯 Análisis de Odio")
                    for hate_type, count in hate_counts.items():
                        percentage = round((count / total_texts * 100), 1)
                        st.metric(
                            f"Tipo {hate_type}",
                            f"{percentage}%",
                            f"{count} textos"
                        )
                
                with col3:
                    st.markdown("#### 📝 Estadísticas de Texto")
                    st.metric(
                        "Texto más largo",
                        f"{st.session_state.analysis_df['Texto'].str.len().max()} caracteres"
                    )
                    st.metric(
                        "Texto más corto",
                        f"{st.session_state.analysis_df['Texto'].str.len().min()} caracteres"
                    )
                    st.metric(
                        "Desviación estándar",
                        f"{st.session_state.analysis_df['Texto'].str.len().std().round(1)} caracteres"
                    )
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Segunda fila: Gráficos de distribución
                
                st.divider()
                st.markdown("### Distribuciones")
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Distribución de Sentimientos")
                    st.markdown("<br>", unsafe_allow_html=True)
                    # Definir colores para sentimientos
                    sentiment_colors = {
                        'POS': '#2ecc71',  # Verde
                        'NEU': '#95a5a6',  # Gris
                        'NEG': '#e74c3c'   # Rojo
                    }
                    fig_sentiment = go.Figure(data=[go.Pie(
                        labels=sentiment_counts.index,
                        values=sentiment_counts.values,
                        hole=.3,
                        marker=dict(colors=[sentiment_colors.get(label, '#3498db') for label in sentiment_counts.index])
                    )])
                    fig_sentiment.update_layout(height=400, margin=dict(t=20, b=20, l=20, r=20))
                    st.plotly_chart(fig_sentiment, use_container_width=True)
                
                with col2:
                    st.markdown("#### Distribución de Tipos de Odio")
                    st.markdown("<br>", unsafe_allow_html=True)
                    # Definir colores para tipos de odio
                    hate_colors = {
                        'hateful': '#e74c3c',    # Rojo
                        'aggressive': '#f39c12',  # Naranja
                        'targeted': '#9b59b6'     # Púrpura
                    }
                    fig_hate = go.Figure(data=[go.Pie(
                        labels=list(hate_counts.keys()),
                        values=list(hate_counts.values()),
                        hole=.3,
                        marker=dict(colors=[hate_colors.get(label, '#3498db') for label in hate_counts.keys()])
                    )])
                    fig_hate.update_layout(height=400, margin=dict(t=20, b=20, l=20, r=20))
                    st.plotly_chart(fig_hate, use_container_width=True)
                
                # Espaciador
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Tercera fila: Nube de palabras
                st.divider()
                st.markdown("### Nube de Palabras")
                st.markdown("<br>", unsafe_allow_html=True)
                
                col1, col2 = st.columns([3, 1])
                
            
                # Combinar todos los textos
                all_text = ' '.join(st.session_state.analysis_df['Texto'])
                
                # Crear nube de palabras
                wordcloud = WordCloud(
                    width=1200,
                    height=600,  
                    mode="RGBA",
                    background_color="black",
                    max_words=100,
                    max_font_size=150,
                    random_state=42,
                    collocations=False
                ).generate(all_text)
                
                # Mostrar la nube de palabras
                fig, ax = plt.subplots(figsize=(15, 8))  # Aumentado el tamaño
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
            
            
                st.markdown("#### Opciones de Exportación")
                
                # Botón para descargar la imagen
                with open("wordcloud.png", "rb") as file:
                    if st.download_button(
                        label="📥 Descargar Nube de Palabras",
                        data=file,
                        file_name="wordcloud.png",
                        mime="image/png"
                    ):
                        st.success("✅ Nube de palabras guardada correctamente")
                
                # Botón para filtrar stopwords
                if st.button("🔍 Filtrar Stopwords"):
                    # Obtener stopwords en español
                    spanish_stopwords = set(stopwords.words('spanish'))
                    
                    # Combinar todos los textos
                    all_text = ' '.join(st.session_state.analysis_df['Texto'])
                    
                    # Crear nube de palabras con stopwords filtradas
                    wordcloud = WordCloud(
                        width=1200,
                        height=600,  
                        mode="RGBA",
                        background_color=None,
                        max_words=100,
                        max_font_size=150,
                        random_state=42,
                        collocations=False,
                        stopwords=spanish_stopwords
                    ).generate(all_text)
                    
                    # Mostrar la nueva nube de palabras
                    fig, ax = plt.subplots(figsize=(15, 8))
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis('off')
                    st.pyplot(fig)
                    
                    # Guardar la nueva imagen
                    if wordcloud.to_file("wordcloud_transparent.png"):
                        st.success("✅ Nube de palabras actualizada sin stopwords")

if __name__ == "__main__":
    main()