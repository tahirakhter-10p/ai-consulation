# AI Consultation Platform

# Backend Architecture

Version: 1.1

Status: Implemented

---

# 1. Overview

## Purpose

This document defines the backend architecture of the AI Consultation Platform.

It describes:

- Project structure
- Layer responsibilities
- Request lifecycle
- Dependency Injection
- Repository Pattern
- AI integration
- Validation
- Exception handling
- Logging
- Configuration management

The backend is implemented using FastAPI and follows a layered architecture to ensure maintainability, readability, testability, and separation of concerns.

The backend architecture implements the requirements defined in:

```text
requirements.md
```

and follows the system architecture defined in:

```text
system-architecture.md
```

---

# 2. Technology Stack

| Technology | Purpose |
|------------|---------|
| FastAPI | REST API Framework |
| SQLAlchemy 2.0 | ORM |
| PostgreSQL | Database |
| Alembic | Database Migrations |
| Pydantic v2 | Request and response validation |
| Uvicorn | ASGI Server |

The AI provider is accessed through an application-level AI abstraction.

The current implementation may use a real AI provider such as OpenAI or a mocked provider.

---

# 3. Project Structure

```text
backend/
│
├── app/
│   │
│   ├── api/
│   │   ├── dashboard.py
│   │   ├── consultations.py
│   │   ├── messages.py
│   │   ├── recommendations.py
│   │   ├── appointments.py
│   │   └── treatment.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   ├── constants.py
│   │   └── exceptions.py
│   │
│   ├── database/
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── models/
│   │   ├── base_model.py
│   │   ├── consultation.py
│   │   ├── consultation_message.py
│   │   ├── recommendation.py
│   │   ├── appointment.py
│   │   └── treatment.py
│   │
│   ├── schemas/
│   │   ├── consultation.py
│   │   ├── message.py
│   │   ├── recommendation.py
│   │   ├── appointment.py
│   │   ├── treatment.py
│   │   └── common.py
│   │
│   ├── repositories/
│   │   ├── consultation_repository.py
│   │   ├── message_repository.py
│   │   ├── recommendation_repository.py
│   │   ├── appointment_repository.py
│   │   └── treatment_repository.py
│   │
│   ├── services/
│   │   ├── dashboard_service.py
│   │   ├── consultation_service.py
│   │   ├── recommendation_service.py
│   │   ├── appointment_service.py
│   │   └── treatment_service.py
│   │
│   ├── ai/
│   │   ├── providers/
│   │   │   └── ai_provider.py
│   │   │
│   │   ├── prompts/
│   │   │   ├── consultation.py
│   │   │   └── recommendation.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── chat.py
│   │   │   └── recommendation.py
│   │   │
│   │   └── service.py
│   │
│   ├── dependencies/
│   │
│   ├── utils/
│   │
│   └── main.py
│
├── tests/
│
├── alembic/
│
├── requirements.txt
│
└── .env
```

---

# 4. Layered Architecture

The backend follows a layered architecture:

```text
Client

↓

API Router

↓

Service Layer

↓

Repository Layer

↓

Database
```

AI interaction is coordinated by the service layer:

```text
Service Layer
      │
      ▼
  AI Service
      │
      ▼
  AI Provider
      │
      ▼
     LLM
```

Each layer has a clearly defined responsibility.

---

# 5. Layer Responsibilities

## API Layer

Responsibilities:

- Define REST endpoints
- Receive HTTP requests
- Validate request payloads
- Resolve dependencies
- Invoke application services
- Return HTTP responses

The API layer does not contain business logic.

---

## Service Layer

Responsibilities:

- Implement business rules
- Coordinate repositories
- Coordinate AI interactions
- Manage consultation workflows
- Generate recommendations
- Coordinate appointment booking
- Manage consultation status transitions

Primary services:

- `DashboardService`
- `ConsultationService`
- `RecommendationService`
- `AppointmentService`

---

## Repository Layer

Responsibilities:

- Execute database queries
- Create records
- Retrieve records
- Update records
- Delete records where required

Repositories contain persistence logic only.

Repositories do not contain application business rules.

---

## Database Layer

Responsibilities:

- SQLAlchemy models
- Entity relationships
- Database sessions
- Transactions
- Database configuration

---

## AI Layer

Responsibilities:

- Generate context-aware consultation responses
- Generate structured recommendations
- Validate AI output through structured schemas
- Communicate with the configured AI provider

The AI layer does not own application business rules or directly access the database.

---

# 6. Request Lifecycle

## 6.1 Chat Message

When an administrator sends a message:

