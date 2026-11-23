# FlyCure implementation audit

## Scope and conclusion

This is a code-and-local-runtime baseline against the [Updated PRD](./FlyCure_Updated_PRD.md), with emphasis on P0 requirements and the Phase 0 exit criteria. It covers the current worktree and local Docker setup, not a deployed production environment, legal review, or formal security assessment.

**Conclusion: not ready for public production use.** The current repository supports a working local marketplace and patient report flow. Report ownership and file delivery are now enforced in the application and verified locally. Several other P0 privacy, provider-governance, demo-data, and production-hardening requirements remain open.

## Current-state matrix

| Capability / PRD areas | Status | Evidence and notes |
|---|---|---|
| Public hospital and doctor discovery (MKT-02–04) | Partial | Browse/detail views and active-record filters exist in [marketplace/views.py](../marketplace/views.py). When `DEBUG=False`, sample hospitals/doctors and listings tied to sample hospitals are excluded. There is still no provider approval or verification workflow. |
| WhatsApp enquiry (ENQ-01–02, ENQ-05) | Partial | Public templates use the configured number and non-sensitive starter messages. [marketplace/context_processors.py](../marketplace/context_processors.py) supplies a placeholder default, so a missing production value does not produce an approved alternative contact route. Operational ownership and response expectations are not represented in the application. |
| Patient accounts and profiles (ACC-01–03) | Partial | Registration, authentication, patient profiles, and role mixins exist. Account recovery and recorded privacy notice/consent are not implemented. |
| Report upload and ownership (REC-01–05) | Uploads disabled for limited-access MVP | `REPORT_UPLOADS_ENABLED` defaults to false. Upload links are hidden, the upload URL shows a limited-MVP notice, and non-GET submissions are rejected. Validation and ClamAV scanning remain available in code for a future configured deployment; retention, deletion, and access-event logging remain absent. Do not use this MVP for real patient reports. |
| Report-file authorization (REC-03–04) | Implemented and locally verified | Focused tests cover owner download, cross-patient denial, detail-page scoping, and lack of a public media route. A live probe against the MySQL-backed Docker app confirmed that the owner can download and another patient cannot. |
| Explanation stub and disclosure (AIR-01) | Implemented as a stub | The explanation service does not call an external model. A configured API key no longer changes the stub’s model label; a regression test verifies the output remains explicitly marked `local-stub`. The explanation feature is not production AI. |
| Provider verification and content governance (MKT-07–08, OPS-01–02) | Missing | There is no provider-verification record or review workflow. Hospital accreditation is editable through [care/forms.py](../care/forms.py) and [care/views.py](../care/views.py), without evidence review or approval history. |
| Demo marketplace data (MKT-08) | Mitigated; approval workflow remains open | Public queries now exclude sample hospitals/doctors and listings tied to sample hospitals when `DEBUG=False`; the seed command refuses to run in that mode, and Docker startup skips it. Existing production records must be explicitly marked non-sample to appear. A separate evidence-backed provider approval workflow is still missing. |
| Privacy operations (ACC-05, REC-06–07) | Missing | No application records for consent/privacy-notice versions, report access audit events, or report retention/deletion requests were found in the reviewed account and records code. |
| Production configuration (PRD 11.2, 16.3) | Partial; public release remains blocked | [config/settings.py](../config/settings.py) now supports Render PostgreSQL URLs, Render host/CSRF configuration, WhiteNoise static files, secure cookies, HTTPS redirects, HSTS, and rejects the development secret when `DEBUG=False`. Team-only access control, production operations, privacy controls, and deployment verification are still outstanding. |
| Care workflows and provider operations (OPS-03–06) | Partial | Availability, appointment-request, and provider-dashboard flows exist. The PRD requires explicit confirmation, operational ownership, source/timezone metadata, and quote lifecycle controls; these need further validation and completion before claims of confirmed appointments or operational service are made. |
| Automated quality coverage (PRD 16) | Partial | Focused tests cover report access, upload validation, AI-stub labeling, and production sample visibility. Other app test modules remain placeholders; the PRD’s broader role, enquiry, care-lifecycle, and operational test coverage is not present. |

