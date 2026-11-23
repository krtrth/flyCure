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