```text
HTTP Request
     │
     ▼
FastAPI Router
     │
     ▼
ConsultationService
     │
     ├──────────────► MessageRepository
     │                      │
     │                      ▼
     │                 PostgreSQL
     │
     ▼
AIService
     │
     ▼
AIProvider
     │
     ▼
LLM
     │
     ▼
AI Response
     │
     ▼
MessageRepository
     │
     ▼
PostgreSQL
     │
     ▼
HTTP Response
```

The conversation history is loaded before generating the AI response so that the AI can maintain context across multiple messages.

Both the user message and assistant response are persisted.

---

# 7. Recommendation Generation Lifecycle

Recommendation generation follows a separate workflow.

```text
HTTP Request
     │
     ▼
Recommendation Router
     │
     ▼
RecommendationService
     │
     ├──────────────► ConsultationRepository
     │
     ├──────────────► MessageRepository
     │
     ▼
AIService
     │
     ▼
AIProvider
     │
     ▼
LLM
     │
     ▼
Structured AI Output
     │
     ▼
Pydantic Validation
     │
     ▼
RecommendationRepository
     │
     ▼
PostgreSQL
     │
     ▼
HTTP Response
```

The structured recommendation contains:

```text
Recommendation
├── Patient Summary
├── Recommended Treatments
└── AI Reasoning (Optional)
```

The Recommendation is persisted before being returned to the client.

The frontend presents the Recommendation through the:

**Consultation Summary** screen.

---

# 8. Dependency Injection

FastAPI dependency injection is used for:

- Database sessions
- Services
- Repositories
- AI Service
- Configuration

Example dependency flow:

```text
API Router
    │
    ▼
Service Dependency
    │
    ├── Repository Dependency
    │
    └── AI Service Dependency
```

Benefits:

- Loose coupling
- Easier unit testing
- Easier mocking
- Better maintainability
- Clear dependency boundaries

---

# 9. Repository Pattern

Each repository manages persistence for one primary entity.

## ConsultationRepository

Responsibilities:

- Create consultation
- Get consultation
- Update consultation
- Search consultations
- Filter consultations

---

## MessageRepository

Responsibilities:

- Create message
- Get consultation messages
- Retrieve messages in chronological order

---

## RecommendationRepository

Responsibilities:

- Create recommendation
- Get recommendation by consultation
- Update recommendation where required

## TreatmentRepository

Responsibilities:

- List the authoritative treatment catalog
- Restrict recommendation and booking selection to active treatments
- Resolve treatments by UUID
- Resolve legacy booking names case-insensitively

---

## AppointmentRepository

Responsibilities:

- Create appointment
- Get appointment
- List appointments

Repositories interact with SQLAlchemy and do not contain business workflow logic.

---

# 10. Service Layer

## ConsultationService

Responsibilities:

- Create consultation
- Retrieve consultation
- Search consultations
- Filter consultations
- Manage consultation lifecycle
- Coordinate chat workflow

---

## RecommendationService

Responsibilities:

- Verify consultation
- Load consultation conversation
- Generate structured recommendation
- Validate that AI output contains one or two distinct catalog IDs
- Resolve all displayed metadata from Treatment rows
- Persist DB-derived treatment snapshots in the existing JSONB field
- Persist recommendation
- Retrieve persisted recommendation

The RecommendationService does not directly communicate with the LLM.

It uses:

```text
RecommendationService
        ↓
AIService
```

---

## AppointmentService

Responsibilities:

- Resolve the selected Treatment by UUID or compatible catalog name
- Reject arbitrary or unknown treatment values
- Book appointment
- Persist appointment
- Update consultation status to `Booked`

---

## DashboardService

Responsibilities:

- Calculate total consultations
- Calculate booked appointments
- Calculate conversion rate

---

# 11. AI Integration

The backend communicates with the AI provider through a dedicated AI service.

```text
Business Service
      │
      ▼
  AI Service
      │
      ▼
 AI Provider
      │
      ▼
Large Language Model
```

Business services never communicate directly with the AI provider.

---

## AI Service Responsibilities

The AI service provides operations for:

### Consultation Response

```text
generate_consultation_response(
    conversation
)
```

Returns an AI assistant response.

---

### Recommendation Generation

```text
generate_recommendation(
    conversation,
    treatment_catalog
)
```

Returns structured recommendation data.

Conceptually:

```text
{
    "patient_summary": "...",
    "recommended_treatment_ids": ["UUID"],
    "ai_reasoning": "..."
}
```

`ai_reasoning` is optional.

---

# 12. AI Provider Abstraction

The application uses an AI provider abstraction.

```text
AIService
    │
    ▼
AIProvider
    │
    ├── OpenAI Provider
    │
    └── Mock Provider
```

The exact provider can be changed through configuration.

This prevents business services from being coupled directly to a specific AI vendor.

---

# 13. AI Prompts

AI prompts are stored separately from business logic.

```text
app/ai/prompts/
│
├── consultation.py
└── recommendation.py
```

## Consultation Prompt

