import pandas as pd
import os
import streamlit as st

#paso 2
@st.cache_data(show_spinner=False, persist=True)  # Asegura recarga si el archivo cambia
def cargar_datos_excel(ruta_archivo: str):
    df = pd.read_excel(ruta_archivo)

    # Normalizar nombres de equipos
    df["Equipo"] = df["Equipo"].str.strip().str.title()

    return df

#paso 3
def obtener_estadisticas_equipo(nombre_equipo, dataframe):
    equipo = dataframe[dataframe["Equipo"] == nombre_equipo]
    if equipo.empty:
        raise ValueError(f"No se encontró información para el equipo '{nombre_equipo}'")
    
    fila = equipo.iloc[0]
    return {
        "nombre": fila["Equipo"],
        "pj": fila["PJ"],
        "goles_favor": fila["GF"],
        "goles_contra": fila["GC"],
        "puntos": (fila["PG"] * 3) + (fila["PE"]),
        "remates": fila["Remates"],
        "amarillas": fila["Amarillas"],
        "esquinas": fila["Esquina"]
    }

# paso 4: modelo usando promedios por partido
def predecir_ganador(equipo1, equipo2):
    # Promedios por partido
    gf1 = equipo1["goles_favor"] / equipo1["pj"]
    gc1 = equipo1["goles_contra"] / equipo1["pj"]
    rem1 = equipo1["remates"] / equipo1["pj"]
    ama1 = equipo1["amarillas"] / equipo1["pj"]
    esq1 = equipo1["esquinas"] / equipo1["pj"]
    pts1 = equipo1["puntos"] / equipo1["pj"]

    gf2 = equipo2["goles_favor"] / equipo2["pj"]
    gc2 = equipo2["goles_contra"] / equipo2["pj"]
    rem2 = equipo2["remates"] / equipo2["pj"]
    ama2 = equipo2["amarillas"] / equipo2["pj"]
    esq2 = equipo2["esquinas"] / equipo2["pj"]
    pts2 = equipo2["puntos"] / equipo2["pj"]

    puntaje_1 = (
        gf1 * 0.4 - gc1 * 0.2 + pts1 * 0.4 + rem1 * 0.3 - ama1 * 0.2 + esq1 * 0.1
    )
    puntaje_2 = (
        gf2 * 0.4 - gc2 * 0.2 + pts2 * 0.4 + rem2 * 0.3 - ama2 * 0.2 + esq2 * 0.1
    )

    if puntaje_1 > puntaje_2:
        return f"Ganaría {equipo1['nombre']} (puntaje: {puntaje_1:.2f} vs {puntaje_2:.2f})"
    elif puntaje_2 > puntaje_1:
        return f"Ganaría {equipo2['nombre']} (puntaje: {puntaje_2:.2f} vs {puntaje_1:.2f})"
    else:
        return "Empate técnico"