# Nacimientos en Chile entre 2020 y 2023

Proyecto del Grupo 2 para MCDI500, Programación para la Ciencia de Datos, Universidad Andrés Bello.

Analizamos descriptivamente los nacidos vivos registrados en Chile durante el período **acumulado 2020–2023**. El proyecto permite practicar la organización de datos, programación en Python, documentación y colaboración mediante Git y GitHub. No incluye predicción ni explicación causal.

Repositorio: [jorgealtamiranonavarrete-art/proyecto-grupo2](https://github.com/jorgealtamiranonavarrete-art/proyecto-grupo2).

## Preguntas del proyecto

1. ¿Qué regiones de residencia materna presentan mayor y menor porcentaje de nacidos vivos de madres menores de 20 años?
2. ¿Qué meses del calendario presentan mayor y menor promedio diario de nacimientos, considerando todas las edades maternas?
3. ¿Qué regiones de residencia materna presentan mayor y menor talla promedio de los recién nacidos, considerando todas las edades maternas?

Las tres preguntas consideran los cuatro años en conjunto, sin rankings separados por año.

## Definición de los indicadores

| Indicador | Cálculo previsto |
|---|---|
| Porcentaje regional de maternidad adolescente | 100 × nacidos vivos de madres menores de 15 y de 15–19 años / total de nacidos vivos de la misma región y período. |
| Promedio diario mensual | Nacimientos de cada mes calendario acumulados en los cuatro años / días de ese mes acumulados en los cuatro años. Febrero tiene 113 días, los meses de 30 días tienen 120 y los de 31 días tienen 124. |
| Talla promedio regional | Media de las tallas válidas en centímetros por región de residencia materna. En F2 se comparará el escenario sin imputación con la mediana general y la mediana por región para tratar los faltantes. |

Una fila representa un nacido vivo inscrito, no una madre distinta ni necesariamente un parto único. Los porcentajes no representan la proporción de adolescentes que se embarazan.

## Datos y procedencia

- **Fuente:** Departamento de Estadísticas e Información de Salud, Ministerio de Salud de Chile ([DEIS](https://deis.minsal.cl/#datosabiertos)).
- **Archivo:** `Serie_Nacimientos_2020_2023.csv`.
- **Formato:** CSV con separador `;` y codificación UTF-8.
- **Dimensiones de referencia:** 735.611 filas y 25 columnas.
- **Documentación complementaria:** `Fichas DA Nacimientos.xlsx`, con ficha y diccionario. No constituye un segundo dataset.
- **Variables principales:** `ANO_NAC`, `MES_NAC`, `GRUPO_ETARIO_MADRE`, `REGION_RESIDENCIA`, `GLOSA_REGION_RESIDENCIA` y `TALLA`.

La revisión inicial encontró 597 nulos en `TALLA`, aproximadamente el 0,081 %. Su tratamiento se justificará en F2. Los faltantes de talla no excluirán nacimientos de los otros indicadores.

Colocar el CSV original, sin modificar, en:

```text
data/raw/Serie_Nacimientos_2020_2023.csv
```

Si no está disponible en el repositorio, obtener la serie 2020–2023 desde la fuente DEIS y conservar el archivo original. F1 calcula su huella SHA-256 para identificar la copia utilizada. **Por completar:** fecha de descarga, enlace directo o versión publicada y condiciones específicas de reutilización. El acceso público no equivale a una licencia abierta confirmada; la redistribución del CSV queda pendiente de revisar.

## Organización del proyecto

Estructura acordada; algunos archivos se generarán al ejecutar F1 y otros se incorporarán en las fases siguientes:

```text
proyecto-grupo2/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/                         # Datos originales
│   └── processed/                   # Salidas de F2
├── F1/
│   └── notebooks/
│       └── F1_Definicion.ipynb      # Notebook propio del grupo
├── F2/                             # Notebook propio por desarrollar
├── src/
│   └── f1_utilidades.py             # Se genera al ejecutar F1
├── docs/
│   └── f1/                         # Ficha, diccionario y comprobaciones de F1
└── outputs/                        # Resultados e informes
```

Los archivos `S1_F1_Definicion.ipynb` y `S1_F2_Preprocesamiento.ipynb` son ejemplos del profesor. Se distinguen del notebook propio `F1_Definicion.ipynb` y no constituyen la entrega adaptada.

## Preparación del entorno en Windows y VS Code

Se propone **Python 3.13**. Instalar las extensiones **Python** y **Jupyter** de Microsoft en VS Code. Abrir la carpeta raíz `proyecto-grupo2` y una terminal PowerShell dentro de ella.

Con Python 3.13 y el lanzador `py` instalados, crear el entorno:

```powershell
py -3.13 -m venv .venv
```

**Estado actual:** el `requirements.txt` revisado todavía no declara todas las dependencias del análisis. Mientras el equipo prepara una versión probada, esta instalación inicial permite trabajar con F1:

```powershell
.\.venv\Scripts\python.exe -m pip install pandas numpy matplotlib ipykernel
```

Este comando instala versiones disponibles al ejecutarlo; todavía no garantiza versiones idénticas entre integrantes. F1 registra las versiones observadas en `docs/f1/dependencias_observadas.txt`. Después de probar el entorno, el equipo debe incorporar las versiones acordadas a `requirements.txt`.

Cuando ese archivo esté actualizado y validado, los demás integrantes instalarán las dependencias con:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Los comandos usan directamente el Python del entorno y no requieren activar un script de PowerShell. Véase la [documentación de entornos virtuales de Python](https://docs.python.org/es/3.13/library/venv.html).

## Ejecución de F1

1. Incorporar el notebook adaptado en `F1/notebooks/F1_Definicion.ipynb` y el CSV en la ruta indicada.
2. Abrir el notebook en VS Code.
3. En **Select Kernel / Seleccionar kernel**, elegir el Python de `.venv` ([guía de VS Code](https://code.visualstudio.com/docs/datascience/jupyter-kernel-management)).
4. Reiniciar el kernel y ejecutar todas las celdas en orden.
5. Revisar las salidas y los mensajes **por completar**.

F1 define el proyecto, comprueba el entorno y reconoce el archivo sin limpiar ni imputar observaciones. Si falta el CSV, informa el pendiente y continúa con la definición y documentación; esa ejecución no equivale a tener toda la fase completada.

F1 genera `src/f1_utilidades.py` y documentos en `docs/f1/`. No sobrescribe el README principal, `.gitignore` ni `requirements.txt`. Si ya existe una versión diferente del módulo, detiene esa operación para que el equipo revise las diferencias. Al repetir F1, regenera sus documentos de `docs/f1/`; los cambios manuales en esas salidas deben incorporarse también al código que las genera.

**F2 está pendiente de adaptación y ejecución.** Allí se realizará el diagnóstico detallado, la preparación y la comparación de alternativas para los faltantes. Los indicadores finales se calcularán y comunicarán en las fases posteriores.

## Equipo y colaboración

| Integrante | Responsabilidades |
|---|---|
| Cristian Hurtado (`churtado82`) | Planteamiento, mapa conceptual, propuesta inicial de F1 para revisión de Jorge, F2 e informe. |
| Jorge Altamirano (`jorgealtamiranonavarrete-art`) | Revisión y desarrollo de F1, repositorio, integración e informe. |
| Renzo Vilchez (usuario por completar) | Colaboración en F2 y revisión del trabajo. |

Cada integrante obtiene los cambios del equipo antes de empezar, trabaja en una rama y registra sus propias modificaciones mediante commits. Después sube su rama y abre un pull request. Otro integrante revisa el código y los resultados antes de integrar los cambios en `main`.

Para evitar conflictos, coordinar quién edita cada notebook. Registrar las tareas y responsables mediante issues. Ejemplos de mensajes de commit:

```text
docs: define preguntas y alcance del proyecto
chore: configura entorno de trabajo
feat: agrega verificacion de columnas
fix: corrige ruta del archivo de nacimientos
```

Excluir mediante `.gitignore` el entorno `.venv/`, las cachés y las credenciales. No subir archivos personales ni copias temporales del proyecto.

## Estado y pendientes

- F1 adaptado preparado; falta integrarlo y registrar su ejecución y revisión en el entorno del equipo.
- CSV pendiente de colocar en `data/raw/` en la copia del repositorio revisada.
- Dependencias exactas e instrucciones de reproducción pendientes de validación conjunta.
- Fecha de descarga, versión de la fuente y condiciones de reutilización por completar.
- Confirmar con el profesor cómo aplicar los criterios del ejemplo sobre dos variables continuas, fecha y texto o alta cardinalidad al análisis descriptivo elegido.
- Usuario de Renzo, accesos, evidencia de commits y revisión cruzada por completar.
- F2, resultados finales y conclusiones del grupo pendientes de desarrollo.

## Referencias

- DEIS/MINSAL. (s. f.). *Serie de nacimientos 2020–2023 y Fichas DA Nacimientos*. https://deis.minsal.cl/#datosabiertos
- Universidad Andrés Bello. (s. f.). *S1_F1_Definicion.ipynb* y *S1_F2_Preprocesamiento.ipynb* [Notebooks docentes de MCDI500].
- Universidad Andrés Bello. (s. f.). *Guía de desarrollo de la Evaluación Sumativa 1 Fases 1 y 2* [Material docente].
