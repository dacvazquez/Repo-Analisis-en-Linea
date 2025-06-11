import tweepy, time
import pandas as pd
import streamlit as st


# Credenciales de la API de Twitter

# Autenticación con la API v2
client = tweepy.Client(bearer_token=st.secrets["TWITTER_BEARER_TOKEN"])

# Crear una tarjeta para los parametros de un Tweet
def create_card(id, text, created_at, like_count):
    card_html = f"""
    <div style="
        padding: 15px;
        border-radius: 10px;
        margin: 10px 20px;
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

# funcion para obtener los tweets de un ID de usuario especifico 

def get_tweets_and_replies(user_id, max_tweets):
    try:
        tweets = client.get_users_tweets(id=user_id, max_results=max_tweets, tweet_fields=["created_at", "public_metrics"])
        data = []
        
        if tweets.data:
            for tweet in tweets.data:
                data.append({
                    "Tweet ID": tweet.id,
                    "Texto": tweet.text,
                    "Creado en": tweet.created_at,
                    "Likes": tweet.public_metrics['like_count'],
                })
            df = pd.DataFrame(data)
            return df
        else:
            print("No se encontraron tweets.")
            return None

        time.sleep(5)
    
    except tweepy.TooManyRequests as e:
        st.write(f"Error 429: Límite de tasa de solicitudes excedido. Esperando 15 minutos antes de continuar...")
        print(e)
        return None
    except tweepy.TweepyException as e:
        st.write(f"Error de la API: {e}")
        print(e)
        return None
    except Exception as e:
        st.write(f"Error inesperado: {e}")
        print(e)
        return None

def get_tweet_comments(tweet_id, max_comments=200):
    try:
        query = f"conversation_id:{tweet_id}"
        data = []
        next_token = None

        while len(data) < max_comments:
            remaining = max_comments - len(data)
            max_results = min(100, remaining)  # Twitter solo permite hasta 100 por llamada

            response = client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=["created_at", "public_metrics"],
                next_token=next_token
            )

            if response.data:
                for reply in response.data:
                    data.append({
                        "Reply ID": reply.id,
                        "Texto": reply.text,
                        "Creado en": reply.created_at,
                        "Likes": reply.public_metrics['like_count']
                    })

            # Obtener el token para la siguiente página, si existe
            meta = response.meta
            next_token = meta.get("next_token", None)
            
            if not next_token:
                break  # No hay más páginas

        if data:
            df = pd.DataFrame(data)
            return df
        else:
            st.warning("No se encontraron comentarios.")
            return None

    except tweepy.TooManyRequests as e:
        st.error("Error 429: Límite de solicitudes excedido. Espera antes de continuar.")
        print(e)
        return None
    except tweepy.TweepyException as e:
        st.error(f"Error de la API: {e}")
        print(e)
        return None
    except Exception as e:
        st.error(f"Error inesperado: {e}")
        print(e)
        return None