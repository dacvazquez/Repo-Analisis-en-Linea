import streamlit as st
import pandas as pd
from x_scraper import get_tweets_and_replies

def main():
    st.title("Extracción de Tweets")
    
    if 'tweets_df' not in st.session_state:
        st.session_state.tweets_df = None
    
    st.write("ID de usuario de la universidad: 2277112266")
    
    # Entrada de usuario
    user_input = st.text_input("Ingresa el ID de usuario o @usuario:")
    max_tweets = st.number_input("Cantidad de tweets a visualizar:", min_value=1, max_value=20, value=10)
    
    if st.button("Buscar Tweets"):
        if user_input:
            # Limpiar la entrada del usuario (eliminar @ si está presente)
            user_id = user_input.replace("@", "").strip()
            
            # Obtener los tweets
            with st.spinner('Obteniendo tweets...'):
                df = get_tweets_and_replies(user_id, max_tweets)
            
            if df is not None and not df.empty:
                st.session_state.tweets_df = df  # Guardar en session_state
                st.toast("Datos obtenidos correctamente")
                st.write("### Vista previa de los datos:")
                st.dataframe(df, use_container_width=True)

                # Exportar a CSV
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="Descargar como CSV",
                    data=csv,
                    file_name=f"tweets_{user_id}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No se encontraron tweets para este usuario")
        else:
            st.warning("Por favor, ingresa un ID de usuario o @usuario.")
    
    # Mostrar tweets guardados si existen
    if st.session_state.tweets_df is not None:
        st.write("### Tweets Guardados:")
        st.dataframe(st.session_state.tweets_df, use_container_width=True)

main()