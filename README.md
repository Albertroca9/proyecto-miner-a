# El precio de la inteligencia — proyecto final

Proyecto de Minería de Datos sobre tarifas de modelos de IA. Contiene el avance original y una evaluación final reproducible: serie temporal fuera de tiempo, comparación frente a baselines, dinámica del catálogo, clasificación repetida, clustering y un recomendador por requisitos y coste.

## Entrega final: ejecución rápida

Desde la raíz de este directorio de trabajo, con Python 3.10 o posterior:

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m scripts.run_avance
python -m scripts.run_final
python -m streamlit run streamlit_app.py
```

El último comando inicia la demo. Su recorrido está en [`docs/demo_final.md`](docs/demo_final.md), y el guion del vídeo en [`docs/guion_final_5_min.md`](docs/guion_final_5_min.md). La presentación editable está en `output/entrega_final_2026-11-23.pptx`.

### Resultados finales y cómo interpretarlos

`results/final/evaluation.json` contiene las métricas; `temporal_predictions.csv`, `catalog_dynamics.csv` y `classification_splits.csv` permiten auditarlas. Hay dos gráficos en el mismo directorio.

- **Serie temporal:** se predice la mediana semanal del coste de 1 M de tokens de entrada y 0,25 M de salida. Se reservan las últimas 26 semanas; cada predicción usa solo semanas anteriores. La regresión con tendencia y retardos obtiene MAE de **0,0381 USD** y sMAPE de **3,91 %**. La persistencia de la última mediana obtiene **0,0145 USD** y **1,46 %**. El baseline es mejor en esta prueba.
- **Dinámica:** en 156 transiciones entre semanas observadas sucesivas hubo **519** modificaciones de tarifa de entrada en **135.928** comparaciones de listados continuadores (**0,382 %**). Se observaron **3.905** eventos de entrada a la cohorte elegible; una entrada puede ser un listado ya existente que antes no cumplía el filtro. La comparación es descriptiva y no asigna causalmente la caída de la mediana a esas entradas.
- **Clasificación:** en cinco separaciones por `model_name`, el bosque aleatorio obtiene macro-F1 medio **0,594** (DE 0,020), frente a **0,158** (DE 0,016) de la clase mayoritaria. Los umbrales de franja y la imputación se calculan solo con entrenamiento en cada partición. Las cinco particiones no son intervalos de confianza.
- **Clustering:** tres grupos seleccionados por silhouette (**0,266**) ayudan a describir perfiles de coste, contexto y capacidades; la métrica no evalúa utilidad comercial.

El catálogo no contiene benchmark de calidad, latencia ni disponibilidad. Por ello, el recomendador encuentra el menor **precio de lista** entre los listados que cumplen los requisitos indicados; no mide calidad-precio. `developer_country` indica país del desarrollador, no del proveedor, y una diferencia entre países no demuestra causalidad. Tampoco existe una definición verificable de «IA de frontera» en estos CSV, por lo que no se extrapola una fecha para 0,10 USD.

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

## Evolución del avance al final

El avance dejó preparado el tratamiento de datos, los primeros experimentos y el recomendador. La entrega final añade prueba cronológica con baseline, cinco particiones para clasificación, seguimiento explícito de entradas y cambios de tarifa, y tres vistas en la demo. El ranking se valida como cálculo y filtro reproducible; su utilidad subjetiva o su calidad de respuesta no se pueden evaluar con los CSV disponibles.

El guion y la estructura de diapositivas para el vídeo de avance están en [`docs/avance_video_4_min.md`](docs/avance_video_4_min.md).
La presentación editable de cinco diapositivas está en [`output/avance_proyecto_2026-11-01.pptx`](output/avance_proyecto_2026-11-01.pptx); incluye el texto de locución en las notas del presentador.
