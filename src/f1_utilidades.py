"""Verificaciones compartidas del proyecto de nacimientos, Grupo 2."""
import hashlib
from pathlib import Path

class ProyectoError(ValueError):
    """Entrada incompatible con las verificaciones del proyecto."""

def verificar_columnas(disponibles, requeridas):
    """Devuelve True si están las columnas requeridas; no modifica la entrada."""
    if not isinstance(disponibles, (list, tuple)) or not isinstance(requeridas, (list, tuple)):
        raise ProyectoError("Las columnas deben proporcionarse como listas o tuplas.")
    if not all(isinstance(c, str) for c in [*disponibles, *requeridas]):
        raise ProyectoError("Cada nombre de columna debe ser texto.")
    faltantes = sorted(set(requeridas) - set(disponibles))
    if faltantes:
        raise ProyectoError(f"Columnas ausentes: {faltantes}")
    return True

def huella_sha256(ruta):
    """Calcula SHA-256 por bloques sin alterar el archivo."""
    digest = hashlib.sha256()
    with Path(ruta).open("rb") as archivo:
        for bloque in iter(lambda: archivo.read(1024 * 1024), b""):
            digest.update(bloque)
    return digest.hexdigest()
