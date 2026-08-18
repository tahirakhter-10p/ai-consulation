# AI Consultation Platform

# Database Design

Version: 1.1

Status: Implemented

---

# 1. Overview

## Purpose

This document defines the relational database design for the AI Consultation Platform.

It includes:

- Database technology
- Design principles
- Entity definitions
- Relationships
- Constraints
- Indexes
- Naming conventions
- Persistence flow

The database design supports the requirements defined in:

```text
requirements.md
```

The database is responsible for persisting the consultation workflow, including:

- Consultations
- Messages
- Recommendations
- Appointments
- Treatments

---

# 2. Database Technology

| Item | Value |
|------|-------|
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.0 (Async) |
| Migration Tool | Alembic |
| Primary Key Type | UUID |
| Timestamp Type | TIMESTAMP WITH TIME ZONE |

These technologies are implementation decisions for this project.

---

# 3. Design Principles

The database follows these principles:

- Normalized relational design
- UUID primary keys
- Foreign key constraints
- Referential integrity
- UTC timestamps
- Minimal redundancy
- Clear relationships between consultation data
- Simple schema focused on assessment requirements
- Persistent consultation state

---

# 4. Entity Relationship Diagram

```text
                         Consultation
                         ┌───────────────┐
                         │ id            │
                         │ patient_name  │
                         │ concern       │
                         │ status        │
                         └───────┬───────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
        Messages          Recommendation      Appointment
                                 │                  │
                                 │                  │
                                 ▼                  ▼
                            Treatments <────────────┘
```

The relationships are independent child relationships from the consultation.

```text
Consultation
    │
    ├── Messages
    │
    ├── Recommendation
    │       │
    │       └── Selected Treatments
    │
    └── Appointment
            │
            └── Treatment
```

Relationship Summary:

- One Consultation has many Messages.
- One Consultation has one persisted Recommendation.
- One Consultation can have one Appointment within the current workflow.
- One Treatment can be referenced by many Appointments.

The one-to-one Recommendation and Appointment relationships are implementation decisions for the current assessment workflow.

---

# 5. Database Tables

---

## 5.1 consultations

Stores the consultation session.

### Columns

| Column | Type | Nullable | Description |
|---------|------|----------|-------------|
| id | UUID | No | Primary Key |
| patient_name | VARCHAR(255) | No | Patient name |
| primary_concern | TEXT | No | Reason for consultation |
| status | ENUM | No | Consultation status |
| created_at | TIMESTAMP WITH TIME ZONE | No | Creation time |
| updated_at | TIMESTAMP WITH TIME ZONE | No | Last modification |

### Status Values

- Pending
- Booked
- Completed

---

## 5.2 consultation_messages

Stores the conversation between the administrator and AI.

### Columns

| Column | Type | Nullable | Description |
|---------|------|----------|-------------|
| id | UUID | No | Primary Key |
| consultation_id | UUID | No | FK → consultations.id |
| role | ENUM | No | Message sender role |
| content | TEXT | No | Message content |
| created_at | TIMESTAMP WITH TIME ZONE | No | Message timestamp |

### Role Values

- user
- assistant

The messages table allows a consultation to contain multiple user and AI messages and preserves the conversation history required for context-aware AI interaction.

---

## 5.3 recommendations

Stores the structured recommendation generated from the consultation conversation.

A Recommendation is the backend/domain entity.

The **Consultation Summary** is the frontend screen that displays this recommendation.

### Columns

| Column | Type | Nullable | Description |
|---------|------|----------|-------------|
| id | UUID | No | Primary Key |
| consultation_id | UUID | No | FK → consultations.id |
| patient_summary | TEXT | No | AI-generated summary of the consultation |
| recommended_treatments | JSONB | No | Structured recommended treatments |
| ai_reasoning | TEXT | Yes | Optional AI reasoning |
| created_at | TIMESTAMP WITH TIME ZONE | No | Creation timestamp |
| updated_at | TIMESTAMP WITH TIME ZONE | No | Last modification |

### Recommended Treatments

`recommended_treatments` remains JSONB for compatibility. New recommendations store
an immutable snapshot assembled from authoritative Treatment rows; the AI selects only
treatment IDs and does not provide catalog metadata.

Example:

```json
[
  {
    "treatment_id": "11111111-1111-4111-8111-111111111111",
    "name": "Dermal Fillers",
    "description": "Injectable fillers restore volume and soften facial lines.",
    "price": "850.00",
    "price_min": "600.00",
    "price_max": "1200.00",
    "duration_minutes": 45,
    "location": "Downtown Medical Center (Primary)",
    "default_target_area": "Nasolabial Folds",
    "priority": 1
  }
]
```

