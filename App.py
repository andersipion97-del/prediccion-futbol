import streamlit as st
import pandas as pd
from modelo_prediccion import cargar_datos_excel, obtener_estadisticas_equipo, predecir_ganador
import matplotlib.pyplot as plt 
import os
import time

@st.cache_data(ttl=60)
def cargar_datos_con_cache(path):
    return cargar_datos_excel(path)

ruta_excel = "estadisticas_equipos.xlsx"

# Cargar los datos con cache
df = cargar_datos_excel("estadisticas_equipos.xlsx")

# Botón para recargar datos manualmente
if st.button("🔄 Recargar archivo Excel"):
    st.cache_data.clear()
    st.warning("Archivo recargado. Vuelve a seleccionar los equipos.")

# Ruta y tiempo de modificación del archivo
ruta_archivo = "estadisticas_equipos.xlsx"
ultima_modificacion = os.path.getmtime(ruta_archivo)

# Si es la primera vez, o si el archivo cambió, actualiza
if "ultima_modificacion" not in st.session_state or st.session_state.ultima_modificacion != ultima_modificacion:
    st.session_state.df = cargar_datos_con_cache(ruta_archivo)
    st.session_state.ultima_modificacion = ultima_modificacion

df = st.session_state.df

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
            # Mostrar promedios por partido de cada equipo
            st.subheader("📌 Estadísticas promedio por partido")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"### {equipo1['nombre']}")
                st.write(f"Goles a favor: {equipo1['goles_favor']:.2f}")
                st.write(f"Goles en contra: {equipo1['goles_contra']:.2f}")
                st.write(f"Puntos por partido: {equipo1['puntos']:.2f}")
                st.write(f"Remates: {equipo1['remates']:.2f}")
                st.write(f"Amarillas: {equipo1['amarillas']:.2f}")
                st.write(f"Esquinas: {equipo1['esquinas']:.2f}")

            with col2:
                st.markdown(f"### {equipo2['nombre']}")
                st.write(f"Goles a favor: {equipo2['goles_favor']:.2f}")
                st.write(f"Goles en contra: {equipo2['goles_contra']:.2f}")
                st.write(f"Puntos por partido: {equipo2['puntos']:.2f}")
                st.write(f"Remates: {equipo2['remates']:.2f}")
                st.write(f"Amarillas: {equipo2['amarillas']:.2f}")
                st.write(f"Esquinas: {equipo2['esquinas']:.2f}")
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

            # Cálculo de promedios por partido
            st.subheader("📊 Comparativa de promedios por partido")

            promedios_equipo1 = {
                "Goles a favor (prom)": equipo1["goles_favor"] / equipo1["pj"],
                "Goles en contra (prom)": equipo1["goles_contra"] / equipo1["pj"],
                "Remates (prom)": equipo1["remates"] / equipo1["pj"],
                "Amarillas (prom)": equipo1["amarillas"] / equipo1["pj"],
                "Esquinas (prom)": equipo1["esquinas"] / equipo1["pj"],
                "Puntos (prom)": equipo1["puntos"] / equipo1["pj"]
            }

            promedios_equipo2 = {
                "Goles a favor (prom)": equipo2["goles_favor"] / equipo2["pj"],
                "Goles en contra (prom)": equipo2["goles_contra"] / equipo2["pj"],
                "Remates (prom)": equipo2["remates"] / equipo2["pj"],
                "Amarillas (prom)": equipo2["amarillas"] / equipo2["pj"],
                "Esquinas (prom)": equipo2["esquinas"] / equipo2["pj"],
                "Puntos (prom)": equipo2["puntos"] / equipo2["pj"]
            }

            df_promedios = pd.DataFrame({
                nombre1: promedios_equipo1,
                nombre2: promedios_equipo2
            })

            st.dataframe(df_promedios.transpose().round(2))

            # Gráfico comparativo de promedios
            st.subheader("📉 Gráfico de promedios por partido")
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            df_promedios.plot(kind='bar', ax=ax2)
            plt.title("Promedios por partido")
            plt.ylabel("Promedio")
            plt.xticks(rotation=45)
            st.pyplot(fig2)

        except ValueError as e:
            st.error(str(e))