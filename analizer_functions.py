# Define sentiment prediction function
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def sentiment_analisys(text,sentiment_analyzer):
    # Preprocess text
    text_words=[]
    for word in text.split(' '):
        if word.startswith('@') and len(word)>1:
            word='@user'
        elif word.startswith('http'):
            word='http'
        text_words.append(word)
    full_text= ' '.join(text_words)
    
    labels = ['Negativo', 'Neutro', 'Positivo']
    colores = ['#FF0000', '#808080', '#00FF00'] 
    
    sentimiento=sentiment_analyzer.predict(full_text)
    #ejemplo de salida: AnalyzerOutput(output=POS, probas={POS: 0.857, NEU: 0.103, NEG: 0.040})
    
    probs = sentimiento.probas #Probabilidades
    sent = sentimiento.output #POS, NEG o NEU
    
    probs_array = np.array(list(probs.values()))
    max_prob=np.max(probs_array)
        
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=probs_array, 
                             textinfo='label+percent', textposition='inside',
                             marker_colors=colores)])
   

    return sent, max_prob*100, fig
    
def hate_analisys(text, hate_analizer):
    # Preprocess text
    text_words=[]
    for word in text.split(' '):
        if word.startswith('@') and len(word)>1:
            word='@user'
        elif word.startswith('http'):
            word='http'
        text_words.append(word)
    full_text= ' '.join(text_words)
    
    hate=hate_analizer.predict(full_text)
    
    #ejemplo de salida: AnalyzerOutput(output=[], probas={hateful: 0.022, targeted: 0.009, aggressive: 0.018})
    
    probs = hate.probas
    hate = hate.output
    
    #labels = ['Odioso', 'Agresivo', 'Dirigido', 'No Odioso']
    
    probs_array = np.array(list(probs.values()))
    #max_prob=np.max(probs_array)
        
    # Etiquetas y valores
    traduccion = {
    'hateful': 'Odioso',
    'aggressive': 'Agresivo',
    'targeted': 'Directo'
    }
    df = pd.DataFrame({
    'Etiqueta': [traduccion[k] for k in probs.keys()],
    'Intensidad': list(probs.values())
    })
    
    #df = pd.DataFrame(list(probs.items()), columns=['Etiqueta', 'Probabilidad'])
    # Crear el gráfico de barras
    fig = px.bar(df, x='Etiqueta', y='Intensidad', color='Etiqueta', color_discrete_map={
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
        resp+=f"El texto es: {color_response} con un rating de {probs[clasificacion]*100:.2f}%. <br>"
    if resp=='':
        resp=f"El texto es: **<font color='green'>No odioso</font>**"
    return hate, probs, fig
    
