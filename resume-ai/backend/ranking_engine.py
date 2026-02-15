from __future__ import annotations

import numpy as np


def cosine_similarity_score(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """Compute cosine similarity for two embedding vectors."""
    denom = np.linalg.norm(vec_a) * np.linalg.norm(vec_b)
    if denom == 0:
        return 0.0
    return float(np.dot(vec_a, vec_b) / denom)


def build_feature_vector(resume_embedding: np.ndarray, job_embedding: np.ndarray) -> np.ndarray:
    """Build classifier feature vector by concatenating two embeddings."""
    return np.concatenate([resume_embedding, job_embedding]).reshape(1, -1)
