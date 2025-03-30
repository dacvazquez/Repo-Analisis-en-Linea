
    if opcion == "Analizar Varios":
        st.header("Análisis Múltiple de Textos")
        
        # Opciones para importar/exportar en pestañas para ahorrar espacio
        tab1, tab2, tab3 = st.tabs(["Añadir Texto", "Importar/Exportar", "Ver Resultados"])
        
        with tab1:
            st.subheader("Añadir Nuevo Texto")
            new_text = st.text_area("Ingrese el texto a analizar", key="new_text_input")
            if st.button("Analizar y Añadir"):
                if new_text:
                    with st.spinner('Analizando texto...'):
                        # Usar la función optimizada con caché
                        sentiment_result, hate_result = analyze_text(new_text, sentiment_analyzer, hate_analizer)
                    
                    # Añadir al DataFrame
                    new_row = pd.DataFrame({
                        'Texto': [new_text],
                        'Análisis de Sentimiento': [sentiment_result],
                        'Análisis de Odio': [hate_result]
                    })
                    st.session_state.analysis_df = pd.concat([st.session_state.analysis_df, new_row], ignore_index=True)
                    st.success("Texto analizado y añadido correctamente")
                    # Limpiar el campo de texto
                    st.session_state.new_text_input = ""
                    # Forzar el rerun para mostrar el DataFrame actualizado
                    st.experimental_rerun()
                else:
                    st.warning("Por favor, ingrese un texto para analizar")
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Importar Datos")
                uploaded_file = st.file_uploader("Sube un archivo CSV", type=['csv'])
                if uploaded_file is not None:
                    try:
                        df = pd.read_csv(uploaded_file)
                        if all(col in df.columns for col in ['Texto', 'Análisis de Sentimiento', 'Análisis de Odio']):
                            st.session_state.analysis_df = df
                            st.success("Archivo importado correctamente")
                        else:
                            st.error("El archivo debe contener las columnas: Texto, Análisis de Sentimiento, Análisis de Odio")
                    except Exception as e:
                        st.error(f"Error al importar el archivo: {str(e)}")
            
            with col2:
                st.subheader("Exportar Datos")
                if not st.session_state.analysis_df.empty:
                    csv = st.session_state.analysis_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Descargar como CSV",
                        data=csv,
                        file_name="analisis_textos.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("No hay datos para exportar")
            
            # Opción para limpiar el DataFrame
            if st.button("Limpiar Todos los Resultados"):
                st.session_state.analysis_df = pd.DataFrame(columns=['Texto', 'Análisis de Sentimiento', 'Análisis de Odio'])
                st.success("Resultados limpiados correctamente")
        
        with tab3:
            st.subheader("Resultados del Análisis")
            if not st.session_state.analysis_df.empty:
                # Usar paginación si hay muchos registros
                page_size = 10
                total_pages = (len(st.session_state.analysis_df) - 1) // page_size + 1
                
                if total_pages > 1:
                    page = st.number_input(
                        f"Página (1-{total_pages})", 
                        min_value=1, 
                        max_value=total_pages, 
                        value=1
                    )
                    start_idx = (page - 1) * page_size
                    end_idx = min(start_idx + page_size, len(st.session_state.analysis_df))
                    st.dataframe(st.session_state.analysis_df.iloc[start_idx:end_idx])
                    st.text(f"Mostrando {start_idx+1}-{end_idx} de {len(st.session_state.analysis_df)} registros")
                else:
                    st.dataframe(st.session_state.analysis_df)
            else:
                st.info("No hay datos para mostrar. Añade textos para analizarlos.")
