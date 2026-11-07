# The Ciphers — Integrated AI Email Threat Detection & Forensic Intelligence

This package combines the React/Vite UI, FastAPI authentication/database/API, and the supplied forensic-engine implementation in one backend process.

## Architecture
React UI → FastAPI → integrated forensic engine → AI adapter → SQLite/PostgreSQL → JSON results

The forensic engine is imported in-process; the old Flask server is not required. The original forensic modules (URL, DNS, IP, redirects, HTTP, TLS, IOC, threat intelligence, correlation, risk, case and timeline) are preserved.

## Backend
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend
```powershell
cd frontend
npm install
npm run dev
```

Open http://127.0.0.1:5173. Register once, then sign in.

## Important endpoints
- `POST /auth/register` — create analyst
- `POST /auth/login` / `GET /auth/me` — authentication
- `POST /analyze` — text/email-content analysis with forensic URL enrichment
- `POST /forensics/url` — complete forensic URL pipeline
- `POST /forensics/email` — complete `.eml` forensic pipeline
- `GET /forensics` — stored forensic history
- `GET /docs` — API documentation

Optional external services can still be enabled with `CYBER_ENGINE_URL`, `AI_API_URL`, and their API keys. Without them, the integrated forensic engine and local AI fallback work locally.


## Bundled local ML integration

The supplied `EmailThreatAI_FINAL.zip` pipeline is integrated in-process.
The trained TF-IDF + calibrated Linear SVM model is stored at
`backend/app/ml/calibrated_svm.pkl` and loaded by FastAPI. No second AI server
is required.

- `POST /analyze` runs the local ML model plus the forensic engine.
- `POST /ai/analyze` runs the local ML model directly.
- `GET /ai/status` reports model availability (requires login).
- Uploaded `.eml` files through `POST /forensics/email` also receive `ai` results.
- `backend/app/ml/train.py` retrains the bundled model if the dataset changes.
