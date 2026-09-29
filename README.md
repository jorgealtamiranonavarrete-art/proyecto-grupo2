# Nacimientos en Chile entre 2020 y 2023

Proyecto del Grupo 2 para MCDI500, Programación para la Ciencia de Datos. El repositorio documenta la definición del problema (F1), la preparación de los datos (F2) y el desarrollo progresivo del análisis algorítmico (F3).

## Preguntas del proyecto

1. ¿Qué regiones de residencia materna presentan la mayor y la menor proporción de nacidos vivos de madres menores de 20 años entre 2020 y 2023?
2. ¿Qué meses del calendario presentan el mayor y el menor promedio diario de nacimientos durante esos cuatro años?
3. ¿Qué regiones de residencia materna presentan la mayor y la menor talla media al nacer?

El análisis es descriptivo. Cada fila corresponde a un nacido vivo inscrito; no representa necesariamente una madre o un parto distinto. Las diferencias observadas no establecen causas ni permiten calcular el riesgo de embarazo adolescente.

## Fuente de datos

La fuente es la *Serie de nacimientos 2020–2023* del [Departamento de Estadísticas e Información de Salud (DEIS), Ministerio de Salud de Chile](https://deis.minsal.cl/#datosabiertos). El archivo de entrada esperado es `data/raw/Serie_Nacimientos_2020_2023.csv`, con separador `;` y codificación UTF-8. Si falta en una copia local, debe obtenerse del portal del DEIS y colocarse con ese nombre en esa ruta. La documentación de la fuente está en [`docs/f1/ficha.json`](docs/f1/ficha.json) y el reconocimiento de sus variables en [`docs/f1/diccionario_variables.csv`](docs/f1/diccionario_variables.csv).

El equipo atribuye los datos a DEIS/MINSAL. La disponibilidad pública del archivo no se interpreta aquí como una licencia específica de redistribución; sus condiciones deben verificarse en la fuente antes de volver a publicar copias o derivados.

## Organización del repositorio

| Ruta | Contenido |
| --- | --- |
| [`F1/notebooks/F1_Definicion.ipynb`](F1/notebooks/F1_Definicion.ipynb) | Problema, preguntas, indicadores y reconocimiento de la fuente. |
| [`F2/F2_Preparacion.ipynb`](F2/F2_Preparacion.ipynb) | Diagnóstico, preparación, comparación de tratamientos de talla y validaciones. |
| [`F3/F3_Avance_Semana2.ipynb`](F3/F3_Avance_Semana2.ipynb) | Avance ejecutable: indicador regional, mediciones de eficiencia y codificación nominal. |
| [`F3/README.md`](F3/README.md) | Instrucciones, arquitectura, resultados y decisiones de optimización de F3. |
| [`src/`](src/) | Funciones reutilizables de F1 y F2. |
| `data/raw/` | Ubicación del CSV original; no se modifica durante el análisis. |
| `data/processed/` | Salida preparada por F2. |
| [`docs/f1/`](docs/f1/) y [`docs/f2/`](docs/f2/) | Diccionario, metadatos, tablas y bitácoras. |
| [`outputs/f2/`](outputs/f2/) | Figuras generadas durante F2. |

La salida actual de F2 es `data/processed/nacimientos_preparados_propuesta.csv`. Conserva las variables seleccionadas y las marcas que distinguen la talla observada de la imputada. F2 compara cuatro escenarios de tratamiento y registra sus resultados en `docs/f2/`.

## Preparación y ejecución

Se propone Python 3.13. Las dependencias declaradas están en [`requirements.txt`](requirements.txt). En Windows, después de comprobar que `python --version` corresponde a Python 3.13, ejecute desde la raíz del repositorio:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

El entorno `.venv` se crea solo una vez por computador. En VS Code, abra la raíz del proyecto y seleccione `.venv\Scripts\python.exe` como kernel del notebook (arriba a la derecha). La configuración `.vscode/settings.json` sugiere ese intérprete y el kernel registrado se llama **Grupo 2 requirements (Python 3.13.5)**. En el selector del notebook aparece bajo **Jupyter Kernels**. VS Code puede recordar una selección anterior: compruebe el kernel real, no solo el nombre mostrado. La primera celda de F1, F2 y F3 compara las versiones instaladas con `requirements.txt` y se detiene antes de escribir archivos si no coinciden. Para reproducir el flujo, compruebe primero que el CSV original está en `data/raw/`; después reinicie el kernel y ejecute todas las celdas de F1 y, a continuación, de F2. Ambos notebooks buscan la raíz del repositorio para construir las rutas de entrada y salida.

## Avance de F3 — Semana 2

El notebook de F3 parte del conjunto preparado por F2 y compara un bucle de Python con `pandas.groupby` para calcular la proporción regional de nacimientos de madres menores de 20 años. También compara leer las 25 columnas originales con leer las seis usadas en F2. En ambos experimentos verifica primero que las salidas equivalentes coinciden y luego registra tres repeticiones de tiempo; para la lectura informa además la memoria de cada DataFrame. La decisión de usar `groupby` y lectura selectiva se basa en esas mediciones, documentadas en [`F3/resultados/mediciones.json`](F3/resultados/mediciones.json).

Como demostración de transformación nominal, `REGION_RESIDENCIA` se codifica con columnas one-hot. El vocabulario se aprende solo en entrenamiento y se aplica a prueba sin crear columnas nuevas; queda documentado en [`F3/resultados/parametros_codificacion.json`](F3/resultados/parametros_codificacion.json). Se conserva el conjunto preparado con categorías y centímetros para tablas y figuras. La talla no se escala en este avance porque no se usan métodos basados en distancias. La función recursiva de F2 aplana los metadatos reales de la ejecución en el notebook. Consulte [`F3/README.md`](F3/README.md) para ejecutarlo.

Los cambios de cada integrante se desarrollan en ramas y se integran tras revisión. El nombre de una carpeta local no cambia el nombre del repositorio de GitHub.
