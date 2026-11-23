# Recorrido de la demo final

## Antes de presentar

1. En la raíz del repositorio, ejecutar `python -m scripts.run_final` y `python -m streamlit run streamlit_app.py`.
2. Comprobar que aparecen las pestañas **Recomendador**, **Evolución** y **Evaluación** y que los gráficos cargan.
3. Mantener la ventana del navegador abierta antes de iniciar el vídeo. La demo en vivo se realiza después del vídeo, cuando lo pida el docente.

## Recorrido de 60 a 90 segundos

1. **Recomendador:** dejar 1.000.000 tokens de entrada, 250.000 de salida, contexto mínimo 32.000 y Visión. Mostrar la tabla ordenada por coste: hay 1.310 opciones. Cambiar el contexto a 256.000; quedan 974 opciones y cambia el primer puesto. Explicar que el coste se calcula con las dos tarifas de lista y que las capacidades son filtros.
2. **Evolución:** mostrar mediana inicial y final. Señalar la curva de continuadores, las entradas a la cohorte y los cambios de tarifa. Decir que 519 cambios se observan entre 135.928 comparaciones de listados presentes en dos semanas observadas sucesivas, sin inferir causalidad.
3. **Evaluación:** mostrar la prueba temporal. Señalar que la persistencia supera a la regresión en MAE. Bajar a las cinco particiones y mostrar que la clasificación supera al baseline de clase mayoritaria en macro-F1.

## Respuestas breves

- **¿Cuál es la mejor predicción temporal?** En el horizonte y periodo evaluados, la persistencia de la última mediana; MAE 0,0145 USD frente a 0,0381 USD de la regresión.
- **¿Por qué cae el precio de mercado si pocas tarifas cambian?** El conjunto de listados varía mucho. Las 519 modificaciones de tarifa se comparan con 3.905 eventos de entrada a la cohorte, pero esas cifras por sí solas no permiten atribuir una fracción exacta de la caída a cada mecanismo.
- **¿Es calidad-precio?** No: el CSV no tiene benchmark de calidad. Es menor coste entre modelos que satisfacen requisitos declarados.
- **¿Qué país es más barato?** Solo observamos país del desarrollador. Las diferencias descriptivas entre EE. UU. y China pueden reflejar mezcla de modelos y proveedores; no identifican el efecto del país.
- **¿Cuándo costará 0,10 USD la IA de frontera?** No es estimable con esta fuente, porque no identifica cuáles modelos son de frontera.
