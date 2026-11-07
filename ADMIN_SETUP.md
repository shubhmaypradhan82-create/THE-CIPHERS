# CHIPERS administrator setup

## Preset administrator

The included demo administrator is:

- **Admin email:** `admin@chipers.in`
- **Admin password:** `CHIPERS@Admin2026!`

Use **Admin Login** on the login screen. The email uses a normal valid domain because the email validator rejects special-use `.local` addresses.

## Start

1. In `backend`, create/activate a Python environment if desired and run:
   `python -m pip install -r requirements.txt`
2. Start the backend:
   `python -m uvicorn app.main:app --reload`
3. In a second terminal, enter `frontend` and run:
   `npm install`
   `npm run dev`
4. Open the Vite URL, normally `http://localhost:5173`.
5. Choose **Admin Login** and use the preset credentials above.

The backend bootstraps/repairs the preset administrator on startup, so an old or missing admin row will not prevent login.

## Login persistence

The frontend stores the Basic-auth credential in browser storage so a page refresh/browser restart can restore the signed-in state. Logging out clears both local and session storage.

## User accounts and IP/city

The Admin Console shows all accounts, latest login IP, last seen time, login count, active/banned status, and audit history. At login, the browser attempts to obtain its public IP from a public IP service and sends that value to the backend. The backend then performs approximate public-IP geolocation (country/city/region/ISP).

On a local-only connection where the browser cannot obtain a public IP, the server may record `127.0.0.1` or `::1`; those addresses have no geographic location. IP geolocation is approximate network/ISP location, not an exact physical address.

## Admin actions

The Admin Console provides:
- Ban / Unban analyst accounts
- Reset analyst passwords
- Remove analyst accounts
- View login/audit history and IPs
- View approximate country/city/ISP for public IPs

Do not expose the admin interface publicly without HTTPS and appropriate access controls.
