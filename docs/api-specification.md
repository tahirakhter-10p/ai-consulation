# AI Consultation Platform

# API Specification

Version: 1.0

Status: Draft

---

# 1. Overview

## Purpose

This document defines the REST APIs required for the AI Consultation Platform.

It includes:

- Endpoint definitions
- Request validation
- Response structure
- HTTP status codes
- Error handling
- Database interactions
- Requirement mapping

The API specification implements the requirements defined in:

```text
requirements.md
```

The API layer exposes the application functionality required by the consultation workflow:

```text
Consultation
    ↓
Messages
    ↓
Recommendation
    ↓
Appointment
```

The frontend displays the persisted Recommendation through the:

**Consultation Summary** screen.

---

# 2. API Standards

## Base URL

```text
/api/v1
```

---

## Content Type

```text
application/json
```

---

## Authentication

Authentication is outside the scope of this assessment.

---

# 3. Response Format

## Success Response

```json
{
  "success": true,
  "message": "Operation completed successfully.",
  "data": {}
}
```

---

## Error Response

```json
{
  "success": false,
  "message": "Validation failed.",
  "errors": [
    {
      "field": "patient_name",
      "message": "Patient name is required."
    }
  ]
}
```

---

# 4. Dashboard APIs

## 4.1 Get Dashboard Statistics

```http
GET /dashboard
```

### Description

Returns the statistics displayed on the Dashboard.

### Response

```http
200 OK
```

```json
{
  "success": true,
  "message": "Dashboard statistics retrieved successfully.",
  "data": {
    "total_consultations": 20,
    "booked_appointments": 12,
    "conversion_rate": 60
  }
}
```

### Database Operations

Read:

- `consultations`
- `appointments`

### Related Requirements

- FR-001

---

# 5. Consultation APIs

## 5.1 Create Consultation

```http
POST /consultations
```

### Description

Creates a new consultation session.

### Request

```json
{
  "patient_name": "John Doe",
  "primary_concern": "Chest pain"
}
```

### Response

```http
201 Created
```

```json
{
  "success": true,
  "message": "Consultation created successfully.",
  "data": {
    "id": "UUID",
    "patient_name": "John Doe",
    "primary_concern": "Chest pain",
    "status": "Pending"
  }
}
```

### Validation

- `patient_name` is required.
- `primary_concern` is required.

### Database Operations

Create:

- `consultations`

### Related Requirements

This endpoint supports the consultation lifecycle required by the application.

---

## 5.2 Get Consultations

```http
GET /consultations
```

### Description

Returns consultation records.

### Query Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| search | No | Search by patient name |
| status | No | Filter by Pending, Booked, or Completed |

### Response

```http
200 OK
```

```json
{
  "success": true,
  "message": "Consultations retrieved successfully.",
  "data": [
    {
      "id": "UUID",
      "patient_name": "John Doe",
      "primary_concern": "Chest pain",
      "recommended_procedure": "Pending",
      "status": "Pending"
    }
  ]
}
```

### Database Operations

Read:

- `consultations`
- Recommendation data when required for `recommended_procedure`

### Related Requirements

- FR-003
- FR-004
- FR-005

---

## 5.3 Get Consultation Details

```http
GET /consultations/{consultation_id}
```

### Description

Returns a single consultation and its relevant persisted information.

### Response

```http
200 OK
```

```json
{
  "success": true,
  "message": "Consultation retrieved successfully.",
  "data": {
    "id": "UUID",
    "patient_name": "John Doe",
    "primary_concern": "Chest pain",
    "status": "Pending"
  }
}
```

### Database Operations

Read:

- `consultations`

Related messages, recommendation, and appointment information may be retrieved through their dedicated APIs.

### Related Requirements

- FR-006

---

## 5.4 Update Consultation Status

```http
PATCH /consultations/{consultation_id}
```

### Description

Updates the consultation status.

### Request

```json
{
  "status": "Booked"
}
```

### Response

```http
200 OK
```

```json
{
  "success": true,
  "message": "Consultation updated successfully.",
  "data": {
    "id": "UUID",
    "status": "Booked"
  }
}
```

### Validation

Allowed statuses:

- Pending
- Booked
- Completed

### Database Operations

Update:

- `consultations`

