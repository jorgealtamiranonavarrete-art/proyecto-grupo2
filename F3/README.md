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
2. En este computador, seleccione el kernel **`base (Python 3.13.5)`** de Anaconda: fue el utilizado para verificar el cuaderno y ya contiene `pandas`, `numpy`, `scikit-learn` e `ipykernel`. No cree otro entorno para esta revisión. En otro computador, utilice un kernel que contenga las dependencias del [`requirements.txt`](../requirements.txt) principal.
3. Abra el notebook, reinicie el kernel y ejecute todas las celdas en orden. El notebook localiza la raíz del proyecto y escribe únicamente los dos JSON pequeños de `resultados/`.
4. Compruebe las afirmaciones de equivalencia y la tabla de tiempos. Los tiempos cambiarán según el equipo y se registrarán nuevamente al ejecutar el cuaderno.

La ejecución documentada del 28 de septiembre de 2026 utilizó Python 3.13.5, pandas 2.2.3, NumPy 2.1.3 y scikit-learn 1.6.1. Las versiones efectivas se imprimen al inicio y quedan en `mediciones.json`. El archivo `requirements.txt` declara las versiones propuestas para instalar el proyecto; este cuaderno fue verificado con las versiones recién indicadas. Se debe contrastar la instalación del equipo antes de entregar.

## Resultados de referencia de esta ejecución

Ambas implementaciones producen exactamente los mismos conteos regionales. Los tiempos y la memoria de la ejecución guardada se encuentran en `resultados/mediciones.json`, que se actualiza al ejecutar el notebook. La medida de memoria describe los objetos DataFrame, no el pico total del proceso. La codificación aprendió 16 categorías regionales solo en entrenamiento y conservó el mismo número de columnas en prueba.

## Diseño y evolución

La separación entre módulo y notebook evita duplicar lógica al continuar el proyecto. La recursión se reutiliza para metadatos anidados de profundidad variable, no para filas. En una fase posterior, el codificador puede encapsularse como un componente con estado que exponga `fit` y `transform`, mientras lectura, cálculo, validación y visualización permanecen separados. Este avance no introduce una clase por obligación: las operaciones de cálculo y medición son funciones independientes.

La comparación de alternativas responde al tema del foro técnico de la Semana 1. La intervención concreta del grupo se añadirá una vez que esté disponible, sin atribuir argumentos no documentados.

## Fuentes

Las referencias APA y sus citas en contexto están en el notebook y en el informe `f3_s02_grupo2.pdf`. Incluyen dos materiales docentes, documentación oficial de Python, pandas y scikit-learn, y el artículo de Pedregosa et al. (2011).
