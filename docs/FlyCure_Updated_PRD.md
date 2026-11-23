# FlyCure — Product Requirements Document (PRD)

**Document status:** Draft for product and engineering review (updated after BRD reconciliation)  
**Product:** FlyCure  
**Platform:** Responsive web application (Django, server-rendered)  
**Primary market:** International patients considering treatment in India  
**Primary conversion:** WhatsApp conversation with a FlyCure care coordinator  
**Last updated:** 30 October 2026
**Revision:** 2 — reconciles the existing marketplace PRD with the broader Flycure Health BRD; native app and telemedicine expansion deferred.

---

## 1. Executive summary

FlyCure is a WhatsApp-first medical-tourism marketplace that helps international patients and their family decision-makers explore treatment options in India. Patients can discover and compare hospitals, doctors, and treatment packages; share medical reports privately; review informational explanations of uploaded reports; and connect with a care coordinator to discuss next steps.

The intended experience combines the clarity and comparison tools of a premium healthcare marketplace with the reassurance and continuity of a personal medical concierge. The marketplace supports informed exploration; it does not independently diagnose patients, guarantee treatment suitability, publish unverified outcomes, or promise fixed treatment prices.

The current product is a Django application with public marketplace pages, patient accounts, report upload and dashboard flows, provider-management functionality, and care-related workflows. Some areas described in the broader product vision are proposed or partially implemented and must not be represented as shipped until verified in the running application.

This PRD establishes:
- The product goals, users, scope, and measurable outcomes.
- The distinction between current implementation and proposed capabilities.
- Functional requirements and acceptance criteria.
- Clinical-safety, privacy, security, and operational requirements.
- A phased delivery plan and decisions required before production launch.

## 1.1 Strategic scope reconciliation — BRD reviewed

A separate 19-page document titled **Business Requirements Document: Flycure Health Digital Platform** was reviewed while updating this PRD. It describes a broader healthcare platform with a website and mobile application, virtual consultations, centralized EHR, digital prescriptions, pharmacy workflows, remote patient monitoring, payments, insurance verification, and future corporate wellness partnerships.

That BRD is retained as strategic input, but it does **not** replace the current product definition. The immediate product remains the international medical-tourism marketplace described in this PRD and in the supplied FlyCure repository context.

### Current product direction

**Build now:** a responsive, server-rendered web marketplace for international patients considering treatment in India, supported by private patient report handling and a human, WhatsApp-first care-coordination journey.

**Defer:** the native mobile application and the broader domestic telemedicine platform. This includes full virtual consultations, a comprehensive longitudinal EHR, e-prescribing, pharmacy fulfilment, insurance eligibility integrations, remote patient monitoring/wearables, and corporate wellness products. These belong in a separately validated future product phase and must not expand the current MVP by implication.

### Scope reconciliation matrix

| Capability in the broader BRD | Decision for this PRD | Clarification |
|---|---|---|
| Responsive website | **In current scope** | Continue the existing Django web application and marketplace. |
| International patient discovery of Indian hospitals/doctors/treatment options | **In current scope** | This is the primary marketplace proposition. |
| WhatsApp-led care coordination | **In current scope** | Primary conversion and human handoff. |
| Private report upload and report dashboard | **In current scope** | Preserve patient ownership and privacy controls. |
| Informational AI report explanation | **Limited / future production integration** | Current implementation is a deterministic local stub. Real interpretation remains gated by clinical, privacy, and security review. |
| Appointment request / provider availability | **Limited current care workflow; verify implementation** | A request or availability display is not a confirmed telemedicine booking. Human/provider confirmation is required. |
| Full self-serve appointment booking and automated reminders | **Deferred** | Future telemedicine/product expansion. |
| Secure video/audio consultation | **Deferred** | Not part of the current marketplace MVP. Requires vendor, clinical, privacy, and operational decisions. |
| Asynchronous clinical messaging/live chat | **Deferred** | WhatsApp coordination does not automatically constitute a clinical messaging service. |
| Comprehensive EHR shared across multiple RMPs | **Deferred** | Current patient reports/profile are not a full EHR. |
| Digital prescriptions and medication lists | **Deferred** | Requires a separately approved clinical and regulatory workflow. |
| Pharmacy search, stock availability, fulfilment and refills | **Deferred** | Not part of the current medical-tourism marketplace. |
| Remote patient monitoring and wearable integration | **Deferred** | Future product line; no current device integration is implied. |
| Integrated consultation payment gateway | **Deferred / business decision required** | Do not introduce consumer teleconsultation billing into the current enquiry/quotation model without an explicit decision. |
| Insurance eligibility and claims assistance | **Deferred** | Any future coverage result must be sourced, qualified, and not represented as a guarantee of reimbursement. |
| RMP social network / provider collaboration | **Deferred** | Not required for the current marketplace. |
| AI symptom chatbot or clinical decision support | **Out of current scope** | No diagnosis, triage, or treatment recommendation capability is authorized by this PRD. |
| Corporate wellness B2B partnerships | **Long-term strategic option** | Requires a distinct buyer, service, commercial model, and implementation plan. |
| Data licensing | **Excluded pending a separate decision and legal review** | Patient health data must not be treated as a monetizable asset. No secondary use is authorized by this PRD. |
| Native Android/iOS application | **Deferred** | Current delivery is the responsive web application. Mobile app discovery and requirements will be a separate update. |

### Important business-model distinction

The BRD proposes a domestic B2C telehealth model with per-visit fees and subscriptions, followed by corporate wellness partnerships. The current PRD describes an international patient acquisition and coordination model in which treatment enquiries and custom quotations are handled with providers and care coordinators.

These models must not be blended by assumption. The current release should not introduce subscription plans, consultation fees, insurance billing, or corporate wellness packages unless the product owner explicitly approves a revised business model.

### Source and decision discipline

- The BRD's market statistics, competitor assessments, revenue projections, and statements about legal or insurance requirements are source-document claims, not independently validated facts in this PRD.
- Its references to the Telemedicine Practice Guidelines, DPDP Act, IT/SPDI rules, IRDAI coverage, and HIPAA are prompts for qualified legal/compliance review, not a legal determination that a proposed feature is compliant.
- Any future telemedicine release requires a fresh clinical, legal, privacy, security, and operational requirements exercise against the rules in force at that time.
- The BRD recommends microservices, while the current implementation is a Django server-rendered application. This PRD retains the modular Django monolith as the near-term architecture; a move to microservices is not justified without demonstrated scaling or organizational needs.
- The broader BRD's proposed 99.9% uptime, encryption algorithms, and other technical targets are not silently adopted as current service commitments. Production SLOs and controls must be selected, threat-modelled, and verified for the actual deployment.

