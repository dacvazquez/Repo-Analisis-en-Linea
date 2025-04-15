import streamlit as st
# Configurar el ancho máximo de la página
st.set_page_config(
    layout="wide",
    page_title="Análisis de Comportamiento Transgresivo en Redes Sociales",
    page_icon="Icons/eye.svg",
)

# Navegación personalizada
pg = st.navigation([
    st.Page("pages/Home.py", title="", icon="🏠"),
    st.Page("pages/1_Individual_Analysis.py", title="Análisis de Texto", icon="🔤"),
    st.Page("pages/2_Tweets.py", title="Extracción de Tweets", icon="🐦"),
    st.Page("pages/3_Social_Media_Scraper.py", title="Extracción de Comentarios", icon="📱"),
    st.Page("pages/4_Multiple_Analysis.py", title="Análisis Múltiple", icon="🌐"),
    st.Page("pages/5_Dashboard.py", title="Dashboard", icon="📊")
])

pg.run()