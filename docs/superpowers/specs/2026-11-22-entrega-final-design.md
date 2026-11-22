# Entrega final: El precio de la inteligencia

## Decisión de alcance

Conservar el pipeline del avance y ampliarlo para cubrir los requisitos explícitos del enunciado: evaluación contra baseline, elemento nuevo, vídeo de cinco minutos y demo en vivo. La aportación nueva será separar la evolución del catálogo de los cambios observados dentro de cada listado. No se afirmará una fecha para el umbral de 0,10 USD de «IA de frontera», porque los CSV no miden calidad ni definen la frontera.

## Datos y métodos

- Fuentes inmutables: catálogo actual y 157 semanas de precios de LiteLLM. La cohorte principal seguirá siendo `mode == chat` con tarifas positivas de entrada y salida.
- Serie temporal: objetivo = mediana semanal del coste de 1 M de tokens de entrada y 0,25 M de salida. Evaluación en las últimas 26 semanas, entrenando únicamente con semanas anteriores a cada predicción. Comparar una regresión con retardos y tendencia con la persistencia de la última mediana; informar MAE y sMAPE. No usar datos futuros para construir características.
- Dinámica del catálogo: por semana, contar listados nuevos, continuadores y salientes; medir cambios de tarifa entre semanas consecutivas de un mismo `model_id`. Mostrar por separado la mediana total y la mediana de la cohorte continuadora. Esta comparación es descriptiva, no una descomposición causal aditiva.
- Clasificación: repetir la separación por `model_name` en cinco semillas. En cada repetición se calculan los umbrales de tramos y la imputación en entrenamiento. Informar distribución de macro-F1 y accuracy frente al clasificador de clase mayoritaria.
- Clustering y recomendación: mantener los perfiles y el ranking por requisitos y coste. No presentar el ranking como medida de calidad-precio.

## Entregables

El comando reproducible generará CSV, JSON y gráficos finales en `results/final/`. La demo mostrará recomendación y resultados temporales y de evaluación sin recalcular modelos durante la presentación. El equipo tendrá un README actualizado, presentación editable y guion cronometrado de cinco minutos, con notas para preguntas y un recorrido corto de demo.

## Comprobación

Pruebas unitarias de separación temporal, conteo de continuadores/entrantes/salientes y evaluación con grupos. Ejecución completa del pipeline, inspección de métricas y gráficos, prueba de la demo y revisión visual de las diapositivas. Cualquier resultado inferior al baseline se mostrará tal cual.