### Product boundary after this update

FlyCure's current web product helps international patients discover and compare Indian care providers, share relevant reports privately, and coordinate next steps with a human team. It is not currently a domestic telemedicine super-app, a virtual clinic, an insurance administrator, an online pharmacy, or a replacement for a provider's EHR.

## 2. Product vision and positioning

### 2.1 Vision

Make it easier and safer for international patients to explore appropriate medical-care options in India, understand what information they need to share, compare providers using trustworthy information, and reach a human care coordinator without navigating a fragmented process alone.

### 2.2 Positioning

FlyCure is a **medical-tourism discovery and coordination service**, not a hospital, medical provider, emergency service, or substitute for professional medical advice.

The experience should feel:
- **Trustworthy:** clear provider identity, transparent data provenance, and visible verification status.
- **Human:** easy access to a real care coordinator, primarily through WhatsApp.
- **Understandable:** plain-language explanations and practical comparison criteria.
- **Respectful:** careful handling of sensitive health information and patient consent.
- **Realistic:** no unsupported claims about outcomes, prices, credentials, availability, or travel arrangements.

### 2.3 Product principles

1. **Human coordination over automated conversion.** Digital flows should help a patient reach an informed conversation, not force a self-serve purchase.
2. **Evidence before claims.** Provider credentials, accreditations, outcomes, pricing, and service commitments require documented sources and review.
3. **Privacy by default.** Medical reports and patient-specific information must never be exposed through public pages or another patient's account.
4. **Clinical boundaries.** AI-generated explanations are informational drafts, not diagnoses, treatment recommendations, or emergency guidance.
5. **Progressive disclosure.** Ask for sensitive information only when it is necessary for the next step.
6. **Honest implementation status.** Demo data and unfinished integrations must be clearly identified internally and excluded from production claims.

## 3. Goals, non-goals, and success measures

### 3.1 Product goals

- Help international patients discover relevant hospitals, doctors, specialties, and treatment options in India.
- Make provider comparison practical and understandable.
- Convert qualified marketplace interest into a WhatsApp conversation or another approved coordinator contact route.
- Let registered patients securely upload and revisit their medical reports.
- Provide carefully bounded, understandable draft explanations of reports, with clear limitations and escalation to a qualified clinician.
- Give authorized providers and internal operators tools to maintain accurate marketplace and care information.
- Establish a production-ready foundation for privacy, security, auditability, and operational support.

### 3.2 Non-goals for the initial release

- Diagnosing a condition or recommending a definitive treatment.
- Replacing a doctor, hospital consultation, second opinion, or emergency service.
- Automatically determining patient eligibility for a procedure.
- Guaranteeing clinical outcomes, recovery times, treatment costs, appointment availability, visas, flights, accommodation, or other travel services.
- Processing payments, booking flights, or completing end-to-end treatment purchases unless separately scoped.
- Offering a real-time hospital EHR integration unless a specific partner integration is approved.
- Treating an LLM report explanation as a medical interpretation or a verified clinical record.
- Launching a native mobile application; the initial product is a responsive web application.

### 3.3 Success metrics

Instrument these metrics before setting numerical targets. Targets should be agreed after a baseline period and operational capacity review.

| Area | Metric | Definition |
|---|---|---|
| Discovery | Search-to-detail rate | Marketplace searches that lead to a hospital or doctor detail view |
| Discovery | Comparison engagement | Users who inspect multiple provider or treatment options in one journey |
| Conversion | WhatsApp click-through rate | Eligible marketplace sessions that click a WhatsApp contact link |
| Conversion | Qualified enquiry rate | Enquiries accepted by the care team as having sufficient information for follow-up |
| Conversion | Enquiry response time | Time from enquiry receipt to first human response; report actual performance, do not promise an SLA until staffed |
| Patient account | Registration completion | Registration starts that result in an active patient account |
| Records | Upload completion rate | Valid report upload attempts that are successfully stored and linked to the owner |
| Records | Report access integrity | Unauthorized report access attempts blocked; target is 100% |
| AI | Explanation availability | Eligible report jobs that reach a completed or clearly failed state |
| AI safety | Unsafe-claim rate | Sampled explanations containing unsupported diagnosis, treatment instruction, or fabricated values |
| Provider operations | Profile completeness | Active provider profiles meeting the required data-completeness standard |
| Trust | Verification coverage | Active listings with current, documented verification for each claim labelled verified |
| Reliability | Application availability and error rate | Standard production monitoring measures |

Do not optimize for report uploads or AI usage at the expense of patient consent, clinical safety, or data minimization.

## 4. Target users and jobs to be done

### 4.1 Primary personas

**A. International patient**

- Lives outside India and is exploring treatment in India.
- Needs to understand available hospitals, doctors, treatment pathways, and likely next steps.
- May have reports from a local doctor or hospital.
- Wants a clear way to ask questions and speak to a human coordinator.
- May face language, time-zone, travel, and unfamiliar-health-system barriers.

**B. Family decision-maker or caregiver**

- Researches options on behalf of a patient.
- Needs information that can be shared and discussed with the patient.
- May coordinate documents, travel questions, and communication.
- Must not automatically receive access to a patient's private reports merely because they are a family member.

**C. Hospital or doctor representative**

- Needs to maintain accurate profile, specialty, service, package, and availability information.
- Should only manage records and enquiries they are authorized to access.
- Must not be able to view unrelated patients' private reports or accounts.

**D. FlyCure care coordinator / operations administrator**

- Receives enquiries and helps patients understand the next steps.
- Coordinates provider communication and, where separately agreed, quotation or appointment requests.
- Needs a reliable view of enquiry status and consented patient-provided information.
- Must follow documented access, communication, and escalation procedures.

### 4.2 Core jobs to be done

- “Help me find credible hospitals and doctors in India for the care I am exploring.”
- “Help me compare options without making me interpret dozens of disconnected websites.”
- “Let me share my reports privately so a coordinator or clinician can review them through an agreed process.”
- “Explain unfamiliar report terminology in plain language without pretending to diagnose me.”
- “Help me reach a real person who can explain what happens next.”
- “Help me understand which details are confirmed and which still need provider confirmation.”

## 5. Product scope and implementation status

The table below reflects the supplied project context and README. It is not a substitute for code-level verification. Before treating any item as production-ready, validate its views, permissions, tests, templates, and runtime behavior.

