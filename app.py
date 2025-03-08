import streamlit as st
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from scipy.special import softmax
import plotly.graph_objects as go
from lime.lime_text import LimeTextExplainer
import torch
from lime.lime_text import LimeTextExplainer
from captum.attr import IntegratedGradients
from captum.attr import LayerIntegratedGradients


roberta = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
beto = f"finiteautomata/beto-sentiment-analysis"

# Load model and vectorizer once
@st.cache_resource
def load_model_RoBerta():
    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)
    return model, tokenizer
@st.cache_resource
def load_model_Beto():
    model = AutoModelForSequenceClassification.from_pretrained(beto)
    tokenizer = AutoTokenizer.from_pretrained(beto)
    return model, tokenizer

def predict_sentiment2(text):
    classifier = pipeline("sentiment-analysis")
    return classifier(text)


def get_probs(text, tokenizer, model):
    inputs=tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    logits=model(**inputs).logits
    probs=torch.nn.functional.softmax(logits, dim=1).detach().numpy()
    return probs

# Define sentiment prediction function
def predict_sentiment(text, model, tokenizer):
    # Preprocess text
    text_words=[]
    for word in text.split(' '):
        if word.startswith('@') and len(word)>1:
            word='@user'
        elif word.startswith('http'):
            word='http'
        text_words.append(word)
    full_text= ' '.join(text_words)
    
    # Predict sentiment
    
    #Via 2
    inputs=tokenizer(full_text, return_tensors='pt', truncation=True, padding=True)
    
    # Realizar la predicción
    with torch.no_grad():
        outputs = model(**inputs)
    
    #Obtener los logits
    logits = outputs.logits
    # Obtener las probabilidades
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    
    print(f"Logits: {logits}")
    print(f"Probabilidades: {probs}")
    
    # Crear el gráfico
    labels = ['Negativo', 'Neutro', 'Positivo']
    colores = ['#FF0000', '#808080', '#00FF00'] 
    fig = go.Figure(data=[go.Pie(labels=labels, values=probs, 
                             textinfo='label+percent', textposition='inside',
                             marker_colors=colores)])
    
    # Obtener la clase predicha
    predicted_class = torch.argmax(probs, dim=-1).item()
    
    # Mapear el índice a la etiqueta de sentimiento 
    predicted_sentiment = labels[predicted_class]
    
    # Obtener la probabilidad de la clase predicha
    confidence = probs[0][predicted_class].item()
    print(f"Texto: {full_text}")
    print(f"Sentimiento predicho: {predicted_sentiment}")
    print(f"Confianza: {confidence:.2f}")
    return predicted_sentiment, confidence, fig

   
    
    # Dar una respuestas
    if labels[indice_max] == 'Negativo':
        color_response="**<font color='red'>Negativo</font>**"
    elif labels[indice_max] == 'Positivo':
        color_response="**<font color='red'>Positivo</font>**"
    else:
        color_response="**<font color='red'>Neutro</font>**"
    return f"El texto es: {color_response} con una probabilidad de {max_probabilidad*100:.2f}%.", fig


# Main app logic
def main():
    st.title("Procesamiento de Texto en Redes Sociales")

    # Load model and tokenizer only once
    model, tokenizer = load_model_Beto()

    # User input
    option = st.selectbox("Elige una opción", ["Introducir texto para búsqueda"])
    
    if option == "Introducir texto para búsqueda":
        text_input = st.text_area("Escriba el texto para realizar el analisis de sentimiento")
        if st.button("Analizar Sentimiento"):
            sentiment,confidence, fig = predict_sentiment(text_input, model, tokenizer)
            #exp=explain_sentiment(text_input, model, tokenizer)
            st.markdown(sentiment, unsafe_allow_html=True)
            st.markdown(confidence, unsafe_allow_html=True)
            #st.markdown(exp)
            with st.container():
                st.write("### Distribución de Sentimientos")
                st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
