import tweepy
import pandas as pd
import time
import streamlit as st
# Credenciales de la API de Twitter (X)
BEARER_TOKEN = f"AAAAAAAAAAAAAAAAAAAAAPTfzQEAAAAAu9acGZjaTCeyNsiBEv%2BrURm%2FHhU%3DqEITh867kzHYwNIjPsTQgSzoG6lm9UgBb6CBdzTHNIufIKldYT"

# Autenticación con la API v2
client = tweepy.Client(bearer_token=BEARER_TOKEN)

def get_tweets_and_replies(user_id, max_tweets):
    try:
        # Obtener los últimos tweets del usuario
        tweets = client.get_users_tweets(id=user_id, max_results=max_tweets, tweet_fields=["created_at", "public_metrics"])

        if not tweets.data:
            return None

        # Lista para almacenar los datos
        data = []

        # Recorrer los tweets y buscar comentarios (respuestas)
        for tweet in tweets.data:
            time.sleep(1)  # Esperar 1 segundo entre cada solicitud
            replies = client.get_users_tweets(id=user_id, max_results=max_tweets, tweet_fields=["created_at", "public_metrics"])  # Limitar a 5 comentarios por tweet
            if replies.data:
                for reply in replies.data:
                    # Guardar los datos en una lista
                    data.append({
                        "Tweet ID": tweet.id,
                        "Tweet Text": tweet.text,
                        "Tweet Created At": tweet.created_at,
                        "Reply ID": reply.id,
                        "Reply Text": reply.text,
                        "Reply Created At": reply.created_at,
                        "Reply Likes": reply.public_metrics['like_count'],
                        "Reply Retweets": reply.public_metrics['retweet_count']
                    })
            time.sleep(5)        

        # Convertir la lista en un DataFrame
        df = pd.DataFrame(data)
        return df

    except tweepy.TooManyRequests as e:
        print(f"Límite de tasa excedido. Esperando 15 minutos antes de continuar...")
        time.sleep(15 * 60)  # Esperar 15 minutos
    except tweepy.TweepyException as e:
        print(f"Error de la API: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")