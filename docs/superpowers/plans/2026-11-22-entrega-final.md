# Entrega final Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Entregar un proyecto final reproducible con evaluación honesta, demo y materiales para el vídeo de cinco minutos.

**Architecture:** `avance/final_analysis.py` implementa funciones analíticas sin E/S. `scripts/run_final.py` ejecuta el pipeline sobre los CSV y guarda resultados. `streamlit_app.py` lee esos resultados para la demostración. Los documentos y diapositivas se basan exclusivamente en las salidas verificadas.

**Tech Stack:** Python, pandas, numpy, scikit-learn, matplotlib, Streamlit y PowerPoint editable.

---

### Task 1: Auditoría de datos y protocolo

**Files:** `docs/superpowers/specs/2026-11-22-entrega-final-design.md`, `avance/final_analysis.py`, `tests/test_final_analysis.py`.

- [x] Confirmar columnas, fechas, duplicados por `model_id` y semana, y cobertura de ambas tarifas con una lectura de los CSV.
- [x] Escribir pruebas que exijan que la predicción de la semana `t` solo utilice semanas anteriores y que los conteos de entrantes, continuadores y salientes sean correctos en una tabla pequeña.
- [x] Ejecutar `python -m unittest tests.test_final_analysis -v` y comprobar que falla por las funciones ausentes.
- [x] Implementar las funciones mínimas y repetir la orden hasta obtener cero fallos.

### Task 2: Experimentos finales

**Files:** `avance/final_analysis.py`, `scripts/run_final.py`, `tests/test_final_analysis.py`, `results/final/`.

- [x] Añadir pruebas de MAE/sMAPE y de particiones por nombre de modelo; ejecutarlas en rojo.
- [x] Evaluar 26 predicciones semanales con entrenamiento expansivo y baseline de persistencia; guardar predicciones y métricas.
- [x] Repetir cinco particiones de clasificación y guardar métricas por semilla y resumen; guardar dinámica semanal del catálogo.
- [x] Ejecutar `python -m scripts.run_final` y comprobar que los archivos producidos contienen 26 predicciones y cinco particiones.

### Task 3: Demo y documentación

**Files:** `streamlit_app.py`, `README.md`, `docs/demo_final.md`.

- [x] Añadir una vista de resultados temporales y evaluación a la demo, leyendo `results/final/` y conservando el recomendador.
- [x] Documentar instalación, ejecución, interpretación de métricas, limitaciones y el orden de la demo.
- [x] Ejecutar la demo con `streamlit.testing.v1.AppTest` y verificar que carga sin excepciones.

### Task 4: Presentación y vídeo

**Files:** `output/entrega_final_2026-11-23.pptx`, `docs/guion_final_5_min.md`.

- [x] Construir una presentación de cinco minutos con problema, datos, novedad, evaluación, recomendador y cierre.
- [x] Incluir métricas finales y límites exactos, sin cifras redactadas antes de ejecutar el pipeline.
- [x] Redactar guion con tiempos, turnos y respuesta a preguntas previsibles.
- [x] Renderizar todas las diapositivas, revisar legibilidad y verificar la duración por recuento de palabras.

### Task 5: Revisión de entrega

**Files:** `tests/`, `results/final/`, `README.md`.

- [x] Ejecutar todas las pruebas y ambos pipelines desde la rama final.
- [x] Verificar el funcionamiento de la demo y la existencia de todos los archivos enlazados en README.
- [x] Revisar el diff y registrar el estado final del repositorio sin incluir archivos temporales.
