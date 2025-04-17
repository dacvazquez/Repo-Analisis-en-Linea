import streamlit as st
import pandas as pd
from x_scraper import get_tweets_and_replies

def main():
    st.title("Extracción de Tweets")
    
    st.write("ID de usuario de la universidad: 2277112266")
    
    # Entrada de usuario
    user_input = st.text_input("Ingresa el ID de usuario o @usuario:")
    max_tweets = st.number_input("Cantidad de tweets a visualizar:", min_value=1, max_value=20, value=10)
    
    if st.button("Buscar Tweets"):
        if user_input:
            # Limpiar la entrada del usuario (eliminar @ si está presente)
            user_id = user_input.replace("@", "").strip()
            
            # Verificar si 'tweets' ya está en session_state
            if 'tweets' not in st.session_state:
                st.session_state.tweets = None
                
            if st.session_state.tweets:
                st.write("Tweets almacenados:", st.session_state.tweets)
            else:
                # Obtener los tweets si no están en session_state
                with st.spinner('Obteniendo tweets...'):
                    container = get_tweets_and_replies(user_id, max_tweets)
                    st.session_state.tweets = container
                st.write("Tweets obtenidos:", container) 
            
            df = None
            if df is not None and not df.empty:
                st.toast("Datos obtenidos correctamente")
                st.write("### Vista previa de los datos:")
                st.dataframe(df)

                # Exportar a CSV
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="Descargar como CSV",
                    data=csv,
                    file_name=f"tweets_{user_id}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("El Data Frame con los tweets está vacío")
        else:
            st.warning("Por favor, ingresa un ID de usuario o @usuario.")


main() 