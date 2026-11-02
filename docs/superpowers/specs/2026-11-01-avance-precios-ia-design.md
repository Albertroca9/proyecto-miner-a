# Avance del proyecto: El precio de la inteligencia

## Objetivo

Entregar un avance reproducible que cumpla la propuesta inicial: datos preparados, entorno experimental, análisis temporal, dos técnicas exploratorias y un recomendador inicial. La entrega final podrá ampliar los modelos, evaluarlos frente a baselines y mostrar una demo en vivo.

## Alcance y datos

- Fuentes: `ai_models_2026.csv` y `ai_model_price_history.csv`, conservados sin cambios.
- Cohorte comparable: listados `chat` con precios positivos de entrada y salida por millón de tokens.
- Coste de ejemplo: un millón de tokens de entrada y 250.000 de salida. El resultado es un precio de lista estimado, en USD.
- País: `developer_country` significa país del desarrollador, nunca del proveedor.
- El conjunto no incluye puntuaciones de calidad; el recomendador ordenará opciones que cumplan requisitos por coste, sin afirmar calidad-precio.

## Componentes

1. Preparación: validar columnas, filtrar la cohorte y derivar coste del ejemplo sin modificar fuentes.
2. Análisis: calcular cobertura, faltantes, evolución semanal, cambios de tarifa de listados existentes y resumen por país.
3. Experimentos: clustering con precio, contexto y capacidades; clasificación de tramos tarifarios con especificaciones, partición por nombre de modelo y baseline de clase mayoritaria.
4. Recomendación: filtrar por contexto y capacidades y ordenar por coste estimado.
5. Presentación: resultados guardados, instrucciones de ejecución, guion de cuatro minutos y una demo simple reutilizable para el final.

## Evaluación y límites

- El clustering tendrá perfiles de grupos y una métrica interna de separación.
- La clasificación tendrá accuracy, macro-F1 y matriz de confusión para modelo y baseline. Los umbrales de tramo se calculan solo con entrenamiento.
- Las medianas temporales son descriptivas: la población de listados cambia con el tiempo. Se cuantificarán los cambios observados dentro de un mismo `model_id`.
- La predicción temporal y una evaluación fuera de tiempo quedan para la entrega final. Un umbral de 0,10 USD para modelos de frontera requiere primero una definición verificable de frontera.

## Criterio de aceptación

Una persona del equipo puede instalar dependencias, ejecutar una orden, obtener datos procesados, gráficos, métricas y recomendaciones, y explicar esos resultados en cuatro minutos sin atribuir causalidad ni calidad no medida.
