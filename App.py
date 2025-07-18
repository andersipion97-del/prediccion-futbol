import streamlit as st
import pandas as pd
from modelo_prediccion import cargar_datos_excel, obtener_estadisticas_equipo, predecir_ganador
import matplotlib.pyplot as plt 

# Cargar los datos una vez
df = cargar_datos_excel("estadisticas_equipos.xlsx")

st.title("⚽ Predicción de Ganador entre Equipos")

# Selección de equipos
equipos_disponibles = df["Equipo"].unique()
equipo1_nombre = st.selectbox("Selecciona el Primer Equipo", equipos_disponibles)
equipo2_nombre = st.selectbox("Selecciona el Segundo Equipo", equipos_disponibles)

# Evitar comparar el mismo equipo consigo mismo
if equipo1_nombre == equipo2_nombre:
    st.warning("Por favor selecciona dos equipos distintos.")
else:
    if st.button("Predecir Resultado"):
        try:
            equipo1 = obtener_estadisticas_equipo(equipo1_nombre, df)
            equipo2 = obtener_estadisticas_equipo(equipo2_nombre, df)
            resultado = predecir_ganador(equipo1, equipo2)
            st.success(resultado)

            # Mostrar tabla comparativa
            st.subheader("📊 Comparativa de estadísticas")

            nombre1 = equipo1["nombre"]
            nombre2 = equipo2["nombre"]

            datos1 = {k: v for k, v in equipo1.items() if k != "nombre"}
            datos2 = {k: v for k, v in equipo2.items() if k != "nombre"}

            estadisticas_comparadas = pd.DataFrame({
                nombre1: datos1,
                nombre2: datos2
            })

            estadisticas_comparadas = estadisticas_comparadas.apply(pd.to_numeric, errors = 'coerce')
            estadisticas_comparadas.dropna(inplace=True)

            st.subheader("Comparativa de estadisticas")
            st.dataframe(estadisticas_comparadas.transpose().round(2))

            # Gráfico de barras comparativo
            st.subheader("📉 Gráfico de comparación")
            fig, ax = plt.subplots(figsize=(10, 5))
            estadisticas_comparadas.plot(kind='bar', ax=ax)
            plt.title("Comparación de estadísticas entre equipos")
            plt.ylabel("Valor")
            plt.xticks(rotation=45)
            st.pyplot(fig)

        except ValueError as e:
            st.error(str(e))