| Capability | Current status from supplied context | PRD treatment |
|---|---|---|
| Django server-rendered application | Implemented | Preserve current architecture for initial delivery |
| Marketplace home and search/filter entry point | Implemented | Improve usability, accessibility, and analytics |
| Hospital list and detail pages | Implemented | Improve comparison and trust metadata |
| Doctor list and detail pages | Implemented | Improve specialty and affiliation information |
| Patient registration and login | Implemented | Harden authentication and account lifecycle |
| Patient profile | Present in broader project context | Verify fields, validation, and consent behavior |
| Report upload and patient dashboard/detail | Implemented in code; disabled by default for the limited-access MVP | Keep uploads disabled until scanner, private storage, and privacy operations are approved |
| AI report explanation | Deterministic local stub | Keep clearly labelled as demo/informational until safe production integration |
| PDF/OCR extraction | Not implemented / future work | Separate future capability with explicit safety and validation |
| Real external LLM call | Not implemented; API key is only a future hook point | Future phase; never imply key presence means model integration works |
| Procedure history and suggested tests | Present in broader project context | Verify implementation and clinical ownership before release |
| Appointment requests and doctor availability | Present in broader project context | Verify workflow, source of availability, and provider confirmation |
| Doctor/hospital dashboards and provider CRUD | Present in broader project context | Verify role-based authorization and tenant boundaries |
| WhatsApp-first enquiry conversion | Intended primary conversion; configuration includes `WHATSAPP_NUMBER` | Verify link generation, message content, consent, and operational handling |
| Treatment quotations | Intended to be coordinated, not guaranteed fixed prices | Future workflow with clear validity and confirmation rules |
| Travel and post-treatment support | Part of broader design direction | Future scope; only advertise services actually staffed and contracted |
| Seed marketplace content | Fictional demo data | Must be replaced or clearly marked before public launch |

### 5.1 Source-of-truth rule

The running code, Django settings, URL configuration, models, migrations, tests, and actual deployed configuration determine what is implemented. Product research and wireframes describe intent, not proof of implementation. The README describes setup and a subset of routes, not the complete product.

## 6. User journeys

### 6.1 Anonymous discovery to WhatsApp enquiry

1. Patient lands on the FlyCure homepage.
2. Patient explores specialties, hospitals, doctors, or treatment categories.
3. Patient applies available filters and opens a detail page.
4. Patient reviews provider information, location, specialties, services, and verification labels.
5. Patient selects the WhatsApp contact action.
6. FlyCure opens the configured WhatsApp destination with a concise, non-sensitive starter message.
7. Patient chooses what to send. The care team handles the enquiry through its approved process.

**Requirements**
- The WhatsApp CTA must work on supported mobile and desktop environments.
- Do not put medical reports, diagnoses, phone numbers, or other sensitive data into a prefilled URL message.
- Do not claim that a coordinator is available 24/7 or will respond within a specific time unless the service is staffed and the claim is approved.
- Preserve the page or provider context in a non-sensitive reference where operationally useful.
- If WhatsApp is unavailable, provide an approved alternative contact route.

### 6.2 Patient registration and profile

1. Patient opens registration.
2. Patient provides only required account information.
3. Application validates the input and creates the account.
4. Patient signs in and views their profile.
5. Patient can update permitted profile details and understand how their information is used.

**Requirements**
- Explain why each required field is collected.
- Use secure password handling and standard Django authentication protections.
- Avoid collecting passport, identity, or detailed medical information unless a defined workflow requires it.
- Provide account recovery and account deactivation/deletion request processes appropriate to applicable law and operational needs.

### 6.3 Medical report upload and access

Report upload is currently disabled by default for the limited-access MVP. Do not collect real patient reports until the selected hosting platform, private storage, malware scanning, retention, and access policies have been reviewed. The workflow below describes the future enabled capability.

1. Authenticated patient opens the report area.
2. Patient sees an explanation of accepted file types, size limits, purpose, and privacy handling.
3. Patient selects a file and submits it.
4. Server validates the file and stores it in private storage.
5. A `MedicalReport` record is associated with the authenticated patient.
6. Patient sees upload status and can open the report detail page.
7. Only the owner and specifically authorized personnel can access the report under an auditable permission policy.

**Requirements**
- Enforce ownership on every list, detail, download, preview, and derived-artifact endpoint.
- Never trust a report ID supplied by the browser as proof of ownership.
- Validate file size, extension, MIME type, and file signature where feasible.
- Generate safe server-side storage names; do not use the original filename as a storage path.
- Reject executable and unsupported formats.
- Serve private files through an authorization-checked handler or short-lived signed URL, not a public media URL.
- Record upload, view, download, deletion, and privileged access events.
- Apply malware scanning and safe document processing before production. The local Docker workflow currently scans uploads with ClamAV; production scanner operations still require review.
- Define retention, deletion, backup, and legal-hold behavior before launch.

### 6.4 Report explanation

1. A report upload creates a report record.
2. The explanation service creates a job or records a clear processing state.
3. In development, the deterministic local stub may produce demo output.
4. In a future production integration, validated text extraction and an approved model may generate a draft explanation.
5. Patient sees the explanation with a prominent informational disclaimer, source limitations, and an instruction to discuss results with a qualified clinician.
6. Failures are shown as failures; the system must not silently substitute fabricated content.

**Requirements**
- Clearly distinguish `demo`, `processing`, `completed`, and `failed` states.
- Label stub output as demo/sample content; never present it as analysis of the uploaded report.
- Never invent test values, units, reference ranges, dates, diagnoses, or treatment advice.
- Preserve the source report and extracted text provenance.
- Provide a way to report an incorrect or concerning explanation.
- Do not use generated explanations as a clinical decision or provider-ranking signal.
- Escalate urgent or potentially dangerous content using a clinically reviewed policy; do not rely on the model alone to identify emergencies.

### 6.5 Appointment and care-request boundary

The broader BRD describes self-serve appointment booking, instant confirmation, automated reminders, and virtual consultations. Those capabilities are deferred. Any appointment-related functionality in the current Django application must be described accurately as an enquiry/request or provider-availability workflow unless the code and operating process prove that a confirmed booking system exists.

Acceptance rules:
- A submitted appointment request is not a confirmed appointment.
- Availability must show its source, timezone, and last-updated status where available.
- Confirmation must come from an authorized provider or coordinator.
- Do not promise instant confirmation, automated reminders, or consultation access unless implemented and operationally supported.
- Do not represent WhatsApp coordination as a secure clinical consultation or a substitute for a telemedicine workflow.

### 6.6 Provider management

