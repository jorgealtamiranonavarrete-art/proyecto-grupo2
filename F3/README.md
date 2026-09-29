# Avance Fase 3 – Semana 2

Este directorio contiene el avance formativo del Grupo 2 para MCDI500. El cuaderno [`F3_Avance_Semana2.ipynb`](F3_Avance_Semana2.ipynb) trabaja con la salida preparada en F2, compara dos implementaciones del indicador regional y dos formas de leer el CSV original, y muestra una codificación one-hot de la región aprendida solo con entrenamiento.

## Archivos y responsabilidades

| Archivo | Función |
| --- | --- |
| `F3_Avance_Semana2.ipynb` | Coordina la ejecución, verifica resultados, presenta mediciones y explica decisiones. |
| `src/f3_algoritmos.py` | Contiene funciones independientes de lectura, cálculo y cronometraje. |
| `resultados/mediciones.json` | Registra los resultados de una ejecución completa y las versiones del entorno. |
| `resultados/parametros_codificacion.json` | Registra el vocabulario aprendido de entrenamiento y las columnas indicadoras. |
| `../src/f2_utilidades.py` | Aporta la función recursiva `aplanar` creada en F2. |

F3 no modifica los CSV ni repite la preparación de F2. La versión legible para tablas y figuras sigue siendo `../data/processed/nacimientos_preparados_propuesta.csv`. La matriz one-hot se construye separadamente en el notebook, con índices que corresponden a las filas del CSV preparado. Una categoría nueva en prueba conserva el mismo esquema de columnas y se representa con una fila de ceros; para interpretarla se conserva la categoría original.

## Cómo ejecutarlo

1. Abra la **raíz del repositorio** en VS Code. Compruebe que existen `data/processed/nacimientos_preparados_propuesta.csv` y `data/raw/Serie_Nacimientos_2020_2023.csv`.
2. Si ya existe `.venv`, reutilícelo; no necesita crearlo en cada ejecución. Solo en una instalación nueva, desde la raíz, cree un entorno virtual con Python 3.13 e instale el [`requirements.txt`](../requirements.txt) principal: `python -m venv .venv` y `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`. En VS Code, use el selector de kernel arriba a la derecha y elija **Jupyter Kernels → Grupo 2 requirements (Python 3.13.5)**. También sirve el intérprete cuya ruta termina en `.venv\Scripts\python.exe`; compruebe la primera celda antes de ejecutar todo. La primera celda verifica las versiones fijadas en `requirements.txt` y detiene la ejecución antes de escribir archivos si VS Code conserva otro kernel.
3. Abra el notebook, reinicie el kernel y ejecute todas las celdas en orden. El notebook localiza la raíz del proyecto y escribe únicamente los dos JSON pequeños de `resultados/`.
4. Compruebe las afirmaciones de equivalencia y la tabla de tiempos. Los tiempos cambiarán según el equipo y se registrarán nuevamente al ejecutar el cuaderno.

La ejecución verificada del 29 de septiembre de 2026 utilizó Python 3.13.5, pandas 3.0.5, NumPy 2.5.2, scikit-learn 1.9.0 y matplotlib 3.11.1: las versiones fijadas en el archivo principal. F1, F2 y F3 se ejecutaron completos en ese mismo entorno. Las versiones efectivas de F3 se imprimen al inicio y quedan en `mediciones.json`.

## Resultados de referencia de esta ejecución

Ambas implementaciones producen exactamente los mismos conteos regionales. Los tiempos y la memoria de la ejecución guardada se encuentran en `resultados/mediciones.json`, que se actualiza al ejecutar el notebook. La medida de memoria describe los objetos DataFrame, no el pico total del proceso. La codificación aprendió 16 categorías regionales solo en entrenamiento y conservó el mismo número de columnas en prueba.

## Diseño y evolución

La separación entre módulo y notebook evita duplicar lógica al continuar el proyecto. La recursión se aplica a los metadatos reales de la medición, anidados a profundidad variable, no a las filas. En una fase posterior, el codificador puede encapsularse como un componente con estado que exponga `fit` y `transform`, mientras lectura, cálculo, validación y visualización permanecen separados. Este avance no introduce una clase por obligación: las operaciones de cálculo y medición son funciones independientes.

Las mediciones y la aplicación de recursividad proporcionan ejemplos para responder la Formativa 2 sobre diseño algorítmico. A la fecha de esta revisión el grupo todavía no había publicado allí una intervención; el notebook no atribuye argumentos de foro que no se hayan presentado.

## Fuentes

Las referencias APA y sus citas en contexto están en el notebook y en el informe `f3_s02_grupo2.pdf`. Incluyen dos materiales docentes, documentación oficial de Python, pandas y scikit-learn, y el artículo de Pedregosa et al. (2011).
