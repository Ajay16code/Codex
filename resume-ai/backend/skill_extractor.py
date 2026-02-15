from __future__ import annotations

import re

COMMON_SKILLS = {
    "python",
    "java",
    "javascript",
    "react",
    "fastapi",
    "docker",
    "kubernetes",
    "aws",
    "machine learning",
    "deep learning",
    "sql",
    "pandas",
    "numpy",
}


def extract_skills(text: str) -> list[str]:
    """Simple keyword-based skill extraction."""
    normalized = re.sub(r"\s+", " ", text.lower())
    found = [skill for skill in COMMON_SKILLS if skill in normalized]
    return sorted(found)