1. Authorized provider user signs in through the provider authentication flow.
2. User sees only the provider entities and actions assigned to their role.
3. User updates permitted profile, service, package, or availability information.
4. Changes are validated and, where required, submitted for internal review.
5. Public listing reflects approved information and its last-updated status.

**Requirements**
- Separate provider identity from provider organization and listing records.
- Enforce object-level permissions, not only hidden navigation or template conditions.
- Track who changed material profile information and when.
- Require internal approval for claims such as accreditation, certification, outcome statistics, and “verified” status.
- Provider users must not be able to grant themselves verification or publish unsupported claims.

## 7. Functional requirements

Priority definitions: **P0** = required for a safe initial public release; **P1** = important follow-on; **P2** = later enhancement.

### 7.1 Marketplace discovery

| ID | Priority | Requirement | Acceptance criteria |
|---|---|---|---|
| MKT-01 | P0 | Public homepage explains FlyCure's service and primary next action. | A first-time visitor can identify the service, intended audience, and how to contact the team without signing in. |
| MKT-02 | P0 | Users can browse hospital listings. | Listing pages load valid active listings and do not expose draft or disabled providers. |
| MKT-03 | P0 | Users can browse doctor listings. | Listing pages show approved public fields and link to the correct detail page. |
| MKT-04 | P0 | Users can open hospital and doctor details. | Detail pages display only approved fields and handle missing optional data gracefully. |
| MKT-05 | P1 | Users can filter and search by supported criteria. | Filters are reflected in results and can be cleared; invalid parameters do not break the page. |
| MKT-06 | P1 | Users can compare selected providers or packages. | Comparison uses like-for-like fields and marks unavailable information as “not provided,” not as a negative or inferred value. |
| MKT-07 | P0 | Listings show data provenance and verification state where applicable. | “Verified” appears only when a current, documented verification record exists. |
| MKT-08 | P0 | Demo listings cannot be mistaken for real partners. | Seeded fictional records are excluded from production or unmistakably labelled in non-production environments. |

### 7.2 WhatsApp and enquiry conversion

| ID | Priority | Requirement | Acceptance criteria |
|---|---|---|---|
| ENQ-01 | P0 | A primary WhatsApp CTA is available on relevant public pages. | CTA uses configured `WHATSAPP_NUMBER`; missing configuration produces a safe fallback, not a broken link. |
| ENQ-02 | P0 | Prefilled message is non-sensitive and user-editable. | Message contains no medical report contents or sensitive patient data. |
| ENQ-03 | P1 | Enquiry context can be recorded without exposing health data in URLs. | Any reference token is opaque, non-guessable, and resolves only through authorized internal tooling. |
| ENQ-04 | P1 | Internal team can track enquiry status. | Status changes are timestamped and attributable to an authorized user. |
| ENQ-05 | P0 | Contact expectations are accurate. | No unapproved response-time, availability, or service guarantees appear in UI or automated messages. |

### 7.3 Accounts and profiles

| ID | Priority | Requirement | Acceptance criteria |
|---|---|---|---|
| ACC-01 | P0 | Patients can register, sign in, and sign out. | Authentication flows work with server-side validation and standard security protections. |
| ACC-02 | P0 | Patients can access and update their own profile. | A patient cannot read or modify another patient's profile by changing a URL or request parameter. |
| ACC-03 | P0 | Provider login is role-restricted. | Provider accounts cannot access patient-only or administrative functions without explicit permission. |
| ACC-04 | P1 | Account recovery is supported. | Recovery does not reveal whether an email/account exists beyond approved response behavior. |
| ACC-05 | P1 | Patient consent and privacy notices are recorded where required. | The system records notice version, timestamp, and consent purpose where consent is the applicable legal basis. |

### 7.4 Medical records

| ID | Priority | Requirement | Acceptance criteria |
|---|---|---|---|
| REC-01 | P0 | Authenticated patients can upload supported reports. | Invalid, oversized, or unsupported files are rejected with a useful message. |
| REC-02 | P0 | Each report is linked to its authenticated owner. | Ownership is assigned server-side and cannot be overridden by submitted form data. |
| REC-03 | P0 | All report access is owner- and role-checked. | Cross-patient access tests fail closed for list, detail, download, preview, and derived outputs. |
| REC-04 | P0 | Files are stored privately. | No anonymous public URL can retrieve a medical report. |
| REC-05 | P0 | Report lifecycle is visible. | Patient can distinguish uploaded, processing, available, failed, and deleted states as applicable. |
| REC-06 | P1 | Patients can request deletion of a report. | Deletion follows the documented retention and backup policy and is auditable. |
| REC-07 | P1 | Authorized access is logged. | Logs include actor, action, report reference, timestamp, and outcome without copying report contents into logs. |

### 7.5 AI report explanations

| ID | Priority | Requirement | Acceptance criteria |
|---|---|---|---|
| AIR-01 | P0 | Current local stub is explicitly identified as demo output. | Stub content cannot be mistaken for an explanation of the uploaded report. |
| AIR-02 | P1 | Explanation jobs have explicit states and failure handling. | A failed job is visible and retry behavior is bounded and logged. |
| AIR-03 | P1 | Text extraction is validated before model use. | Extracted values retain units, reference ranges, and source locations where available; uncertain extraction is flagged. |
| AIR-04 | P1 | Model output follows an approved schema and safety prompt. | Output is checked for unsupported diagnoses, fabricated values, and treatment instructions before display. |
| AIR-05 | P1 | Patient sees limitations and clinician-review guidance. | Disclaimer is adjacent to the explanation and remains visible on mobile. |
| AIR-06 | P1 | AI provider use is disclosed and controlled. | Data sent to an external processor is covered by approved privacy, security, contractual, and retention review. |
| AIR-07 | P2 | Clinician review workflow can be added. | Review status, reviewer identity, and changes are recorded; generated content is not represented as clinician-approved before review. |

### 7.6 Provider and care operations

| ID | Priority | Requirement | Acceptance criteria |
|---|---|---|---|
| OPS-01 | P0 | Authorized users can maintain provider records. | CRUD actions are permission-checked and validated server-side. |
| OPS-02 | P0 | Public listing status is controlled. | Draft, inactive, or unapproved records are not publicly visible. |
| OPS-03 | P1 | Provider availability can be maintained. | Availability has a source, timezone, last-updated time, and confirmation status. |
| OPS-04 | P1 | Appointment requests can be recorded and tracked. | Request is not shown as confirmed until the provider or authorized operator confirms it. |
| OPS-05 | P1 | Treatment quotation requests can be coordinated. | A quote identifies currency, included/excluded items, source, issue date, expiry/validity if supplied, and confirmation status. |
| OPS-06 | P2 | Travel and follow-up coordination can be represented. | Only contracted and operationally supported services are shown as available. |

