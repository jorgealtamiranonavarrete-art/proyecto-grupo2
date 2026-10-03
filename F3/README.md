# Avance Fase 3 – Semana 2

Este directorio contiene el avance formativo y la Sumativa 2 del Grupo 2 para MCDI500. El cuaderno [`F3_Avance_Semana2.ipynb`](F3_Avance_Semana2.ipynb) compara dos implementaciones del indicador regional y dos formas de leer el CSV original, y muestra una codificación one-hot aprendida solo con entrenamiento. [`F3_Nucleo_Algoritmico.ipynb`](F3_Nucleo_Algoritmico.ipynb) amplía ese avance con clases, pruebas y mediciones en varios tamaños.

**Qué archivo corresponde a cada entrega.** La **Formativa 3** utiliza `F3_Avance_Semana2.ipynb`; su informe editable es `f3_s02_grupo2.docx` y el archivo para Canvas es `f3_s02_grupo2.pdf`. La **Sumativa 2** utiliza `F3_Nucleo_Algoritmico.ipynb`; su informe editable es `f3_s02_grupo2_sum.docx` y el archivo para Canvas es `f3_s02_grupo2_sum.pdf`. Los notebooks y sus módulos permanecen en el repositorio como evidencia ejecutable; los PDF corresponden a las entregas escritas.

## Archivos y responsabilidades

| Archivo | Función |
| --- | --- |
| `F3_Avance_Semana2.ipynb` | Coordina la ejecución, verifica resultados, presenta mediciones y explica decisiones. |
| `F3_Nucleo_Algoritmico.ipynb` | Sumativa 2: muestra validaciones de F2 y una matriz one-hot, coordina clases, verifica casos límite y mide tiempo y memoria en tres tamaños. |
| `src/f3_algoritmos.py` | Contiene funciones independientes de lectura, cálculo y medición de tiempo y memoria, además de `AnalizadorNacimientos`, la clase de análisis regional propuesta por Jorge Altamirano. |
| `src/f3_estrategias_talla.py` | Contiene cuatro clases de tratamiento de talla y un comparador que utiliza la misma interfaz. |
| `resultados/mediciones.json` | Registra los resultados de una ejecución completa y las versiones del entorno. |
| `resultados/sumativa2_verificacion.json` | Registra parámetros aprendidos, controles de F2, vocabulario one-hot, ocho comprobaciones y mediciones de Sumativa 2. |
| `resultados/parametros_codificacion.json` | Registra el vocabulario aprendido de entrenamiento y las columnas indicadoras. |
| `../src/f2_utilidades.py` | Aporta la función recursiva `aplanar` creada en F2. |

F3 no modifica los CSV ni repite la preparación de F2. La versión legible para tablas y figuras sigue siendo `../data/processed/nacimientos_preparados_propuesta.csv`. La matriz one-hot se construye separadamente en el notebook, con índices que corresponden a las filas del CSV preparado. Una categoría nueva en prueba conserva el mismo esquema de columnas y se representa con una fila de ceros; para interpretarla se conserva la categoría original.

## Cómo ejecutarlo

1. Abra la **raíz del repositorio** en VS Code. El CSV original se encuentra en `data/raw/Serie_Nacimientos_2020_2023.csv` y ejecute F2 para generar `data/processed/nacimientos_preparados_propuesta.csv`. Si ya tiene ambos archivos en este computador, reutilícelos; no hace falta descargarlos ni ejecutar F2 cada vez.
2. Si ya existe `.venv`, reutilícelo; no necesita crearlo en cada ejecución. Solo en una instalación nueva, desde la raíz, cree un entorno virtual con Python 3.13 e instale el [`requirements.txt`](../requirements.txt) principal: `python -m venv .venv` y `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`. En VS Code, use el selector de kernel arriba a la derecha y elija **Jupyter Kernels → Grupo 2 requirements (Python 3.13.5)**. También sirve el intérprete cuya ruta termina en `.venv\Scripts\python.exe`; compruebe la primera celda antes de ejecutar todo. La primera celda verifica las versiones fijadas en `requirements.txt` y detiene la ejecución antes de escribir archivos si VS Code conserva otro kernel.
3. Abra `F3_Avance_Semana2.ipynb` o `F3_Nucleo_Algoritmico.ipynb`, reinicie el kernel y ejecute todas las celdas en orden. Ambos notebooks localizan la raíz del proyecto y escriben únicamente JSON pequeños de `resultados/`.
4. Compruebe las afirmaciones de equivalencia y la tabla de tiempos. Los tiempos cambiarán según el equipo y se registrarán nuevamente al ejecutar el cuaderno.

