# Guion final — vídeo de cinco minutos

**Comprobación previa:** las métricas citadas corresponden a `results/final/evaluation.json`. Confirmar con el docente la composición del grupo: el enunciado indica cinco integrantes y la propuesta nombra seis. Repartir los bloques entre quienes efectivamente presenten. El vídeo dura aproximadamente cinco minutos; la demo en vivo va después.

## Diapositiva 1 — 0:00 a 0:20 — Portada

«Somos el equipo de *El precio de la inteligencia*. Estudiamos cómo evolucionan los precios de lista de modelos de IA y construimos una herramienta para encontrar opciones que cumplan requisitos al menor coste. En la entrega final ampliamos el avance con evaluación fuera de tiempo y una demo en vivo.»

## Diapositiva 2 — 0:20 a 1:00 — Datos y pregunta

«Usamos el catálogo de 4.403 listados y 167.787 registros históricos de LiteLLM. Para comparar tarifas por tokens seleccionamos modelos chat con precios positivos de entrada y salida: 3.082 listados actuales y 139.874 observaciones históricas. Definimos un trabajo de ejemplo de un millón de tokens de entrada y 250.000 de salida. Los datos son precios publicados, no pagos reales. El país disponible es el del desarrollador, no el del proveedor.»

## Diapositiva 3 — 1:00 a 1:55 — La novedad: dinámica del catálogo

«La mediana del coste del trabajo de ejemplo pasa de 3,0075 a 1,10 dólares entre la primera y la última semana. Ese cambio mezcla listados distintos. Para entenderlo mejor, seguimos cada identificador de modelo de una semana observada a la siguiente. Entre 135.928 comparaciones de listados continuadores encontramos 519 cambios de tarifa de entrada, apenas un 0,382 por ciento. A la vez hay 3.905 eventos de entrada a la cohorte elegible. La composición cambia mucho, pero no asignamos a cada mecanismo un porcentaje causal de la caída.»

## Diapositiva 4 — 1:55 a 2:50 — Predicción temporal evaluada

«Para predecir la mediana semanal del coste, reservamos las últimas 26 semanas, de abril a septiembre de 2026. En cada semana entrenamos la regresión solo con el pasado y la comparamos con una regla simple: repetir el último precio observado. Medimos el error absoluto medio, donde menos es mejor. La regresión obtiene 0,0381 dólares y la persistencia 0,0145. El baseline gana. La serie cambia poco de una semana a otra, así que esta es una advertencia útil: un modelo más complejo no aporta valor automáticamente.»

## Diapositiva 5 — 2:50 a 3:50 — Clasificación y perfiles

«También clasificamos listados en tres rangos de coste usando contexto y capacidades, sin incluir el precio como predictor. Repetimos cinco separaciones por nombre de modelo para no compartir nombres entre entrenamiento y prueba. El bosque aleatorio alcanza macro-F1 medio de 0,594, frente a 0,158 de predecir siempre la clase mayoritaria. Este resultado es más sólido que el de una sola partición del avance. En paralelo, el clustering distingue tres perfiles de coste, contexto y capacidades, con silhouette 0,266; es una descripción exploratoria, no una puntuación de calidad.»

## Diapositiva 6 — 3:50 a 4:35 — Recomendador y demo

«El recomendador toma el volumen de tokens, el contexto mínimo y capacidades como visión. Filtra los listados compatibles y los ordena por su coste de lista calculado. En la demo cambiaremos el contexto para mostrar cómo se reduce el conjunto de opciones, y enseñaremos también las curvas y métricas usadas en el vídeo. Así el resultado es utilizable y auditable a partir de los CSV originales.»

## Diapositiva 7 — 4:35 a 5:00 — Conclusiones

«Concluimos que la caída de la mediana del catálogo no equivale a una rebaja general de cada modelo. La clasificación supera claramente su baseline, mientras que en predicción semanal la persistencia es mejor que la regresión. Nuestra recomendación minimiza coste bajo requisitos, pero la fuente no mide calidad ni identifica IA de frontera. Por eso no damos una fecha para el umbral de diez centavos ni afirmamos diferencias causales entre países. Muchas gracias.»