## 8. Information architecture and key screens

The exact routes must be verified against the repository before implementation planning. The following is the intended information architecture.

### 8.1 Public experience

- Home
- Hospital search/list
- Hospital detail
- Doctor search/list
- Doctor detail
- Specialty or treatment discovery (where supported by data)
- About FlyCure / How it works
- Trust, verification, privacy, and medical disclaimer information
- Contact / WhatsApp

### 8.2 Patient experience

- Patient registration
- Patient login
- Patient dashboard
- Patient profile
- Medical records list
- Medical report upload
- Medical report detail
- Report explanation detail and status
- Procedure or care history (verify current implementation)
- Suggested tests (verify clinical ownership and meaning)
- Appointment requests (verify current implementation)

### 8.3 Provider and internal operations

- Provider login
- Doctor dashboard
- Hospital dashboard
- Provider profile management
- Specialty and service management
- Treatment package management
- Availability management
- Appointment request management
- Internal administration and verification review
- Enquiry operations (if implemented or added)

### 8.4 Screen-level UX requirements

All screens must:
- Work on mobile, tablet, and desktop.
- Use clear page titles, readable typography, accessible contrast, and keyboard-accessible controls.
- Provide loading, empty, validation-error, permission-denied, and system-error states.
- Avoid dark patterns and pressure tactics around medical decisions.
- Display prices with currency and scope; display “request a quote” when a reliable price is not available.
- Display timestamps with an explicit timezone when timing affects patient decisions.
- Use plain language and explain medical terms without overstating certainty.

## 9. Trust, provider verification, and content governance

### 9.1 Verification model

Do not use a generic “verified” badge without a defined process. Define verification separately for:
- Legal identity of the hospital or clinic.
- Doctor identity and registration/licence, including issuing jurisdiction and expiry/recheck date.
- Hospital accreditation and certification.
- Specialty and service availability.
- Treatment package contents and pricing.
- Outcome or success-rate claims.
- Reviews and testimonials.

Each verification record should capture:
- Claim being verified.
- Evidence source and document/reference.
- Reviewer and review timestamp.
- Validity or expiry date, if applicable.
- Status: unverified, pending, verified, expired, rejected.
- Public wording permitted by the evidence.

### 9.2 Content rules

- No fabricated provider profiles, reviews, patient stories, accreditations, or outcome statistics in production.
- Do not imply that a doctor is “best,” “top,” or “leading” without a transparent and defensible basis.
- Do not present a package price as a guaranteed final cost unless the provider has explicitly confirmed its scope and validity.
- Clearly separate provider-supplied information from FlyCure editorial content.
- Keep a last-verified or last-updated date for material provider information.

## 10. Clinical safety and AI governance

### 10.1 Intended use

The future report explanation feature is intended to help patients understand terminology and organize questions for a qualified clinician. It is not intended to diagnose, triage, recommend treatment, change medication, or replace a clinician's interpretation.

### 10.2 Safety requirements

- Use a clinically reviewed content policy and disclaimers before enabling real report interpretation.
- Do not generate a diagnosis or treatment plan from an uploaded report.
- Do not tell patients to start, stop, or change medication.
- Do not infer missing values or normalize uncertain OCR results into confident statements.
- Preserve units, reference ranges, dates, and report context; flag ambiguity.
- Make it clear that reference ranges vary by laboratory, age, sex, clinical context, and other factors.
- Include a clear route to contact a clinician or care coordinator for questions.
- Include emergency guidance reviewed for the target markets and avoid delaying emergency care. The app must not claim to monitor emergencies.
- Maintain model version, prompt version, extraction version, job timestamp, and output provenance for each generated explanation.
- Establish a human review and incident process before any clinical-facing deployment.

### 10.3 AI release gate

Real LLM integration must not be enabled merely because `OPENAI_API_KEY` exists. Release requires:
1. Approved use case and data-flow map.
2. Privacy and vendor/processor review.
3. Secure secrets management.
4. PDF and image extraction pipeline with validation.
5. Clinical safety review of prompts, output schema, and refusal/escalation behavior.
6. Test corpus representing supported report types and poor-quality scans.
7. Evaluation for fabricated values, omissions, incorrect units, and unsafe advice.
8. Monitoring, rate limits, cost controls, and incident response.
9. Clear user disclosure and consent where required.
10. Rollback switch that disables model processing without breaking report access.

## 11. Privacy, security, and compliance requirements

FlyCure handles sensitive health information. Applicable obligations depend on the patient's location, the service's operating entities, processing locations, partners, and the exact data flows. Obtain qualified legal and security review before production. This PRD is not legal advice and does not declare compliance with any law or certification.

### 11.1 Data protection principles

- Collect the minimum information required for each workflow.
- Explain the purpose of collection before asking for sensitive data.
- Record the applicable legal basis and consent where required.
- Restrict access by role and business need.
- Separate public marketplace data from patient-private data.
- Define retention and deletion periods by data category.
- Provide a process for access, correction, deletion, and other applicable data-subject requests.
- Review international transfers and third-party processing before enabling them.
- Do not use patient reports for model training or unrelated purposes without a separately reviewed lawful basis and explicit product decision.

### 11.2 Technical security baseline

**Authentication and authorization**
- Use Django's password hashing and authentication protections.
- Require strong staff/admin authentication; enable MFA for privileged accounts where feasible.
- Apply least privilege and object-level authorization.
- Use CSRF protection for state-changing browser requests.
- Rate-limit login, password reset, upload, and enquiry endpoints.
- Review session lifetime, cookie flags, and session invalidation.

**Application and infrastructure**
- Production must use HTTPS.
- Set `DEBUG=False`, secure `ALLOWED_HOSTS`, secure cookies, HSTS after deployment validation, and a production secret key.
- Keep secrets out of source control, images, logs, and client-side code.
- Patch Django, Python, system packages, and dependencies.
- Use a supported production database such as PostgreSQL unless an explicitly reviewed alternative is selected.
- Run dependency and vulnerability scanning.
- Restrict admin access and monitor privileged actions.
- Back up databases and files with encryption, access control, restore tests, and documented retention.

**Medical files**
- Use private object storage in production.
- Encrypt files at rest and in transit.
- Use short-lived authorized access links or a permission-checked download endpoint.
- Scan uploads before parsing or previewing.
- Avoid logging report contents, extracted health values, or signed URLs.
- Define deletion behavior for originals, extracted text, generated explanations, temporary files, and backups.

