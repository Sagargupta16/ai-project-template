from __future__ import annotations

import logging
from dataclasses import dataclass

from src.core.config import get_settings

logger = logging.getLogger(__name__)


@dataclass
class Chunk:
    text: str
    metadata: dict


def chunk_text(text: str, chunk_size: int | None = None, overlap: int | None = None) -> list[Chunk]:
    """Split text into overlapping chunks. Replace with a semantic splitter for production."""
    settings = get_settings()
    size = chunk_size or settings.rag.chunk_size
    overlap = settings.rag.chunk_overlap if overlap is None else overlap
    step = size - overlap

    chunks: list[Chunk] = []
    for i in range(0, len(text), step):
        piece = text[i : i + size]
        if piece:
            chunks.append(Chunk(text=piece, metadata={"start": i}))
    logger.info("Split %d chars into %d chunks", len(text), len(chunks))
    return chunks