### Notes

Appointment booking automatically updates the consultation status to `Booked`.

This endpoint is also available for consultation lifecycle management where required by the application.

---

# 6. Chat APIs

## 6.1 Get Conversation

```http
GET /consultations/{consultation_id}/messages
```

### Description

Returns the complete conversation history for a consultation.

### Response

```http
200 OK
```

```json
{
  "success": true,
  "message": "Conversation retrieved successfully.",
  "data": [
    {
      "id": "UUID",
      "role": "user",
      "content": "I have headaches.",
      "created_at": "2026-08-10T10:00:00Z"
    },
    {
      "id": "UUID",
      "role": "assistant",
      "content": "Can you describe the symptoms?",
      "created_at": "2026-08-10T10:00:01Z"
    }
  ]
}
```

### Database Operations

Read:

- `consultation_messages`

### Related Requirements

- FR-008
- FR-009

---

## 6.2 Send Message

```http
POST /consultations/{consultation_id}/messages
```

### Description

Sends a user message and returns the AI response.

### Request

```json
{
  "message": "I have headaches for two days."
}
```

### Processing Flow

```text
1. Validate request.
2. Verify consultation exists.
3. Save user message.
4. Load previous conversation.
5. Provide conversation context to AI.
6. Generate AI response.
7. Save AI response.
8. Return both messages.
```

### Response

```http
200 OK
```

```json
{
  "success": true,
  "message": "Message processed successfully.",
  "data": {
    "user_message": {
      "id": "UUID",
      "role": "user",
      "content": "I have headaches for two days."
    },
    "assistant_message": {
      "id": "UUID",
      "role": "assistant",
      "content": "Can you describe the pain?"
    }
  }
}
```

### Database Operations

Create:

- User message
- Assistant message

Read:

- Previous consultation messages

### AI Operations

- Load conversation context
- Generate context-aware response

### Related Requirements

- FR-007
- FR-008
- FR-009
- FR-010

---

# 7. Recommendation APIs

## 7.1 Generate Recommendation

```http
POST /consultations/{consultation_id}/recommendation
```

### Description

Generates a structured recommendation from the consultation conversation.

The generated Recommendation is persisted in the database.

The Recommendation is later displayed by the frontend through the:

**Consultation Summary** screen.

### Processing Flow

```text
1. Validate consultation.
2. Verify consultation exists.
3. Load consultation messages.
4. Load the authoritative Treatment catalog.
5. Send conversation context and allowed treatment IDs to AI Service.
6. Validate that the AI selected one or two distinct catalog IDs.
7. Build treatment metadata snapshots from database rows.
8. Persist Recommendation.
9. Return Recommendation.
```

### Response

```http
201 Created
```

```json
{
  "success": true,
  "message": "Recommendation generated successfully.",
  "data": {
    "id": "UUID",
    "consultation_id": "UUID",
    "patient_summary": "Patient reports recurring headaches for two days.",
    "recommended_treatments": [
      {
        "treatment_id": "11111111-1111-4111-8111-111111111111",
        "name": "Dermal Fillers",
        "specialty": "Dermatology",
        "description": "Injectable fillers restore volume and soften facial lines.",
        "price": "850.00",
        "price_min": "600.00",
        "price_max": "1200.00",
        "duration_minutes": 45,
        "location": "Downtown Medical Center (Primary)",
        "default_target_area": "Nasolabial Folds",
        "priority": 1
      }
    ],
    "ai_reasoning": "Optional AI reasoning."
  }
}
```

### Database Operations

Read:

- `consultations`
- `consultation_messages`
- `treatments`

Create:

- `recommendations`

### AI Operations

- Generate structured recommendation
- Generate patient summary
- Generate recommended treatments
- Optionally generate AI reasoning

### Related Requirements

- FR-011
- FR-012

---

## 7.2 Get Recommendation

```http
GET /consultations/{consultation_id}/recommendation
```

### Description

Returns the persisted Recommendation for a consultation.

The frontend uses this response to display the:

**Consultation Summary** screen.

The API does not regenerate the recommendation.

### Response

```http
200 OK
```

