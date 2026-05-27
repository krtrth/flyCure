# Medical Tourism Marketplace Design Research and Wireframes

## Brief

Build a premium, warm, practical medical tourism facilitator and marketplace for international patients coming to India. The site should help patients compare hospitals, doctors, and packages across allopathic treatment categories including cosmetic surgery, dental, IVF/fertility, cardiac, orthopedic, oncology, transplant, neurology, gastroenterology, urology, bariatric surgery, ophthalmology, ENT, and general multi-specialty care.

Brand name: FlyCure.

Primary audience: broad global English-speaking patients and family decision-makers researching treatment in India.

Tone: premium hospital-grade, warm and reassuring, affordable and practical.

Chosen product stance: a balanced hybrid of premium marketplace and personal medical concierge.

Demo data stance: use realistic-sounding fictional sample hospitals and doctors in the static site until real partner data is available.

Primary conversion path: WhatsApp-first. Treatment quotations are not shown as fixed public prices; they are shared through WhatsApp after the patient sends treatment needs and medical reports.

## Research Snapshot

Reviewed comparable medical tourism and healthcare marketplace sites:

- AfyaAssist: strong “compare hospitals and specialists” positioning, free quote flow, 24-hour response promise, patient journey, visa/travel support, multilingual support, accreditation trust markers, patient stories, FAQ, privacy/editorial policy.
- Karetrip: concierge-forward positioning, prominent WhatsApp CTA, trust badges, partner hospital cards, doctor cards with ratings, “how it works” journey, international patient support.
- Curevo: marketplace-forward browsing by treatment, destination cards, center cards with accreditation, starting prices, ratings, reviews, filters, provider-side marketplace promise.
- Meditor and similar platforms: broad doctor/hospital search, city selector, large verified doctor/hospital numbers, luxury travel and medical concierge claims.
- India treatment cost references: procedure-level cost factors and expected hospitalization durations. Avoid publishing exact public prices in the first static version because quotes are handled through WhatsApp.
- Government/PIB medical value travel data: India’s medical arrivals, source-country demand, popular allopathic treatments, and hospital accreditation context.

## Market Data to Use Carefully

Use these as design proof-points, not as unsourced marketing claims:

- India recorded 507,244 foreign nationals arriving for medical treatment in 2025, about 5.5% of foreign tourist arrivals.
- Top medical tourist source countries listed for 2025 include Bangladesh, Iraq, Uzbekistan, Somalia, Turkmenistan, Oman, and Kenya.
- Common allopathic treatment categories include cardiac surgery, orthopedics, cancer care, organ transplants, neurological interventions, cosmetic surgery, dental care, and fertility treatment.
- India has NABH-accredited hospitals and several JCI-accredited hospitals; accreditation should be shown at provider level where verified.

## Design Direction

### Product Positioning

Working concept:

"Compare accredited hospitals, doctors, and treatment packages in India, with a dedicated care coordinator from first report review to recovery follow-up."

### Visual Language

- Clean hospital-grade layout with generous whitespace and precise information hierarchy.
- Palette should avoid a cold all-blue hospital look. Suggested: deep ink text, clinical teal accents, warm ivory surfaces, soft green success states, restrained amber cost highlights.
- Real healthcare and city imagery should be used later, but the first viewport should emphasize the marketplace search experience, not a marketing hero alone.
- Cards should be practical and information-dense: accreditation, city, specialties, doctors, beds, typical stay estimate, response time, and WhatsApp quote action.

### Core Trust Signals

- Verified hospitals and doctors
- JCI/NABH/ISO accreditation where applicable
- Transparent package ranges
- Medical visa and invitation support
- Multilingual coordinators
- Report review before travel
- Secure medical record handling
- Dedicated case manager
- Follow-up after return home
- WhatsApp-first coordination for faster international communication

## Information Architecture

Top navigation:

- Treatments
- Hospitals
- Doctors
- Packages
- Patient Journey
- Cost Guides
- Stories
- WhatsApp

Persistent CTAs:

- WhatsApp Coordinator
- Get Free Treatment Plan
- Upload Reports

