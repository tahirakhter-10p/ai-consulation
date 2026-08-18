# AI Consultation Platform

# System Architecture

Version: 1.0

Status: Draft

---

# 1. Overview

## Purpose

This document describes the technical architecture of the AI Consultation Platform.

It defines:

- Overall system structure
- Technology stack
- Application layers
- Component responsibilities
- Request and data flow
- AI integration architecture
- Development principles

The architecture is designed to satisfy the requirements defined in:

```text
requirements.md
```

while remaining simple, maintainable, and scalable.

The requirements document defines **what** the system must do. This document defines **how** we will implement it.

---

# 2. High-Level Architecture

```text
                        +----------------------+
                        |   React Frontend     |
                        |  (TypeScript + MUI)  |
                        +----------+-----------+
                                   |
                              REST API
                                   |
                                   ▼
+----------------------------------------------------------+
|                  FastAPI Backend                          |
|----------------------------------------------------------|
| API Routers                                              |
| Business Services                                        |
| Recommendation Service                                   |
| AI Service                                               |
| Repository Layer                                         |
| Database Layer                                           |
+---------------------------+------------------------------+
                            |
                    SQLAlchemy ORM
                            |
                            ▼
                  PostgreSQL Database
                            |
          +-----------------+------------------+
          |                 |                  |
          ▼                 ▼                  ▼
   Consultations      Treatments        Recommendations
          |
          +------------------+
          |
          ▼
       Appointments
```

---

# 3. Technology Stack

The assessment does not mandate a specific technology stack. The following stack is our implementation choice.

## Frontend

| Technology | Purpose |
|------------|---------|
| React | User Interface |
| TypeScript | Type Safety |
| Vite | Build Tool |
| Material UI | UI Components |
| TanStack Query | Server State Management |
| React Router | Routing |
| Axios | API Communication |

---

## Backend

| Technology | Purpose |
|------------|---------|
| FastAPI | REST APIs |
| SQLAlchemy 2.0 | ORM |
| Alembic | Database Migrations |
| Pydantic v2 | Validation |
| Uvicorn | ASGI Server |

---

## Database

| Technology | Purpose |
|------------|---------|
| PostgreSQL | Relational Database |

---

## AI

The AI layer is responsible for:

- Processing consultation conversations
- Generating context-aware consultation responses
- Generating structured recommendations
- Producing patient summaries from consultation conversations
- Producing recommended treatments
- Optionally producing AI reasoning

The AI implementation may use a real AI provider or a mocked implementation.

The current implementation is designed to support a real AI provider such as OpenAI through the AI provider abstraction.

---

# 4. System Components

The system consists of three primary application components.

## Frontend

Responsibilities:

- Render user interface
- Capture user input
- Display consultation information
- Display AI responses
- Display Consultation Summary
- Display recommendations
- Invoke backend APIs
- Manage presentation state
- Display validation and error messages

The frontend does not own backend business rules or database operations.

---

## Backend

Responsibilities:

- Expose REST APIs
- Validate requests
- Execute business rules
- Coordinate consultation workflows
- Coordinate AI interactions
- Persist data
- Return API responses

---

## Database

Responsibilities:

- Store consultations
- Store messages
- Store recommendations
- Store appointments
- Maintain relationships between these entities

The database is the persistent source of truth for application state.

---

# 5. Backend Architecture

The backend follows a layered architecture.

```text
API Router

↓

Service Layer

↓

Repository Layer

↓

Database
```

The AI integration is used by the service layer through the AI abstraction.

```text
Service Layer

      ↓

   AI Service

      ↓

 AI Provider

      ↓

     LLM
```

---

## API Router

Responsibilities:

- Define REST endpoints
- Receive HTTP requests
- Validate request payloads
- Invoke application services
- Return HTTP responses

The router does not contain business logic.

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

The service layer contains application/business logic.

Primary services include:

- Dashboard Service
- Consultation Service
- Recommendation Service
- Appointment Service

---

## Repository Layer

Responsibilities:

- Read data
- Save data
- Update data
- Delete data where required

Repositories contain database operations and persistence logic.

Repositories do not contain application business rules.

---

## Database Layer

Responsibilities:

- SQLAlchemy models
- Database sessions
- Transactions
- Database configuration

---

# 6. Frontend Architecture

The frontend follows a feature-oriented component architecture.

```text
Pages

↓

Components / Hooks

↓

API Services

↓

REST API
```

---

## Pages

Each page represents a screen or workflow defined by the assessment.

Primary pages include:

- Dashboard
- Consultation Records
- Consultation Detail
- Consultation Summary
- Appointment Booking

---

## Components

Reusable UI components include:

- Sidebar
- Header
- Consultation Table
- Chat Window
- Chat Message
- Summary Card
- Recommendation Card
- Appointment Form
- Loading State
- Error State
- Empty State