La ejecución verificada del 29 de septiembre de 2026 utilizó Python 3.13.5, pandas 3.0.5, NumPy 2.5.2, scikit-learn 1.9.0 y matplotlib 3.11.1: las versiones fijadas en el archivo principal. F1, F2 y F3 se ejecutaron completos en ese mismo entorno. Las versiones efectivas de F3 se imprimen al inicio y quedan en `mediciones.json`.

## Resultados de referencia de esta ejecución

Ambas implementaciones producen exactamente los mismos conteos regionales. Los tiempos y la memoria de la ejecución guardada se encuentran en `resultados/mediciones.json`, que se actualiza al ejecutar el notebook. La medida de memoria describe los objetos DataFrame, no el pico total del proceso. La codificación aprendió 16 categorías regionales solo en entrenamiento y conservó el mismo número de columnas en prueba.

## Diseño y evolución

La separación entre módulo y notebook evita duplicar lógica al continuar el proyecto. La recursión se aplica a los metadatos reales de la medición, anidados a profundidad variable, no a las filas. En una fase posterior, el codificador puede encapsularse como un componente con estado que exponga `fit` y `transform`, mientras lectura, cálculo, validación y visualización permanecen separados. La clase regional agrupa la carga y los dos cálculos sin duplicar sus algoritmos; las funciones independientes siguen disponibles para medir muestras de distintos tamaños.

En su intervención inicial en la Formativa 2 (29 de septiembre de 2026), Cristian Hurtado Cabezas justificó la agrupación o iteración para los 735.611 registros y la recursividad para aplanar metadatos anidados. También propuso comparar alternativas solo después de verificar resultados equivalentes y medir tiempo y memoria. El notebook aplica esos criterios; sus cifras corresponden a la ejecución registrada en `resultados/mediciones.json` y pueden diferir de las publicadas en el foro.

## Sumativa 2: núcleo orientado a objetos

La Sumativa 2 comprueba además que la clase regional y las funciones independientes producen los mismos indicadores. El notebook también confirma el número de filas, años, meses, tallas observadas e imputadas y la huella SHA-256 del archivo original frente a los metadatos de F2. Los metadatos de F2 registran la mediana regional como tratamiento aprobado por el grupo. Una tabla pequeña muestra los 16 indicadores one-hot aprendidos solo con entrenamiento.

La clase abstracta `EstrategiaTalla` define los métodos `ajustar` y `transformar`. `SinImputar`, `MediaGeneral`, `MedianaGeneral` y `MedianaRegional` comparten esa interfaz y conservan sus parámetros aprendidos dentro de cada objeto. `ComparadorImputacion` recibe las cuatro estrategias y las aplica sin depender de una clase concreta. Este uso del patrón *Strategy* permite cambiar un tratamiento sin modificar el comparador. El notebook verifica igualdad fila por fila con la función original de F2 y prueba ocho casos normales, límite y de error, incluido que modificar una copia de parámetros no altera la clase. No se modifica la selección metodológica documentada en F2.

El benchmark compara `proporcion_bucle` y `proporcion_groupby` en 10.000, 100.000 y 735.611 filas con tres repeticiones por combinación. Primero comprueba resultados iguales y después mide. Los tiempos varían entre equipos; `resultados/sumativa2_verificacion.json` guarda cada repetición, versiones y parámetros. El cuaderno mide por separado el tamaño de entrada y salida y el pico de asignaciones rastreadas por `tracemalloc`. Este último no incluye toda la memoria nativa de pandas ni equivale al máximo del proceso. La función recursiva `aplanar` de F2 registra estos metadatos sin aplicar recursión a las filas.

El historial de Git incluye el merge `2f8f42d` del 18 de septiembre, registrado con la identidad «HR Informática» (cuenta HardyRojas). Esa identidad no corresponde a un integrante del Grupo 2 y el equipo no le atribuye los análisis del proyecto. Se conserva la atribución histórica del merge; `.mailmap` normaliza únicamente los nombres de los cuatro integrantes.

## Fuentes

Las referencias APA y sus citas en contexto están en los notebooks y en los informes editables. La Sumativa 2 incorpora documentación oficial de Python y pandas y el artículo reciente de Thimbleby (2024) sobre verificación de código científico, además del material del curso. Los PDF versionados corresponden a las copias de entrega de cada informe.
