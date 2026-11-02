"""Exploratory clustering and tariff-band classification."""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, silhouette_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler


CAPABILITY_COLUMNS = (
    "supports_vision", "supports_function_calling", "supports_reasoning",
    "supports_prompt_caching", "supports_pdf_input", "supports_web_search",
    "supports_audio_input", "supports_audio_output", "supports_video_input",
    "supports_response_schema", "supports_computer_use", "supports_system_messages",
)
CLASSIFICATION_FEATURES = ("max_input_tokens", "max_output_tokens", *CAPABILITY_COLUMNS)


def make_group_split(frame, test_size=0.25, random_state=7):
    splitter = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)
    return next(splitter.split(frame, groups=frame["model_name"]))


def price_bands(train, test):
    thresholds = tuple(float(x) for x in np.quantile(train, [1 / 3, 2 / 3]))
    return (
        np.digitize(train, thresholds),
        np.digitize(test, thresholds),
        thresholds,
    )


def _feature_matrix(frame: pd.DataFrame, include_prices: bool) -> np.ndarray:
    columns = list(CLASSIFICATION_FEATURES)
    if include_prices:
        columns += ["input_price_per_1m_tokens", "output_price_per_1m_tokens"]
    matrix = frame[columns].apply(pd.to_numeric, errors="coerce")
    for column in ("max_input_tokens", "max_output_tokens"):
        matrix[column] = np.log1p(matrix[column].clip(lower=0))
    if include_prices:
        for column in ("input_price_per_1m_tokens", "output_price_per_1m_tokens"):
            matrix[column] = np.log1p(matrix[column].clip(lower=0))
    return matrix.to_numpy(dtype=float)


def evaluate_classifier(frame: pd.DataFrame) -> dict:
    train_idx, test_idx = make_group_split(frame)
    train, test = frame.iloc[train_idx], frame.iloc[test_idx]
    y_train, y_test, thresholds = price_bands(
        train["example_cost_usd"].to_numpy(), test["example_cost_usd"].to_numpy()
    )
    x_train = _feature_matrix(train, include_prices=False)
    x_test = _feature_matrix(test, include_prices=False)
    imputer = SimpleImputer(strategy="median", keep_empty_features=True)
    x_train = imputer.fit_transform(x_train)
    x_test = imputer.transform(x_test)
    model = RandomForestClassifier(n_estimators=150, min_samples_leaf=4, random_state=7, n_jobs=1)
    baseline = DummyClassifier(strategy="most_frequent")
    model.fit(x_train, y_train)
    baseline.fit(x_train, y_train)

    def score(estimator):
        pred = estimator.predict(x_test)
        return {
            "accuracy": float(accuracy_score(y_test, pred)),
            "macro_f1": float(f1_score(y_test, pred, average="macro", zero_division=0)),
            "confusion_matrix": confusion_matrix(y_test, pred, labels=[0, 1, 2]).tolist(),
        }

    return {
        "train_rows": len(train),
        "test_rows": len(test),
        "train_model_names": train.model_name.nunique(),
        "test_model_names": test.model_name.nunique(),
        "band_thresholds_usd": thresholds,
        "model": score(model),
        "baseline": score(baseline),
    }


def evaluate_clusters(frame: pd.DataFrame) -> tuple[dict, pd.DataFrame]:
    matrix = _feature_matrix(frame, include_prices=True)
    matrix = SimpleImputer(strategy="median", keep_empty_features=True).fit_transform(matrix)
    matrix = StandardScaler().fit_transform(matrix)
    scores = {}
    labels_by_k = {}
    for k in range(2, 7):
        labels = KMeans(n_clusters=k, n_init=10, random_state=7).fit_predict(matrix)
        scores[k] = float(silhouette_score(matrix, labels, sample_size=min(1000, len(matrix)), random_state=7))
        labels_by_k[k] = labels
    best_k = max(scores, key=scores.get)
    labelled = frame.copy()
    labelled["cluster"] = labels_by_k[best_k]
    profile = labelled.groupby("cluster", as_index=False).agg(
        n_listings=("model_id", "size"),
        median_example_cost_usd=("example_cost_usd", "median"),
        median_context_tokens=("max_input_tokens", "median"),
        share_vision=("supports_vision", "mean"),
        share_reasoning=("supports_reasoning", "mean"),
    )
    return {"chosen_k": best_k, "silhouette_by_k": scores}, profile