Used to generate context-aware responses during the consultation conversation.

The prompt receives the relevant conversation context.

---

## Recommendation Prompt

Used to transform the consultation conversation into structured recommendation output.

The recommendation prompt receives an explicit DB-backed treatment catalog and
instructs the model to return one or two IDs from that catalog. Expected output includes:

```text
Patient Summary
Recommended Treatment IDs
Optional AI Reasoning
```

---

# 14. AI Schemas

Structured AI responses are validated using Pydantic models.

```text
app/ai/schemas/
│
├── chat.py
└── recommendation.py
```

The recommendation schema represents:

```text
Recommendation
├── patient_summary
├── recommended_treatment_ids (one or two catalog UUIDs)
└── ai_reasoning (optional)
```

AI output must be validated before being persisted.

---

# 15. Validation

Request and response validation is performed using Pydantic.

Validation includes:

- Required fields
- Data types
- String length
- Enum values
- Structured recommendation output

Examples:

### Consultation

- Patient name is required.
- Primary concern is required.

### Chat

- Message cannot be empty.

### Recommendation

- Consultation must exist.
- Conversation data must be available.
- AI output must match the expected structured schema.

### Appointment

- Treatment is required.
- Appointment date/time is required.
- Location is required.

---

# 16. Exception Handling

Global exception handling manages:

- Request validation errors
- Resource not found
- Database exceptions
- AI provider failures
- Unexpected application exceptions

API errors follow the common response format:

```json
{
  "success": false,
  "message": "Error message",
  "errors": []
}
```

The API should return appropriate HTTP status codes according to the API specification.

---

# 17. Logging

Application logging includes:

- Incoming requests
- Application errors
- AI provider failures
- Database exceptions

Logging configuration is centralized.

Sensitive information such as credentials or API keys must not be logged.

---

# 18. Configuration

Application configuration is managed through environment variables.

Configuration includes:

- Database URL
- AI provider configuration
- AI model configuration
- API settings
- Environment settings

Example:

```text
DATABASE_URL
AI_PROVIDER
AI_MODEL
AI_API_KEY
```

Secrets must not be hardcoded in source code.

---

# 19. Response Models

All APIs return a consistent response structure.

## Success

```json
{
  "success": true,
  "message": "Operation completed successfully.",
  "data": {}
}
```

## Error

```json
{
  "success": false,
  "message": "Validation failed.",
  "errors": []
}
```

The exact API behavior is defined in:

```text
api-specification.md
```

---

# 20. Transaction Management

Database transactions are coordinated at the service/application workflow level.

For example, appointment booking requires:

```text
Create Appointment
        +
Update Consultation Status
```

These operations should be committed consistently so that the system does not leave the consultation and appointment in an inconsistent state.

---

# 21. Design Principles

The backend follows:

- Separation of Concerns
- Single Responsibility Principle
- Layered Architecture
- Repository Pattern
- Dependency Injection
- Modular Design
- Consistent API Design
- Clear AI abstraction
- Structured validation
- Maintainable code

---

# 22. Testing Strategy

The architecture supports:

- Repository tests
- Service tests
- AI service tests
- API endpoint tests
- Integration tests
- End-to-end workflow tests

Important workflows to test include:

```text
Create Consultation
        ↓
Send Messages
        ↓
Generate Recommendation
        ↓
Retrieve Recommendation
        ↓
Book Appointment
        ↓
Verify Consultation Status
```

Testing is part of the project verification process even though the exact test implementation is defined separately.

---

# 23. Implementation Order

The recommended implementation order is:

1. Project Setup
2. Database Configuration
3. SQLAlchemy Models
4. Alembic Migrations
5. Repository Layer
6. Service Layer
7. AI Provider and AI Service
8. API Routers
9. API/Swagger Verification
10. Frontend Integration
11. End-to-End Testing

---

# 24. Backend Responsibility Boundaries

The following boundaries must be maintained:

```text
Router
  │
  │ HTTP concerns only
  ▼
Service
  │
  │ Business/workflow concerns
  ▼
Repository
  │
  │ Persistence concerns
  ▼
Database
```

AI interaction follows:

```text
Service
  │
  ▼
AIService
  │
  ▼
AIProvider
  │
  ▼
LLM
```

The following direct dependencies are prohibited:

```text
Router ────────► Repository
Router ────────► AI Provider

Repository ────► AI Service
Repository ────► Business Logic

AI Provider ───► Database
```

This keeps the architecture modular and testable.

---

# 25. Current Scope

The backend currently focuses on the assessment requirements:

- Consultation management
- Conversation/message management
- Context-aware AI interaction
- Recommendation generation
- Recommendation persistence
- Appointment booking
- Consultation status management
- Dashboard statistics

Additional capabilities are outside the current scope unless explicitly required by the project requirements.
