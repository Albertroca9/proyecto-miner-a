"""Build the reproducible outputs used in the four-minute progress video."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from avance.data import INPUT_PRICE, OUTPUT_PRICE, prepare_snapshot
from avance.history import prepare_history, price_changes, weekly_summary
from avance.models import evaluate_classifier, evaluate_clusters
from avance.recommend import recommend


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def save_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def plot_history(weekly: pd.DataFrame) -> None:
    fig, (prices, counts) = plt.subplots(2, 1, figsize=(9, 6), sharex=True, layout="constrained")
    prices.plot(weekly.week_start, weekly.median_input_usd, label="Entrada")
    prices.plot(weekly.week_start, weekly.median_output_usd, label="Salida")
    prices.set(ylabel="USD / millón de tokens", title="Mediana semanal de listados chat con dos tarifas positivas")
    prices.legend()
    counts.plot(weekly.week_start, weekly.n_listings, color="#2563a6")
    counts.set(xlabel="Semana", ylabel="Listados elegibles")
    fig.savefig(RESULTS / "evolucion_semanal.png", dpi=180)
    plt.close(fig)


def plot_country(snapshot: pd.DataFrame) -> None:
    subset = snapshot.loc[snapshot.developer_country.isin(["USA", "China"])]
    medians = subset.groupby("developer_country")[[INPUT_PRICE, OUTPUT_PRICE]].median().reindex(["USA", "China"])
    fig, ax = plt.subplots(figsize=(6, 4), layout="constrained")
    medians.rename(columns={INPUT_PRICE: "Entrada", OUTPUT_PRICE: "Salida"}).plot.bar(ax=ax, rot=0)
    ax.set(xlabel="País del desarrollador", ylabel="USD / millón de tokens", title="Medianas descriptivas: modelos chat")
    fig.savefig(RESULTS / "pais_desarrollador.png", dpi=180)
    plt.close(fig)


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    raw_snapshot = pd.read_csv(ROOT / "ai_models_2026.csv")
    raw_history = pd.read_csv(ROOT / "ai_model_price_history.csv")
    snapshot = prepare_snapshot(raw_snapshot)
    history = prepare_history(raw_history)
    weekly = weekly_summary(history)

    snapshot.to_csv(RESULTS / "clean_snapshot.csv", index=False)
    weekly.to_csv(RESULTS / "weekly_summary.csv", index=False)

    country = snapshot.loc[snapshot.developer_country.isin(["USA", "China"])].groupby("developer_country").agg(
        n_listings=("model_id", "size"),
        median_input_usd=(INPUT_PRICE, "median"),
        median_output_usd=(OUTPUT_PRICE, "median"),
        median_example_cost_usd=("example_cost_usd", "median"),
    )
    country.to_csv(RESULTS / "country_summary.csv")

    cluster_metrics, profiles = evaluate_clusters(snapshot)
    classifier_metrics = evaluate_classifier(snapshot)
    profiles.to_csv(RESULTS / "cluster_profiles.csv", index=False)
    save_json(RESULTS / "metrics.json", {"clustering": cluster_metrics, "classification": classifier_metrics})

    example = recommend(snapshot, 1_000_000, 250_000, 32_000, ["supports_vision"])
    example[["model_id", "model_name", "provider", "max_input_tokens", "estimated_cost_usd"]].head(10).to_csv(
        RESULTS / "recommendations_example.csv", index=False
    )
    summary = {
        "snapshot_rows": len(raw_snapshot),
        "history_rows": len(raw_history),
        "eligible_snapshot_chat": len(snapshot),
        "eligible_history_chat": len(history),
        "history_weeks": len(weekly),
        "first_week": str(weekly.week_start.iloc[0].date()),
        "last_week": str(weekly.week_start.iloc[-1].date()),
        "first_week_listings": int(weekly.n_listings.iloc[0]),
        "last_week_listings": int(weekly.n_listings.iloc[-1]),
        "first_week_median_input_usd": float(weekly.median_input_usd.iloc[0]),
        "last_week_median_input_usd": float(weekly.median_input_usd.iloc[-1]),
        "first_week_median_output_usd": float(weekly.median_output_usd.iloc[0]),
        "last_week_median_output_usd": float(weekly.median_output_usd.iloc[-1]),
        "input_price_changes": price_changes(history, INPUT_PRICE),
        "output_price_changes": price_changes(history, OUTPUT_PRICE),
        "country_counts": {name: int(value) for name, value in snapshot.developer_country.value_counts().items()},
        "missing_current_input_pct": float(100 * raw_snapshot[INPUT_PRICE].isna().mean()),
        "missing_current_output_pct": float(100 * raw_snapshot[OUTPUT_PRICE].isna().mean()),
    }
    save_json(RESULTS / "summary.json", summary)
    plot_history(weekly)
    plot_country(snapshot)
    print(f"Resultados guardados en {RESULTS}")
    print(f"Listados chat elegibles: {len(snapshot)}; semanas: {len(weekly)}")
    print(f"Clasificación macro-F1: {classifier_metrics['model']['macro_f1']:.3f}; baseline: {classifier_metrics['baseline']['macro_f1']:.3f}")


if __name__ == "__main__":
    main()
