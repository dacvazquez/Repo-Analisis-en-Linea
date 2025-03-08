
# Función para obtener la probabilidad de la predicción
def get_probs_eficient(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    probs = torch.nn.functional.softmax(logits, dim=1).numpy()  # Convertir logits a probabilidades
    return probs

def explain_sentiment(text, model, tokenizer):
    # Preparar los inputs
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    input_ids = inputs["input_ids"].long()
    attention_mask = inputs["attention_mask"].long()

    # Asegurarse de que los tensores están en el dispositivo correcto
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    input_ids = input_ids.to(device)
    attention_mask = attention_mask.to(device)

    # Definir una función de predicción para Captum
    def predict(inputs, attention_mask):
        outputs = model(inputs, attention_mask=attention_mask)
        return outputs.logits  
    

    lig = LayerIntegratedGradients(predict, model.roberta.embeddings)
    
    attributions, delta = lig.attribute(
        inputs=input_ids,
        additional_forward_args=(attention_mask,),
        target=0,
        return_convergence_delta=True,
        n_steps=50
    )

    # Convertir los IDs a tokens y mapearlos con sus importancias
    tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
    attributions = attributions.sum(dim=-1).squeeze(0).detach().cpu().numpy()

    # Crear un diccionario con las palabras y sus importancias
    word_importance = {token: attribution for token, attribution in zip(tokens, attributions)}

    # Mostrar las palabras ordenadas por importancia
    sorted_importance = sorted(word_importance.items(), key=lambda x: x[1], reverse=True)
    for word, importance in sorted_importance:
        print(f"Palabra: {word} - Importancia: {importance:.4f}")

    return word_importance

    labels = ['Negativo', 'Neutro', 'Positivo']  
    colores = ['#FF0000', '#808080', '#00FF00']  
    
    colores = ['#FF0000', '#00FF00']  # Rojo, Verde
    labels = ['Negativo', 'Positivo']
    
    if model==AutoModelForSequenceClassification.from_pretrained(roberta):
        return terciary_clasification(labels, indice_max, max_probabilidad, fig)
    elif model==AutoModelForSequenceClassification.from_pretrained(beto):   
        return binary_clasification(labels, indice_max, max_probabilidad, fig)
    
def binary_clasification(labels, indice_max, max_probabilidad, fig):
    # Dar una respuestas
    if labels[indice_max] == 'Negativo':
        color_response="**<font color='red'>Negativo</font>**"
    elif labels[indice_max] == 'Positivo':
        color_response="**<font color='red'>Positivo</font>**"
    return f"El texto es: {color_response} con una probabilidad de {max_probabilidad*100:.2f}%.", fig
def terciary_clasification(labels, indice_max, max_probabilidad, fig):
    # Dar una respuestas
    if labels[indice_max] == 'Negativo':
        color_response="**<font color='red'>Negativo</font>**"
    elif labels[indice_max] == 'Positivo':
        color_response="**<font color='red'>Positivo</font>**"
    else:
        color_response="**<font color='red'>Neutro</font>**"
    return f"El texto es: {color_response} con una probabilidad de {max_probabilidad*100:.2f}%.", fig