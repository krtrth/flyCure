from django.core.management.base import BaseCommand
from django.utils.text import slugify

from providers.models import Doctor, Hospital, Specialty, TreatmentPackage


SPECIALTIES = [
    ("Cardiac sciences", "cardiac", "H", "CABG, valve repair, angioplasty, electrophysiology, pediatric cardiology."),
    ("Orthopedics", "ortho", "+", "Knee replacement, hip replacement, spine surgery, sports injury care."),
    ("Oncology", "oncology", "*", "Surgery, chemotherapy, radiation planning, second opinions, tumor boards."),
    ("IVF and fertility", "fertility", "F", "IVF cycles, ICSI, fertility preservation, advanced diagnostics."),
    ("Dental care", "dental", "D", "Implants, crowns, smile design, full mouth rehabilitation."),
    ("Cosmetic surgery", "cosmetic", "C", "Rhinoplasty, hair transplant, body contouring, facial procedures."),
    ("Transplant programs", "transplant", "T", "Liver, kidney, bone marrow, donor evaluation and hospital coordination."),
    ("Neurosciences", "neuro", "N", "Brain, spine, stroke, epilepsy, movement disorder consultations."),
    ("Gastroenterology", "gastro", "G", "GI surgery, liver care, endoscopy, bariatric-linked diagnostics."),
    ("Urology", "urology", "U", "Kidney stones, prostate care, reconstructive surgery, uro-oncology."),
    ("Bariatric surgery", "bariatric", "B", "Weight-loss surgery, metabolic assessment, dietician-led follow-up."),
    ("Eye and ENT", "eye-ent", "E", "Cataract, LASIK, cochlear implant, sinus and airway procedures."),
]


class Command(BaseCommand):
    help = "Seed sample specialties, hospitals, doctors, and packages for FlyCure."

    def handle(self, *args, **options):
        specialty_map = {}
        for name, code, icon, description in SPECIALTIES:
            specialty, _ = Specialty.objects.update_or_create(
                slug=slugify(name),
                defaults={
                    "name": name,
                    "short_code": code,
                    "icon": icon,
                    "description": description,
                    "is_active": True,
                },
            )
            specialty_map[code] = specialty

        hospitals_data = [
            {
                "name": "Asteria Heart & Multi-Specialty Institute",
                "city": "Delhi NCR",
                "accreditation": "NABH sample",
                "summary": "Strong fit for CABG, valve procedures, electrophysiology, and international cardiac second opinions.",
                "image_url": "https://images.unsplash.com/photo-1538108149393-fbbd81895907?auto=format&fit=crop&w=900&q=80",
                "typical_stay": "4-6 day stay",
                "tags": "4-6 day stay, International desk, Arabic interpreter",
                "specialty_codes": ["cardiac"],
            },
            {
                "name": "Meridian Ortho MedCity",
                "city": "Bengaluru",
                "accreditation": "JCI sample",
                "summary": "Designed for joint replacement, spine surgery, sports injury repair, and structured rehabilitation planning.",
                "image_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=900&q=80",
                "typical_stay": "5-7 day stay",
                "tags": "5-7 day stay, Rehab planning, Family lounge",
                "specialty_codes": ["ortho"],
            },
            {
                "name": "BloomBridge Fertility & Women's Health",
                "city": "Chennai",
                "accreditation": "ISO sample",
                "summary": "Focused on IVF, ICSI, reproductive endocrinology, and discreet international patient coordination.",
                "image_url": "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?auto=format&fit=crop&w=900&q=80",
                "typical_stay": "OPD pathway",
                "tags": "OPD pathway, Female specialists, Embryology lab",
                "specialty_codes": ["fertility"],
            },
            {
                "name": "NovaDent Global Care",
                "city": "Mumbai",
                "accreditation": "ISO sample",
                "summary": "Dental implants, full mouth rehab, and smile design for international patients.",
                "image_url": "https://images.unsplash.com/photo-1629909615184-74f495363b67?auto=format&fit=crop&w=900&q=80",
                "typical_stay": "OPD visits",
                "tags": "Implant center, Digital scans, Same-week planning",
                "specialty_codes": ["dental"],
            },
        ]

        hospital_map = {}
        for item in hospitals_data:
            hospital, _ = Hospital.objects.update_or_create(
                slug=slugify(item["name"]),
                defaults={
                    "name": item["name"],
                    "city": item["city"],
                    "accreditation": item["accreditation"],
                    "summary": item["summary"],
                    "image_url": item["image_url"],
                    "typical_stay": item["typical_stay"],
                    "tags": item["tags"],
                    "is_sample": True,
                    "is_active": True,
                },
            )
            hospital.specialties.set([specialty_map[code] for code in item["specialty_codes"]])
            hospital_map[item["name"]] = hospital

        doctors_data = [
            {
                "name": "Dr. Arvind Mehra",
                "title": "Cardiac surgeon",
                "hospital": "Asteria Heart & Multi-Specialty Institute",
                "specialty": "cardiac",
                "city": "Delhi NCR",
                "years": 21,
                "bio": "CABG, valve surgery, complex adult cardiac cases.",
                "languages": "English · Hindi · Arabic support",
                "initials": "AM",
            },
            {
                "name": "Dr. Kavya Srinath",
                "title": "Orthopedic surgeon",
                "hospital": "Meridian Ortho MedCity",
                "specialty": "ortho",
                "city": "Bengaluru",
                "years": 18,
                "bio": "Knee replacement, hip replacement, revision surgery.",
                "languages": "English · Hindi · French support",
                "initials": "KS",
            },
            {
                "name": "Dr. Rohan Nair",
                "title": "Medical oncologist",
                "hospital": "Asteria Heart & Multi-Specialty Institute",
                "specialty": "oncology",
                "city": "Mumbai",
                "years": 16,
                "bio": "Chemotherapy planning, second opinions, tumor board review.",
                "languages": "English · Hindi · Swahili support",
                "initials": "RN",
            },
        ]

        for item in doctors_data:
            Doctor.objects.update_or_create(
                slug=slugify(item["name"]),
                defaults={
                    "name": item["name"],
                    "title": item["title"],
                    "hospital": hospital_map[item["hospital"]],
                    "specialty": specialty_map[item["specialty"]],
                    "city": item["city"],
                    "years_experience": item["years"],
                    "bio": item["bio"],
                    "languages": item["languages"],
                    "initials": item["initials"],
                    "is_sample": True,
                    "is_active": True,
                },
            )

        packages_data = [
            ("CABG surgery plan", "Asteria Heart & Multi-Specialty Institute", "cardiac", "4-6 hospital days"),
            ("Dental implant plan", "NovaDent Global Care", "dental", "OPD visits"),
            ("IVF cycle plan", "BloomBridge Fertility & Women's Health", "fertility", "OPD pathway"),
            ("Knee replacement plan", "Meridian Ortho MedCity", "ortho", "5-7 hospital days"),
        ]

        for name, hospital_name, specialty_code, stay in packages_data:
            TreatmentPackage.objects.update_or_create(
                slug=slugify(name),
                defaults={
                    "name": name,
                    "hospital": hospital_map[hospital_name],
                    "specialty": specialty_map[specialty_code],
                    "typical_stay": stay,
                    "includes": "Doctor consultation, procedure estimate, standard hospital stay, routine diagnostics, airport pickup, interpreter support, coordinator assistance.",
                    "excludes": "Complications, extended stay, donor-related costs, premium rooms, international flights, personal expenses, major plan changes after arrival.",
                    "is_active": True,
                },
            )

        self.stdout.write(self.style.SUCCESS("Seeded FlyCure sample marketplace data."))