The exact structure will be enforced through the application/API schema.

### AI Reasoning

`ai_reasoning` is optional.

It may contain the reasoning or explanation returned by the AI model when available.

---

## 5.4 appointments

Stores booked appointments.

### Columns

| Column               | Type                     | Nullable | Description                                       |
| -------------------- | ------------------------ | -------- | ------------------------------------------------- |
| id                   | UUID                     | No       | Primary Key                                       |
| consultation_id      | UUID                     | No       | FK → consultations.id                             |
| treatment_id         | UUID                     | Yes      | FK → treatments.id; nullable for legacy rows      |
| treatment            | VARCHAR(255)             | No       | Compatibility snapshot of selected treatment name |
| appointment_datetime | TIMESTAMP WITH TIME ZONE | No       | Appointment date and time                         |
| location             | VARCHAR(255)             | No       | Clinic/location                                   |
| created_at           | TIMESTAMP WITH TIME ZONE | No       | Creation timestamp                                |
| updated_at           | TIMESTAMP WITH TIME ZONE | No       | Last modification                                 |


---

## 5.5 treatments

Stores the authoritative treatment catalog used by recommendation generation and appointment booking.

| Column               | Type                     | Nullable | Description                                       |
| -------------------- | ------------------------ | -------- | ------------------------------------------------- |
| id                   | UUID                     | No       | Primary Key                                       |
| consultation_id      | UUID                     | No       | FK → consultations.id                             |
| treatment_id         | UUID                     | Yes      | FK → treatments.id; nullable for legacy rows      |
| treatment            | VARCHAR(255)             | No       | Compatibility snapshot of selected treatment name |
| appointment_datetime | TIMESTAMP WITH TIME ZONE | No       | Appointment date and time                         |
| location             | VARCHAR(255)             | No       | Clinic/location                                   |
| created_at           | TIMESTAMP WITH TIME ZONE | No       | Creation timestamp                                |
| updated_at           | TIMESTAMP WITH TIME ZONE | No       | Last modification                                 |


The treatments table is the authoritative source for treatment information displayed throughout the recommendation and booking workflow.

Treatment information includes:

Treatment name
Specialty
Description
Price
Price range
Duration
Location
Target area
Active/inactive status

---

# 6. Relationships

## 6.1 Consultation → Messages

Relationship:

**One-to-Many**

```text
Consultation
     │
     └──< Messages
```

A consultation may contain multiple chat messages.

Example:

```text
Consultation
    │
    ├── User Message
    ├── Assistant Message
    ├── User Message
    └── Assistant Message
```

---

## 6.2 Consultation → Recommendation

Relationship:

**One-to-One**

```text
Consultation
     │
     └──── Recommendation
```

A consultation has one persisted recommendation in the current workflow.

The recommendation contains:

- Patient summary
- Recommended treatments
- Optional AI reasoning

The frontend presents this information through the:

**Consultation Summary** screen.

---

## 6.3 Consultation → Appointment

Relationship:

**One-to-One**

```text
Consultation
     │
     └──── Appointment
```

A consultation can have one appointment within the current assessment workflow.

When the appointment is successfully created, the consultation status is updated to:

```text
Booked
```

## 6.4 Treatment → Appointment

Relationship: **One-to-Many**

New appointments reference an authoritative Treatment. The foreign key is nullable
only so appointments created before migration `0006` remain readable.

---

# 7. Constraints

## 7.1 consultations

- Primary Key on `id`
- `patient_name` cannot be NULL
- `primary_concern` cannot be NULL
- `status` cannot be NULL

---

## 7.2 consultation_messages

- Primary Key on `id`
- `consultation_id` cannot be NULL
- `role` cannot be NULL
- `content` cannot be NULL
- `consultation_id` must reference an existing consultation

---

## 7.3 recommendations

- Primary Key on `id`
- `consultation_id` cannot be NULL
- `consultation_id` must reference an existing consultation
- One recommendation per consultation
- `patient_summary` cannot be NULL
- `recommended_treatments` cannot be NULL
- `ai_reasoning` may be NULL

---

## 7.4 appointments

- Primary Key on `id`
- `consultation_id` cannot be NULL
- `consultation_id` must reference an existing consultation
- One appointment per consultation
- `treatment` cannot be NULL
- New bookings must resolve `treatment_id` to an existing treatment
- `appointment_datetime` cannot be NULL
- `location` cannot be NULL

## 7.5 treatments

- Primary Key on `id`
- `name` is unique and non-empty
- `description` is non-empty
- `specialty` is non-empty
- Monetary values cannot be negative
- Range minimum cannot exceed range maximum
- Duration, when present, must be positive

---

# 8. Foreign Keys

## consultation_messages