## Changes verified in this worktree

- Report files are stored under `PRIVATE_MEDIA_ROOT`, outside public `MEDIA_URL`, with UUID-based storage paths. See [records/models.py](../records/models.py), [config/settings.py](../config/settings.py), and the storage migration [0002_alter_medicalreport_file.py](../records/migrations/0002_alter_medicalreport_file.py).
- The public media-serving route was removed. The authenticated report download view scopes the report to the signed-in patient and sends it as a private attachment. See [config/urls.py](../config/urls.py), [records/urls.py](../records/urls.py), and [records/views.py](../records/views.py).
- Docker now mounts a separate private-media volume. The report detail page links to the authorized download endpoint rather than a public media URL.
- AI output remains clearly identified as a local stub even if an API key is configured; no external model call has been implemented.
- Sample records are hidden from public marketplace queries and sample seeding is skipped when `DEBUG=False`.
- Report uploads enforce the documented PDF/JPEG/PNG/DOCX, 10 MB policy and reject mismatched extensions, MIME types, and signatures.
- Report upload is disabled by default for this limited-access MVP. The Docker default stack no longer starts a scanner service.
- The Docker entrypoint retains local MySQL development behavior and supports PostgreSQL `DATABASE_URL`, static collection, and Gunicorn for a Render deployment.
- Local test-only artifacts from the runtime access probe were deleted after verification.

## Remaining release blockers and decisions

1. **Upload safety:** Keep report uploads disabled for limited team review. Re-enabling requires a configured scanner deployment, signature-update monitoring, capacity/timeout planning, private storage, and safe document-processing controls.
2. **Provider approval:** The public read path now excludes sample records in production mode, but there is no separate approval state/evidence workflow; establish that before publishing real partner listings.
3. **Provider verification:** Define evidence, reviewer, expiry/recheck, and permitted public wording; prevent unreviewed accreditation or other trust claims from being presented as verified.
4. **Privacy operations:** Decide applicable consent and notice requirements, permitted staff access, report retention/deletion periods, backup behavior, and audit-log policy; then implement and test the approved workflows.
5. **Production deployment configuration:** Select hosting and storage, use fail-closed production settings and managed secrets, configure HTTPS/cookie protections and monitoring, and test backups/restores.
6. **AI scope:** Keep explanations explicitly deferred/stubbed until the PRD’s clinical, privacy, security, extraction, evaluation, and rollback gates are satisfied. An API key alone must not enable or imply real analysis.
7. **Broader test coverage:** Add the PRD-required permission, validation, listing-visibility, account, and care-workflow tests.
8. **Open decisions:** Product launch markets, provider onboarding standard, staff report access, retention, AI launch scope/vendor, production database, hosting/storage, background processing, and production scanner operations remain unresolved in PRD Section 19. The current report upload format/size policy is PDF/JPEG/PNG/DOCX up to 10 MB per file.

## Validation evidence

- `python manage.py check` in Docker: passed.
- `python manage.py makemigrations --check --dry-run` in Docker: no changes detected after adding the storage migration.
- `python manage.py test` using the supported SQLite fallback: 19 tests passed, including disabled-upload route/UI behavior, report authorization/upload validation/scanner failure handling, AI-stub labeling, production sample visibility, and seed-command guards.
- MySQL-backed local runtime probe: owner download succeeded; public media URL and another patient’s download were denied.
- Local homepage returned HTTP 200; MySQL and web containers were running, with MySQL healthy.
- `git diff --check`: passed.

The Docker MySQL application account cannot create Django’s test database, so the automated test suite was run against SQLite rather than claiming MySQL test-suite coverage. The storage migration was applied to the local MySQL database and the report authorization probe ran against that database. Production-database migration and deployment testing remain outstanding.
