
import tweepy, time
import pandas as pd
import streamlit as st

# Credenciales de la API de Twitter
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAPTfzQEAAAAAu9acGZjaTCeyNsiBEv%2BrURm%2FHhU%3DqEITh867kzHYwNIjPsTQgSzoG6lm9UgBb6CBdzTHNIufIKldYT"
API_KEY = "eTnF2iZzw7oQLF4E4TaIsfavw"
API_SECRET_KEY = "bPhEcnkUJ6hBcTiTqJ9QWw6Ism1uUqKUdeXYpIMWRFC4qvQpbY"
ACCESS_TOKEN = "1520488576177299456-kjjoaZy5ZhskDG0R98ZgbdavYm4PTl"
ACCESS_TOKEN_SECRET = "ahQhvazxfudKmnBSx0Cy91AhIEhDIxlGibKrN0DVJeNu0"

# Autenticación con la API v2
client = tweepy.Client(bearer_token=BEARER_TOKEN)
# ID de usuario de la universidad
user_id = 2277112266

def create_card(id, text, created_at, like_count):
    card_html = f"""
    <div style="
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border: 2px solid #1DA1F2;
        background-color: #15202B;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        color: white;
        font-family: Arial, sans-serif;
    ">
        <h4 style="margin: 0; color: #1DA1F2;">ID: {id}</h4>
        <h5 style="margin: 5px 0; color: #8899A6;">📅 Creado el: {created_at}</h5>
        <p style="margin: 10px 0; color: white;">💬 {text}</p>
        <h5 style="margin: 5px 0; color: #1DA1F2;">❤️ Likes: {like_count}</h5>
    </div>
    """
    return card_html
def get_tweets_and_replies(user_id, max_tweets):
    try:
        
        #if f"{user_id}".isnumeric()==0:
            #user = client.get_user(username=user_id)
            #user_id = user.data.id
            
        # Obtener los últimos tweets del usuario (máximo 10 para evitar muchas solicitudes)
        tweets = client.get_users_tweets(id=user_id, max_results=max_tweets, tweet_fields=["created_at", "public_metrics"])
        data=[]
        
        if tweets.data:
            for tweet in tweets.data:
                #print(f"Tweet ID: {tweet.id}")
                #print(f"Texto: {tweet.text}")
                #print(f"Creado el: {tweet.created_at}")
                #print(f"Likes: {tweet.public_metrics['like_count']}")
                #print(f"Retweets: {tweet.public_metrics['retweet_count']}")
                #print("-" * 40)
                data.append({
                        "Tweet ID": tweet.id,
                        "Tweet Text": tweet.text,
                        "Tweet Created At": tweet.created_at,
                        "Tweet Likes": tweet.public_metrics['like_count'],
                    })
                st.write(create_card(tweet.id, tweet.text, tweet.created_at, tweet.public_metrics['like_count']), unsafe_allow_html=True)
        
                #df = pd.DataFrame(data)
                #return df
        else:
            print("No se encontraron tweets.")

        # Esperar 5 segundos entre solicitudes para evitar exceder el límite de tasa
        time.sleep(5)
    
    except tweepy.TooManyRequests as e:
        # Manejar el error de exceso de solicitudes
        st.write(f"Error 429: Límite de tasa de solicitudes excedido. Esperando 15 minutos antes de continuar...")
        print(e)
    except tweepy.TweepyException as e:
        # Manejar otros errores de la API
        st.write(f"Error de la API: {e}")
        print(e)
    except Exception as e:
        # Manejar cualquier otro error
        st.write(f"Error inesperado: {e}")
        print(e)