---

## API Layer

The API layer is responsible for communicating with backend APIs.

Example organization:

```text
api/
├── axios.ts
├── dashboard.ts
├── consultations.ts
├── recommendations.ts
└── appointments.ts
```

The API layer does not contain UI rendering logic.

---

# 7. Request Flow

## 7.1 Sending a Chat Message

The chat workflow is:

```text
Administrator
      │
      ▼
React Chat Input
      │
      ▼
POST /consultations/{id}/messages
      │
      ▼
FastAPI Router
      │
      ▼
Consultation Service
      │
      ├──────────────► Message Repository
      │                      │
      │                      ▼
      │                 PostgreSQL
      │
      ▼
AI Service
      │
      ▼
AI Provider
      │
      ▼
LLM
      │
      ▼
AI Response
      │
      ▼
Message Repository
      │
      ▼
PostgreSQL
      │
      ▼
FastAPI Response
      │
      ▼
React Chat UI
```

Both user and assistant messages are persisted as part of the consultation conversation.

This allows subsequent AI requests to use previous conversation messages as context.

---

# 8. Recommendation Generation Flow

Recommendation generation is separate from displaying the Consultation Summary.

The backend domain concept is:

```text
Recommendation
```

The frontend presentation screen is:

```text
Consultation Summary
```

The flow is:

```text
Consultation
      │
      ▼
Retrieve Conversation Messages
      │
      ▼
Recommendation Service
      │
      ├──────────────────────┐
      │                      │
      ▼                      ▼
   AI Service          Treatment Repository
      │                      │
      ▼                      ▼
 AI Provider           PostgreSQL
      │                      │
      ▼                      │
     LLM                    │
      │                      │
      ▼                      │
Structured Treatment        │
Recommendation              │
      │                      │
      └──────────┬───────────┘
                 ▼
       Match Recommended
       Treatments
                 │
                 ▼
       Retrieve Treatment
       Details from Database
                 │
                 ▼
       Validate Structured
            Output
                 │
                 ▼
       Recommendation
          Repository
                 │
                 ▼
            PostgreSQL
                 │
                 ▼
       Consultation Summary UI
```

The recommendation is persisted so that the Summary screen does not need to regenerate the recommendation every time it is opened.

---

# 9. Consultation Workflow

The complete application workflow is:

```text
Dashboard
    │
    ▼
Consultation Records
    │
    ▼
Consultation Detail
    │
    ▼
AI Conversation
    │
    ▼
Generate Recommendation
    │
    ▼
Select / Retrieve Suitable Treatments
    │
    ▼
Consultation Summary
    │
    ▼
Appointment Booking
    │
    ▼
Update Consultation Status
    │
    ▼
Consultation Records
```

The system maintains the consultation context throughout this workflow.

---

# 10. Data Flow

The primary persisted entities are:

```text
Consultation
    │
    ├──────────► Messages
    │
    ├──────────► Recommendation
    │
    └──────────► Appointment

Treatment
    │
    └──────────► Recommendation
```

The consultation is the central entity connecting the workflow.

---

## Consultation → Messages

A consultation can contain multiple messages.

```text
Consultation
    │
    └── Messages
          ├── User Message
          ├── AI Message
          ├── User Message
          └── AI Message
```

---

## Consultation → Recommendation

A recommendation is generated from the consultation conversation.

```text
Consultation
      │
      ▼
Conversation
      │
      ▼
AI Analysis
      │
      ▼
Recommended Treatment(s)
      │
      ▼
Treatment Database
      │
      ▼
Recommendation
```

The recommendation contains the structured outcome of the consultation.

---

## Consultation → Appointment

An appointment is created after the consultation recommendation has been reviewed.

```text
Consultation
      │
      ▼
Recommendation
      │
      ▼
Selected Treatment
      │
      ▼
Appointment
```

Successful appointment booking updates the consultation status to:

```text
Booked
```

---

# 11. Folder Structure

## Backend

```text
backend/
│
├── app/
│   ├── api/                 # FastAPI routers
│   │
│   ├── core/                # Configuration, logging, constants
│   │
│   ├── database/            # Database connection & session
│   │
│   ├── models/              # SQLAlchemy models
│   │
│   ├── schemas/             # Pydantic request/response models
│   │
│   ├── repositories/        # Database operations
│   │
│   ├── services/            # Business logic
│   │
│   ├── ai/
│   │   ├── providers/       # AI provider implementations
│   │   │   └── ai_provider.py
│   │   │
│   │   ├── prompts/         # System prompts
│   │   │   ├── consultation.py
│   │   │   └── recommendation.py
│   │   │
│   │   ├── schemas/         # AI request/response models
│   │   │   ├── chat.py
│   │   │   └── recommendation.py
│   │   │
│   │   └── service.py       # AI orchestration service
│   │
│   ├── dependencies/        # FastAPI dependencies
│   │
│   ├── utils/               # Shared helper functions
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

## Frontend

```text
frontend/