## Page 1: Homepage Wireframe

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Logo       Treatments Hospitals Doctors Packages Journey Stories  WhatsApp  │
├────────────────────────────────────────────────────────────────────────────┤
│ H1: Compare treatment options in India with expert guidance                 │
│ Subcopy: Accredited hospitals, verified specialists, transparent packages,  │
│ and one coordinator from report review to recovery.                         │
│                                                                            │
│ [Search treatment, doctor, hospital] [Country] [Budget] [Find options]      │
│ Popular: Cardiac | IVF | Dental | Orthopedic | Oncology | Cosmetic          │
│                                                                            │
│ Trust strip: JCI/NABH partners | 24h plan | Visa support | Secure records   │
├────────────────────────────────────────────────────────────────────────────┤
│ Allopathic treatment categories grid                                        │
│ Cardiac  Orthopedic  Oncology  IVF  Dental  Cosmetic  Transplant  Neuro     │
│ Gastro   Urology     Bariatric Ophthalmology ENT  Multi-specialty           │
├────────────────────────────────────────────────────────────────────────────┤
│ Featured comparison module                                                  │
│ Hospital card      Doctor card       Package card       WhatsApp panel      │
│ City/accreditation Experience      Custom quote       "Chat with coordinator"│
├────────────────────────────────────────────────────────────────────────────┤
│ How it works: 1 Upload reports  2 Compare options  3 Video consult          │
│               4 Travel to India 5 Treatment & recovery 6 Follow-up          │
├────────────────────────────────────────────────────────────────────────────┤
│ Why India: affordability, specialists, English-speaking care, accreditation  │
├────────────────────────────────────────────────────────────────────────────┤
│ Patient stories + source countries + FAQs + final quote form                │
└────────────────────────────────────────────────────────────────────────────┘
```

Homepage priority:

- Lead with search and comparison.
- Put the WhatsApp coordinator panel above the fold or as a right-side panel on desktop.
- Show real marketplace inventory early: hospitals, doctors, package types, stay estimates, and WhatsApp quote actions.

## Page 2: Treatment Detail Wireframe

Example: Knee Replacement in India

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Breadcrumb: Treatments > Orthopedics > Knee Replacement                     │
├────────────────────────────────────────────────────────────────────────────┤
│ H1: Knee replacement in India                                               │
│ Quick stats: Custom quote on WhatsApp | 5-7 hospital days | 2-4 week plan   │
│ [Chat on WhatsApp] [Compare hospitals] [Upload reports]                     │
├────────────────────────────────────────────────────────────────────────────┤
│ Tabs: Overview | Costs | Hospitals | Doctors | Recovery | FAQs              │
├────────────────────────────────────────────────────────────────────────────┤
│ Left: treatment overview, who it helps, procedure types                     │
│ Right sticky: WhatsApp coordinator + upload reports form                    │
├────────────────────────────────────────────────────────────────────────────┤
│ Cost table: standard / advanced implant / bilateral                         │
│ Includes: surgeon, hospital stay, implant, tests, airport transfer optional  │
├────────────────────────────────────────────────────────────────────────────┤
│ Recommended hospitals with filters: city, accreditation, budget, language    │
├────────────────────────────────────────────────────────────────────────────┤
│ Doctor list: specialty, years, hospital, languages, video consult CTA        │
├────────────────────────────────────────────────────────────────────────────┤
│ Timeline: report review -> travel clearance -> surgery -> rehab -> followup │
└────────────────────────────────────────────────────────────────────────────┘
```

Treatment page priority:

- Explain what affects cost without pretending to give final pricing.
- Include clinical disclaimers: final plan depends on doctor review and diagnostics.
- Let patients compare hospitals/doctors from the treatment page itself.

