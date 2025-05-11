import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import plotly.graph_objects as go
import nltk
from nltk.corpus import stopwords
import re

# Download required NLTK data
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def preprocess_text(text):
    # Convertir a minúsculas
    text = text.lower()
    # Eliminar caracteres especiales y números
    text = re.sub(r'[^a-zA-Záéíóúñ\s]', '', text)
    # Tokenizar usando split
    tokens = text.split()
    # Eliminar stopwords
    stop_words = set(stopwords.words('spanish'))
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

def get_important_words(df, target_column, n_words=10):
    # Preprocesar textos
    processed_texts = df['Texto'].apply(preprocess_text)
    
    # Crear vectorizador TF-IDF
    vectorizer = TfidfVectorizer(max_features=1000)
    X = vectorizer.fit_transform(processed_texts)
    
    # Obtener nombres de características
    feature_names = vectorizer.get_feature_names_out()
    
    # Manejar diferentes tipos de columnas
    if target_column == 'Análisis de Sentimiento':
        # Para sentimiento, usar los valores categóricos directamente
        y = df[target_column]
    else:
        # Para columnas booleanas, convertir a entero
        y = df[target_column].astype(int)
    
    # Entrenar clasificador
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    
    # Obtener importancia de características
    importances = clf.feature_importances_
    
    # Obtener índices de las palabras más importantes
    indices = np.argsort(importances)[::-1]
    
    # Obtener las palabras más importantes y sus importancias
    important_words = [(feature_names[i], importances[i]) for i in indices[:n_words]]
    
    return important_words

def create_word_importance_plot(words_importance):
    words, importances = zip(*words_importance)
    
    fig = go.Figure(data=[
        go.Bar(
            x=importances,
            y=words,
            orientation='h',
            marker=dict(
                color='rgba(58, 71, 80, 0.6)',
                line=dict(color='rgba(58, 71, 80, 1.0)', width=3)
            )
        )
    ])
    
    fig.update_layout(
        yaxis_title="Palabras",
        xaxis_title="Importancia",
        height=400,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

def main():
    st.title("Análisis de Palabras Influentes")
    
    if 'analysis_df' not in st.session_state or st.session_state.analysis_df.empty:
        st.warning("No hay datos para analizar. Por favor, ingresa algunos textos primero.")
        return
    
    df = st.session_state.analysis_df
    
    st.markdown("""
    Este análisis muestra las palabras que más influyen en las decisiones de:
    - Sentimiento (Positivo, Negativo, Neutro)
    - Odio (Odioso, Agresivo, Objetivo)
    """)
    
    # Análisis de sentimiento
    st.subheader("Palabras Influentes en la decisión de Sentimiento Positivo")
    sentiment_words = get_important_words(df, 'Análisis de Sentimiento')
    fig_sentiment = create_word_importance_plot(
        sentiment_words
    )
    st.plotly_chart(fig_sentiment, use_container_width=True, key="sentiment_chart")
    
    # Análisis de odio
    st.subheader("Palabras Influentes en la detección de Odio")
    hate_words = get_important_words(df, 'Odio')
    fig_hate = create_word_importance_plot(
        hate_words
    )
    st.plotly_chart(fig_hate, use_container_width=True, key="hate_chart")
    
    # Análisis de agresividad
    st.subheader("Palabras Influentes en la detección de Agresividad")
    aggressive_words = get_important_words(df, 'Agresividad')
    fig_aggressive = create_word_importance_plot(
        aggressive_words
    )
    st.plotly_chart(fig_aggressive, use_container_width=True, key="aggressive_chart")
    
    # Análisis de objetivismo
    st.subheader("Palabras Influentes en la detección de Objetivismo")
    targeted_words = get_important_words(df, 'Objetivismo')
    fig_targeted = create_word_importance_plot(
        targeted_words
    )
    st.plotly_chart(fig_targeted, use_container_width=True, key="targeted_chart")

main() 