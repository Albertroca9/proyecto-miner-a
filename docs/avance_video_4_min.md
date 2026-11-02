# Avance de proyecto — vídeo de 4 minutos

Las cifras proceden de `results/summary.json` y `results/metrics.json`. Regenerar los resultados antes de grabar si cambian los CSV o el código. Cinco diapositivas, aproximadamente cuatro minutos.

Antes de grabar, confirmar con el docente la composición del grupo: el enunciado indica cinco integrantes y el guion inicial nombra seis.

## 1. Pregunta y compromiso inicial — 0:00–0:35

**En pantalla:** título, equipo y flujo `LiteLLM → datos preparados → análisis/modelos → recomendador y predicción`.

**Guion:** «Seguimos con *El precio de la inteligencia*. En la propuesta prometimos preparar los datos, montar el entorno experimental y comenzar con modelos exploratorios. Hoy mostramos ese avance y qué falta para poder recomendar tarifas y estudiar su evolución con rigor».

## 2. Base preparada y límites — 0:35–1:20

**En pantalla:** 4.403 listados actuales, 167.787 filas históricas, 157 semanas; flecha de filtrado a 3.082 listados chat comparables.

**Guion:** «Partimos de dos CSV de precios de lista. Para comparar tarifas por tokens seleccionamos modelos de chat con precios positivos de entrada y salida; resultan 3.082 listados actuales y 139.874 observaciones históricas. Dejamos los originales intactos y automatizamos el procesamiento. El archivo indica el país del desarrollador, no del proveedor. Tampoco incluye una puntuación de calidad, por lo que nuestra recomendación inicial se basa en requisitos y coste».

## 3. Primer hallazgo temporal — 1:20–2:15

**En pantalla:** `results/evolucion_semanal.png`.

**Guion:** «La mediana del precio de entrada de los listados comparables baja de 1,875 a 0,60 dólares por millón de tokens entre la primera y la última semana. Al mismo tiempo, la oferta observada crece de 41 a 3.082 listados. Por eso no atribuimos toda la caída a rebajas: entre 136.118 comparaciones sucesivas de precio de entrada del mismo listado detectamos 573 cambios. La entrada de nuevos modelos podría explicar parte de la diferencia; lo estudiaremos en la entrega final».

**Precisión para preguntas:** 573/136.118 = 0,42 %. Son observaciones sucesivas disponibles de cada `model_id`, no necesariamente semanas de calendario adyacentes.

## 4. Primeros modelos y baseline — 2:15–3:20

**En pantalla:** tabla breve con tres perfiles de `cluster_profiles.csv`; macro-F1 del clasificador 0,606 y baseline 0,178.

**Guion:** «Probamos clustering con precios, contexto y capacidades; tres grupos dan la mayor silhouette entre dos y seis grupos, 0,266. Encontramos un grupo numeroso de menor coste y contexto mediano de 128.000 tokens, y otros con mayor contexto y más capacidades. También entrenamos una clasificación exploratoria de tres rangos de coste usando solo especificaciones, nunca el precio que queremos predecir. Separando por nombre de modelo, el macro-F1 es 0,606 frente a 0,178 del baseline que elige la clase mayoritaria. Es un resultado inicial de una partición, que ampliaremos para el final».

## 5. Recomendador y próximo paso — 3:20–4:00

**En pantalla:** demo de `streamlit_app.py` o captura de sus filtros y primera tabla.

**Guion:** «El prototipo permite indicar volumen de entrada y salida, contexto mínimo y capacidades como visión. Filtra los modelos que cumplen los requisitos y los ordena por coste estimado. En la entrega final conectaremos esta herramienta con una evaluación temporal frente a un baseline, estudiaremos cuánto del cambio de precios proviene de rebajas y cuánto de nuevos modelos, y haremos una demo en vivo. Para hablar de calidad-precio o de IA de frontera necesitamos primero una medida externa de calidad. Gracias».

## Preguntas previsibles

- **¿Por qué no predecir ya cuándo la frontera llegará a 0,10 USD?** Hay listados por debajo de ese umbral, pero los datos no identifican cuáles son de frontera. Definiremos una cohorte medible antes de extrapolar.
- **¿EE. UU. es más caro que China?** En esta muestra, las medianas son distintas, pero las gamas y capacidades también pueden serlo. La variable disponible es país del desarrollador y la comparación aún no controla esas diferencias.
- **¿Qué significa “mejor valor”?** El menor coste de lista que satisface los requisitos indicados. No mide calidad, latencia ni disponibilidad.
- **¿Cuál es el baseline?** En clasificación, la clase mayoritaria. Para el análisis temporal final, el último precio observado.
