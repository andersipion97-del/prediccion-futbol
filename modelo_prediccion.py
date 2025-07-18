import pandas as pd

#paso 2
def cargar_datos_excel(ruta_archivo):
    return pd.read_excel(ruta_archivo)

#paso 3
def obtener_estadisticas_equipo(nombre_equipo, dataframe):
    equipo = dataframe[dataframe["Equipo"] == nombre_equipo]
    if equipo.empty:
        raise ValueError(f"No se encontró información para el equipo '{nombre_equipo}'")
    
    fila = equipo.iloc[0]
    return {
        "nombre": fila["Equipo"],
        "goles_favor": fila["GF"],
        "goles_contra": fila["GC"],
        "puntos": (fila["PG"] * 3) + (fila["PE"]),
        "remates": fila["Remates"],
        "amarillas": fila["Amarillas"],
        "esquinas": fila["Esquina"]
    }

#paso 4 + 5 nuevas variables
def predecir_ganador(equipo1, equipo2):
    puntaje_1 = (
        equipo1['goles_favor'] * 0.4 -
        equipo1['goles_contra'] * 0.2 +
        equipo1['puntos'] * 0.4 +
        equipo1['remates'] * 0.3 -
        equipo1['amarillas'] * 0.2 +
        equipo1['esquinas'] * 0.1
    )
    puntaje_2 = (
        equipo2['goles_favor'] * 0.4 -
        equipo2['goles_contra'] * 0.2 +
        equipo2['puntos'] * 0.4 +
        equipo2['remates'] * 0.3 -
        equipo2['amarillas'] * 0.2 +
        equipo2['esquinas'] * 0.1
    )

    if puntaje_1 > puntaje_2:
        return f"Ganaría {equipo1['nombre']} (puntaje:  {puntaje_1:.2f} vs {puntaje_2:.2f})"
    elif puntaje_2 > puntaje_1:
        return f"Ganaría {equipo2['nombre']} (puntaje: {puntaje_2:.2f} vs {puntaje_1:.2f})"
    else:
        return "Empate técnico"