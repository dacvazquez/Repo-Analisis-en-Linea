import streamlit as st
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from scipy.special import softmax
import plotly.graph_objects as go
from lime.lime_text import LimeTextExplainer
import torch
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from pysentimiento import create_analyzer


@st.cache_resource
def load_analizers():
    
    # Para análisis de sentimiento
    sentiment_analyzer = create_analyzer(task="sentiment", lang="es")
    
    # Para detección de discurso de odio
    hate_analizer = create_analyzer(task="hate_speech", lang="es")

    return sentiment_analyzer, hate_analizer

# Define sentiment prediction function
def sentiment_analisys(text):
    # Preprocess text
    text_words=[]
    for word in text.split(' '):
        if word.startswith('@') and len(word)>1:
            word='@user'
        elif word.startswith('http'):
            word='http'
        text_words.append(word)
    full_text= ' '.join(text_words)
    
    sentiment_analyzer=load_analizers()[0]
    
    labels = ['Negativo', 'Neutro', 'Positivo']
    colores = ['#FF0000', '#808080', '#00FF00'] 
    
    sentimiento=sentiment_analyzer.predict(full_text)
    #ejemplo de salida: AnalyzerOutput(output=POS, probas={POS: 0.857, NEU: 0.103, NEG: 0.040})
    
    probs = sentimiento.probas
    sent = sentimiento.output
    
    probs_array = np.array(list(probs.values()))
    max_prob=np.max(probs_array)
        
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=probs_array, 
                             textinfo='label+percent', textposition='inside',
                             marker_colors=colores)])
   
        # Dar una respuestas
    if sent == 'NEG':
        color_response="**<font color='red'>Negativo</font>**"
    elif sent == 'POS':
        color_response="**<font color='green'>Positivo</font>**"
    else:
        color_response="**<font color='grey'>Neutro</font>**"
    resp=f"El texto es: {color_response} con una probabilidad de {max_prob*100:.2f}%."

    return resp, fig
    
def hate_analisys(text):
    # Preprocess text
    text_words=[]
    for word in text.split(' '):
        if word.startswith('@') and len(word)>1:
            word='@user'
        elif word.startswith('http'):
            word='http'
        text_words.append(word)
    full_text= ' '.join(text_words)
    
    hate_analizer=load_analizers()[1]
    
    hate=hate_analizer.predict(full_text)
    
    #ejemplo de salida: AnalyzerOutput(output=[], probas={hateful: 0.022, targeted: 0.009, aggressive: 0.018})
    
    probs = hate.probas
    hate = hate.output
    
    #labels = ['Odioso', 'Agresivo', 'Dirigido', 'No Odioso']
    
    probs_array = np.array(list(probs.values()))
    max_prob=np.max(probs_array)
        
    # Etiquetas y valores
    traduccion = {
    'hateful': 'Odioso',
    'aggressive': 'Agresivo',
    'targeted': 'Dirigido'
    }
    df = pd.DataFrame({
    'Etiqueta': [traduccion[k] for k in probs.keys()],
    'Probabilidad': list(probs.values())
    })
    #df = pd.DataFrame(list(probs.items()), columns=['Etiqueta', 'Probabilidad'])
    # Crear el gráfico de barras
    fig = px.bar(df, x='Etiqueta', y='Probabilidad', color='Etiqueta', color_discrete_map={
    'Odioso': '#FF0000',  # Rojo
    'Agresivo': '#FF9900',  # Naranja
    'Dirigido': '#FFFF00'  # Amarillo
    })
        # Dar una respuestas
    resp=''
    for clasificacion in hate:
        if clasificacion == 'hateful':
            color_response = "**<font color='red'>Odioso</font>**"
        elif clasificacion == 'aggressive':
            color_response = "**<font color='orange'>Agresivo</font>**"
        elif clasificacion == 'targeted':
            color_response = "**<font color='yellow'>Dirigido</font>**"
        resp+=f"El texto es: {color_response} con una intensidad de {probs[clasificacion]*100:.2f}%. <br>"
    if resp=='':
        resp=f"El texto es: **<font color='green'>No odioso</font>**"
    return resp, fig
    

# Main app logic
def main():
    st.title("Procesamiento de Texto en Redes Sociales")
    # User input
    option = st.selectbox("Elige una opción", ["Análisis de Sentimiento", "Detección de Odio"])

    if option == "Análisis de Sentimiento":
        text_input = st.text_area("Escriba el texto para realizar el analisis de sentimiento")
        if st.button("Analizar Sentimiento"):
            resp, fig=sentiment_analisys(text_input)
            st.markdown(resp, unsafe_allow_html=True)
            with st.container():
                st.write("### Distribución de Sentimientos")
                st.plotly_chart(fig, use_container_width=True)
    elif option == "Detección de Odio":             
        text_input = st.text_area("Escriba el texto para relizar detección de Odio") 
        if st.button("Analizar Odio"):
            resp, fig=hate_analisys(text_input)  
            st.markdown(resp, unsafe_allow_html=True)
            with st.container():
                st.write("### Distribución de Sentimientos")
                st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
