# Medical Tourism Marketplace Design Research and Wireframes

## Brief

Build a premium, warm, practical medical tourism facilitator and marketplace for international patients coming to India. The site should help patients compare hospitals, doctors, and packages across allopathic treatment categories including cosmetic surgery, dental, IVF/fertility, cardiac, orthopedic, oncology, transplant, neurology, gastroenterology, urology, bariatric surgery, ophthalmology, ENT, and general multi-specialty care.

Brand name: FlyCure.

Primary audience: broad global English-speaking patients and family decision-makers researching treatment in India.

Tone: premium hospital-grade, warm and reassuring, affordable and practical.

Chosen product stance: a balanced hybrid of premium marketplace and personal medical concierge.

Demo data stance: use clearly labelled fictional sample hospitals and doctors until real partner data is available.

Primary conversion path: WhatsApp-first. Do not show unconfirmed fixed prices or require patients to send reports through WhatsApp; providers confirm any quotation after reviewing the relevant information through an approved process.

## Status and source of truth

This file is exploratory research and a directional wireframe, not approved production copy or a complete description of shipped functionality. For implementation, use the [updated PRD](./FlyCure_Updated_PRD.md) for product scope and safety rules, the [design requirements](./FlyCure_Design_Requirements.md) for visual tokens, and the [high-fidelity mockups](./FlyCure_High_Fidelity_Visual_Mockups.png) as visual reference.

- Treat market statistics and competitor statements below as unverified until independently sourced and approved.
- Do not publish unverified accreditation, ratings, outcomes, provider counts, response-time commitments, visa/travel services, or patient stories.
- Label fictional profiles and sample package data clearly; never imply they represent real partners.
- WhatsApp prefilled messages must be user-editable and contain no patient health information.
- Keep the experience within the current web marketplace scope. A wireframe does not authorize diagnosis, treatment recommendations, telemedicine, travel fulfillment, or other deferred services.

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

"Explore and compare available information about hospitals, doctors, and treatment options in India, then contact a care coordinator with questions."

### Visual Language

- Clean hospital-grade layout with generous whitespace and precise information hierarchy.
- Palette should avoid a cold all-blue hospital look. Suggested: deep ink text, clinical teal accents, warm ivory surfaces, soft green success states, restrained amber cost highlights.
- Real healthcare and city imagery should be used later, but the first viewport should emphasize the marketplace search experience, not a marketing hero alone.
- Cards should prioritize available provider details: name, city, specialties, profile information, and a clear next action.
- Show verification labels only when current evidence and approval records support them. Mark fictional data as demo content.

### Trust and transparency

- Explain what information is provided and what a patient should confirm directly.
- Display provider credentials or accreditation only when verified with documented evidence.
- Distinguish indicative package information from a provider-confirmed quotation.
- Avoid response-time, travel-support, report-review, or follow-up promises until operationally approved.
- Keep health information out of WhatsApp prefilled messages.
- Label demo profiles and package details in a way that cannot be mistaken for real listings.

## Information Architecture

Top navigation:

- Treatments
- Hospitals
- Doctors
- Packages
- Patient Journey
- WhatsApp

Use existing routes and anchors; add navigation destinations only when those pages exist. Primary CTAs:

- WhatsApp Coordinator
- Browse hospitals or doctors
- Upload a report from the signed-in patient area

