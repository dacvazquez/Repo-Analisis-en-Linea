import streamlit as st
from ntscraper import Nitter
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoConfig
import numpy as np
from scipy.special import softmax
#pip install streamlit transformers torch numpy

roberta = f"cardiffnlp/twitter-roberta-base-sentiment-latest"

# Load model and vectorizer once
@st.cache_resource
def load_model_RoBerta():
    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)
    config = AutoConfig.from_pretrained(roberta)
    return model, tokenizer

def predict_sentiment2(text):
    classifier = pipeline("sentiment-analysis")
    return classifier(text)

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
    print(full_text)
    
    # Predict sentiment
   
    encoded_input = tokenizer(text, return_tensors='tf')
    output = model(encoded_input)
    scores = output[0][0].numpy()
    scores = softmax(scores)
    indice_max = np.argmax(scores)
    max_probabilidad
    colores = ['#FF0000', '#808080', '#00FF00']  # Rojo, Gris, Verde
    labels = ['Negative','Neutro', 'Positive']
    
    # Crear el gráfico
    fig = go.Figure(data=[go.Pie(labels=labels, values=scores, 
                             textinfo='label+percent', textposition='inside',
                             marker_colors=colores)])
    # Dar una respuestas
    if lables[indice_max] == 'Negativo':
        return f"El texto es: **<font color='red'>Negativo</font>** con una probabilidad de {max_probabilidad*100:.2f}%.", fig
    elif lables[indice_max] == 'Positivo':
        return f"El texto es: **<font color='green'>Positivo</font>** con una probabilidad de {max_probabilidad*100:.2f}%.", fig
    else:
        return f"El texto es: **<font color='grey'>Neutro</font>** con una probabilidad de {max_probabilidad*100:.2f}%.", fig


# Main app logic
def main():
    st.title("Procesamiento de Texto en Redes Sociales")

    # Load model and tokenizer only once
    model, tokenizer = load_model_RoBerta()

    # User input
    option = st.selectbox("Elige una opción", ["Introducir texto para búsqueda"])
    
    if option == "Introducir texto para búsqueda":
        text_input = st.text_area("Escriba el texto para realizar el analisis de sentimiento")
        if st.button("Analizar Sentimiento"):
            sentiment, fig = predict_sentiment(text_input, model)
            st.markdown(sentiment, unsafe_allow_html=True)
            with st.container():
                st.write("### Distribución de Sentimientos")
                st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
