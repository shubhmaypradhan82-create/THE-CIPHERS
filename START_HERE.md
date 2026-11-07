# The Ciphers — Integrated Version

## 1. Backend
Open PowerShell in `backend`:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Backend: http://127.0.0.1:8000
Docs: http://127.0.0.1:8000/docs

## 2. Frontend
Open a second PowerShell in `frontend`:

```powershell
npm install
npm run dev
```

Frontend: http://localhost:5173

## 3. What is connected
- Login/register/authentication
- Dashboard live summary and threat search
- Threats search + severity filter + email details
- Geolocation aggregation from stored IP results
- Forensic history and case details
- Cases/investigations create + close
- Reports listing + JSON export
- Settings profile name + notification preferences
- Email text analysis using bundled ML + forensic engine
- URL forensic analysis
- `.eml` forensic upload
- AI/ML status and results

## Important
Run the backend first, then the frontend. The backend creates the SQLite database automatically on first start.

## UI/forensic fixes included
- Cases navigation removed completely.
- System-wide timestamp display normalized to UTC-aware parsing in the frontend.
- Pasted email From/To/Subject headers are extracted instead of using a fake sender.
- Threat detail URLs and AI results are expandable.
- Forensic evidence is shown in structured sections with raw JSON kept under an advanced accordion.
- Geolocation now shows IP details and stored forensic infrastructure intelligence.
- Reports export the complete stored forensic payload instead of a summary shell.
- Threat search protects against stale asynchronous responses.
