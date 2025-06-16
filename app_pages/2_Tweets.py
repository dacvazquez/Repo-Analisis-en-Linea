import streamlit as st
import pandas as pd
from x_scraper import get_tweets_and_replies, get_tweet_comments

def main():
    st.title("Extracción de Tweets")
    
    if 'tweets_df' not in st.session_state:
        st.session_state.tweets_df = None
    
    # st.write("ID de usuario de la universidad: 2277112266")
    
    # Sección para cargar tweets previos
    st.subheader("Cargar Tweets Locales")
    uploaded_file = st.file_uploader("Cargar archivo CSV de tweets previos", type=['csv'])
    if uploaded_file is not None:
        try:
            df_previo = pd.read_csv(uploaded_file)
            # Renombrar las columnas si es necesario
            columnas_deseadas = {
                df_previo.columns[0]: "Tweet ID",
                df_previo.columns[1]: "Texto",
                df_previo.columns[2]: "Creado en",
                df_previo.columns[3]: "Likes"
            }
            df_previo = df_previo.rename(columns=columnas_deseadas)
            
            if st.session_state.tweets_df is None:
                st.session_state.tweets_df = df_previo
            else:
                # Combinar con tweets existentes y eliminar duplicados
                st.session_state.tweets_df = pd.concat([st.session_state.tweets_df, df_previo]).drop_duplicates(subset=['Tweet ID'])
            st.toast("Tweets previos cargados exitosamente 👍")
        except Exception as e:
            st.error(f"Error al cargar el archivo: {str(e)}")
    
    # Entrada de usuario para nuevos tweets
    st.subheader("Obtener Nuevos Tweets")
    user_input = st.text_input("Ingresa el ID de usuario o @usuario:", placeholder="@usuario")
    max_tweets = st.number_input("Cantidad de tweets a visualizar:", min_value=1, max_value=20, value=10)
    
    if st.button("Buscar Tweets"):
        if user_input:
            # Limpiar la entrada del usuario (eliminar @ si está presente)
            user_id = user_input.replace("@", "").strip()
            
            # Obtener los tweets
            with st.spinner('Obteniendo tweets...'):
                df_nuevos = get_tweets_and_replies(user_id, max_tweets)
            
            if df_nuevos is not None and not df_nuevos.empty:
                # Combinar con tweets existentes si los hay
                if st.session_state.tweets_df is not None:
                    st.session_state.tweets_df = pd.concat([st.session_state.tweets_df, df_nuevos]).drop_duplicates(subset=['Tweet ID'])
                else:
                    st.session_state.tweets_df = df_nuevos
                
                st.toast("Datos obtenidos correctamente")
                st.write("### Nuevos tweets obtenidos:")
                st.dataframe(df_nuevos, use_container_width=True)
            else:
                st.warning("No se encontraron tweets para este usuario")
        else:
            st.warning("Por favor, ingresa un ID de usuario o @usuario.")
    
    # Mostrar todos los tweets guardados
    if st.session_state.tweets_df is not None:
        st.write("### Tweets Guardados:")
        st.dataframe(st.session_state.tweets_df, use_container_width=True)
        
        bot1, bot2, bot3=st.columns([3,3,7])
        with bot1:
            # Botón para descargar todos los tweets
            csv = st.session_state.tweets_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="Descargar los Tweets como CSV",
                data=csv,
                file_name="tweets.csv",
                mime="text/csv"
            )
        with bot2:    
            # Botón para limpiar todos los tweets
            if st.button("Vaciar tabla de Tweets", help='Recuerda eliminar el archivo cargado previamente en "Cargar Tweets Locales" para completar la opercacion, sino se seguiran cargando los tweets del mismo archivo'):
                st.session_state.tweets_df = None
                st.toast("La tabla de tweets ha sido vaciada exitosamente 👍")
                st.rerun()

    # Sección para ver comentarios de un tweet específico
    st.subheader("Ver Comentarios de un Tweet")
    tweet_id = st.text_input("Ingresa el ID del tweet para ver sus comentarios:")
    max_comments = st.number_input("Cantidad de comentarios a mostrar:", min_value=1, max_value=20, value=10)
    
    if st.button("Buscar Comentarios"):
        if tweet_id:
            with st.spinner('Obteniendo comentarios...'):
                comments_df = get_tweet_comments(tweet_id, max_comments)
            
            if comments_df is not None and not comments_df.empty:
                st.write("### Comentarios del Tweet:")
                st.dataframe(comments_df, use_container_width=True)
                
                # Botón para descargar comentarios
                csv_comments = comments_df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="Descargar Comentarios como CSV",
                    data=csv_comments,
                    file_name=f"comentarios_{tweet_id}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No se encontraron comentarios para este tweet")
        else:
            st.warning("Por favor, ingresa un ID de tweet válido.")
    
main() 