## Page 3: Hospital Profile Wireframe

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Hospital image/banner                                                       │
│ Hospital name | City, India | Rating | JCI/NABH/ISO badges                  │
│ Specialties chips | Beds | International desk | Languages                   │
│ [Chat with coordinator] [Request quote] [Book video consult]                │
├────────────────────────────────────────────────────────────────────────────┤
│ Overview | Specialties | Doctors | Packages | Facilities | Reviews          │
├────────────────────────────────────────────────────────────────────────────┤
│ Key reasons to choose: accreditation, equipment, high-volume specialties     │
├────────────────────────────────────────────────────────────────────────────┤
│ Top doctors at this hospital                                                │
│ Doctor cards with specialty, experience, languages, availability            │
├────────────────────────────────────────────────────────────────────────────┤
│ Package cards: treatment, quote via WhatsApp, stay, inclusions, exclusions   │
├────────────────────────────────────────────────────────────────────────────┤
│ Facilities: ICU, robotic surgery, interpreter, family stay, airport pickup   │
├────────────────────────────────────────────────────────────────────────────┤
│ Patient reviews and coordinator help panel                                  │
└────────────────────────────────────────────────────────────────────────────┘
```

Hospital page priority:

- Show verifiable comparison criteria, not generic claims.
- Use package cards as conversion bridges.
- Keep CTAs tied to “request quote” and “compare with similar hospitals.”

## Page 4: Packages / WhatsApp Quote Wireframe

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ H1: Compare treatment packages in India                                     │
│ Filters: Treatment | City | Hospital type | Accreditation | Stay            │
├────────────────────────────────────────────────────────────────────────────┤
│ Compare table                                                               │
│ Package        Hospital              Doctor        Quote       Stay   CTA    │
│ CABG           Asteria Heart Centre   Cardiac team   WhatsApp    4-6 d WhatsApp│
│ Dental implant NovaDent Global Care   Dentist        WhatsApp    OPD   WhatsApp│
│ IVF cycle      BloomBridge Fertility  Fertility      WhatsApp    OPD   WhatsApp│
│ Knee replace   Meridian Ortho MedCity Ortho          WhatsApp    5-7 d WhatsApp│
├────────────────────────────────────────────────────────────────────────────┤
│ What custom quotes may include/exclude                                      │
│ Included: consultation, surgery, standard hospital stay, basic tests         │
│ Excluded: complications, extended stay, donor costs, travel, premium rooms   │
├────────────────────────────────────────────────────────────────────────────┤
│ WhatsApp-first custom quote panel                                           │
└────────────────────────────────────────────────────────────────────────────┘
```

Package page priority:

- This should feel practical and transparent.
- Avoid public fixed pricing; use clear quote-via-WhatsApp actions and explain inclusions/exclusions.
- Let users save/compare 2-3 packages later if we build interactivity.

## Page 5: Consultation / Contact Flow Wireframe

```text
Step 1: Patient basics
Name, country, WhatsApp, email, preferred language

Step 2: Treatment need
Treatment category, diagnosis, desired city/budget, urgency

Step 3: Medical reports
Upload reports/images/prescriptions, notes, previous treatment

Step 4: Preferences
Hospital type, doctor gender if relevant, room type, attendant count, visa help

Step 5: WhatsApp handoff and confirmation
"Your coordinator can review your case on WhatsApp and share 2-3 suitable options within 24 hours."
Show WhatsApp continuation, report privacy reassurance, and email backup.
```

Flow priority:

- Ask enough to triage, but do not overwhelm.
- Reassure users that medical records are private.
- Offer WhatsApp as the primary action at every step.

## Content Modules to Reuse

- Treatment category cards
- Hospital comparison cards
- Doctor cards
- Package comparison rows
- Coordinator CTA panel
- Patient journey timeline
- Accreditation/trust strip
- Cost explainer panel
- FAQ accordion
- Report upload form
- WhatsApp coordinator launcher

## Resolved Direction

1. Brand stance: balanced hybrid of marketplace and concierge.
2. Static demo data: sample hospitals and sample doctors.
3. Audience: broad global English.
4. Conversion: WhatsApp-first.
5. Treatment taxonomy: allopathic categories only.
6. Brand name: FlyCure.
7. Quotations: shared through WhatsApp, not displayed as fixed public prices.
8. Sample providers: realistic fictional hospital and doctor names.

## Remaining Design Questions

1. Should FlyCure use a more clinical visual identity or a more travel-enabled care identity?
2. Should we build one long scrolling static page first, or separate static pages for homepage, treatment, hospital, packages, and contact flow?
