# Registro de mejoras del proyecto

Este registro vincula decisiones técnicas con cambios que ya están en el historial. Los identificadores corresponden a commits verificables del repositorio. La Fase 4 se comparte en la rama `f4-cristian` para revisión del grupo. El informe, la presentación y el notebook requieren la revisión de sus responsables antes de integrarse a `main` y entregarse en Canvas.

| Fecha | Cambio | Commit | Justificación y efecto |
| --- | --- | --- | --- |
| 2026-09-29 | Alinear notebooks e informe con las versiones de `requirements.txt` | [`8ec15aa`](https://github.com/jorgealtamiranonavarrete-art/proyecto-grupo2/commit/8ec15aa) | Evita comparar resultados obtenidos con entornos diferentes y facilita la ejecución reproducible. |
| 2026-09-30 | Incorporar el núcleo de la Sumativa 2 | [`6c661d9`](https://github.com/jorgealtamiranonavarrete-art/proyecto-grupo2/commit/6c661d9) | Reúne estrategias de talla, verificaciones y mediciones de tiempo y memoria; permite elegir `groupby` con evidencia. |
| 2026-10-01 | Retirar archivos residuales y aclarar entregables F3 | [`00a0339`](https://github.com/jorgealtamiranonavarrete-art/proyecto-grupo2/commit/00a0339) | Reduce confusiones sobre qué notebook e informe corresponden a cada actividad. |
| 2026-10-01 | Sincronizar PDF con informes editables F3 | [`e7103c5`](https://github.com/jorgealtamiranonavarrete-art/proyecto-grupo2/commit/e7103c5) | Mantiene concordancia entre los formatos del mismo entregable. |
| 2026-10-02 | Compartir F4 para revisión del equipo: notebook, informe, presentación, figuras y mapas | Rama `f4-cristian` | Reutiliza la salida de F2 y el núcleo de F3 para producir conclusiones rastreables. Jorge revisará el informe, Luis la presentación y Renzo el notebook y la coordinación del video antes de integrar los cambios a `main`. |

**Impacto conjunto.** F2 dejó la fuente y las imputaciones trazables. F3 separó responsabilidades en módulos y mostró que `groupby` tardó 0,0090 s frente a 0,1423 s del bucle en la medición registrada, aunque la memoria rastreada requiere interpretación aparte. F4 conecta esas decisiones con tablas y figuras que responden las preguntas originales. Las cifras de rendimiento dependen del equipo y del entorno de la prueba.
