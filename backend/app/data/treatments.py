from decimal import Decimal
from uuid import UUID


def _treatment(
    number: int,
    *,
    name: str,
    specialty: str,
    description: str,
    price: str | None,
    duration_minutes: int | None,
    location: str | None,
    target_area: str | None,
    price_min: str | None = None,
    price_max: str | None = None,
) -> dict[str, object]:
    """Build one deterministic, database-ready catalog record."""

    return {
        "id": UUID(f"{number:08d}-0000-4000-8000-{number:012d}"),
        "name": name,
        "specialty": specialty,
        "description": description,
        "price": Decimal(price) if price is not None else None,
        "price_min": Decimal(price_min) if price_min is not None else None,
        "price_max": Decimal(price_max) if price_max is not None else None,
        "duration_minutes": duration_minutes,
        "location": location,
        "default_target_area": target_area,
        "is_active": True,
    }


# Demonstration catalog requested for the capstone workflow. Stable IDs make repeated
# upserts safe. Exact prices remain null when the supplied data provides only a range.
TREATMENT_SEED_DATA: tuple[dict[str, object], ...] = (
    {
        "id": UUID("11111111-1111-4111-8111-111111111111"),
        "name": "Dermal Fillers",
        "specialty": "Aesthetic Medicine",
        "description": (
            "Targeted hyaluronic acid injections to address facial volume loss, fine lines, "
            "and structural support."
        ),
        "price": Decimal("850.00"),
        "price_min": Decimal("600.00"),
        "price_max": Decimal("1200.00"),
        "duration_minutes": 45,
        "location": "Downtown Medical Center",
        "default_target_area": "Nasolabial Folds",
        "is_active": True,
    },
    {
        "id": UUID("22222222-2222-4222-8222-222222222222"),
        "name": "Laser Resurfacing",
        "specialty": "Dermatology",
        "description": (
            "Fractional non-ablative laser therapy to improve skin texture, stimulate collagen "
            "production, and address mild pigmentation."
        ),
        "price": None,
        "price_min": Decimal("400.00"),
        "price_max": Decimal("800.00"),
        "duration_minutes": 60,
        "location": "Downtown Medical Center",
        "default_target_area": "Face / Skin Texture",
        "is_active": True,
    },
    _treatment(
        3,
        name="General Medical Consultation",
        specialty="General Physician",
        description="General assessment, diagnosis, and initial care planning.",
        price="75.00",
        duration_minutes=30,
        location="Main Clinic",
        target_area="General Health",
    ),
    _treatment(
        4,
        name="Preventive Health Screening",
        specialty="General Physician",
        description="Routine health review with risk-factor and preventive-care assessment.",
        price="120.00",
        duration_minutes=45,
        location="Main Clinic",
        target_area="General Health",
    ),
    _treatment(
        5,
        name="Cardiology Consultation",
        specialty="Cardiology",
        description=(
            "Cardiology consultation for evaluation of cardiovascular symptoms and "
            "assessment of heart health."
        ),
        price=None,
        price_min="100.00",
        price_max="200.00",
        duration_minutes=45,
        location="Heart & Vascular Center",
        target_area="Cardiovascular System",
    ),
    _treatment(
        6,
        name="Electrocardiogram Review",
        specialty="Cardiology",
        description="ECG recording with a clinician interpretation and follow-up plan.",
        price="110.00",
        duration_minutes=30,
        location="Heart Care Center",
        target_area="Heart",
    ),
    _treatment(
        7,
        name="Neurology Consultation",
        specialty="Neurology",
        description=(
            "Neurological consultation for evaluation of headaches, dizziness, nerve-related "
            "symptoms, and other neurological concerns."
        ),
        price=None,
        price_min="100.00",
        price_max="200.00",
        duration_minutes=45,
        location="Specialist Medical Center",
        target_area="Nervous System",
    ),
    _treatment(
        8,
        name="Headache Assessment",
        specialty="Neurology",
        description="Focused evaluation of recurrent headaches and contributing factors.",
        price="165.00",
        duration_minutes=40,
        location="Neuroscience Clinic",
        target_area="Head and Nervous System",
    ),
    _treatment(
        9,
        name="Comprehensive Eye Examination",
        specialty="Ophthalmology",
        description="Vision and ocular-health examination with clinical recommendations.",
        price="95.00",
        duration_minutes=40,
        location="Vision Care Center",
        target_area="Eyes",
    ),
    _treatment(
        10,
        name="Dry Eye Evaluation",
        specialty="Ophthalmology",
        description="Assessment of tear-film health and factors contributing to dry eye.",
        price="85.00",
        duration_minutes=30,
        location="Vision Care Center",
        target_area="Eyes",
    ),
    _treatment(
        11,
        name="Dental Examination and Cleaning",
        specialty="Dentistry",
        description="Oral examination with routine professional dental cleaning.",
        price="130.00",
        duration_minutes=60,
        location="Dental Care Center",
        target_area="Teeth and Gums",
    ),
    _treatment(
        12,
        name="Tooth Restoration",
        specialty="Dentistry",
        description="Assessment and restoration of a damaged or decayed tooth.",
        price="220.00",
        duration_minutes=60,
        location="Dental Care Center",
        target_area="Affected Tooth",
    ),
    _treatment(
        13,
        name="Orthopedic Consultation",
        specialty="Orthopedics",
        description=(
            "Orthopedic assessment for musculoskeletal pain, injuries, and mobility-related "
            "concerns."
        ),
        price=None,
        price_min="100.00",
        price_max="200.00",
        duration_minutes=45,
        location="Specialist Medical Center",
        target_area="Musculoskeletal System",
    ),
    _treatment(
        14,
        name="Joint Mobility Assessment",
        specialty="Orthopedics",
        description="Focused examination of joint function, stability, and range of motion.",
        price="145.00",
        duration_minutes=45,
        location="Musculoskeletal Clinic",
        target_area="Affected Joint",
    ),
    _treatment(
        15,
        name="ENT Consultation",
        specialty="Otolaryngology",
        description="Evaluation of ear, nose, and throat symptoms and conditions.",
        price=None,
        price_min="75.00",
        price_max="150.00",
        duration_minutes=30,
        location="Specialist Medical Center",
        target_area="Ear / Nose / Throat",
    ),
    _treatment(
        16,
        name="Hearing Assessment",
        specialty="ENT",
        description="Clinical hearing evaluation with review of the measured results.",
        price="125.00",
        duration_minutes=45,
        location="ENT Clinic",
        target_area="Ears and Hearing",
    ),
    _treatment(
        17,
        name="Gastroenterology Consultation",
        specialty="Gastroenterology",
        description="Specialist review of digestive symptoms and gastrointestinal history.",
        price="185.00",
        duration_minutes=40,
        location="Digestive Health Center",
        target_area="Digestive System",
    ),
    _treatment(
        18,
        name="Digestive Health Follow-up",
        specialty="Gastroenterology",
        description="Follow-up review of symptoms, investigations, and the current care plan.",
        price="125.00",
        duration_minutes=30,
        location="Digestive Health Center",
        target_area="Digestive System",
    ),
    _treatment(
        19,
        name="Gynecology Consultation",
        specialty="Gynecology",
        description="Confidential specialist assessment of gynecological health concerns.",
        price="175.00",
        duration_minutes=40,
        location="Women's Health Center",
        target_area="Reproductive Health",
    ),
    _treatment(
        20,
        name="Women's Preventive Health Visit",
        specialty="Gynecology",
        description="Preventive health review and age-appropriate screening discussion.",
        price="155.00",
        duration_minutes=45,
        location="Women's Health Center",
        target_area="Women's Health",
    ),
    _treatment(
        21,
        name="General Physician Consultation",
        specialty="General Medicine",
        description=(
            "General medical consultation for evaluating common symptoms, health concerns, "
            "and determining the appropriate next step."
        ),
        price=None,
        price_min="50.00",
        price_max="100.00",
        duration_minutes=30,
        location="Main Medical Clinic",
        target_area="General Health",
    ),
    _treatment(
        22,
        name="Comprehensive Dental Examination",
        specialty="Dentistry",
        description=(
            "Comprehensive dental examination including assessment of teeth, gums, and "
            "overall oral health."
        ),
        price=None,
        price_min="50.00",
        price_max="100.00",
        duration_minutes=30,
        location="Dental Care Center",
        target_area="Oral Health",
    ),
    _treatment(
        23,
        name="Professional Dental Cleaning",
        specialty="Dentistry",
        description=(
            "Professional cleaning to remove plaque and tartar and support overall dental "
            "and gum health."
        ),
        price=None,
        price_min="80.00",
        price_max="150.00",
        duration_minutes=45,
        location="Dental Care Center",
        target_area="Teeth / Gums",
    ),
    _treatment(
        24,
        name="Dental Filling",
        specialty="Dentistry",
        description=(
            "Restorative dental procedure for treating cavities and restoring the affected "
            "tooth."
        ),
        price=None,
        price_min="100.00",
        price_max="250.00",
        duration_minutes=45,
        location="Dental Care Center",
        target_area="Tooth",
    ),
    _treatment(
        25,
        name="ECG Examination",
        specialty="Cardiology",
        description=(
            "Electrocardiogram examination used to evaluate the electrical activity and "
            "rhythm of the heart."
        ),
        price=None,
        price_min="40.00",
        price_max="80.00",
        duration_minutes=20,
        location="Heart & Vascular Center",
        target_area="Heart",
    ),
    _treatment(
        26,
        name="Dermatology Consultation",
        specialty="Dermatology",
        description="Dermatology consultation for evaluation of skin, hair, and nail conditions.",
        price=None,
        price_min="75.00",
        price_max="150.00",
        duration_minutes=30,
        location="Downtown Medical Center",
        target_area="Skin / Hair / Nails",
    ),
    _treatment(
        27,
        name="Ophthalmology Consultation",
        specialty="Ophthalmology",
        description=(
            "Eye examination and ophthalmology consultation for evaluating vision and common "
            "eye-related concerns."
        ),
        price=None,
        price_min="75.00",
        price_max="150.00",
        duration_minutes=30,
        location="Vision Care Center",
        target_area="Eyes",
    ),
    _treatment(
        28,
        name="Physiotherapy Assessment",
        specialty="Physiotherapy",
        description=(
            "Initial assessment of movement, mobility, strength, and functional limitations "
            "to develop an appropriate therapy plan."
        ),
        price=None,
        price_min="60.00",
        price_max="120.00",
        duration_minutes=45,
        location="Rehabilitation Center",
        target_area="Musculoskeletal System",
    ),
    _treatment(
        29,
        name="Nutrition Consultation",
        specialty="Nutrition",
        description=(
            "Nutrition assessment and consultation for developing an individualized dietary "
            "and wellness plan."
        ),
        price=None,
        price_min="50.00",
        price_max="100.00",
        duration_minutes=45,
        location="Wellness Center",
        target_area="Nutrition / Wellness",
    ),
)
