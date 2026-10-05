# Registro de mejoras del proyecto

Este registro vincula decisiones técnicas con cambios verificables del repositorio. La Fase 4 se integró en `main` mediante el PR #9; las revisiones posteriores y la ejecución cruzada confirmada por Renzo forman parte del cierre del equipo. La entrega en Canvas es un paso independiente.

| Fecha | Cambio | Commit | Justificación y efecto |
| --- | --- | --- | --- |
| 2026-09-29 | Alinear notebooks e informe con las versiones de `requirements.txt` | [`8ec15aa`](https://github.com/jorgealtamiranonavarrete-art/proyecto-grupo2/commit/8ec15aa) | Evita comparar resultados obtenidos con entornos diferentes y facilita la ejecución reproducible. |
| 2026-09-30 | Incorporar el núcleo de la Sumativa 2 | [`6c661d9`](https://github.com/jorgealtamiranonavarrete-art/proyecto-grupo2/commit/6c661d9) | Reúne estrategias de talla, verificaciones y mediciones de tiempo y memoria; permite elegir `groupby` con evidencia. |
| 2026-10-01 | Retirar archivos residuales y aclarar entregables F3 | [`00a0339`](https://github.com/jorgealtamiranonavarrete-art/proyecto-grupo2/commit/00a0339) | Reduce confusiones sobre qué notebook e informe corresponden a cada actividad. |
| 2026-10-01 | Sincronizar PDF con informes editables F3 | [`e7103c5`](https://github.com/jorgealtamiranonavarrete-art/proyecto-grupo2/commit/e7103c5) | Mantiene concordancia entre los formatos del mismo entregable. |
| 2026-10-02 | Compartir F4 para revisión del equipo: notebook, informe, presentación, figuras y mapas | [`d8b1b7e`](https://github.com/jorgealtamiranonavarrete-art/proyecto-grupo2/commit/d8b1b7e) | Reutilizó la salida de F2 y el núcleo de F3 para producir conclusiones rastreables y solicitar la revisión del equipo. |
| 2026-10-02 | Integrar F4 en `main` | [`8d63714`](https://github.com/jorgealtamiranonavarrete-art/proyecto-grupo2/commit/8d63714) | El PR #9 incorporó el notebook, el informe y la presentación para el cierre conjunto. |
| 2026-10-04 | Corregir avisos de notebooks y revisar documentos F4 | [`b9104ef`](https://github.com/jorgealtamiranonavarrete-art/proyecto-grupo2/commit/b9104ef), [`bf7e46e`](https://github.com/jorgealtamiranonavarrete-art/proyecto-grupo2/commit/bf7e46e) | Renzo corrigió avisos de F1–F3 y Luis subió nuevas versiones del Word y la presentación; Renzo confirmó la ejecución cruzada. |
| 2026-10-04 | Versionar el CSV original y cerrar la documentación de F1–F4 | [`09aec8b`](https://github.com/jorgealtamiranonavarrete-art/proyecto-grupo2/commit/09aec8b) | La fuente original queda disponible al clonar el proyecto; F1 y F2 registran las decisiones reales del equipo y el informe y la presentación de F4 reflejan el estado de la revisión. |

**Impacto conjunto.** F2 dejó la fuente y las imputaciones trazables. F3 separó responsabilidades en módulos y mostró que `groupby` tardó 0,0090 s frente a 0,1423 s del bucle en la medición registrada, aunque la memoria rastreada requiere interpretación aparte. F4 conecta esas decisiones con tablas y figuras que responden las preguntas originales. Las cifras de rendimiento dependen del equipo y del entorno de la prueba.
