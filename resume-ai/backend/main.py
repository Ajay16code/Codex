from __future__ import annotations

import fitz
import numpy as np
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from sentence_transformers import SentenceTransformer

from model_loader import load_classifier
from ranking_engine import build_feature_vector, cosine_similarity_score
from skill_extractor import extract_skills

app = FastAPI(title="AI Candidate Intelligence Engine", version="1.0.0")


@app.on_event("startup")
def startup_event() -> None:
    app.state.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    app.state.classifier = load_classifier()


def _extract_pdf_text(file_bytes: bytes) -> str:
    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            return "\n".join(page.get_text("text") for page in doc).strip()
    except Exception as exc:  # pragma: no cover - parser edge-cases
        raise HTTPException(status_code=400, detail="Invalid PDF file.") from exc


def _predict(resume_text: str, job_description: str) -> dict:
    model = app.state.embedding_model
    classifier = app.state.classifier

    resume_embedding = model.encode(resume_text)
    job_embedding = model.encode(job_description)

    features = build_feature_vector(
        np.array(resume_embedding), np.array(job_embedding)
    )

    prediction = int(classifier.predict(features)[0])

    if hasattr(classifier, "predict_proba"):
        confidence = float(classifier.predict_proba(features)[0][prediction])
    else:
        confidence = 0.0

    similarity = cosine_similarity_score(
        np.array(resume_embedding), np.array(job_embedding)
    )

    return {
        "prediction": "Fit" if prediction == 1 else "Not Fit",
        "confidence_score": confidence,
        "similarity_score": similarity,
        "resume_skills": extract_skills(resume_text),
        "job_skills": extract_skills(job_description),
    }


@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
) -> dict:
    if resume.content_type not in {"application/pdf", "application/octet-stream"}:
        raise HTTPException(status_code=400, detail="Upload a PDF file.")

    resume_text = _extract_pdf_text(await resume.read())
    if not resume_text:
        raise HTTPException(status_code=400, detail="No extractable text found in PDF.")

    return _predict(resume_text=resume_text, job_description=job_description)
