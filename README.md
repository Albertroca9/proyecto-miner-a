# El precio de la inteligencia — avance

Proyecto de Minería de Datos sobre tarifas de modelos de IA. Este repositorio contiene una primera entrega reproducible: preparación de datos, análisis temporal, clustering, clasificación de tramos tarifarios y un recomendador por requisitos y coste.

## Reproducir el avance

Desde la raíz del repositorio, con Python 3.10 o posterior:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m scripts.run_avance
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

La última orden abre la demo interactiva. Para regenerar las tablas y los gráficos basta con `python -m scripts.run_avance` si las dependencias ya están instaladas.

## Datos y selección

- `ai_models_2026.csv`: catálogo actual de 4.403 listados y 31 columnas.
- `ai_model_price_history.csv`: 167.787 observaciones de 157 semanas, del 18-09-2023 al 28-09-2026.
- Cohorte principal: `mode == chat` y precios de entrada y salida positivos. Quedan 3.082 listados del catálogo y 139.874 observaciones históricas.
- Coste de ejemplo: precio de **un millón de tokens de entrada más 250.000 de salida**, en USD. Se calcula como `input_price_per_1m_tokens + 0.25 * output_price_per_1m_tokens`.
- `developer_country` es el país del **desarrollador del modelo**. No identifica el país del proveedor.

El archivo `LICENSE_LiteLLM_source_data.txt` acompaña las fuentes facilitadas. Los CSV originales no se modifican; el pipeline guarda sus derivados en `results/`.

## Qué produce el pipeline

| Archivo | Contenido |
| --- | --- |
| `results/summary.json` | Volumen, cobertura, cambios observados de precio y recuentos por país. |
| `results/clean_snapshot.csv` | Cohorte actual comparable y coste del ejemplo. |
| `results/weekly_summary.csv` | Medianas y recuento de listados por semana. |
| `results/country_summary.csv` | Comparación descriptiva por país del desarrollador. |
| `results/cluster_profiles.csv` | Tamaño, precios, contexto y capacidades de los grupos. |
| `results/metrics.json` | Silhouette, clasificación y baseline. |
| `results/recommendations_example.csv` | Primeras diez opciones con visión y 32.000 tokens de contexto. |
| `results/evolucion_semanal.png` | Precios medianos y número de listados a lo largo del tiempo. |
| `results/pais_desarrollador.png` | Medianas descriptivas de EE. UU. y China. |

## Experimentos y lectura correcta

**Clustering.** Se aplican KMeans de 2 a 6 grupos a logaritmos de precios y contexto junto con indicadores de capacidades. Se elige el número de grupos con la mayor silhouette calculada sobre una muestra fija. Los perfiles ayudan a interpretar los grupos; silhouette es una métrica interna, no una medida de utilidad para un usuario.

**Clasificación.** Se predice una franja del coste de ejemplo usando únicamente contexto y capacidades. Los umbrales de los tres tramos se calculan con los datos de entrenamiento. El conjunto de prueba se separa por `model_name`, de modo que un nombre no aparece en ambos lados. Se comparan un bosque aleatorio y un baseline de clase mayoritaria mediante accuracy y macro-F1. Es una primera partición exploratoria; la evaluación final requerirá más particiones o validación apropiada.

**Recomendación.** Se filtra por contexto y capacidades requeridas y se ordena por coste de lista estimado para un volumen de tokens indicado. No se dispone de una puntuación de calidad, latencia, disponibilidad ni descuentos; el sistema no afirma cuál tiene la mejor calidad-precio.

**Tiempo y geografía.** Las medianas de cada semana incluyen modelos diferentes, por lo que sus cambios no equivalen a rebajas de un mismo modelo. Se calculan por separado cambios entre observaciones sucesivas del mismo `model_id`. La comparación entre países es descriptiva y está afectada por diferencias de gama, capacidades y proveedores; no permite una conclusión causal.

## Próxima entrega

Para la entrega final: evaluar predicción temporal frente a una tarifa persistente como baseline, profundizar en rebajas de modelos existentes frente a entrada de nuevos modelos, consolidar la demo y validar la utilidad del ranking. El umbral de 0,10 USD para «IA de frontera» requiere primero una definición medible de frontera; el archivo actual no tiene benchmarks de calidad.

El guion y la estructura de diapositivas para el vídeo de avance están en [`docs/avance_video_4_min.md`](docs/avance_video_4_min.md).
La presentación editable de cinco diapositivas está en [`output/avance_proyecto_2026-11-01.pptx`](output/avance_proyecto_2026-11-01.pptx); incluye el texto de locución en las notas del presentador.
