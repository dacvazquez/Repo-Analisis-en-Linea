import streamlit as st
from pysentimiento import create_analyzer
from analizer_functions import sentiment_analisys, hate_analisys

@st.cache_resource
def load_analizers():
    sentiment_analyzer = create_analyzer(task="sentiment", lang="es")
    hate_analizer = create_analyzer(task="hate_speech", lang="es")
    return sentiment_analyzer, hate_analizer

def main():
    st.title("Análisis de Texto")
    
    # Cargar analizadores
    sentiment_analyzer, hate_analizer = load_analizers()
    
    option = st.selectbox("Elige una opción", ["Análisis de Sentimiento", "Detección de Odio"])
    st.markdown("<br>", unsafe_allow_html=True)
    
    if option == "Análisis de Sentimiento":
        text_input = st.text_area("Escriba el texto para realizar el análisis de sentimiento")
        if st.button("Analizar Sentimiento"):
            with st.spinner('Analizando sentimiento...'):
                resp, prob, fig = sentiment_analisys(text_input, sentiment_analyzer)
            st.markdown(resp, unsafe_allow_html=True)
            with st.container():
                st.write("### Distribución de Sentimientos")
                st.plotly_chart(fig, use_container_width=True)
    elif option == "Detección de Odio":             
        text_input = st.text_area("Escriba el texto para realizar detección de Odio") 
        if st.button("Analizar Odio"):
            with st.spinner('Analizando discurso de odio...'):
                hate, hate_probs, fig = hate_analisys(text_input, hate_analizer) 
            st.markdown(hate, unsafe_allow_html=True)
            with st.container():
                st.write("### Distribución de Sentimientos")
                st.plotly_chart(fig, use_container_width=True)


main() 