**Auditability**
- Record authentication events, permission denials, report access, provider record changes, admin actions, consent changes, and AI processing events.
- Protect audit logs from ordinary application-user modification.
- Do not store unnecessary sensitive payloads in logs.
- Define retention and access rules for audit data.

### 11.3 Production privacy checklist

- Privacy notice and terms reviewed for target jurisdictions.
- Patient consent and authorization flows reviewed.
- Data inventory and data-flow diagram completed.
- Data processor agreements and vendor review completed.
- Hosting region and international transfer review completed.
- Retention and deletion schedule approved.
- Incident response and breach-notification process documented.
- Access-control and penetration testing completed.
- Backup restoration and disaster recovery tested.
- Support and staff access procedures documented.

## 12. Data and domain model considerations

The actual Django models are authoritative; the following is a conceptual model for PRD completeness and future design review.

| Entity | Purpose | Important considerations |
|---|---|---|
| User | Authentication identity | Avoid conflating login identity with patient/provider business records |
| PatientProfile | Patient-specific profile | Minimize fields; apply ownership checks |
| ProviderOrganization | Hospital/clinic identity | Organization-level permissions and status |
| DoctorProfile | Doctor identity and public details | Credentials, issuing authority, verification dates |
| Specialty | Controlled specialty taxonomy | Avoid uncontrolled duplicate labels |
| TreatmentPackage | Provider-supplied package information | Scope, exclusions, currency, source, validity, confirmation |
| ProviderVerification | Evidence and status for claims | Reviewer, evidence reference, expiry, audit history |
| MedicalReport | Patient-owned report metadata | Owner, private storage key, type, status, timestamps |
| ReportArtifact | Extracted text or generated explanation | Provenance, versioning, retention, access control |
| ExplanationJob | AI processing lifecycle | Status, model/prompt version, failure reason, retries |
| ProcedureHistory | Patient's care/procedure history | Patient-entered vs provider-confirmed provenance |
| SuggestedTest | Suggested or requested test information | Must not be presented as a clinical order without authorization |
| AvailabilitySlot | Provider availability | Timezone, source, last-updated, confirmation status |
| AppointmentRequest | Patient request for an appointment | Requested vs confirmed status |
| Enquiry | Marketplace-to-coordinator handoff | Consent, source page, status, assignment, timestamps |
| AuditEvent | Security and operational trace | Actor, action, target, timestamp, outcome |

### 12.1 Data modeling rules

- Every patient-owned object must have an explicit patient relationship or another unambiguous ownership mechanism.
- Every provider-managed object must have an explicit organization/user authorization path.
- Use controlled status fields and documented transitions.
- Store money as decimal amounts with explicit currency; never use floating-point values for financial amounts.
- Store timestamps consistently and display them in the appropriate user/provider timezone.
- Keep source and verification metadata for externally supplied claims.
- Avoid storing the same sensitive data in multiple tables without a clear need and retention plan.

## 13. Technical architecture and engineering constraints

### 13.1 Current stack

- Python and Django 6 (the project context also references Django 6.1; confirm the exact installed version from dependency files and runtime).
- Django templates and server-rendered views; no separate frontend framework.
- SQLite for local development when `MYSQL_HOST` is unset.
- Docker Compose supports a MySQL-backed local setup according to the README.
- Pillow for image support.
- `python-dotenv` and `mysqlclient` are listed in the broader project context.
- Apps include `marketplace`, `providers`, `accounts`, `records`, `ai_reports`, and `care` in the broader code map.
- Public marketplace browsing is in `marketplace`; provider entities and seeded data are in `providers`; patient report handling is in `records`; explanation logic is in `ai_reports`; patient/provider care workflows are in `care`.

### 13.2 Architecture principles

- Keep the initial product as a modular Django monolith.
- Keep business logic out of templates and thin view functions where practical.
- Centralize authorization and report ownership checks in reusable services/querysets or policy helpers.
- Keep AI provider integration behind a service interface so it can be disabled or replaced.
- Use asynchronous background processing for expensive OCR/LLM work before production launch; do not block a web request on long-running model calls.
- Keep uploaded documents in private storage, separate from static assets.
- Add structured logging, monitoring, and error reporting without sensitive payloads.
- Use migrations and automated tests for all schema and permission changes.

### 13.3 Environment and configuration

The README identifies:
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `WHATSAPP_NUMBER`
- `OPENAI_API_KEY` (optional)
- `AI_REPORT_MODEL`
- `MAX_REPORT_UPLOAD_SIZE_MB` (default: `10`)
- `REPORT_UPLOADS_ENABLED` (default: `False`; Docker Compose forces `False` for the limited-access MVP)
- `CLAMAV_HOST` (scanner host; configure only when uploads are explicitly re-enabled)
- `CLAMAV_PORT` (default: `3310`)
- `CLAMAV_SCAN_TIMEOUT_SECONDS` (default: `30`)

Additional production configuration will likely be required for database credentials, storage, email, background workers, logging, monitoring, and external service endpoints. Document all required variables in `.env.example` with safe placeholders. Never commit `.env` or real credentials.

### 13.4 Database decision

SQLite is acceptable for local development. The README documents a MySQL Docker setup, while the broader project context describes SQLite development and a possible PostgreSQL production target. Select one production database before launch and test migrations, indexes, backups, restore procedures, and deployment operations against it. Do not assume that changing a connection string alone completes the migration.

## 14. Non-functional requirements

| Category | Requirement |
|---|---|
| Security | All patient-private endpoints enforce authentication and object-level authorization. |
| Privacy | Medical files are private by default and never exposed through guessable public URLs. |
| Reliability | Failed uploads and background jobs produce recoverable, visible states. |
| Performance | Public listing and detail pages should be optimized for mobile networks; establish measurable latency budgets before launch. |
| Accessibility | Aim for WCAG 2.2 AA for core patient and marketplace journeys, subject to formal audit. |
| Responsive design | Core journeys work on small mobile screens through desktop. |
| Localization | Store locale/timezone where needed; plan translation before expanding target markets. |
| Maintainability | Use modular Django apps, automated tests, documented service boundaries, and migration discipline. |
| Observability | Monitor application errors, job failures, upload failures, latency, and security events. |
| Scalability | Keep report processing asynchronous and storage externalizable; scale based on measured demand. |
| Compatibility | Support current major browsers used by target patients; define an explicit support matrix. |
| Data integrity | Provider, appointment, quote, and report states must not imply confirmation before it occurs. |

## 15. Analytics and event instrumentation

