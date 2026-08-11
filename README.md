# FlyCure (Django)

WhatsApp-first medical tourism marketplace for international patients comparing hospitals, doctors, and treatment packages in India — with private patient report uploads and AI draft explanations.

## Stack

- **Django 6** — auth, admin, ORM, templates
- **SQLite** (dev) — swap to Postgres for production
- **Pillow** — image support for uploads
- Apps: `marketplace`, `providers`, `accounts`, `records`, `ai_reports`

## Quick start

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
| Report dashboard / upload | `/records/`, `/records/upload/` |
| AI explanation detail | `/records/<id>/` |
| Django admin | `/admin/` |

## AI report explanations

Uploading a report creates a `MedicalReport` and immediately runs `ai_reports.services.queue_report_explanation`.

- Without `OPENAI_API_KEY`, a **local stub** explanation is generated so the patient flow works offline.
- With an API key set in `.env`, the same service is the hook point for a real LLM call (PDF/OCR parsing still to be wired).

## Environment

See `.env.example`:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `WHATSAPP_NUMBER`
- `OPENAI_API_KEY` (optional)
- `AI_REPORT_MODEL`

## Notes

- Sample hospitals/doctors from `seed_marketplace` are fictional demo data.
- Medical report files are stored under `media/records/` and are only listed for the owning patient.
- Treat health data carefully before production: private object storage, HTTPS, audit logs, retention policy.
