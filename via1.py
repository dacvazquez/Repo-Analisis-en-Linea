"""
    #Via 1
    encoded_input = tokenizer(full_text, return_tensors='pt')
    output = model(**encoded_input)
    scores=output[0][0].detach().numpy()
    scores = softmax(scores)
    indice_max = np.argmax(scores)
    max_probabilidad=max(scores)
"""