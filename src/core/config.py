from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MLSettings(BaseSettings):
    random_seed: int = 42
    test_size: float = 0.2
    # RandomForestClassifier hyperparameters, defaulting to scikit-learn's own defaults.
    min_samples_leaf: int | float = 1
    max_features: Literal["sqrt", "log2"] | int | float | None = "sqrt"

    model_config = SettingsConfigDict(env_prefix="ML_")


class LLMSettings(BaseSettings):
    provider: str = "anthropic"
    model: str = "claude-sonnet-4-6"
    max_tokens: int = 4096
    temperature: float = 0.2
    api_key: str | None = None

    model_config = SettingsConfigDict(env_prefix="LLM_")


class RAGSettings(BaseSettings):
    embedding_model: str = "text-embedding-3-small"
    chunk_size: int = 1000
    chunk_overlap: int = 100
    top_k: int = 5
    vector_store: str = "chroma"

    model_config = SettingsConfigDict(env_prefix="RAG_")


class ObservabilitySettings(BaseSettings):
    tracing_enabled: bool = False
    tracing_backend: str = "phoenix"
    cost_tracking: bool = True

    model_config = SettingsConfigDict(env_prefix="OBS_")


class Settings(BaseSettings):
    """Root settings. Loads from .env and environment variables."""

    project_root: Path = Path(__file__).resolve().parents[2]
    env: str = "dev"
    log_level: str = "INFO"

    ml: MLSettings = Field(default_factory=MLSettings)
    llm: LLMSettings = Field(default_factory=LLMSettings)
    rag: RAGSettings = Field(default_factory=RAGSettings)
    observability: ObservabilitySettings = Field(default_factory=ObservabilitySettings)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    @property
    def data_dir(self) -> Path:
        return self.project_root / "data"

    @property
    def raw_data_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def interim_data_dir(self) -> Path:
        return self.data_dir / "interim"

    @property
    def processed_data_dir(self) -> Path:
        return self.data_dir / "processed"

    @property
    def external_data_dir(self) -> Path:
        return self.data_dir / "external"

    @property
    def models_dir(self) -> Path:
        return self.project_root / "models"

    @property
    def reports_dir(self) -> Path:
        return self.project_root / "reports"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
