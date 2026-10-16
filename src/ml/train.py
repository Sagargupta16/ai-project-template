from __future__ import annotations

import logging
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from src.core.config import Settings, get_settings

logger = logging.getLogger(__name__)


def train_model(
    df: pd.DataFrame,
    target_column: str = "target",
    settings: Settings | None = None,
):
    """Train a model on the given data. Returns the trained model."""
    settings = settings or get_settings()
    logger.info("Training model on %d samples", len(df))

    X = df.drop(columns=[target_column])
    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=settings.ml.test_size, random_state=settings.ml.random_seed
    )

    model = RandomForestClassifier(
        min_samples_leaf=settings.ml.min_samples_leaf,
        max_features=settings.ml.max_features,
        random_state=settings.ml.random_seed,
    )
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    logger.info("Test accuracy: %.4f", score)

    return model


def save_model(model, path: Path | str) -> None:
    """Save a trained model to disk."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    logger.info("Model saved to %s", path)
