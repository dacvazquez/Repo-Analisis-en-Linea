import streamlit as st
from analizer_functions import sentiment_analisys, hate_analisys
from model_loader import load_models as lm
import colores_resp as cr

def main():
    st.title("Análisis de Texto")
    
    # Cargar analizadores
    sentiment_analyzer, hate_analizer = lm()
    
    option = st.selectbox("Elige una opción", ["Análisis de Sentimiento", "Detección de Odio"])
    st.markdown("<br>", unsafe_allow_html=True)
    
    if option == "Análisis de Sentimiento":
        text_input = st.text_area("Texto a realizar análisis de sentimiento")
        if st.button("Analizar Sentimiento"):
            with st.spinner('Analizando sentimiento...'):
                sentiment, sent_probs, fig = sentiment_analisys(text_input, sentiment_analyzer)
                
            # Declarar color del sentimiento
            if sentiment == 'NEG':
                color_resp=cr.negativo
            elif sentiment == 'POS':
                color_resp=cr.positivo
            else:
                color_resp=cr.neutro

            st.markdown(f"El texto es sentimentalmente: {color_resp}", unsafe_allow_html=True)
            with st.container():
                st.write("### Distribución de Sentimientos")
                st.plotly_chart(fig, use_container_width=True)
    elif option == "Detección de Odio":             
        text_input = st.text_area("Texto a realizar detección de Odio") 
        if st.button("Analizar Odio"):
            with st.spinner('Analizando discurso de odio...'):
                hate, hate_probs, fig = hate_analisys(text_input, hate_analizer) 
                
            # Declarar color del Odio
            resp=''
            for clasification in hate:
                if clasification == 'hateful':
                    hate_response = cr.odioso
                elif clasification == 'aggressive':
                    hate_response = cr.agresivo
                elif clasification == 'targeted':
                    hate_response = cr.dirigido
                elif clasification == 'none':
                    hate_response = cr.no_odioso
                resp+=f"El texto es: {hate_response} con una precisión de {hate_probs[clasification]*100:.2f}%. <br>"
            if resp=='':
                resp=f"El texto es: **<font color='green'>No odioso</font>**"
            st.markdown(resp, unsafe_allow_html=True)
            with st.container():
                st.write("### Metricas de Odio")
                st.plotly_chart(fig, use_container_width=True)


main() 