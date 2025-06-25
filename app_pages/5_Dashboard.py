import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import nltk
import io

# Download required NLTK data
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def save_wordcloud_to_buffer(wordcloud):
    """Guarda la nube de palabras en un buffer de memoria."""
    buffer = io.BytesIO()
    plt.figure(figsize=(15, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    buffer.seek(0)
    return buffer

def main():
    st.title("Estadísticas del Análisis")
    
    if 'analysis_df' not in st.session_state or st.session_state.analysis_df.empty:
        st.warning("No hay datos para analizar. Por favor, ingresa algunos textos primero.")
    else:
        # Primera fila: Métricas principales
        st.markdown("### Métricas Principales")
        
        # Calcular métricas adicionales
        total_texts = len(st.session_state.analysis_df)
        sentiment_counts = st.session_state.analysis_df['Análisis de Sentimiento'].value_counts()
        dominant_sentiment = sentiment_counts.index[0]
        
        # Calcular porcentajes de sentimientos
        sentiment_percentages = (sentiment_counts / total_texts * 100).apply(lambda x: round(x, 1))
        
        # Calcular métricas de odio
        hate_counts = {
            'Odio': st.session_state.analysis_df['Odio'].sum(),
            'Agresividad': st.session_state.analysis_df['Agresividad'].sum(),
            'Objetivismo': st.session_state.analysis_df['Objetivismo'].sum()
        }
        # total_hate = sum(hate_counts.values())
        
        # Longitud promedio de textos
        avg_text_length = round(st.session_state.analysis_df['Texto'].str.len().mean(), 1)
        
        # Tasa de odio
        # hate_rate = round((total_hate / total_texts * 100), 1)
        
        # Primera fila: Métricas básicas
        col1, col2, col3 = st.columns(3, border=True)
        
        with col1:
            st.markdown("#### 📊 Total de Análisis")
            st.metric("Total de Textos", total_texts)
            st.metric("Longitud Promedio", f"{avg_text_length} caracteres")
        
        with col2:
            st.markdown("#### 😊 Sentimiento")
            st.metric("Sentimiento Dominante", dominant_sentiment)
            st.metric("Porcentaje", f"{sentiment_percentages[dominant_sentiment]}%")
        
        with col3:
            dominant_hate = max(hate_counts.items(), key=lambda x: x[1])[0]
            st.markdown("#### 🤬 Análisis de Odio")
            st.metric("Tipo de Odio Dominante", dominant_hate)
            # Mostrar tasas individuales para cada tipo de odio
            for hate_type, count in hate_counts.items():
                rate = round((count / total_texts * 100), 1)
                max_hate_type = max(hate_counts, key=lambda x: hate_counts[x] / total_texts)
                # st.metric(f"Tasa de {hate_type}", f"{rate}%")
                max_rate = round((hate_counts[max_hate_type] / total_texts * 100), 1)
            st.metric(f"Tasa de {max_hate_type}", f"{max_rate}%")
        
        # Segunda fila: Métricas detalladas
        st.markdown("<br>", unsafe_allow_html=True)
        st.divider()

        st.markdown("### Métricas del Análisis")
        
        col1, col2, col3 = st.columns(3, border=True)
        
        with col1:
            st.markdown("#### 📈 Análisis de Sentimientos")
            for sentiment, percentage in sentiment_percentages.items():
                st.metric(
                    f"Sentimiento {sentiment}",
                    f"{percentage}%",
                    f"{sentiment_counts[sentiment]} textos"
                )
        
        with col2:
            st.markdown("#### 🎯 Análisis de Odio")
            for hate_type, count in hate_counts.items():
                percentage = round((count / total_texts * 100), 1)
                st.metric(
                    f"{hate_type}",
                    f"{percentage}%",
                    f"{count} textos"
                )
        
        with col3:
            st.markdown("#### 📝 Estadísticas de Texto")
            st.metric(
                "Texto más largo",
                f"{st.session_state.analysis_df['Texto'].str.len().max()} caracteres"
            )
            st.metric(
                "Texto más corto",
                f"{st.session_state.analysis_df['Texto'].str.len().min()} caracteres"
            )
            st.metric(
                "Desviación estándar",
                f"{st.session_state.analysis_df['Texto'].str.len().std().round(1)} caracteres"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Segunda fila: Gráficos de distribución
        st.divider()
        st.markdown("### Distribuciones")
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2, border=True)
        
        with col1:
            st.markdown("#### 😊 Distribución de Sentimientos")
            st.markdown("<br>", unsafe_allow_html=True)

            sentiment_counts = pd.Series(st.session_state.analysis_df['Análisis de Sentimiento'].value_counts())
            
            # Definir colores para sentimientos
            sentiment_colors = {
                'Positivo': '#2ecc71',  # Verde
                'Neutro': '#95a5a6',    # Gris
                'Negativo': '#e74c3c'   # Rojo
            }
            
            # Convertir valores a lista para evitar el error con max
            sentiment_values = sentiment_counts.tolist()
            max_sentiment = max(sentiment_values)
            
            fig_sentiment = go.Figure(data=[go.Pie(
                labels=sentiment_counts.index,
                values=sentiment_values,
                hole=0.3,
                marker=dict(
                    colors=[sentiment_colors.get(label, '#3498db') for label in sentiment_counts.index],
                    line=dict(color='white', width=2)  # Borde blanco para mejor contraste
                ),
                textinfo='percent+label',  # Muestra porcentaje y etiqueta
                textposition='inside',     # Texto dentro de las porciones
                insidetextorientation='radial',  # Orientación del texto
                rotation=45,              # Rotación inicial del gráfico
                hoverinfo='label+percent+value',  # Info al pasar el mouse
                textfont=dict(size=14, family='Arial', color='white'),  # Fuente del texto
                pull=[0.05 if val == max_sentiment else 0 for val in sentiment_values] # Destacar la porción mayor
            )])

            # Personalización del layout
            fig_sentiment.update_layout(
                height=500,
                margin=dict(t=0, b=20, l=0, r=50),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=12)
                ),
                plot_bgcolor='rgba(0,0,0,0)',  # Fondo transparente
                paper_bgcolor='rgba(0,0,0,0)'
            )
            fig_sentiment.update_traces(
                hovertemplate="<b>%{label}</b><br>Porcentaje: %{percent}<br>Total: %{value}",
                hoverlabel=dict(
                    bgcolor="black",  # Fondo del tooltip
                    font_size=14,     # Tamaño de fuente
                    font_family="Arial",
                    bordercolor="#333"  # Borde del tooltip
                ),
                name=""  # Eliminar "trace:0"
            )
            st.plotly_chart(fig_sentiment, use_container_width=True)
        
        with col2:
            st.markdown("#### 🤬 Distribución de Tipos de Odio")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Definir colores para tipos de odio
            hate_colors = {
                'Odio': '#e74c3c',    # Rojo
                'Agresividad': '#f39c12',  # Naranja
                'Objetivismo': '#9b59b6'     # Púrpura
            }
            fig_hate = go.Figure(data=[go.Pie(
            labels=list(hate_counts.keys()),
            values=list(hate_counts.values()),
            hole=0.3,
            marker=dict(
            colors=[hate_colors.get(label, '#3498db') for label in hate_counts.keys()],
            line=dict(color='white', width=2)  # Borde blanco para mejor contraste
            ),
            textinfo='percent+label',  # Muestra porcentaje y etiqueta
            textposition='inside',     # Texto dentro de las porciones
            insidetextorientation='radial',  # Orientación del texto
            rotation=45,              # Rotación inicial del gráfico
            hoverinfo='label+percent+value',  # Info al pasar el mouse
            textfont=dict(size=14, family='Arial', color='white'),  # Fuente del texto
            pull=[0.05 if max(hate_counts.values()) == val else 0 for val in hate_counts.values()]  # Destacar la porción mayor
            )])

             # Personalización del layout
            fig_hate.update_layout(
            height=500,
            margin=dict(t=0, b=20, l=0, r=50),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(size=12)
            ),
            plot_bgcolor='rgba(0,0,0,0)',  # Fondo transparente
            paper_bgcolor='rgba(0,0,0,0)'
            )
            fig_hate.update_traces(
                hovertemplate="<b>%{label}</b><br>Porcentaje: %{percent}<br>Total: %{value}",
                hoverlabel=dict(
                    bgcolor="black",  # Fondo del tooltip
                    font_size=14,     # Tamaño de fuente
                    font_family="Arial",
                    bordercolor="#333"  # Borde del tooltip
                ),
                name=""  # ¡Esto es clave para eliminar "trace:0"!
            )
            st.plotly_chart(fig_hate, use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True)
                    
        # Tercera fila: Nube de palabras
        st.divider()
        st.markdown("### Nube de Palabras")
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            # Combinar todos los textos
            all_text = ' '.join(st.session_state.analysis_df['Texto'])
            
            # Crear nube de palabras
            wordcloud = WordCloud(
                width=1400,
                height=600,  
                mode="RGBA",
                background_color="black",
                max_words=100,
                max_font_size=150,
                random_state=42,
                collocations=False
            ).generate(all_text)
            
            # Mostrar la nube de palabras
            fig, ax = plt.subplots(figsize=(15, 8))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
            
            st.markdown("#### Opciones de Exportación")
            
            # Guardar la nube de palabras en un buffer
            buffer = save_wordcloud_to_buffer(wordcloud)
            
            # Botón para descargar la imagen
            if st.download_button(
                label="📥 Descargar Nube de Palabras",
                data=buffer,
                file_name="wordcloud.png",
                mime="image/png"
            ):
                st.toast("Nube de palabras guardada correctamente")
        
        # Botón para filtrar stopwords
        if st.button("🔍 Filtrar Stopwords"):
            with col2:
                # Obtener stopwords en español
                spanish_stopwords = set(stopwords.words('spanish'))
                
                # Crear nube de palabras con stopwords filtradas
                wordcloud_filtered = WordCloud(
                    width=1400,
                    height=600,  
                    mode="RGBA",
                    background_color=None,
                    max_words=100,
                    max_font_size=150,
                    random_state=42,
                    collocations=False,
                    stopwords=spanish_stopwords
                ).generate(all_text)
                
                # Mostrar la nueva nube de palabras
                fig, ax = plt.subplots(figsize=(15, 8))
                ax.imshow(wordcloud_filtered, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
                
                # Guardar la nube de palabras filtrada en un buffer
                buffer_filtered = save_wordcloud_to_buffer(wordcloud_filtered)
                
                # Botón para descargar la imagen filtrada
                if st.download_button(
                    label="📥 Descargar Nube de Palabras (sin stopwords)",
                    data=buffer_filtered,
                    file_name="wordcloud_filtered.png",
                    mime="image/png"
                ):
                    st.toast("Nube de palabras filtrada guardada correctamente")

        # Nueva sección: Análisis de Patrones
        st.divider()
        st.markdown("### Análisis de Patrones")
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, border=True)
        
        with col1:
            st.markdown("#### 📈 Patrones de Sentimiento y Odio")

            # Calcular porcentaje de textos con odio por sentimiento
            sentiment_hate_pattern = pd.crosstab(
                st.session_state.analysis_df['Análisis de Sentimiento'],
                st.session_state.analysis_df['Odio'],
                normalize='index'
            ) * 100

            # Asegurar que existan ambas columnas (True y False)
            if True not in sentiment_hate_pattern.columns:
                sentiment_hate_pattern[True] = 0
            if False not in sentiment_hate_pattern.columns:
                sentiment_hate_pattern[False] = 0

            # Colores personalizados
            colors = {
                True: '#FF553B',   # Rojo para "Con Odio"
                False: '#636EFA'   # Azul para "Sin Odio"
            }

            # Crear gráfico de barras apiladas
            fig_pattern = go.Figure()

            for hate in [True, False]:
                if hate in sentiment_hate_pattern.columns:
                    fig_pattern.add_trace(go.Bar(
                        name='Con Odio' if hate else 'Sin Odio',
                        x=sentiment_hate_pattern.index,
                        y=sentiment_hate_pattern[hate],
                        text=sentiment_hate_pattern[hate].round(1).astype(str) + '%',
                        textposition='inside',
                        marker_color=colors[hate],
                        hovertemplate='%{y:.1f}%<br>Sentimiento: %{x}<extra></extra>'
                    ))

            fig_pattern.update_layout(
                barmode='stack',
                title='Distribución de Odio por Sentimiento',
                xaxis_title='Sentimiento',
                yaxis_title='Porcentaje',
                height=450,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=14),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.3,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=13)
                ),
                margin=dict(t=60, b=80)
            )

            st.plotly_chart(fig_pattern, use_container_width=True)
        with col2:
            st.markdown("#### 📊 Distribución de Longitud de Textos")

            # Crear histograma de longitudes de texto
            text_lengths = st.session_state.analysis_df['Texto'].str.len()

            fig_length = go.Figure()
            fig_length.add_trace(go.Histogram(
                x=text_lengths,
                nbinsx=30,
                name='Longitud de Textos',
                marker_color='#636EFA',  # Azul moderno para coherencia
                opacity=0.85,
                hovertemplate='Longitud: %{x}<br>Frecuencia: %{y}<extra></extra>'
            ))

            fig_length.update_layout(
                title='Distribución de Longitud de Textos',
                xaxis_title='Longitud (caracteres)',
                yaxis_title='Frecuencia',
                height=450,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=14),
                margin=dict(t=60, b=80),
                bargap=0.05
            )

            st.plotly_chart(fig_length, use_container_width=True)
main() 