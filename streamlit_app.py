"""Small interactive demonstration of the cost-and-requirements recommender."""

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


st.title("El precio de la inteligencia")
st.caption("Prototipo: modelos chat que cumplen requisitos, ordenados por coste de lista estimado.")
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
st.caption("No se mide calidad ni disponibilidad. Los precios son los del archivo facilitado y pueden haber cambiado.")

