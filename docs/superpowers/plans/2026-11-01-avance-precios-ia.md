# Avance de precios de IA Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Generar el avance reproducible y presentable del proyecto con los dos CSV existentes.

**Architecture:** Funciones separadas para preparar datos, resumir el histórico, entrenar experimentos y recomendar. Un ejecutable produce resultados en `results/` y un guion explica exactamente qué mostrar. Las fuentes originales permanecen intactas.

**Tech Stack:** Python, pandas, numpy, scikit-learn, matplotlib, Streamlit opcional para la demo.

---

### Task 1: Preparación y recomendación

**Files:** Create `avance/data.py`, `avance/recommend.py`, `tests/test_data.py`, `tests/test_recommend.py`.

- [x] Escribir pruebas para filtro `chat` con dos precios positivos, coste `entrada + 0.25 * salida`, y filtro por contexto/capacidades.
- [x] Ejecutar `python -m unittest discover -s tests -v` y verificar el fallo por funciones ausentes.
- [x] Implementar `prepare_snapshot(frame)` y `recommend(frame, input_tokens, output_tokens, min_context, required_capabilities)`; validar volúmenes no negativos y ordenar por coste.
- [x] Ejecutar las pruebas y comprobar que pasan.

### Task 2: Resumen temporal

**Files:** Create `avance/history.py`, `tests/test_history.py`.

- [x] Escribir pruebas con dos semanas y dos modelos para mediana semanal y cambios emparejados por `model_id`.
- [x] Ejecutar las pruebas y verificar el fallo esperado.
- [x] Implementar `prepare_history(frame)`, `weekly_summary(frame)` y `price_changes(frame)` con precios positivos y fechas válidas.
- [x] Ejecutar las pruebas y comprobar que pasan.

### Task 3: Modelos exploratorios

**Files:** Create `avance/models.py`, `tests/test_models.py`.

- [x] Escribir pruebas de tramos calculados en entrenamiento, separación por `model_name` y ausencia de precios en las variables de clasificación.
- [x] Ejecutar las pruebas y verificar el fallo esperado.
- [x] Implementar clustering KMeans y clasificación con baseline DummyClassifier, métricas y perfiles de grupos.
- [x] Ejecutar las pruebas y comprobar que pasan.

### Task 4: Salidas y presentación

**Files:** Create `scripts/run_avance.py`, `requirements.txt`, `README.md`, `docs/avance_video_4_min.md`, `.gitignore`.

- [x] Ejecutar el pipeline con los CSV del repositorio y producir `results/summary.json`, `results/metrics.json`, `results/clean_snapshot.csv`, `results/weekly_summary.csv`, perfiles, recomendaciones y gráficos.
- [x] Comparar las cifras generadas con la auditoría exploratoria: 4.403 listados actuales, 167.787 filas históricas y 3.082 listados `chat` elegibles.
- [x] Documentar comando de reproducción, definiciones, límites, interpretación de resultados y guion del vídeo de 4 minutos.
- [x] Ejecutar todas las pruebas y el pipeline de nuevo, revisar salidas y `git diff --check`.

### Task 5: Presentación editable

**Files:** Create `scripts/build_avance_deck.mjs`, `output/avance_proyecto_2026-11-01.pptx`.

- [x] Convertir las cifras verificadas y el guion a cinco diapositivas con notas del presentador.
- [x] Conservar los gráficos cuantitativos como objetos nativos con datos editables.
- [x] Validar la estructura del PPTX e inspeccionar visualmente las cinco diapositivas finales.