Use privacy-conscious event instrumentation. Do not send report contents, extracted values, diagnoses, or other health information to general-purpose analytics.

Suggested events:
- `marketplace_home_viewed`
- `hospital_search_performed`
- `doctor_search_performed`
- `provider_detail_viewed`
- `provider_compare_started`
- `whatsapp_cta_clicked`
- `patient_registration_started`
- `patient_registration_completed`
- `report_upload_started`
- `report_upload_completed`
- `report_upload_failed`
- `report_detail_viewed`
- `report_explanation_requested`
- `report_explanation_completed`
- `report_explanation_failed`
- `appointment_request_submitted`

Event properties should be limited to non-sensitive operational context such as page type, anonymous session identifier, coarse campaign source, and non-sensitive internal IDs where approved. Apply consent and analytics rules appropriate to the user's jurisdiction.

## 16. Testing and quality strategy

### 16.1 Required automated tests

- Authentication and role-permission tests.
- Patient profile ownership tests.
- Report upload validation tests.
- Cross-patient report access tests for list, detail, preview, download, and generated artifacts.
- Private-storage access tests.
- Provider organization and object-level permission tests.
- Public visibility tests for draft, inactive, and unverified listings.
- WhatsApp link configuration and safe-message tests.
- Explanation stub tests and explicit demo labelling tests.
- AI job state, timeout, retry, and failure tests when background processing is introduced.
- Form validation and error-state tests.
- Migration and database compatibility tests for the chosen production database.

### 16.2 Manual and operational testing

- Mobile-first usability testing with representative international users.
- Keyboard and screen-reader review of key journeys.
- Upload tests using valid, invalid, oversized, malformed, and potentially malicious files.
- Timezone and locale testing.
- Provider onboarding and verification workflow walkthrough.
- Coordinator handoff and enquiry-response simulation.
- Backup restoration and incident-response exercises.
- Security review and penetration test before public production launch.

### 16.3 Release-blocking defects

A release must be blocked if:
- A patient can access another patient's report or profile.
- Medical files are publicly accessible.
- Demo or fictional provider data is presented as real.
- AI output can be mistaken for a clinician's diagnosis or verified interpretation.
- A public claim about credentials, outcomes, prices, or services lacks evidence.
- Production is running with debug settings or exposed secrets.
- Critical security vulnerabilities remain unresolved.

## 17. Phased roadmap

The phases are capability-based. Dates and estimates should be assigned after repository review and team capacity planning.

### Phase 0 — Repository and product baseline

**Objective:** Establish an accurate picture of what exists and remove ambiguity.

Deliverables:
- Audit routes, models, migrations, templates, services, permissions, and tests.
- Confirm exact Django and dependency versions.
- Map current patient, provider, and admin roles.
- Identify every endpoint that reads or serves report data.
- Verify current WhatsApp behavior and environment configuration.
- Identify all fictional seed data and ensure production exclusion.
- Create a data inventory and initial threat model.
- Resolve production database and hosting decisions.

**Exit criteria:** Current-state implementation matrix is verified against code; critical ownership and exposure risks are documented.

### Phase 1 — Safe marketplace and human handoff

**Objective:** Make public discovery and coordinator contact reliable.

Deliverables:
- Responsive homepage, hospital/doctor browse and detail flows.
- Reliable search/filter behavior.
- Provider data completeness and internal approval process.
- Evidence-backed trust labels.
- WhatsApp CTA and safe prefilled message.
- Accurate service, pricing, and response-time language.
- Analytics for discovery and conversion.

**Exit criteria:** A visitor can discover real, approved providers and contact FlyCure without misleading claims or broken conversion paths.

### Phase 2 — Patient accounts and secure records

**Objective:** Deliver a trustworthy patient account and report-management experience.

Deliverables:
- Registration, login, profile, and recovery hardening.
- Private report storage.
- File validation, malware scanning, and safe document processing suitable for the selected production environment.
- Owner-scoped list, detail, preview, and download paths.
- Audit events and retention/deletion policy.
- Privacy notice and consent flows as required.

**Exit criteria:** Security tests demonstrate that patients cannot access one another's records; private storage and operational controls are in place.

### Phase 3 — Care coordination workflows

**Objective:** Support structured follow-up after an enquiry.

Deliverables:
- Enquiry record, assignment, and status lifecycle.
- Internal coordinator workflow.
- Provider availability with source and timezone.
- Appointment request and confirmation states.
- Treatment quotation request and response workflow.
- Operational playbooks and escalation ownership.

**Exit criteria:** Enquiries, appointments, and quotes have clear owners and statuses; requests are never misrepresented as confirmed.

### Phase 4 — Production-grade report explanation

**Objective:** Introduce bounded, clinically reviewed report explanation.

Deliverables:
- Supported document types and extraction pipeline.
- OCR/PDF parsing with confidence and provenance.
- Asynchronous job processing.
- Approved external model integration behind a feature flag.
- Structured output validation and safety evaluation.
- Clinical review, incident handling, monitoring, and rollback.
- Patient disclosure and consent updates.

**Exit criteria:** Clinical, privacy, security, and product owners approve the use case and evaluation results. The feature can be disabled independently.

### Phase 5 — Expanded marketplace and patient support

**Objective:** Expand only after core discovery, privacy, and operations are stable.

Potential deliverables:
- Rich provider comparison.
- Verified patient education content.
- Additional languages and localized journeys.
- Travel coordination and post-treatment follow-up, if operationally supported.
- Partner integrations and richer provider workflows.
- Carefully evaluated patient feedback and review features.

**Exit criteria:** Each added service has a defined owner, evidence standard, support process, and measurable patient benefit.

### Future product track — broader Flycure Health platform (not committed)

The BRD's broader digital-health concept should be maintained as a separate discovery track after the current marketplace is validated. It is not an automatic continuation of the current committed roadmap.

Potential discovery areas:
- Native Android/iOS patient application.
- Domestic patient acquisition and B2C teleconsultation.
- RMP appointment booking and secure video/audio consultations.
- Clinical messaging and follow-up.
- A comprehensive patient EHR and provider record-sharing permissions.
- Digital prescriptions, medication reminders, pharmacy discovery, and fulfilment.
- Payment gateway, invoicing, subscriptions, and insurance eligibility/claims workflows.
- Remote patient monitoring and wearable/device integrations.
- Provider collaboration tools and corporate wellness programmes.

Before any of these move into delivery, create a separate product brief/PRD that defines the target geography and patient segment, clinical operating model, RMP responsibilities, partner dependencies, business model, data flows, regulatory review, safety controls, support model, and measurable MVP. The mobile application should be planned as a separate platform initiative rather than assumed to be a wrapper around the current website.