```json
{
  "success": true,
  "message": "Recommendation retrieved successfully.",
  "data": {
    "id": "UUID",
    "consultation_id": "UUID",
    "patient_summary": "Patient reports recurring headaches for two days.",
    "recommended_treatments": [
      {
        "treatment_id": "11111111-1111-4111-8111-111111111111",
        "name": "Dermal Fillers",
        "specialty": "Dermatology",
        "description": "Injectable fillers restore volume and soften facial lines.",
        "price": "850.00",
        "duration_minutes": 45,
        "location": "Downtown Medical Center (Primary)",
        "priority": 1
      }
    ],
    "ai_reasoning": "Optional AI reasoning."
  }
}
```

### Database Operations

Read:

- `recommendations`

### Related Requirements

- FR-011
- FR-012

---

# 8. Treatment and Appointment APIs

## 8.1 Get Treatment Catalog

```http
GET /treatments
```

Returns active authoritative treatment metadata, including specialty and lifecycle
status. Unknown operational values are returned as `null`; the API does not synthesize
missing PDF data.

## 8.2 Book Appointment

```http
POST /consultations/{consultation_id}/appointment
```

### Description

Creates an appointment for a consultation.

### Request

```json
{
  "treatment_id": "11111111-1111-4111-8111-111111111111",
  "appointment_datetime": "2026-08-10T14:00:00Z",
  "location": "Downtown Medical Center (Primary)"
}
```

For compatibility, `treatment` may be supplied instead of `treatment_id`; it must
case-insensitively match an existing catalog name. Arbitrary treatment strings are
rejected.

### Processing Flow

```text
1. Validate request.
2. Verify consultation exists.
3. Validate selected treatment.
4. Create appointment.
5. Update consultation status to Booked.
6. Return appointment.
```

### Response

```http
201 Created
```

```json
{
  "success": true,
  "message": "Appointment booked successfully.",
  "data": {
    "appointment_id": "UUID",
    "consultation_id": "UUID",
    "treatment_id": "11111111-1111-4111-8111-111111111111",
    "treatment": "Dermal Fillers",
    "specialty": "Dermatology",
    "treatment_description": "Injectable fillers restore volume and soften facial lines.",
    "default_target_area": "Nasolabial Folds",
    "appointment_datetime": "2026-08-10T14:00:00Z",
    "location": "Downtown Medical Center (Primary)",
    "price": "850.00",
    "duration_minutes": 45,
    "status": "Booked"
  }
}
```

### Database Operations

Create:

- `appointments`

Read:

- `treatments`

Update:

- `consultations.status`

### Related Requirements

- FR-013
- FR-014
- FR-015
- FR-016
- FR-017

---

## 8.3 Get Appointments

```http
GET /appointments
```

### Description

Returns appointments.

This endpoint can be used by application screens that need appointment data.

### Response

```http
200 OK
```

```json
{
  "success": true,
  "message": "Appointments retrieved successfully.",
  "data": []
}
```

### Database Operations

Read:

- `appointments`

### Scope

This is a supporting API. The assessment specifically requires appointment booking; listing appointments is not a separate mandatory functional requirement.

---

# 9. HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Successful request |
| 201 | Resource created |
| 400 | Validation error |
| 404 | Resource not found |
| 409 | Resource conflict |
| 500 | Internal server error |

---

# 10. Validation Rules

## Consultation

- Patient name is required.
- Primary concern is required.

---

## Chat

- Message cannot be empty.
- Consultation must exist.

---

## Recommendation

- Consultation must exist.
- Consultation must have conversation data before recommendation generation.
- AI output must satisfy the expected structured response schema.

---

## Appointment

- Treatment is required.
- Appointment date/time is required.
- Location is required.
- Consultation must exist.
- A consultation cannot have more than one appointment within the current workflow.

---

# 11. API to Database Mapping

| API | Tables |
|-----|--------|
| GET /dashboard | consultations, appointments |
| GET /treatments | treatments |
| POST /consultations | consultations |
| GET /consultations | consultations, recommendations |
| GET /consultations/{id} | consultations |
| PATCH /consultations/{id} | consultations |
| GET /consultations/{id}/messages | consultation_messages |
| POST /consultations/{id}/messages | consultation_messages |
| POST /consultations/{id}/recommendation | consultations, consultation_messages, treatments, recommendations |
| GET /consultations/{id}/recommendation | recommendations |
| POST /consultations/{id}/appointment | treatments, appointments, consultations |
| GET /appointments | appointments |

