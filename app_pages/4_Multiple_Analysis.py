import streamlit as st
import pandas as pd
from analizer_functions import sentiment_analisys, hate_analisys
from model_loader import load_models as lm
import colores_resp as cr

help="""
Realiza un análisis de sentimiento y detección de odio 
\n
El análisis de sentimiento sirve para determinar si el tono emocional del mensaje es positivo, negativo o neutro
\n
El odio o el discurso de odio se define como manifestaciones verbales o escritas de intolerancia y 
hostilidad, representan una amenaza insidiosa para la cohesión social y la dignidad humana. 
"""

def main():
    st.title("Análisis a Texto")

    if 'analysis_df' not in st.session_state:
        st.session_state.analysis_df = pd.DataFrame(columns=[
            'Texto', 
            'Análisis de Sentimiento',
            'Odio',
            'Agresividad',
            'Objetivismo'
        ])

    if 'last_analysis_results' not in st.session_state:
        st.session_state.last_analysis_results = None

    if 'show_toast' in st.session_state:
        st.toast(st.session_state.show_toast)
        del st.session_state.show_toast

    sentiment_analyzer, hate_analizer = lm()

    new_text = st.text_area("Ingrese el texto a analizar 🔍")

    col1, col2, col3, col4 = st.columns([1, 1, 1, 6])
    with col1:
        analizar = st.button("Analizar", help=help)
    with col2:
        anadir = st.button("Añadir", help="Añade el texto y los resultados de su análisis a la tabla")
    with col3:  
        descartar = st.button("Descartar", 
                            help="Elimina los resultados del análisis actual",
                            disabled='last_analysis_results' not in st.session_state or st.session_state.last_analysis_results is None)

    if analizar:
        if new_text:
            sentiment, prob_sentiment, fig_sentiment = sentiment_analisys(new_text, sentiment_analyzer)
            hate, probs_hate, fig_hate = hate_analisys(new_text, hate_analizer)
            
            # Guardar el texto analizado en session_state
            st.session_state.last_analyzed_text = new_text

            if sentiment == 'NEG':
                sentiment='Negativo'
                sentiment_response=cr.negativo
            elif sentiment == 'POS':
                sentiment='Positivo'
                sentiment_response=cr.positivo
            else:
                sentiment='Neutro'
                sentiment_response=cr.neutro

            resp=''
            hateful = False
            aggressive = False
            targeted = False

            for clasification in hate:
                if clasification == 'hateful':
                    hateful = True
                    hate_response = cr.odioso
                elif clasification == 'aggressive':
                    aggressive = True
                    hate_response = cr.agresivo
                elif clasification == 'targeted':
                    targeted = True
                    hate_response = cr.dirigido
                elif clasification == 'none':
                    hate_response = cr.no_odioso
                resp+=f"El texto es: {hate_response} con una precisión de {probs_hate[clasification]*100:.2f}%. <br>"
            if resp=='':
                resp=f"El texto es: {cr.no_odioso}"

            sentiment_result = f"El sentimiento es {sentiment_response} con una intensidad de {prob_sentiment:.2f}"
            st.session_state.last_analysis_results = (sentiment_result, resp, fig_sentiment, fig_hate)

    if anadir:
        if new_text:
            if new_text in st.session_state.analysis_df['Texto'].values:
                st.toast("Este texto ya fue analizado anteriormente 👀")
            elif new_text == '':
                st.toast("No se puede añadir un texto vacío 👀")
            elif not st.session_state.last_analysis_results:
                st.toast("Por favor, analiza el texto primero 🔍")
            else:
                # Obtener el texto del último análisis
                sentiment_result, hate_result, fig_sentiment, fig_hate = st.session_state.last_analysis_results
                
                # Verificar si el texto actual coincide con el último análisis
                if 'last_analyzed_text' in st.session_state and st.session_state.last_analyzed_text == new_text:
                    # Solo proceder si el texto coincide con el último análisis
                    if 'Negativo' in sentiment_result:
                        sentiment = 'Negativo'
                    elif 'Positivo' in sentiment_result:
                        sentiment = 'Positivo'
                    else:
                        sentiment = 'Neutro'

                    # Corregir la lógica para detectar odio
                    hateful = False
                    aggressive = False
                    targeted = False
                    
                    if 'odioso' in hate_result.lower() and 'no odioso' not in hate_result.lower():
                        hateful = True
                    if 'agresivo' in hate_result.lower():
                        aggressive = True
                    if 'dirigido' in hate_result.lower():
                        targeted = True

                    new_row = pd.DataFrame({
                        'Texto': [new_text],
                        'Análisis de Sentimiento': [sentiment],
                        'Odio': [hateful],
                        'Agresividad': [aggressive],
                        'Objetivismo': [targeted]
                    })
                    st.session_state.analysis_df = pd.concat([st.session_state.analysis_df, new_row], ignore_index=True)
                    st.session_state.last_analysis_results = None  # Limpiamos los resultados
                    st.toast("Texto añadido correctamente 👍")
                    st.rerun()
                else:
                    st.toast("El texto actual no coincide con el último texto analizado. Por favor, analize el texto antes de añadirlo 🔍")
        else:
            st.toast("No hay texto para añadir 👀")
    if descartar:
        st.session_state.last_analysis_results = None
        if 'last_analyzed_text' in st.session_state:
               del st.session_state.last_analyzed_text
        st.toast("Resultados descartados correctamente")
        st.rerun()
            
    if st.session_state.last_analysis_results:
        with st.expander(f'Resultados del análisis para el texto: "*{st.session_state.last_analyzed_text}*"', icon="🔍", expanded=True):  
            sentiment_result, hate_result, fig_sentiment, fig_hate = st.session_state.last_analysis_results

            st.write(sentiment_result, unsafe_allow_html=True)
            st.write(hate_result, unsafe_allow_html=True)
            st.markdown("---")
            col1,col2= st.columns([1,1])    
            with col1:
                st.write("### Distribución de Sentimientos")
                st.plotly_chart(fig_sentiment, use_container_width=True)
            with col2:
                st.write("### Métricas de Odio")
                st.plotly_chart(fig_hate, use_container_width=True)

        if not st.session_state.analysis_df.empty:
            st.subheader("Tabla de Resultados")
            st.write(st.session_state.analysis_df)

    st.subheader("Importar Datos")
    
    # Añadir opción para analizar tweets
    if 'tweets_df' in st.session_state and st.session_state.tweets_df is not None:
        if st.button("Analizar Tweets Extraídos"):
            tweets_df = st.session_state.tweets_df
            sentiment_analyzer, hate_analizer = lm()
            
            results_df = pd.DataFrame(columns=[
                'Texto', 
                'Análisis de Sentimiento',
                'Odio',
                'Agresividad',
                'Objetivismo'
            ])
            
            for _, row in tweets_df.iterrows():
                text = row['Texto']
                sentiment, prob_sentiment, _ = sentiment_analisys(text, sentiment_analyzer)
                hate, probs_hate, _ = hate_analisys(text, hate_analizer)
                
                if sentiment == 'NEG':
                    sentiment = 'Negativo'
                elif sentiment == 'POS':
                    sentiment = 'Positivo'
                else:
                    sentiment = 'Neutro'
                
                hateful = 'hateful' in hate
                aggressive = 'aggressive' in hate
                targeted = 'targeted' in hate
                
                new_row = pd.DataFrame({
                    'Texto': [text],
                    'Análisis de Sentimiento': [sentiment],
                    'Odio': [hateful],
                    'Agresividad': [aggressive],
                    'Objetivismo': [targeted]
                })
                results_df = pd.concat([results_df, new_row], ignore_index=True)
            
            st.session_state.analysis_df = pd.concat([st.session_state.analysis_df, results_df], ignore_index=True)
            st.toast("Tweets analizados correctamente 👍")
            st.rerun()
    
    uploaded_file = st.file_uploader("Sube un archivo CSV", type=['csv'], help="""Solo se aceptan archivos en el mismo formato 
                                     que los que se descargan desde la app
                                     descargar en el boton de la parte superior derecha de la tabla. Si se carga una sola columna de textos directamente se analizarán.""")

    if uploaded_file is not None and 'last_uploaded_file' not in st.session_state:
        try:
            encodings = ['utf-8', 'latin1']
            delimiters = [',', ';', '\t', '\n']
            df = None

            for encoding in encodings:
                try:
                    for delimiter in delimiters:
                        try:
                            df = pd.read_csv(uploaded_file, encoding=encoding, delimiter=delimiter)
                            if not df.empty:
                                break
                        except (UnicodeDecodeError, pd.errors.EmptyDataError):
                            continue

                    if df is None or df.empty:
                        uploaded_file.seek(0)
                        content = uploaded_file.read().decode(encoding)
                        lines = [line.strip() for line in content.split('\n') if line.strip()]
                        if lines:
                            df = pd.DataFrame({'Texto': lines})
                except Exception:
                    continue

                if df is not None and not df.empty:
                    break

            if df is None or df.empty:
                st.error("No se pudo leer el archivo. Por favor, asegúrate de que el archivo contenga datos válidos.")
                return
            
            # Eliminar columnas de índice duplicadas
            if 'Unnamed: 0' in df.columns:
                df = df.drop('Unnamed: 0', axis=1)
            
            # Si el archivo tiene una sola columna analizar los textos 
            if len(df.columns) == 1:
                st.info("Archivo con una sola columna, se analizarán los textos.")
                text_column = df.columns[0]
                sentiment_analyzer, hate_analizer = lm()

                results_df = pd.DataFrame(columns=[
                    'Texto', 
                    'Análisis de Sentimiento',
                    'Odio',
                    'Agresividad',
                    'Objetivismo'
                ])

                for text in df[text_column]:
                    sentiment, prob_sentiment, fig_sentiment = sentiment_analisys(text, sentiment_analyzer)
                    hate, probs_hate, fig_hate = hate_analisys(text, hate_analizer)

                    if sentiment == 'NEG':
                        sentiment='Negativo'
                    elif sentiment == 'POS':
                        sentiment='Positivo'
                    else:
                        sentiment='Neutro'

                    hateful = 'hateful' in hate
                    aggressive = 'aggressive' in hate
                    targeted = 'targeted' in hate

                    new_row = pd.DataFrame({
                        'Texto': [text],
                        'Análisis de Sentimiento': [sentiment],
                        'Odio': [hateful],
                        'Agresividad': [aggressive],
                        'Objetivismo': [targeted]
                    })
                    results_df = pd.concat([results_df, new_row], ignore_index=True)

                st.session_state.analysis_df = results_df
                st.toast("Textos analizados correctamente 👍")
                st.session_state.last_uploaded_file = uploaded_file.name
                st.rerun()
                

            else:
                required_columns = ['Texto', 'Análisis de Sentimiento', 'Odio', 'Agresividad', 'Objetivismo']
                if all(col in df.columns for col in required_columns):
                    st.session_state.analysis_df = df
                    st.toast("Archivo importado correctamente 👍")
                    st.session_state.last_uploaded_file = uploaded_file.name
                    st.rerun()
                else:
                    st.error(f"El archivo debe contener las columnas: {', '.join(required_columns)}")
        except Exception as e:
            st.error(f"Error al importar el archivo: {str(e)}")

    if st.button("Limpiar Todos los Resultados :wastebasket:"):
        st.session_state.analysis_df = pd.DataFrame(columns=[
            'Texto', 
            'Análisis de Sentimiento',
            'Odio',
            'Agresividad',
            'Objetivismo'
        ])
        st.session_state.last_analysis_results = None
        if 'last_uploaded_file' in st.session_state:
            del st.session_state.last_uploaded_file
        st.toast("Resultados limpiados correctamente")
        st.rerun()

main()
