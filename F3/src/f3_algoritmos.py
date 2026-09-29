"""Prototipos de F3: lectura, indicador regional y mediciones reproducibles."""

from __future__ import annotations

from pathlib import Path
from time import perf_counter
from typing import Callable

import pandas as pd


COLUMNAS_ORIGEN = [
    "ANO_NAC", "MES_NAC", "GRUPO_ETARIO_MADRE", "REGION_RESIDENCIA",
    "GLOSA_REGION_RESIDENCIA", "TALLA",
]
COLUMNAS_INDICADOR = ["REGION_RESIDENCIA", "madre_menor_20"]


def cargar_preparado(ruta: str | Path) -> pd.DataFrame:
    """Carga las dos columnas necesarias del CSV preparado por F2."""
    ruta = Path(ruta)
    if not ruta.is_file():
        raise FileNotFoundError(f"No se encontró la salida de F2: {ruta}")
    datos = pd.read_csv(ruta, usecols=COLUMNAS_INDICADOR)
    if datos.empty or datos[COLUMNAS_INDICADOR].isna().any().any():
        raise ValueError("La salida de F2 está vacía o tiene regiones/indicadores ausentes.")
    if not pd.api.types.is_bool_dtype(datos["madre_menor_20"]):
        raise ValueError("madre_menor_20 debe ser una columna booleana.")
    return datos


def proporcion_bucle(datos: pd.DataFrame) -> pd.DataFrame:
    """Cuenta nacimientos y madres menores de 20 con un recorrido de filas."""
    conteos: dict[int, list[int]] = {}
    for region, es_menor in datos[COLUMNAS_INDICADOR].itertuples(index=False, name=None):
        clave = int(region)
        if clave not in conteos:
            conteos[clave] = [0, 0]
        conteos[clave][0] += 1
        conteos[clave][1] += int(es_menor)
    salida = pd.DataFrame(
        [(region, total, menores) for region, (total, menores) in conteos.items()],
        columns=["REGION_RESIDENCIA", "nacimientos", "madres_menores_20"],
    ).sort_values("REGION_RESIDENCIA").reset_index(drop=True)
    salida["porcentaje"] = 100 * salida["madres_menores_20"] / salida["nacimientos"]
    return salida


def proporcion_groupby(datos: pd.DataFrame) -> pd.DataFrame:
    """Calcula el mismo indicador con la agrupación de pandas."""
    salida = (
        datos.groupby("REGION_RESIDENCIA", sort=True, observed=True)["madre_menor_20"]
        .agg(nacimientos="size", madres_menores_20="sum")
        .reset_index()
    )
    salida["porcentaje"] = 100 * salida["madres_menores_20"] / salida["nacimientos"]
    return salida


def medir_tiempos(funcion: Callable[[], object], repeticiones: int = 3) -> list[float]:
    """Repite una operación y devuelve cada duración en segundos."""
    if repeticiones < 1:
        raise ValueError("repeticiones debe ser al menos 1")
    duraciones = []
    for _ in range(repeticiones):
        inicio = perf_counter()
        funcion()
        duraciones.append(perf_counter() - inicio)
    return duraciones


def leer_original(ruta: str | Path, columnas: list[str] | None = None) -> pd.DataFrame:
    """Lee el CSV original completo o un subconjunto, sin modificarlo."""
    return pd.read_csv(ruta, sep=";", encoding="utf-8", usecols=columnas, low_memory=False)