```text
consultation_messages.consultation_id
            ↓
consultations.id
```

---

## recommendations

```text
recommendations.consultation_id
            ↓
consultations.id
```

---

## appointments

```text
appointments.consultation_id
            ↓
consultations.id
```

```text
appointments.treatment_id
            ↓
treatments.id
```

---

# 9. Indexes

## consultations

- Primary Key: `id`
- Index: `status`
- Index: `patient_name`

---

## consultation_messages

- Primary Key: `id`
- Index: `consultation_id`

An index on `(consultation_id, created_at)` may also be used to efficiently retrieve a consultation's messages in chronological order.

---

## recommendations

- Primary Key: `id`
- Unique constraint/index: `consultation_id`

---

## appointments

- Primary Key: `id`
- Unique constraint/index: `consultation_id`
- Index: `treatment_id`

## treatments

- Primary Key: `id`
- Unique index: `name`
- Index: `specialty`
- Index: `is_active`

---

# 10. Cascade Behavior

A consultation owns the associated messages, recommendation, and appointment within the current data model.

When a consultation is deleted, its dependent records should be deleted:

```text
Consultation
    │
    ├── Messages        → CASCADE DELETE
    │
    ├── Recommendation  → CASCADE DELETE
    │
    └── Appointment     → CASCADE DELETE
```

The cascade should be implemented consistently at the SQLAlchemy relationship and/or database foreign-key level.

---

# 11. Naming Conventions

## Tables

Use plural snake_case names.

Examples:

```text
consultations
consultation_messages
recommendations
appointments
treatments
```

---

## Primary Keys

Use:

```text
id
```

---

## Foreign Keys

Use:

```text
<entity>_id
```

Example:

```text
consultation_id
```

---

## Timestamps

Use:

```text
created_at
updated_at
```

All timestamps should be stored with timezone information and handled consistently as UTC.

---

# 12. Enumerations

## ConsultationStatus

| Value |
|------|
| Pending |
| Booked |
| Completed |

---

## MessageRole

| Value |
|------|
| user |
| assistant |

---

# 13. Migration Order

The migration order should respect foreign-key dependencies.

### Migration 001

Create:

```text
consultations
```

---

### Migration 002

Create:

```text
consultation_messages
```

with:

```text
consultation_id → consultations.id
```

---

### Migration 003

Create:

```text
recommendations
```

with:

```text
consultation_id → consultations.id
```

---

### Migration 004

Create:

```text
appointments
```

with:

```text
consultation_id → consultations.id
```

---

### Migration 005

Add `updated_at` to recommendations and appointments and align their existing
schemas with the persisted recommendation workflow.

---

### Migration 006

Create `treatments`, seed the two PDF-backed catalog records, add nullable
`appointments.treatment_id`, backfill matching legacy names, and add the treatment
foreign key and index.

---

### Migration 007

Add required `specialty` and `is_active` fields plus their constraints and indexes.
The repeatable seed command expands the development catalog after the migration.

---

# 14. Expected Data Flow

The database persistence flow follows the consultation lifecycle.

```text
Create Consultation
        ↓
Store Consultation
        ↓
Store Chat Messages
        ↓
Generate Recommendation
        ↓
Store Recommendation
        ↓
Book Appointment
        ↓
Store Appointment
        ↓
Update Consultation Status
```

The recommendation is generated from the persisted consultation conversation.

The Consultation Summary UI retrieves the persisted recommendation.

---

# 15. Recommendation Persistence Flow

The recommendation generation process is:

```text
Consultation
      ↓
Load Messages
      ↓
AI Service
      ↓
LLM
      ↓
Structured Recommendation
      ↓
Validate Output
      ↓
Save Recommendation
      ↓
PostgreSQL
```

The persisted recommendation contains:

```text
Recommendation
├── Patient Summary
├── Recommended Treatments
└── AI Reasoning (Optional)
```

The recommendation is not regenerated merely because the Consultation Summary screen is opened.

---

# 16. SQLAlchemy Models

The following ORM models will be implemented:

- `Consultation`
- `ConsultationMessage`
- `Recommendation`
- `Appointment`
- `Treatment`

Each model will use:

- UUID primary key
- SQLAlchemy relationships
- Async SQLAlchemy
- Appropriate constraints
- Automatic timestamps

The `Recommendation` model represents the persisted recommendation domain entity.

The `Consultation Summary` is a frontend presentation of the Recommendation and is not a separate database entity.

---

# 17. Future Considerations

The current schema is intentionally limited to the assessment scope.

Additional entities such as:

- Users
- Doctors
- Departments
- Attachments
- Notifications

are outside the current implementation scope.

Future entities can be introduced when required by future product requirements.
