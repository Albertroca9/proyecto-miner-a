"""Live demo: cost ranking, catalogue dynamics and measured model performance."""

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from avance.data import prepare_snapshot
from avance.recommend import recommend


ROOT = Path(__file__).resolve().parent
CAPABILITIES = {
    "Visión": "supports_vision",
    "Llamada a funciones": "supports_function_calling",
    "Razonamiento": "supports_reasoning",
    "Entrada PDF": "supports_pdf_input",
    "Entrada de audio": "supports_audio_input",
    "Salida de audio": "supports_audio_output",
}


@st.cache_data
def load_listings() -> pd.DataFrame:
    return prepare_snapshot(pd.read_csv(ROOT / "ai_models_2026.csv"))


@st.cache_data
def load_final_results() -> tuple[dict, pd.DataFrame]:
    folder = ROOT / "results" / "final"
    evaluation = json.loads((folder / "evaluation.json").read_text(encoding="utf-8"))
    splits = pd.read_csv(folder / "classification_splits.csv")
    return evaluation, splits


st.title("El precio de la inteligencia")
st.caption("Precios de lista de modelos chat: análisis histórico y recomendación por requisitos.")
ranking_tab, history_tab, evaluation_tab = st.tabs(["Recomendador", "Evolución", "Evaluación"])

with ranking_tab:
    st.subheader("Menor coste entre opciones que cumplen tus requisitos")
    listings = load_listings()
    input_tokens = st.number_input("Tokens de entrada", min_value=0, value=1_000_000, step=100_000)
    output_tokens = st.number_input("Tokens de salida", min_value=0, value=250_000, step=50_000)
    min_context = st.number_input("Contexto mínimo de entrada", min_value=0, value=32_000, step=8_000)
    selected = st.multiselect("Capacidades requeridas", list(CAPABILITIES), default=["Visión"])
    choices = recommend(listings, input_tokens, output_tokens, min_context, [CAPABILITIES[name] for name in selected])
    st.write(f"{len(choices)} listados cumplen los requisitos.")
    st.dataframe(
        choices[["model_name", "provider", "developer_country", "max_input_tokens", "estimated_cost_usd"]]
        .head(20)
        .rename(columns={
            "model_name": "Modelo", "provider": "Proveedor", "developer_country": "País del desarrollador",
            "max_input_tokens": "Contexto", "estimated_cost_usd": "Coste estimado (USD)",
        }),
        hide_index=True,
        width="stretch",
    )
    st.caption("Coste = entrada × tarifa de entrada + salida × tarifa de salida. No se mide calidad, latencia ni disponibilidad.")

try:
    final, splits = load_final_results()
except FileNotFoundError:
    with history_tab:
        st.error("Faltan resultados finales. Ejecuta: python -m scripts.run_final")
else:
    with history_tab:
        dynamics = final["catalog_dynamics"]
        st.subheader("Cómo cambia el catálogo")
        st.metric("Mediana del coste de ejemplo: primera semana", f"${dynamics['first_week_median_example_cost_usd']:.2f}")
        st.metric("Mediana del coste de ejemplo: última semana", f"${dynamics['last_week_median_example_cost_usd']:.2f}")
        st.image(str(ROOT / "results" / "final" / "dinamica_catalogo.png"))
        st.write(
            f"En {dynamics['continuing_listing_weeks']:,} comparaciones de listados presentes en dos semanas "
            f"observadas sucesivas hubo {dynamics['input_price_change_events']:,} cambios de tarifa de entrada "
            f"({dynamics['change_share_of_continuing_pct']:.2f} %)."
        )
        st.caption("Las entradas son nuevas en la cohorte elegible; pueden ser listados antiguos que antes no cumplían el filtro. Las curvas no constituyen una descomposición causal.")

    with evaluation_tab:
        temporal = final["temporal"]
        classification = final["classification_repeated"]
        st.subheader("Predicción de la mediana semanal")
        st.write(f"Prueba cronológica: {temporal['holdout_weeks']} semanas, {temporal['first_test_week']} a {temporal['last_test_week']}.")
        st.metric("MAE regresión", f"${temporal['regression']['mae_usd']:.4f}")
        st.metric("MAE persistencia", f"${temporal['persistence']['mae_usd']:.4f}")
        st.image(str(ROOT / "results" / "final" / "prediccion_temporal.png"))
        st.caption("El baseline copia la última mediana observada. Un MAE menor es mejor; en esta prueba la persistencia gana.")
        st.subheader("Clasificación de franjas tarifarias")
        st.write(
            f"Macro-F1 medio en {classification['splits']} separaciones por nombre de modelo: "
            f"bosque aleatorio {classification['model_macro_f1']['mean']:.3f} "
            f"(DE {classification['model_macro_f1']['std']:.3f}); "
            f"clase mayoritaria {classification['baseline_macro_f1']['mean']:.3f} "
            f"(DE {classification['baseline_macro_f1']['std']:.3f})."
        )
        st.dataframe(splits[["seed", "model_macro_f1", "baseline_macro_f1", "model_accuracy", "baseline_accuracy"]], hide_index=True)
        st.caption("No hay benchmark de calidad para identificar IA de frontera o evaluar calidad-precio.")