src/

    api/

    components/

    hooks/

    layouts/

    pages/

    routes/

    types/

    utils/

    App.tsx
```

---

# 12. Layer Responsibilities

| Layer | Responsibility |
|---------|---------------|
| React Pages | Screen Rendering |
| Components | Reusable UI |
| Hooks | UI and server-state interaction |
| API Layer | HTTP Communication |
| Routers | HTTP Endpoints |
| Services | Business Logic |
| Repositories | Database Operations |
| Database | Persistent Storage |
| AI Service | AI Interaction |
| AI Provider | Communication with LLM Provider |

---

# 13. Dependency Flow

Dependencies flow in one direction.

```text
Pages
  ↓
Components / Hooks
  ↓
API Layer
  ↓
REST API
  ↓
Routers
  ↓
Services
  ↓
Repositories
  ↓
Database
```

AI interaction is coordinated by the service layer:

```text
Service
  ↓
AI Service
  ↓
AI Provider
  ↓
LLM
```

No lower layer should depend on a higher application layer.

The AI provider should not be accessed directly by API routers or repositories.

---

# 14. Error Handling

Errors are handled consistently across application layers.

## Backend

Responsibilities include:

- Validate requests
- Validate AI responses
- Handle database failures
- Handle AI provider failures
- Return appropriate HTTP status codes
- Return consistent error responses

## Frontend

Responsibilities include:

- Display API errors
- Display validation errors
- Display loading states
- Display empty states
- Provide user-friendly feedback

---

# 15. Logging

The backend shall log relevant operational information, including:

- Incoming requests
- Application errors
- Database errors
- AI service failures

Sensitive information and secrets must not be written to logs.

Logs will assist during debugging and development.

---

# 16. Security

For the scope of this assessment:

- Input validation shall be performed.
- SQL injection shall be prevented using parameterized SQL/SQLAlchemy.
- Sensitive configuration shall be stored in environment variables.
- API errors should not expose sensitive internal implementation details.

Authentication and authorization are outside the current project scope.

---

# 17. Development Principles

The implementation shall follow these principles:

- Separation of Concerns
- Single Responsibility Principle
- Layered Architecture
- Modular Design
- Reusable Components
- Consistent API Design
- Maintainable Code
- Readable Project Structure
- Clear separation between AI integration and business logic

---

# 18. Architecture Decisions

| Decision | Reason |
|----------|--------|
| FastAPI | Lightweight and suitable for REST API development |
| PostgreSQL | Relational data with strong entity relationships |
| SQLAlchemy | Mature ORM with async support |
| React | Component-based frontend |
| Material UI | Consistent reusable user interface components |
| TanStack Query | Server-state management and API data handling |
| Layered Architecture | Clear separation of responsibilities |
| Repository Pattern | Decouples persistence from business logic |
| AI Provider Abstraction | Allows the LLM provider to be changed without modifying business logic |
| Pydantic | Request and structured AI response validation |

---

# 19. Future Extension Points

The architecture allows future enhancements without requiring major restructuring.

Possible extensions include:

- Authentication
- Multiple AI providers
- Notifications
- File attachments
- Additional dashboard analytics
- Cloud deployment
- Advanced AI workflows

These extensions are not part of the current project scope.

---

# 20. AI Module Architecture

The AI module is isolated from core business logic to maintain a clear separation of concerns.

## Responsibilities

The AI module is responsible for:

- Managing communication with the AI provider
- Storing and organizing system prompts
- Defining structured AI request and response models
- Generating consultation responses
- Generating structured recommendations
- Producing patient summaries as part of the recommendation output
- Producing recommended treatments as part of the recommendation output

---

## Module Structure

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
OpenAI / Mock Provider
        │
        ▼
Large Language Model
```

---

## Recommendation Output

The AI recommendation should be represented as structured data.

Conceptually:

```text
Recommendation
├── Patient Summary
├── Recommended Treatments
└── AI Reasoning (Optional)
```

The AI output should be validated before it is persisted.

```text
LLM Output
    │
    ▼
Pydantic Validation
    │
    ▼
Recommendation Repository
    │
    ▼
PostgreSQL
```

---

## Design Principles

- Business services never communicate directly with an AI provider.
- AI prompts are stored separately from business logic.
- AI request and response models are centralized.
- AI output is validated before persistence.
- AI providers can be replaced without affecting the rest of the application.
- The AI layer does not directly access the database.
- The AI layer does not contain appointment or consultation business rules.
