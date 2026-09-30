"""Cuatro tratamientos intercambiables de talla, compatibles con la comparación de F2.

`ajustar` aprende valores de referencia y `transformar` los aplica sin alterar
las tallas observadas. Si se usaran en un modelo predictivo, el ajuste debería
hacerse solo con entrenamiento; aquí se reproducen los escenarios descriptivos
de F2 sobre la misma población completa para comprobar equivalencia.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Sequence

import numpy as np
import pandas as pd


COLUMNAS = ("REGION_RESIDENCIA", "talla_observada_cm")


def _columnas_validas(datos: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    """Comprueba la entrada común antes de aprender o aplicar una estrategia."""
    if not isinstance(datos, pd.DataFrame):
        raise TypeError("La entrada debe ser un DataFrame.")
    faltan = set(COLUMNAS) - set(datos.columns)
    if faltan:
        raise ValueError(f"Faltan columnas: {sorted(faltan)}")
    if datos.empty:
        raise ValueError("No hay registros para analizar.")
    region = pd.to_numeric(datos["REGION_RESIDENCIA"], errors="raise")
    talla = pd.to_numeric(datos["talla_observada_cm"], errors="raise").astype(float)
    if region.isna().any() or not np.isfinite(region).all() or (region % 1 != 0).any():
        raise ValueError("REGION_RESIDENCIA debe contener códigos enteros no ausentes.")
    if np.isinf(talla).any() or talla.dropna().le(0).any():
        raise ValueError("Las tallas observadas deben ser positivas y finitas.")
    return region.astype(int), talla


class EstrategiaTalla(ABC):
    """Contrato común: aprender parámetros y devolver una serie alineada."""

    nombre: str

    def __init__(self) -> None:
        self._ajustada = False
        self._parametros: dict[str, object] = {}

    def ajustar(self, datos: pd.DataFrame) -> EstrategiaTalla:
        region, talla = _columnas_validas(datos)
        if not talla.notna().any():
            raise ValueError("No hay tallas válidas para calcular valores de imputación.")
        self._ajustar(region, talla)
        self._ajustada = True
        return self

    def transformar(self, datos: pd.DataFrame) -> pd.Series:
        if not self._ajustada:
            raise RuntimeError("Primero debe llamar a ajustar().")
        region, talla = _columnas_validas(datos)
        salida = self._transformar(region, talla)
        if not salida.index.equals(talla.index) or not salida.loc[talla.notna()].equals(talla.dropna()):
            raise RuntimeError("La estrategia alteró las tallas observadas o el índice.")
        return salida.rename("talla_analisis_cm")

    @property
    def parametros(self) -> dict[str, object]:
        """Copia de los parámetros aprendidos, para registro sin alterar el estado."""
        if not self._ajustada:
            raise RuntimeError("Todavía no hay parámetros: llame a ajustar().")
        return deepcopy(self._parametros)

    @abstractmethod
    def _ajustar(self, region: pd.Series, talla: pd.Series) -> None:
        """Aprende los valores necesarios para esta alternativa."""

    @abstractmethod
    def _transformar(self, region: pd.Series, talla: pd.Series) -> pd.Series:
        """Aplica el tratamiento elegido con los parámetros ya aprendidos."""


class SinImputar(EstrategiaTalla):
    """Conserva ausencias para excluirlas solo del cálculo de talla."""

    nombre = "sin_imputar"

    def _ajustar(self, region: pd.Series, talla: pd.Series) -> None:
        self._parametros = {}

    def _transformar(self, region: pd.Series, talla: pd.Series) -> pd.Series:
        return talla.copy()


class MediaGeneral(EstrategiaTalla):
    """Rellena ausencias con la media observada del conjunto de ajuste."""

    nombre = "media_general"

    def _ajustar(self, region: pd.Series, talla: pd.Series) -> None:
        self._valor = float(talla.mean())
        self._parametros = {"valor_cm": self._valor}

    def _transformar(self, region: pd.Series, talla: pd.Series) -> pd.Series:
        return talla.fillna(self._valor)


class MedianaGeneral(EstrategiaTalla):
    """Rellena ausencias con la mediana observada del conjunto de ajuste."""

    nombre = "mediana_general"

    def _ajustar(self, region: pd.Series, talla: pd.Series) -> None:
        self._valor = float(talla.median())
        self._parametros = {"valor_cm": self._valor}

    def _transformar(self, region: pd.Series, talla: pd.Series) -> pd.Series:
        return talla.fillna(self._valor)


class MedianaRegional(EstrategiaTalla):
    """Usa la mediana regional y, si falta, la mediana general de respaldo."""

    nombre = "mediana_region"

    def _ajustar(self, region: pd.Series, talla: pd.Series) -> None:
        medianas = talla.groupby(region).median().dropna()
        self._medianas = {int(codigo): float(valor) for codigo, valor in medianas.items()}
        self._respaldo = float(talla.median())
        self._parametros = {
            "medianas_por_region_cm": self._medianas.copy(),
            "respaldo_general_cm": self._respaldo,
        }

    def _transformar(self, region: pd.Series, talla: pd.Series) -> pd.Series:
        valores_regionales = region.map(self._medianas).fillna(self._respaldo)
        return talla.fillna(valores_regionales)


class ComparadorImputacion:
    """Aplica cualquier conjunto de estrategias mediante la misma interfaz."""

    def __init__(self, estrategias: Sequence[EstrategiaTalla]) -> None:
        if not estrategias or any(not isinstance(e, EstrategiaTalla) for e in estrategias):
            raise ValueError("Se requiere al menos una EstrategiaTalla válida.")
        nombres = [e.nombre for e in estrategias]
        if len(nombres) != len(set(nombres)):
            raise ValueError("Los nombres de las estrategias deben ser únicos.")
        self._estrategias = tuple(estrategias)

    def comparar(self, datos: pd.DataFrame) -> tuple[dict[str, pd.Series], pd.DataFrame]:
        _, observada = _columnas_validas(datos)
        resultados: dict[str, pd.Series] = {}
        filas = []
        for estrategia in self._estrategias:
            salida = estrategia.ajustar(datos).transformar(datos)
            resultados[estrategia.nombre] = salida
            filas.append({
                "metodo": estrategia.nombre,
                "n_validos": int(salida.count()),
                "n_imputados": int((observada.isna() & salida.notna()).sum()),
                "media_cm": float(salida.mean()),
                "mediana_cm": float(salida.median()),
                "desv_cm": float(salida.std(ddof=1)),
            })
        return resultados, pd.DataFrame(filas)
