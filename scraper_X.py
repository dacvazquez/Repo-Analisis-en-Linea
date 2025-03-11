import tweepy
import streamlit as st
import pandas as pd
import time

# Credenciales de la API de Twitter (X)
BEARER_TOKEN = f"AAAAAAAAAAAAAAAAAAAAAPTfzQEAAAAAu9acGZjaTCeyNsiBEv%2BrURm%2FHhU%3DqEITh867kzHYwNIjPsTQgSzoG6lm9UgBb6CBdzTHNIufIKldYT"

# Autenticación con la API v2
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Función para obtener los tweets y comentarios de un usuario
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
            st.write(f"**Tweet ID:** {tweet.id}")
            st.write(f"**Texto:** {tweet.text}")
            st.write(f"**Creado el:** {tweet.created_at}")
            st.write(f"**Likes:** {tweet.public_metrics['like_count']}")
            st.write(f"**Retweets:** {tweet.public_metrics['retweet_count']}")
            st.write("-" * 40)

            # Buscar respuestas al tweet
            replies = client.search_recent_tweets(query=f"conversation_id:{tweet.id}", max_results=10, tweet_fields=["created_at", "public_metrics"])

            if replies.data:
                for reply in replies.data:
                    st.write(f"**Comentario ID:** {reply.id}")
                    st.write(f"**Texto:** {reply.text}")
                    st.write(f"**Creado el:** {reply.created_at}")
                    st.write(f"**Likes:** {reply.public_metrics['like_count']}")
                    st.write(f"**Retweets:** {reply.public_metrics['retweet_count']}")
                    st.write("-" * 20)

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

        # Convertir la lista en un DataFrame
        df = pd.DataFrame(data)
        return df

    except tweepy.TooManyRequests as e:
        st.error(f"Límite de tasa excedido. Esperando 15 minutos antes de continuar...")
        time.sleep(15 * 60)  # Esperar 15 minutos
    except tweepy.TweepyException as e:
        st.error(f"Error de la API: {e}")
    except Exception as e:
        st.error(f"Error inesperado: {e}")
def main():
    # Interfaz de la aplicación Streamlit
    st.title("Comentarios de Twitter (X)")

    # Entrada de usuario
    user_input = st.text_input("Ingresa el ID de usuario o @usuario:")
    max_tweets = st.number_input("Cantidad de tweets a visualizar:", min_value=1, max_value=100, value=10)

    # Botón para ejecutar la búsqueda
    if st.button("Buscar Comentarios"):
        if user_input:
            # Limpiar la entrada del usuario (eliminar @ si está presente)
            #user = client.get_user(username=user_input.replace("@", "").strip())
            #user_id = user.data.id
            
            # ID de usuario de la universidad
            user_id = 2277112266
            # Obtener los tweets y comentarios
            
            df = get_tweets_and_replies(user_id, max_tweets)

            if df is not None and not df.empty:
                st.success("Datos obtenidos correctamente.")
                st.write("### Vista previa de los datos:")
                st.dataframe(df)

                # Exportar a CSV
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Descargar como CSV",
                    data=csv,
                    file_name=f"comentarios_{user_id}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No se encontraron tweets o comentarios.")
        else:
            st.warning("Por favor, ingresa un ID de usuario o @usuario.")
        
if __name__ == "__main__":
    main()
        