---

# 12. Requirement Traceability

The following mappings use the requirement identifiers defined in:

```text
requirements.md
```

| Requirement | API |
|-------------|-----|
| FR-001 | GET /dashboard |
| FR-002 | Frontend navigation |
| FR-003 | GET /consultations |
| FR-004 | GET /consultations?status=... |
| FR-005 | GET /consultations?search=... |
| FR-006 | GET /consultations/{consultation_id} |
| FR-007 | POST /consultations/{consultation_id}/messages |
| FR-008 | GET /consultations/{consultation_id}/messages |
| FR-009 | POST /consultations/{consultation_id}/messages |
| FR-010 | POST /consultations/{consultation_id}/messages |
| FR-011 | POST /consultations/{consultation_id}/recommendation |
| FR-012 | POST /consultations/{consultation_id}/recommendation |
| FR-013 | POST /consultations/{consultation_id}/appointment |
| FR-014 | POST /consultations/{consultation_id}/appointment |
| FR-015 | POST /consultations/{consultation_id}/appointment |
| FR-016 | POST /consultations/{consultation_id}/appointment |
| FR-017 | POST /consultations/{consultation_id}/appointment |

Some requirements are primarily frontend behavior and therefore do not map to a dedicated backend API.

---

# 13. API Error Scenarios

## Consultation Not Found

```http
404 Not Found
```

```json
{
  "success": false,
  "message": "Consultation not found.",
  "errors": []
}
```

---

## Recommendation Not Found

```http
404 Not Found
```

```json
{
  "success": false,
  "message": "Recommendation not found.",
  "errors": []
}
```

---

## Invalid Request

```http
400 Bad Request
```

```json
{
  "success": false,
  "message": "Validation failed.",
  "errors": [
    {
      "field": "message",
      "message": "Message cannot be empty."
    }
  ]
}
```

---

## Appointment Already Exists

```http
409 Conflict
```

```json
{
  "success": false,
  "message": "An appointment already exists for this consultation.",
  "errors": []
}
```

---

## AI Generation Failure

```http
500 Internal Server Error
```

```json
{
  "success": false,
  "message": "Unable to generate recommendation.",
  "errors": []
}
```

The actual implementation may use a more specific error classification where appropriate.

---

# 14. API Layer Responsibilities

API routers should only:

- Receive HTTP requests
- Validate request schemas
- Resolve dependencies
- Invoke application services
- Return HTTP responses

Business logic must remain in the service layer.

For example:

```text
POST /consultations/{id}/recommendation
              │
              ▼
Recommendation Router
              │
              ▼
Recommendation Service
              │
       ┌──────┴───────┐
       ▼              ▼
  AI Service     Recommendation
                     Repository
       │                  │
       ▼                  ▼
      LLM             PostgreSQL
```

---

# 15. Recommendation vs Consultation Summary

The API uses **Recommendation** as the backend/domain resource.

The frontend uses **Consultation Summary** as the presentation screen.

```text
Backend:

Recommendation
    │
    ├── patient_summary
    ├── recommended_treatments
    └── ai_reasoning
             │
             ▼
Frontend:

Consultation Summary
```

Therefore the API endpoints are:

```http
POST /consultations/{id}/recommendation
GET  /consultations/{id}/recommendation
```

and not:

```http
POST /consultations/{id}/summary
GET  /consultations/{id}/summary
```

The Summary screen consumes the Recommendation data.

---

# 16. End-to-End API Flow

```text
1. Create Consultation

POST /consultations
        ↓
consultations


2. Send Messages

POST /consultations/{id}/messages
        ↓
consultation_messages


3. Generate Recommendation

POST /consultations/{id}/recommendation
        ↓
AI Service
        ↓
LLM
        ↓
recommendations


4. Display Consultation Summary

GET /consultations/{id}/recommendation
        ↓
recommendations
        ↓
Consultation Summary UI


5. Book Appointment

POST /consultations/{id}/appointment
        ↓
appointments
        +
consultations.status = Booked


6. Return to Consultation Records

GET /consultations
        ↓
Updated consultation status
```
