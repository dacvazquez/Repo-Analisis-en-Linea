import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import tweepy
import instaloader
import facebook_scraper
import time
import re

def get_tweet_id(url):
    """Extract tweet ID from URL"""
    # Handle different Twitter URL formats
    patterns = [
        r'twitter\.com/\w+/status/(\d+)',
        r'twitter\.com/\w+/statuses/(\d+)',
        r'twitter\.com/\w+/status/(\d+)/photo/\d+',
        r'twitter\.com/\w+/status/(\d+)/video/\d+'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def scrape_twitter_comments(url, max_comments):
    comments = []
    try:
        # Initialize Twitter API client
        client = tweepy.Client(bearer_token=st.secrets["TWITTER_BEARER_TOKEN"])
        
        # Get tweet ID from URL
        tweet_id = get_tweet_id(url)
        if not tweet_id:
            st.error("URL de Twitter no válida")
            return comments
        
        # Get tweet replies
        for tweet in tweepy.Paginator(
            client.search_recent_tweets,
            query=f"conversation_id:{tweet_id}",
            max_results=100,
            limit=max_comments
        ):
            if not tweet.data:
                continue
                
            for t in tweet.data:
                comments.append({
                    'Platform': 'Twitter',
                    'Text': t.text,
                    'Date': t.created_at,
                    'Username': t.author_id
                })
                
                if len(comments) >= max_comments:
                    break
                    
            if len(comments) >= max_comments:
                break
                
    except Exception as e:
        st.error(f"Error al obtener comentarios de Twitter: {str(e)}")
    return comments

def scrape_instagram_comments(url, max_comments, username=None, password=None):
    comments = []
    try:
        L = instaloader.Instaloader()
        
        # Si se proporcionan credenciales, intentar login
        if username and password:
            try:
                L.login(username, password)
                st.success("✅ Login exitoso en Instagram")
            except Exception as e:
                error_msg = str(e)
                if "Checkpoint required" in error_msg:
                    # Extraer el enlace de verificación del mensaje de error
                    import re
                    challenge_path = re.search(r'Point your browser to (.*?) -', error_msg)
                    if challenge_path:
                        challenge_url = f"https://www.instagram.com{challenge_path.group(1)}"
                        st.error("⚠️ Instagram requiere verificación de seguridad")
                        st.markdown(f"""
                        ### Pasos para completar la verificación:
                        1. Abre este enlace en tu navegador: [{challenge_url}]({challenge_url})
                        2. Sigue las instrucciones de Instagram para verificar tu identidad
                        3. Una vez completada la verificación, vuelve a intentar el inicio de sesión aquí
                        
                        **Nota:** Este es un proceso de seguridad normal de Instagram para proteger tu cuenta.
                        """)
                    else:
                        st.error("Error de verificación de Instagram. Por favor, intenta iniciar sesión directamente en la aplicación de Instagram y vuelve a intentar.")
                else:
                    st.error(f"Error al hacer login en Instagram: {str(e)}")
                return comments
        
        # Extract post shortcode from URL
        shortcode = url.split('/')[-2]
        
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        for i, comment in enumerate(post.get_comments()):
            if i >= max_comments:
                break
            comments.append({
                'Platform': 'Instagram',
                'Text': comment.text,
                'Date': comment.created_at_utc,
                'Username': comment.owner.username
            })
    except Exception as e:
        st.error(f"Error al obtener comentarios de Instagram: {str(e)}")
    return comments

def scrape_facebook_comments(url, max_comments):
    comments = []
    try:
        for i, comment in enumerate(facebook_scraper.get_posts(url, pages=1)):
            if i >= max_comments:
                break
            comments.append({
                'Platform': 'Facebook',
                'Text': comment['text'],
                'Date': comment['time'],
                'Username': comment['username']
            })
    except Exception as e:
        st.error(f"Error al obtener comentarios de Facebook: {str(e)}")
    return comments

def main():
    st.title("Extracción de Comentarios de Redes Sociales")
    
    # Selección de plataforma
    platform = st.selectbox(
        "Selecciona la plataforma social:",
        ["Twitter", "Instagram", "Facebook"]
    )
    
    # Mostrar campos de login solo para Instagram
    instagram_username = None
    instagram_password = None
    
    if platform == "Instagram":
        st.markdown("### 🔐 Credenciales de Instagram")
        st.info("Para acceder a los comentarios de Instagram, necesitas iniciar sesión.")
        instagram_username = st.text_input("Usuario de Instagram:")
        instagram_password = st.text_input("Contraseña de Instagram:", type="password")
    
    # Entrada de URL
    url = st.text_input(f"Ingresa la URL del post de {platform}:")
    
    # Número máximo de comentarios
    max_comments = st.number_input(
        "Número máximo de comentarios a extraer:",
        min_value=1,
        max_value=1000,
        value=100
    )
    
    if st.button("Extraer Comentarios"):
        if url:
            with st.spinner('Extrayendo comentarios...'):
                comments = []
                if platform == "Twitter":
                    comments = scrape_twitter_comments(url, max_comments)
                elif platform == "Instagram":
                    if not instagram_username or not instagram_password:
                        st.warning("Por favor, ingresa tus credenciales de Instagram para acceder a los comentarios.")
                        return
                    comments = scrape_instagram_comments(url, max_comments, instagram_username, instagram_password)
                elif platform == "Facebook":
                    comments = scrape_facebook_comments(url, max_comments)
                
                if comments:
                    # Convertir a DataFrame
                    df = pd.DataFrame(comments)
                    
                    # Mostrar vista previa
                    st.write("### Vista previa de los comentarios:")
                    st.dataframe(df)
                    
                    # Opciones de exportación
                    st.write("### Exportar Comentarios")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Exportar a CSV
                        csv = df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
                        st.download_button(
                            label="📥 Descargar como CSV",
                            data=csv,
                            file_name=f"comentarios_{platform.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    
                    with col2:
                        # Botón para añadir al análisis múltiple
                        if st.button("➕ Añadir al Análisis Múltiple"):
                            if 'analysis_df' not in st.session_state:
                                st.session_state.analysis_df = pd.DataFrame(columns=['Texto', 'Análisis de Sentimiento', 'Análisis de Odio'])
                            
                            # Añadir solo los textos al DataFrame de análisis
                            new_rows = pd.DataFrame({
                                'Texto': df['Text'],
                                'Análisis de Sentimiento': [''] * len(df),
                                'Análisis de Odio': [''] * len(df)
                            })
                            
                            st.session_state.analysis_df = pd.concat([st.session_state.analysis_df, new_rows], ignore_index=True)
                            st.toast(f"Se han añadido {len(df)} comentarios al análisis múltiple")
                else:
                    st.warning("No se encontraron comentarios o hubo un error en la extracción.")
        else:
            st.warning("Por favor, ingresa una URL válida.")


main() 