## Page 1: Homepage Wireframe

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Logo          Treatments  Hospitals  Doctors  Journey        Contact        │
├────────────────────────────────────────────────────────────────────────────┤
│ H1: Explore care in India, with a clearer path forward                      │
│ Subcopy: Compare available hospital and doctor information, explore options,│
│ and ask a human care coordinator about next steps.                          │
│                                                                            │
│ [Search care options] [Specialty] [City] [Search options]                   │
│                                                                            │
│ Context: Explore providers | Compare available details | Ask when ready     │
├────────────────────────────────────────────────────────────────────────────┤
│ Allopathic treatment categories grid                                        │
│ Cardiac  Orthopedic  Oncology  IVF  Dental  Cosmetic  Transplant  Neuro     │
│ Gastro   Urology     Bariatric Ophthalmology ENT  Multi-specialty           │
├────────────────────────────────────────────────────────────────────────────┤
│ Hospital and doctor profiles, clearly marking fictional demo data           │
│ Available profile information; no inferred ratings, credentials or prices  │
├────────────────────────────────────────────────────────────────────────────┤
│ Journey: Explore -> Compare -> Ask questions -> Confirm directly            │
│ Patient account/report links appear only when relevant and clearly explained│
├────────────────────────────────────────────────────────────────────────────┤
│ Final coordinator CTA with a non-sensitive, editable WhatsApp starter       │
└────────────────────────────────────────────────────────────────────────────┘
```

Homepage priority:

- Lead with search and comparison.
- Make the coordinator contact route visible without promising a response time.
- Show available provider inventory early and label sample content.
- Use a calm patient/coordinator image rather than operating-room imagery.

## Page 2: Treatment Detail Wireframe

Example: Knee Replacement in India

```text
┌────────────────────────────────────────────────────────────────────────────┐
│ Breadcrumb: Treatments > Orthopedics > Knee Replacement                     │
├────────────────────────────────────────────────────────────────────────────┤
│ H1: Knee replacement in India                                               │
│ Context: indicative information only; confirm clinical and commercial details│
│ [Ask a question] [Browse providers]                                         │
├────────────────────────────────────────────────────────────────────────────┤
│ Tabs: Overview | Costs | Hospitals | Doctors | Recovery | FAQs              │
├────────────────────────────────────────────────────────────────────────────┤
│ Left: treatment overview, who it helps, procedure types                     │
│ Right sticky: WhatsApp coordinator + upload reports form                    │
├────────────────────────────────────────────────────────────────────────────┤
│ Cost explainer: quote depends on provider review and confirmed scope        │
├────────────────────────────────────────────────────────────────────────────┤
│ Recommended hospitals with filters: city, accreditation, budget, language    │
├────────────────────────────────────────────────────────────────────────────┤
│ Doctor list: specialty, years, hospital, languages, video consult CTA        │
├────────────────────────────────────────────────────────────────────────────┤
│ Any care timeline is provider-confirmed, not a FlyCure guarantee             │
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
│ Hospital name | City | clearly sourced profile information                  │
│ Specialties chips | approved provider details                               │
│ [Ask a coordinator] [View listed information]                               │
├────────────────────────────────────────────────────────────────────────────┤
│ Overview | Specialties | Doctors | Packages                                 │
├────────────────────────────────────────────────────────────────────────────┤
│ Provider-supplied details with source/verification status where available   │
├────────────────────────────────────────────────────────────────────────────┤
│ Top doctors at this hospital                                                │
│ Doctor cards with specialty, experience, languages, availability            │
├────────────────────────────────────────────────────────────────────────────┤
│ Package cards: treatment, quote via WhatsApp, stay, inclusions, exclusions   │
├────────────────────────────────────────────────────────────────────────────┤
│ Only facilities and services with approved supporting information           │
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
│ Filters: Treatment | City | supported provider attributes                    │
├────────────────────────────────────────────────────────────────────────────┤
│ Compare table                                                               │
│ Package        Provider              Scope          Price       Stay   CTA   │
│ Demo item      Demo provider         Confirmed by provider       Ask for info│
├────────────────────────────────────────────────────────────────────────────┤
│ Ask provider to confirm scope, inclusions, exclusions, currency, validity    │
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
Step 1: Explore public provider and specialty information without signing in.

Step 2: If the patient chooses to enquire, open WhatsApp with a generic, editable
starter message. Do not prefill diagnosis, treatment need, country, reports, or
other patient information.

Step 3: Let the patient decide what to share directly with the care team.
Provide an approved alternative contact route if WhatsApp is unavailable.

Step 4: Keep report upload inside the authenticated patient account and explain
supported formats and privacy handling before accepting real health data.
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
- Evidence and data-provenance indicators
- Cost explainer panel
- FAQ accordion
- Report upload form
- WhatsApp coordinator launcher

## Resolved Direction

1. Brand stance: balanced hybrid of marketplace and concierge.
2. Demo data: clearly labelled fictional sample hospitals and doctors; never imply they are partners.
3. Audience: broad global English.
4. Conversion: WhatsApp-first.
5. Treatment taxonomy: allopathic categories only.
6. Brand name: FlyCure.
7. Quotations: shared through WhatsApp, not displayed as fixed public prices.
8. Provider claims, ratings, prices, outcomes, and service commitments: show only when supported and approved.

## Remaining Design Questions

1. The visual direction is defined in `FlyCure_Design_Requirements.md`: warm, premium, and hospital-grade without unsupported care or travel promises.
2. The current app uses a responsive homepage plus separate hospital and doctor directories/details. Future page types require product scope in the PRD before implementation.