## 18. Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Sensitive report exposure | Severe privacy and patient harm | Private storage, object-level authorization, security tests, audit logs, penetration testing |
| AI hallucination or misinterpretation | Patient confusion or unsafe decisions | Keep stub clearly labelled; clinical review; extraction validation; constrained outputs; no diagnosis or treatment advice |
| Unverified provider claims | Loss of trust and potential legal exposure | Evidence-backed verification workflow and content approval |
| Misleading treatment prices | Financial harm and disputes | Quote workflow with scope, exclusions, currency, source, and validity |
| Unconfirmed appointment availability | Travel disruption and patient frustration | Explicit requested/pending/confirmed states and timestamps |
| Unstaffed WhatsApp promise | Poor patient experience | Publish only operationally supported response expectations |
| Fictional seed data in production | Misrepresentation | Environment guards, deployment checks, production seed policy |
| International privacy obligations overlooked | Regulatory and contractual exposure | Jurisdictional legal review, data-flow mapping, vendor review |
| OCR errors | Incorrect explanation | Confidence thresholds, source traceability, ambiguity flags, human escalation |
| Provider account compromise | Unauthorized changes or data access | MFA for privileged roles, least privilege, audit trail, anomaly monitoring |
| Unclear operational ownership | Enquiries or requests abandoned | Named queue owners, status SLAs internally, escalation playbooks |

## 19. Open product and engineering decisions

Resolve these before the relevant phase begins.

### Product and operations
1. Which countries and patient markets are in the first launch cohort?
2. Which specialties and treatment categories are in scope at launch?
3. Which languages are required at launch?
4. Who operates the WhatsApp inbox, during what hours, and what response expectation can be supported?
5. Is FlyCure acting only as a discovery/referral coordinator, or does it provide additional contracted services?
6. What is the provider onboarding and verification standard?
7. Who approves public pricing, package descriptions, outcome claims, and testimonials?
8. What is the enquiry lifecycle and who owns each status?
9. What is the policy for family members or caregivers acting on behalf of a patient?

### Patient records and AI
10. Current upload policy: PDF, JPEG, PNG, and DOCX, up to 10 MB per file. Revisit this policy if supported workflows require other formats or sizes.
11. Which staff roles may access patient reports, for what purpose, and with what patient authorization?
12. What are the retention and deletion periods for reports, extracted text, and explanations?
13. Which jurisdictions and hosting regions apply to report processing?
14. Is AI explanation in the initial public launch or explicitly deferred?
15. Which clinicians or clinical advisors approve the intended use, prompts, disclaimers, and evaluation set?
16. Which model provider and data-processing terms are acceptable?

### Engineering and infrastructure
17. Is PostgreSQL the production database, or will MySQL be retained?
18. Which hosting provider and private object-storage service will be used?
19. Which background-job system will run OCR and AI tasks?
20. Which email/SMS service, if any, is required for account recovery and notifications?
21. What are the expected traffic, file-volume, availability, and recovery objectives?
22. Which monitoring, error reporting, and security scanning tools will be used?

## 20. Definition of done

A feature is complete only when:
- Its user outcome and scope are documented.
- UI states include loading, empty, success, validation, permission, and failure cases where relevant.
- Server-side validation and authorization are implemented.
- Automated tests cover critical behavior and security boundaries.
- Sensitive data is not exposed in URLs, logs, analytics, or public storage.
- Accessibility and responsive behavior are reviewed.
- User-facing copy is accurate and approved.
- Operational ownership and support implications are documented.
- Relevant documentation and environment examples are updated.
- The feature has been tested against the selected production database and deployment configuration where applicable.

A production release additionally requires the release-blocking checks in Section 16.3 to pass.

## 21. Repository reference and local development

The supplied README describes the following local workflows. Verify these against the current repository before using them in deployment documentation.

### Docker

```bash
cp .env.example .env
docker compose up --build
```

The README lists:
- FlyCure home: `http://localhost:8000/`
- Patient login: `http://localhost:8000/accounts/login/`
- Provider login: `http://localhost:8000/accounts/provider/login/`
- Django admin: `http://localhost:8000/admin/`
- phpMyAdmin: `http://localhost:8080/`
- MySQL: `localhost:3306`, database `flycure`

The README lists demo credentials for local use. These must never be reused in production.

### Local Python / SQLite

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

### Relevant code areas from project context

- `accounts/` — authentication and patient profiles
- `marketplace/` — public browse/search views and URLs
- `providers/` — specialties, hospitals, doctors, treatment packages, and seed data
- `records/` — patient-owned medical report upload and access
- `ai_reports/` — report explanation model and currently stubbed explanation service
- `care/` — patient history, appointments, doctor slots, and provider dashboards/actions
- `templates/`, `static/` — server-rendered UI and assets
- `docs/design-research-wireframes.md` — product vision, positioning, trust signals, and proposed flows

### Important implementation notes

- The current report explanation service is a deterministic local stub. Setting `OPENAI_API_KEY` does not, by itself, invoke a real external model.
- PDF/OCR parsing and real model integration remain future work.
- Report queries are scoped to the logged-in patient in the supplied project context. Preserve and test this boundary across every report and file access path.
- Local uploaded files are stored under `media/records/`; this is not an acceptable public production storage design for sensitive medical reports without additional private-storage and access controls.
- Seeded hospitals and doctors are fictional demo data.

---

## Appendix A — Terminology

| Term | Meaning |
|---|---|
| Patient | Person exploring or receiving care |
| Caregiver | Person helping a patient with research or coordination |
| Provider | Hospital, clinic, doctor, or other care organization/person represented in the marketplace |
| Care coordinator | Human FlyCure representative handling patient enquiries and coordination |
| Enquiry | A patient's expression of interest or request for contact |
| Treatment package | Provider-supplied description of a proposed service and its included/excluded items |
| Quote | A provider-confirmed commercial estimate with defined scope and validity |
| Medical report | Patient-provided health document |
| Report explanation | Informational, non-diagnostic explanation generated from report content |
| Verified claim | A claim checked against documented evidence under FlyCure's verification process |

## Appendix B — Important product boundary

FlyCure should help patients make better-informed enquiries and coordinate conversations with appropriate providers. It must not create the impression that browsing, an AI-generated explanation, a package listing, an availability slot, or a WhatsApp message constitutes a medical consultation, treatment recommendation, confirmed appointment, guaranteed price, or guaranteed clinical outcome.
