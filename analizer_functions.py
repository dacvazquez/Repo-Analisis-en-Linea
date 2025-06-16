import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pysentimiento.preprocessing import preprocess_tweet

def sentiment_analisys(text, sentiment_analyzer):
    """
    Analiza el sentimiento de un texto utilizando un modelo de análisis de sentimientos.

    Esta función preprocesa el texto, reemplazando menciones de usuario (@usuario) y URLs,
    y luego utiliza un modelo de análisis de sentimientos para determinar el sentimiento
    general del texto y sus probabilidades asociadas.

    Args:
        text (str): El texto a analizar.
        sentiment_analyzer: Modelo de análisis de sentimientos pre-entrenado.

    Returns:
        tuple: Una tupla que contiene:
            - sent (str): El sentimiento predominante ('POS', 'NEG' o 'NEU').
            - max_prob (float): La probabilidad máxima asociada al sentimiento (0-100).
            - fig (plotly.graph_objects.Figure): Gráfico de pie que muestra la distribución
              de probabilidades de los sentimientos.

    Example:
        >>> sent, prob, fig = sentiment_analisys("Me encanta este producto!", analyzer)
        >>> print(f"Sentimiento: {sent}, Probabilidad: {prob}%")
        Sentimiento: POS, Probabilidad: 85.7%
    """

    # Preprocesamiento del texto
    # Antiguo método básico de preprocesamiento de texto:
    """
    text_words=[]
    for word in text.split(' '):
        if word.startswith('@') and len(word)>1:
            word='@usuario'
        elif word.startswith('http'):
            word=''
        text_words.append(word)
    processed_text= ' '.join(text_words)
    """
    # Utilizando el preprocesamiento de pysentimiento
    processed_text=preprocess_tweet(text)

    labels = ['Negativo', 'Neutro', 'Positivo']
    colores = ['#FF0000', '#808080', '#00FF00'] 
    
    sentimiento=sentiment_analyzer.predict(processed_text)
    #ejemplo de salida: AnalyzerOutput(output=POS, probas={POS: 0.857, NEU: 0.103, NEG: 0.040})
    
    probs = sentimiento.probas #Probabilidades
    sent = sentimiento.output #POS, NEG o NEU
    
    probs_array = np.array(list(probs.values()))
    max_prob=np.max(probs_array)
        
    # Definir colores modernos y consistentes
    colors = {
        'Positivo': '#2ecc71',  # Verde
        'Neutro': '#95a5a6',    # Gris
        'Negativo': '#e74c3c'   # Rojo
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=probs_array, 
        textinfo='label+percent', 
        textposition='inside',
        marker_colors=[colors[label] for label in labels],
        hole=0.3,
        rotation=45,
        hovertemplate='%{label}<br>Probabilidad: %{percent:.1%}<extra></extra>'
    )])
    
    # Personalización del layout
    fig.update_layout(
        height=450,
        margin=dict(t=60, b=80, l=0, r=50),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            font=dict(size=13)
        )
    )

    return sent, max_prob*100, fig
    
def hate_analisys(text, hate_analizer):
    """
    Analiza el contenido de odio en un texto utilizando un modelo de detección de odio.

    Esta función preprocesa el texto, reemplazando menciones de usuario (@usuario) y URLs,
    y luego utiliza un modelo de detección de odio para identificar diferentes tipos de
    contenido ofensivo y sus probabilidades asociadas.

    Args:
        text (str): El texto a analizar.
        hate_analizer: Modelo de detección de odio pre-entrenado.

    Returns:
        tuple: Una tupla que contiene:
            - hate (list): Lista de categorías de odio detectadas en el texto
              (puede incluir 'hateful', 'aggressive', 'targeted').
            - probs (dict): Diccionario con las probabilidades asociadas a cada categoría
              de odio.
            - fig (plotly.graph_objects.Figure): Gráfico de barras que muestra la
              distribución de probabilidades de las diferentes categorías de odio.

    Categories:
        - Odioso (hateful): Contenido que expresa odio o discriminación.
        - Agresivo (aggressive): Contenido con lenguaje agresivo o violento.
        - Directo (targeted): Contenido dirigido específicamente a un individuo o grupo.

    Example:
        >>> hate, probs, fig = hate_analisys("Texto ofensivo", analyzer)
        >>> print(f"Categorías detectadas: {hate}")
        >>> print(f"Probabilidades: {probs}")
        Categorías detectadas: ['hateful', 'aggressive']
        Probabilidades: {'hateful': 0.022, 'aggressive': 0.018, 'targeted': 0.009}
    """
    # Preprocesamiento del texto
    # Antiguo método básico de preprocesamiento de texto:
    """
    text_words=[]
    for word in text.split(' '):
        if word.startswith('@') and len(word)>1:
            word='@usuario'
        elif word.startswith('http'):
            word=''
        text_words.append(word)
    processed_text= ' '.join(text_words)
    """
    # Utilizando el preprocesamiento de pysentimiento
    processed_text=preprocess_tweet(text)

    hate=hate_analizer.predict(processed_text)
    #ejemplo de salida: AnalyzerOutput(output=[], probas={hateful: 0.022, targeted: 0.009, aggressive: 0.018})
    
    probs = hate.probas
    hate = hate.output
    
    #labels = ['Odioso', 'Agresivo', 'Dirigido', 'No Odioso']
    
    # Etiquetas y valores
    traduccion = {
        'hateful': 'Odioso',
        'aggressive': 'Agresivo',
        'targeted': 'Directo'
    }
    
    # Definir colores modernos y consistentes
    colors = {
        'Odioso': '#e74c3c',    # Rojo
        'Agresivo': '#f39c12',  # Naranja
        'Directo': '#9b59b6'     # Púrpura
    }
    
    df = pd.DataFrame({
        'Etiqueta': [traduccion[k] for k in probs.keys()],
        'Intensidad': list(probs.values())
    })
    
    # Crear el gráfico de barras con estilo moderno
    fig = go.Figure(data=[go.Bar(
        x=df['Etiqueta'],
        y=df['Intensidad'],
        marker_color=[colors[label] for label in df['Etiqueta']],
        text=df['Intensidad'].apply(lambda x: f'{x:.1%}'),
        textposition='inside',
        hovertemplate='%{x}<br>Intensidad: %{y:.1%}<extra></extra>'
    )])
    
    # Personalización del layout
    fig.update_layout(
        height=450,
        margin=dict(t=60, b=80, l=0, r=50),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14),
        xaxis_title='Tipo de Contenido',
        yaxis_title='Intensidad',
        bargap=0.05,
        showlegend=False
    )
    
    """    
    # Dar una respuestas
    resp=''
    for clasificacion in hate:
        if clasificacion == 'hateful':
            color_response = "**<font color='red'>Odioso</font>**"
        elif clasificacion == 'aggressive':
            color_response = "**<font color='orange'>Agresivo</font>**"
        elif clasificacion == 'targeted':
            color_response = "**<font color='yellow'>Dirigido</font>**"
        resp+=f"El texto es: {color_response} con un rating de {probs[clasificacion]*100:.2f}%. <br>"
    if resp=='':
        resp=f"El texto es: **<font color='green'>No odioso</font>**"
    """    
    return hate, probs, fig
    
