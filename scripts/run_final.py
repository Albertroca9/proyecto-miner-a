"""Generate the final, reproducible evaluation and presentation evidence."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from avance.data import INPUT_PRICE, OUTPUT_PRICE, prepare_snapshot
from avance.final_analysis import catalog_dynamics, forecast_weekly_cost, score_forecasts
from avance.history import prepare_history
from avance.models import evaluate_classifier


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "final"


def save_json(name: str, payload: dict) -> None:
    (OUT / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def plot_forecast(predictions: pd.DataFrame, actual_history: pd.Series) -> None:
    fig, ax = plt.subplots(figsize=(10, 5), layout="constrained")
    recent = actual_history.iloc[-52:]
    ax.plot(recent.index, recent.values, label="Mediana observada", color="#172554", linewidth=2)
    ax.plot(predictions.week_start, predictions.prediction, label="Regresión", color="#ea580c")
    ax.plot(predictions.week_start, predictions.baseline, label="Persistencia", color="#16a34a", alpha=.8)
    ax.axvline(predictions.week_start.iloc[0], color="#64748b", linestyle="--", linewidth=1)
    ax.set(title="Predicción semanal fuera de tiempo", ylabel="USD por 1 M entrada + 0,25 M salida", xlabel="Semana")
    ax.legend()
    fig.savefig(OUT / "prediccion_temporal.png", dpi=180)
    plt.close(fig)


def plot_dynamics(dynamics: pd.DataFrame) -> None:
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(10, 6), sharex=True, layout="constrained")
    top.plot(dynamics.week_start, dynamics.median_all_input_usd, label="Todos los listados", color="#172554")
    top.plot(dynamics.week_start, dynamics.median_continuer_input_usd, label="Continuadores semanales", color="#ea580c")
    top.set(ylabel="USD por 1 M entrada", title="Mediana del catálogo y de listados presentes en semanas consecutivas")
    top.legend()
    bottom.plot(dynamics.week_start, dynamics.entrants, label="Entradas a la cohorte", color="#16a34a")
    bottom.plot(dynamics.week_start, dynamics.input_price_changes, label="Tarifas modificadas", color="#dc2626")
    bottom.set(xlabel="Semana", ylabel="N.º de listados")
    bottom.legend()
    fig.savefig(OUT / "dinamica_catalogo.png", dpi=180)
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    snapshot = prepare_snapshot(pd.read_csv(ROOT / "ai_models_2026.csv"))
    history = prepare_history(pd.read_csv(ROOT / "ai_model_price_history.csv"))
    history["example_cost_usd"] = history[INPUT_PRICE] + .25 * history[OUTPUT_PRICE]
    weekly_cost = history.groupby("week_start")["example_cost_usd"].median().sort_index()
    predictions = forecast_weekly_cost(weekly_cost, holdout=26, min_history=20)
    temporal_metrics = score_forecasts(predictions)
    dynamics = catalog_dynamics(history)
    predictions.to_csv(OUT / "temporal_predictions.csv", index=False)
    dynamics.to_csv(OUT / "catalog_dynamics.csv", index=False)

    seeds = [7, 11, 19, 23, 31]
    evaluations = []
    for seed in seeds:
        metrics = evaluate_classifier(snapshot, random_state=seed)
        evaluations.append({
            "seed": seed,
            "train_rows": metrics["train_rows"],
            "test_rows": metrics["test_rows"],
            "model_macro_f1": metrics["model"]["macro_f1"],
            "baseline_macro_f1": metrics["baseline"]["macro_f1"],
            "model_accuracy": metrics["model"]["accuracy"],
            "baseline_accuracy": metrics["baseline"]["accuracy"],
        })
    repeated = pd.DataFrame(evaluations)
    repeated.to_csv(OUT / "classification_splits.csv", index=False)
    classification_summary = {
        column: {"mean": float(repeated[column].mean()), "std": float(repeated[column].std(ddof=1))}
        for column in ("model_macro_f1", "baseline_macro_f1", "model_accuracy", "baseline_accuracy")
    }
    temporal_summary = {
        "holdout_weeks": len(predictions),
        "first_test_week": str(predictions.week_start.iloc[0].date()),
        "last_test_week": str(predictions.week_start.iloc[-1].date()),
        "regression": temporal_metrics["model"],
        "persistence": temporal_metrics["baseline"],
    }
    dynamics_summary = {
        "weekly_transitions": len(dynamics) - 1,
        "entrant_events": int(dynamics.entrants.iloc[1:].sum()),
        "continuing_listing_weeks": int(dynamics.continuers.iloc[1:].sum()),
        "input_price_change_events": int(dynamics.input_price_changes.iloc[1:].sum()),
        "change_share_of_continuing_pct": float(100 * dynamics.input_price_changes.iloc[1:].sum() / dynamics.continuers.iloc[1:].sum()),
        "first_week_median_example_cost_usd": float(weekly_cost.iloc[0]),
        "last_week_median_example_cost_usd": float(weekly_cost.iloc[-1]),
        "last_week_entrants": int(dynamics.entrants.iloc[-1]),
    }
    save_json("evaluation.json", {
        "temporal": temporal_summary,
        "classification_repeated": {"splits": len(repeated), **classification_summary},
        "catalog_dynamics": dynamics_summary,
    })
    plot_forecast(predictions, weekly_cost)
    plot_dynamics(dynamics)
    print(f"Final outputs: {OUT}")
    print(f"Temporal MAE: regression {temporal_metrics['model']['mae_usd']:.4f}, persistence {temporal_metrics['baseline']['mae_usd']:.4f}")
    print(f"Classification macro-F1: model {classification_summary['model_macro_f1']['mean']:.3f}, baseline {classification_summary['baseline_macro_f1']['mean']:.3f}")


if __name__ == "__main__":
    main()
