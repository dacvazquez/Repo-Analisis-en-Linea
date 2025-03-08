#Esta funcion trabaja bien clasificando el sentimiento con RoBerta en ingles 
def predict_sentiment_for_roberta(text, model, tokenizer):
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
    
    inputs=tokenizer(full_text, return_tensors='pt', truncation=True, padding=True)
    logits=model(**inputs).logits
    probs=torch.nn.functional.softmax(logits, dim=1).detach().numpy()[0]
    print(probs)
    indice_max = np.argmax(probs)
    max_probabilidad=np.max(probs)
    
    labels = ['Negativo', 'Neutro', 'Positivo']  
    colores = ['#FF0000', '#808080', '#00FF00']  
        
    # Crear el gráfico PD: cambiar values=scores por probs dependiendo de cual via se use
    fig = go.Figure(data=[go.Pie(labels=labels, values=probs, 
                             textinfo='label+percent', textposition='inside',
                             marker_colors=colores)])
    
    # Dar una respuestas
    if labels[indice_max] == 'Negativo':
        color_response="**<font color='red'>Negativo</font>**"
    elif labels[indice_max] == 'Positivo':
        color_response="**<font color='red'>Positivo</font>**"
    else:
        color_response="**<font color='red'>Neutro</font>**"
    return f"El texto es: {color_response} con una probabilidad de {max_probabilidad*100:.2f}%.", fig
