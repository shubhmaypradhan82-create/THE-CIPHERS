# Integrated Backend

The backend is now a single FastAPI service. The supplied forensic engine has been moved into `app/modules`, `app/utils`, and `app/correlation` and is called directly by `app/forensic_service.py`.

## Run

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Main API

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`
- `POST /analyze`
- `POST /forensics/url`
- `POST /forensics/email` (`multipart/form-data`, field `file`, `.eml` only)
- `GET /forensics`
- `GET /emails`
- `GET /ai-results`
- `GET /docs`

No second Flask server is required.

## Network safety

The forensic modules perform DNS/HTTP/TLS lookups. Conservative defaults are configured in `.env.example` so an unreachable target does not block the application indefinitely. Live RDAP/IP intelligence is opt-in with `FORENSIC_IP_INTEL=true`.
