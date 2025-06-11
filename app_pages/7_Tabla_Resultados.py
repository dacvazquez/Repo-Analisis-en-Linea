import streamlit as st
import pandas as pd
from analizer_functions import sentiment_analisys, hate_analisys
from model_loader import load_models as lm

st.title("✏️ Resultados de Análisis")

# Verifica si el DataFrame existe en session_state
if 'analysis_df' not in st.session_state or st.session_state.analysis_df.empty:
    st.warning("No hay datos disponibles. Agrega textos desde la sección de análisis.")
    st.stop()

# Copia editable del DataFrame
editable_df = st.session_state.analysis_df.copy().reset_index(drop=True)

# Mostrar tabla con selección
st.subheader("📋 Tabla de Resultados")
st.dataframe(editable_df, use_container_width=True, height=400)

# Selección de fila para editar o eliminar
row_to_edit = st.number_input("Selecciona el índice de la fila a editar", min_value=0, max_value=len(editable_df)-1, step=1)

# Botones de acciones
col1, col2, col3, col4 = st.columns([1,1,1,1], vertical_alignment="center", gap="large")
with col1:
    if st.button("⬆️ Mover Arriba"):
        if row_to_edit > 0:
            st.session_state.analysis_df.iloc[[row_to_edit-1, row_to_edit]] = \
                st.session_state.analysis_df.iloc[[row_to_edit, row_to_edit-1]].values
            st.toast("Fila movida hacia arriba")
with col2:
    if st.button("⬇️ Mover Abajo"):
        if row_to_edit < len(editable_df) - 1:
            st.session_state.analysis_df.iloc[[row_to_edit, row_to_edit+1]] = \
                st.session_state.analysis_df.iloc[[row_to_edit+1, row_to_edit]].values
            st.toast("Fila movida hacia abajo")
with col3:
    if st.button("🗑️ Eliminar Fila"):
        st.session_state.analysis_df.drop(index=row_to_edit, inplace=True)
        st.session_state.analysis_df.reset_index(drop=True, inplace=True)
        st.toast(f"Fila {row_to_edit} eliminada")
with col4:
    graficos = st.button("📊 Ver Gráficos")
if graficos:
    texto = editable_df.iloc[row_to_edit]['Texto']
    sentiment_analyzer, hate_analizer = lm()
    
    # Realizar análisis
    sentiment, prob_sentiment, fig_sentiment = sentiment_analisys(texto, sentiment_analyzer)
    hate, probs_hate, fig_hate = hate_analisys(texto, hate_analizer)
    
    # Mostrar gráficos
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Distribución de Sentimientos")
        st.plotly_chart(fig_sentiment, use_container_width=True)
    with col2:
        st.write("### Métricas de Odio")
        st.plotly_chart(fig_hate, use_container_width=True)

# Mostrar DataFrame actualizado si hubo cambios
st.markdown("---")
st.subheader("🔄 Vista Actualizada de la Tabla")
st.dataframe(st.session_state.analysis_df, use_container_width=True)
