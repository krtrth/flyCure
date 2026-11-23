# FlyCure (Django)

WhatsApp-first medical tourism marketplace for international patients comparing hospitals, doctors, and treatment packages in India — with private patient report uploads and AI draft explanations.

## Stack

- **Django 6** — auth, admin, ORM, templates
- **SQLite** (dev) — swap to Postgres for production
- **Pillow** — image support for uploads
- Apps: `marketplace`, `providers`, `accounts`, `records`, `ai_reports`

## Docker (recommended)

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/).
Report uploads are disabled by default for this limited-access MVP. Do not use the app to store real patient reports or other sensitive health information.

```bash
cp .env.example .env
docker compose up --build
```

| Service | URL |
| --- | --- |
| FlyCure home | http://localhost:8000/ |
| Patient login | http://localhost:8000/accounts/login/ (`patient` / `patient`) |
| Doctor / hospital login | http://localhost:8000/accounts/provider/login/ (`doctor` / `doctor`, `hospital` / `hospital`) |
| Django admin | http://localhost:8000/admin/ (`admin` / `admin`) |
| phpMyAdmin | http://localhost:8080/ (user `flycure` / `flycure`, or `root` / `root`) |

MySQL is available at `localhost:3306` (database `flycure`).

## Render deployment (Docker)

The Docker image supports both the local MySQL Compose setup and a Render PostgreSQL `DATABASE_URL`.
For a limited team demo:

1. Push the project to GitHub without `.env` (it is ignored).
2. In Render, create a PostgreSQL database and a Docker web service from this repository, in the same region.
3. Set the web service's `DATABASE_URL` to the database's **internal** connection URL.
4. Add `DJANGO_SECRET_KEY` using Render's Generate option, and set `DJANGO_DEBUG=False` and `REPORT_UPLOADS_ENABLED=False`.
5. Deploy with the Dockerfile defaults; the container runs migrations, collects static files, and starts Gunicorn.
6. Create an admin user from the Render Shell with `python manage.py createsuperuser`.

The app automatically allows `RENDER_EXTERNAL_HOSTNAME` and trusts its HTTPS origin for CSRF. Do not copy `.env` into Render. Free database availability, lifetime, storage, and web-service sleep behavior can change; check Render's current free-tier limits and export data you need to keep. This app is not approved for real patient information, and a Render URL is public unless you add an access-control layer.

## Local Python (SQLite)

Leave `MYSQL_HOST` unset in `.env` to use SQLite.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_marketplace
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

## What is included

| Area | Routes |
|------|--------|
| Marketplace home + filters | `/` |
| Hospital search / detail | `/hospitals/`, `/hospitals/<slug>/` |
| Doctor search / detail | `/doctors/`, `/doctors/<slug>/` |
| Patient register / login | `/accounts/register/`, `/accounts/login/` |
| Report dashboard | `/records/` |
| AI explanation detail | `/records/<id>/` |
| Django admin | `/admin/` |

## AI report explanations

Uploading a report creates a `MedicalReport` and immediately runs `ai_reports.services.queue_report_explanation`.

- Without `OPENAI_API_KEY`, a **local stub** explanation is generated so the patient flow works offline.
- Setting `OPENAI_API_KEY` does not enable a real LLM call; the current service always returns a clearly labelled local stub. PDF/OCR parsing and model integration remain future work.

## Environment

See `.env.example`:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DATABASE_URL` (PostgreSQL connection URL for Render; keep it secret)
- `WHATSAPP_NUMBER`
- `OPENAI_API_KEY` (optional)
- `AI_REPORT_MODEL`
- `MAX_REPORT_UPLOAD_SIZE_MB` (default: `10`)
- `REPORT_UPLOADS_ENABLED` (default: `False`; Docker Compose forces `False`)
- `CLAMAV_HOST` and `CLAMAV_PORT` (scanner configuration required only if uploads are explicitly re-enabled outside the default Compose setup)

## Notes

- Sample hospitals/doctors from `seed_marketplace` are fictional demo data. They are only seeded with `DEBUG=True`, and public marketplace pages exclude sample hospitals/doctors and listings tied to sample hospitals when `DEBUG=False`. Production provider records must be explicitly marked non-sample before they are visible.
- When report uploads are enabled, accepted formats are PDF, JPEG, PNG, or DOCX up to `MAX_REPORT_UPLOAD_SIZE_MB` (10 MB by default), with extension, declared MIME type, and file-signature checks.
- Report uploads are disabled by default via `REPORT_UPLOADS_ENABLED=False`, and Docker Compose forces them off. Keep them disabled for team review; re-enabling requires a configured malware scanner and an approved private-storage setup.
- Medical report files use a separate private storage volume and an authenticated, owner-checked download route. The local Docker setup is for non-sensitive demo data only; it is not a production health-data environment.
- Treat health data carefully before production: private object storage, HTTPS, audit logs, retention policy.
