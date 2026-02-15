# AI Candidate Intelligence Engine

Production-oriented starter for resume-to-job matching with notebook training, FastAPI inference, React dashboard, and Dockerized deployment.

## Structure

- `notebooks/`: model training notebook
- `data/`: sample dataset
- `models/`: exported model artifacts
- `backend/`: FastAPI inference service
- `frontend/`: React + Tailwind dashboard
- `docker-compose.yml`: local multi-service startup

## Quickstart

1. Train and export model from notebook to `models/resume_classifier.pkl`.
2. Start stack:

```bash
docker-compose up --build
```

3. Open frontend at `http://localhost:3000`.

## API

### POST `/analyze`

Form-data:
- `resume`: PDF file
- `job_description`: text

Response:

```json
{
  "prediction": "Fit",
  "confidence_score": 0.93,
  "similarity_score": 0.81,
  "resume_skills": ["python"],
  "job_skills": ["python", "machine learning"]
}
```
