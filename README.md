# AI Consultation Platform

A full-stack AI-assisted consultation platform for managing patient
consultations, conducting persistent multi-message AI conversations,
generating structured treatment recommendations, and booking
appointments.

The application is built around one complete, stateful workflow:

**Dashboard → Consultation Records → AI Consultation → Recommendation →
Appointment Booking → Updated Consultation Records**

> This project is an assessment prototype. AI-generated recommendations
> are assistive and require appropriate professional review.

------------------------------------------------------------------------

## 1. Core Features

### Dashboard

-   Live **Total Consultations**
-   Live **Booked Appointments**
-   Live **Conversion Rate**
-   Navigation to consultation records and new consultation flow

### Consultation Records

-   Create consultations using patient name and primary concern
-   Search consultations by patient name
-   Filter by `Pending`, `Booked`, and `Completed`
-   Display recommended procedure and current consultation status
-   Reopen existing consultations without losing persisted data

### AI Consultation

-   Multi-message user/assistant conversation
-   Conversation history persisted in PostgreSQL
-   Previous messages supplied as context for subsequent AI responses
-   Saved conversation restored when a consultation is reopened

### Recommendation

-   Generates a patient summary
-   AI selects one or two treatments from the active database-backed
    treatment catalog
-   Stores structured treatment snapshots in PostgreSQL JSONB
-   Stores optional AI reasoning
-   Persisted recommendations can be retrieved without another AI
    request

### Appointment Booking

-   Select a recommended treatment
-   Choose appointment date/time and location
-   Persist one appointment per consultation
-   Automatically update consultation status to `Booked`

------------------------------------------------------------------------

## 2. End-to-End Consultation Flow

``` mermaid
flowchart TD
    A[Dashboard]
    A --> B[Consultation Records]
    B --> C[Create or Open Consultation]
    C --> D[Consultation Detail]
    D --> E[Retrieve Persisted Messages]
    E --> F[AI Consultation]

    F --> G[Send Message]
    G --> H[Message Service]
    H --> I[(PostgreSQL)]
    H --> J[AI Service]
    J --> K[AI Provider]
    K --> L[OpenAI]
    L --> M[Assistant Response]
    M --> I
    I --> N[Updated Conversation UI]

    N --> O{Continue Conversation?}
    O -->|Yes| G
    O -->|No| P[Generate Recommendation]

    P --> Q[Recommendation Workflow]
    Q --> R[Persisted Recommendation]
    R --> S[Consultation Summary UI]
    S --> T[Appointment Booking]
    T --> U[Appointment Service]
    U --> V[(PostgreSQL)]
    V --> W[Consultation Status: Booked]
    W --> X[Consultation Records]
    X --> Y[Refresh Dashboard Metrics]
```

### Workflow

1.  Start from the Dashboard and open Consultation Records.
2.  Create a consultation or reopen an existing one.
3.  Load the persisted conversation and continue the AI-assisted
    consultation.
4.  Every user and assistant message is stored in PostgreSQL.
5.  Generate a structured recommendation from the complete conversation.
6.  Resolve recommended treatments against the database-backed treatment
    catalog.
7.  Persist the final recommendation and display it in the Consultation
    Summary.
8.  Select a recommended treatment and book an appointment.
9.  Persist the appointment and update the consultation to `Booked`.
10. Refresh Consultation Records and Dashboard metrics from persisted
    state.

------------------------------------------------------------------------

## 3. Technology Stack

### Backend

  Technology                        Purpose
  --------------------------------- -------------------------------------------------------
  Python 3.13                       Backend runtime
  FastAPI                           REST API and OpenAPI/Swagger
  Pydantic v2                       Request, response, settings, and AI-output validation
  SQLAlchemy 2.0                    Async ORM and persistence
  asyncpg                           Async PostgreSQL driver
  PostgreSQL                        Primary relational database and JSONB storage
  Alembic                           Database schema migrations and seed migrations
  Uvicorn                           ASGI development server
  Pytest / pytest-asyncio / HTTPX   Backend testing
  Ruff                              Python linting and formatting checks

### Frontend

  Technology         Purpose
  ------------------ --------------------------------------------------
  React 18           User interface
  TypeScript 5.7     Type-safe frontend development
  Vite 6             Development server and production build
  Material UI 6      UI components, layout, icons, and theming
  React Router 7     Client-side routing
  TanStack Query 5   Server-state fetching, caching, and invalidation
  Axios              HTTP client
  ESLint             Frontend linting

### AI

  ---------------------------------------------------------------------
  Technology                         Purpose
  ---------------------------------- ----------------------------------
  OpenAI API                         AI chat and recommendation
                                     generation

  OpenAI Python SDK                  Backend integration with the
                                     OpenAI Responses API

  AI Provider Abstraction            Separates business logic from
                                     provider-specific SDK code

  Mock AI Provider                   Deterministic local development
                                     and automated testing

  Structured AI Output               Validated recommendation output
                                     containing summary, treatment IDs,
                                     and reasoning
  ---------------------------------------------------------------------

The AI provider and model are selected through environment
configuration. The OpenAI API key is never stored in source code.

------------------------------------------------------------------------

## 4. High-Level System Architecture

``` mermaid
flowchart TD
    A[Clinic Administrator]
    A --> B[React + TypeScript Frontend]
    B --> C[Axios / TanStack Query]
    C --> D[FastAPI REST API]
    D --> E[Service Layer]

    E --> F[Repository Layer]
    F --> G[(PostgreSQL)]

    E --> H[AI Service]
    H --> I[AI Provider]
    I --> J[OpenAI API]

    G --> K[Persisted Application State]
    J --> L[AI Output]
    L --> E
    E --> B
```

The frontend communicates only through the REST API. FastAPI delegates
business workflows to services, repositories isolate persistence,
PostgreSQL remains the source of truth, and AI-provider-specific
behavior is isolated behind the AI service/provider boundary.

------------------------------------------------------------------------

## 5. Backend Architecture

``` mermaid
flowchart TD
    A[FastAPI Router]
    A --> B[Service Layer]

    B --> C[Repository Layer]
    C --> D[SQLAlchemy Async Session]
    D --> E[(PostgreSQL)]

    B --> F[AI Service]
    F --> G[AI Provider]
    G --> H{Configured Provider}
    H -->|OpenAI| I[OpenAI API]
    H -->|Mock| J[Deterministic Mock Provider]

    I --> K[Validated AI Result]
    J --> K
    K --> B
    B --> A
```

### Layer responsibilities

**Router** - Defines HTTP endpoints - Validates request/response
contracts - Resolves dependencies - Delegates business work to services

**Service** - Owns consultation, recommendation, and appointment
workflows - Enforces business rules - Coordinates repositories and AI
services

**Repository** - Encapsulates SQLAlchemy queries and persistence - Keeps
database access separate from HTTP and AI concerns

**AI Service / Provider** - Builds AI input from consultation context -
Validates AI output - Isolates OpenAI-specific implementation details -
Supports a deterministic mock provider for development/testing

This gives the backend the primary dependency direction:

``` text
Router → Service → Repository → PostgreSQL
                 ↓
             AI Service → AI Provider → OpenAI
```

------------------------------------------------------------------------

## 6. Frontend Architecture

``` mermaid
flowchart TD
    A[React Router]
    A --> B[Route-Level Pages]
    B --> C[Reusable Material UI Components]

    B --> D[TanStack Query]
    D --> E[Typed API Modules]
    E --> F[Shared Axios Client]
    F --> G[FastAPI REST API]

    G --> H[API Response]
    H --> D
    D --> I[Query Cache]
    I --> B

    B --> J[Dashboard]
    B --> K[Consultation Records]
    B --> L[AI Consultation]
    B --> M[Recommendation]
    B --> N[Appointment Booking]
```

TanStack Query owns server state, including fetching, mutation state,
caching, and invalidation. Axios provides the shared HTTP client
configured through `VITE_API_BASE_URL`. Route-level pages compose
reusable Material UI components without duplicating persisted backend
state in the browser.

### Frontend routes

  -------------------------------------------------------------------------
  Screen                              Route
  ----------------------------------- -------------------------------------
  Dashboard                           `/dashboard`

  Consultation Records                `/consultations`

  Consultation Detail / AI Chat       `/consultations/:id`

  Consultation Recommendation         `/consultations/:id/recommendation`

  Appointment Booking / Confirmation  `/consultations/:id/appointment`
  -------------------------------------------------------------------------

------------------------------------------------------------------------

## 7. AI Recommendation Architecture

The AI does **not** choose or recommend treatment records directly. It
analyzes the consultation context and refines the user's intent into
structured treatment-search input. The backend then uses that refined
output to retrieve related treatments from PostgreSQL.

``` mermaid
flowchart TD
    A[Consultation]
    A --> B[Retrieve Conversation Messages]
    B --> C[Recommendation Service]

    C --> D[AI Service]
    D --> E[AI Provider]
    E --> F[OpenAI / LLM]

    F --> G[Analyze Consultation Context]
    G --> H[Refine User Intent<br/>and Treatment Search Criteria]
    H --> I[Validate Refined AI Output]

    I --> J[Recommendation Service]
    J --> K[Treatment Repository]
    K --> L[(PostgreSQL)]

    L --> M[Retrieve Related Treatments]
    M --> N[Build Recommendation]

    N --> O[Recommendation Repository]
    O --> P[(PostgreSQL)]

    P --> Q[Consultation Summary UI]
```

### Responsibility Boundary

-   **AI:** understands the consultation and refines the
    treatment-search intent.
-   **Recommendation Service:** orchestrates AI analysis, database
    retrieval, and persistence.
-   **Treatment Repository:** finds treatments related to the refined AI
    output.
-   **PostgreSQL:** remains the authoritative source for treatment
    records and metadata.
-   **Recommendation:** stores and returns treatments actually retrieved
    from the database.

The LLM is therefore not the source of truth for treatments.
`GET /api/v1/consultations/{consultation_id}/recommendation` returns the
persisted recommendation and does **not** invoke the AI provider again.

------------------------------------------------------------------------

## 8. Data Model

```
erDiagram
    CONSULTATIONS ||--o{ CONSULTATION_MESSAGES : contains
    CONSULTATIONS ||--o| RECOMMENDATIONS : produces
    CONSULTATIONS ||--o| APPOINTMENTS : books
    TREATMENTS ||--o{ APPOINTMENTS : selected_for

    CONSULTATIONS {
        uuid id PK
        varchar patient_name
        text primary_concern
        consultation_status status
        timestamptz created_at
        timestamptz updated_at
    }

    CONSULTATION_MESSAGES {
        uuid id PK
        uuid consultation_id FK
        message_role role
        text content
        timestamptz created_at
    }

    RECOMMENDATIONS {
        uuid id PK
        uuid consultation_id FK_UK
        text patient_summary
        jsonb recommended_treatments
        text ai_reasoning
        timestamptz created_at
        timestamptz updated_at
    }

    TREATMENTS {
        uuid id PK
        varchar name UK
        varchar specialty
        text description
        numeric price
        numeric price_min
        numeric price_max
        integer duration_minutes
        varchar location
        varchar default_target_area
        boolean is_active
        timestamptz created_at
        timestamptz updated_at
    }

    APPOINTMENTS {
        uuid id PK
        uuid consultation_id FK_UK
        uuid treatment_id FK
        varchar treatment
        timestamptz appointment_datetime
        varchar location
        timestamptz created_at
        timestamptz updated_at
    }
```

### Key relationships

-   A consultation can have many messages.
-   A consultation has at most one recommendation.
-   A consultation has at most one appointment.
-   Recommended treatment snapshots are stored in
    `recommendations.recommended_treatments` as JSONB.
-   Appointments reference treatments from the treatment catalog.
-   Booking an appointment updates the consultation status to `Booked`.

------------------------------------------------------------------------

## 9. REST API

The API base path is:

``` text
/api/v1
```

  ------------------------------------------------------------------------------------
  Method            Endpoint                                      Purpose
  ----------------- --------------------------------------------- --------------------
  `GET`             `/health`                                     Application health
                                                                  check

  `GET`             `/api/v1/dashboard`                           Dashboard metrics

  `POST`            `/api/v1/consultations`                       Create consultation

  `GET`             `/api/v1/consultations`                       List/search/filter
                                                                  consultations

  `GET`             `/api/v1/consultations/{id}`                  Get consultation

  `PATCH`           `/api/v1/consultations/{id}`                  Update consultation
                                                                  status

  `GET`             `/api/v1/consultations/{id}/messages`         Get conversation
                                                                  history

  `POST`            `/api/v1/consultations/{id}/messages`         Send message and
                                                                  generate AI reply

  `POST`            `/api/v1/consultations/{id}/recommendation`   Generate
                                                                  recommendation

  `GET`             `/api/v1/consultations/{id}/recommendation`   Get persisted
                                                                  recommendation

  `GET`             `/api/v1/treatments`                          List active
                                                                  treatments

  `POST`            `/api/v1/consultations/{id}/appointment`      Book appointment

  `GET`             `/api/v1/appointments`                        List appointments
  ------------------------------------------------------------------------------------

### API documentation

With the backend running:

-   Swagger UI: `http://localhost:8000/docs`
-   OpenAPI JSON: `http://localhost:8000/openapi.json`
-   Health check: `http://localhost:8000/health`

------------------------------------------------------------------------

## 10. Quick Start

### Prerequisites

-   Python `>=3.13,<3.14`
-   Node.js 22+
-   npm
-   PostgreSQL
-   OpenAI API key when using the OpenAI provider

### 1. Start PostgreSQL

The repository does not currently include Docker Compose configuration.
Use an existing PostgreSQL installation, or optionally start a local
PostgreSQL container:

``` bash
docker run --name ai-consultation-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=ai_consultation \
  -p 5432:5432 \
  -d postgres:16
```

> The Docker command above is an optional local-development convenience;
> it is not repository-managed infrastructure.

If PostgreSQL is already installed locally, create the database instead:

``` bash
createdb ai_consultation
```

Alembic creates the application schema.

### 2. Start the Backend

``` bash
cd backend

cp .env.example .env

python3.13 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e '.[dev]'

alembic upgrade head

uvicorn app.main:app --reload
```

Backend:

``` text
http://localhost:8000
```

Swagger:

``` text
http://localhost:8000/docs
```

### 3. Start the Frontend

Open another terminal:

``` bash
cd frontend

cp .env.example .env

npm install
npm run dev
```

Frontend:

``` text
http://localhost:5173
```

------------------------------------------------------------------------

## 11. Environment Configuration

### Backend --- `backend/.env`

Use the supplied `.env.example` and configure local values:

``` env
AI_CONSULTATION_APP_ENVIRONMENT=development
AI_CONSULTATION_DEBUG=true

AI_CONSULTATION_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/ai_consultation

AI_CONSULTATION_CORS_ORIGINS=["http://localhost:5173"]

AI_CONSULTATION_AI_PROVIDER=openai
AI_CONSULTATION_AI_MODEL=your-supported-model
AI_CONSULTATION_OPENAI_API_KEY=your-openai-api-key
```

For deterministic local development without OpenAI credentials:

``` env
AI_CONSULTATION_AI_PROVIDER=mock
```

Never commit real API keys or database credentials.

### Frontend --- `frontend/.env`

``` env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

------------------------------------------------------------------------

## 12. Database Migrations

Run Alembic commands from `backend/`:

``` bash
# Apply all migrations
alembic upgrade head

# Show current revision
alembic current

# Show migration history
alembic history
```

The application expects migrations to be applied before database-backed
endpoints are used.

------------------------------------------------------------------------

## 13. Tests and Quality Checks

### Backend

``` bash
cd backend

pytest
ruff check .
ruff format --check .
```

AI behavior is mocked in automated tests so tests do not depend on live
OpenAI calls.

### Frontend

``` bash
cd frontend

npm run lint
npm run build
```

The frontend currently has lint and production-build checks but no
automated frontend test script.

------------------------------------------------------------------------

## 14. Project Structure

``` text
.
├── backend/
│   ├── app/
│   │   ├── ai/              # AI service, prompts, schemas, providers
│   │   ├── api/             # FastAPI routers
│   │   ├── core/            # Settings, logging, constants, exceptions
│   │   ├── data/            # Treatment seed data
│   │   ├── database/        # Session and Alembic migrations
│   │   ├── dependencies/    # FastAPI dependencies
│   │   ├── models/          # SQLAlchemy models
│   │   ├── repositories/    # Persistence layer
│   │   ├── schemas/         # REST schemas
│   │   ├── services/        # Business workflows
│   │   └── main.py
│   └── tests/
├── frontend/
│   └── src/
│       ├── api/             # Axios API modules
│       ├── components/      # Shared and feature components
│       ├── layouts/         # Application layout
│       ├── pages/           # Route-level screens
│       ├── routes/          # React Router
│       ├── types/           # TypeScript domain/API types
│       ├── App.tsx
│       └── main.tsx
├── docs/
└── README.md
```

------------------------------------------------------------------------

## 15. Consultation Lifecycle

``` mermaid
flowchart TD
    A[Create Consultation]
    A --> B[Status: Pending]

    B --> C{Next Workflow Action}

    C -->|Book Appointment| D[Appointment Service]
    D --> E[(Persist Appointment)]
    E --> F[Status: Booked]

    C -->|Complete via supported status update| G[Status: Completed]
    F -->|Complete via supported status update| G
```

New consultations begin as `Pending`. Booking an appointment persists
the appointment and changes the consultation to `Booked`. The backend
also supports the `Completed` status.

------------------------------------------------------------------------

## 16. Assumptions and Scope

-   The primary user is a clinic administrator in a simplified
    single-organization workflow.
-   Authentication and authorization are outside the assessment scope.
-   PostgreSQL is available before application startup and Alembic
    migrations are applied.
-   Real AI behavior requires an externally supplied OpenAI API key and
    supported model.
-   The mock provider is available for deterministic local
    development/testing.
-   AI recommendations are assistive and are not a substitute for
    professional clinical judgment.
-   A consultation has at most one persisted recommendation and one
    appointment.

The assessment scope does not include authentication, payments,
notifications, RAG, autonomous agents, patient/doctor master-data
modules, or production deployment infrastructure.

------------------------------------------------------------------------

## 17. Demo Flow

For a complete end-to-end demonstration:

1.  Open `http://localhost:5173/dashboard`.
2.  Show live consultation, booking, and conversion metrics.
3.  Open **Consultation Records**.
4.  Create a consultation with a patient name and primary concern.
5.  Send multiple messages in the AI consultation.
6.  Reopen the consultation to demonstrate persisted conversation
    history.
7.  Generate the recommendation.
8.  Review the patient summary, recommended treatments, and AI
    reasoning.
9.  Select a recommended treatment.
10. Choose appointment date/time and location.
11. Book the appointment.
12. Return to Consultation Records and confirm the `Booked` status.
13. Return to Dashboard and confirm the metrics have refreshed.

------------------------------------------------------------------------

## 18. Key Design Decisions

**Layered backend architecture**\
HTTP handling, business workflows, persistence, and AI integration are
separated into dedicated layers.

**PostgreSQL as the source of truth**\
Consultations, messages, treatments, recommendations, and appointments
are persisted so the workflow survives navigation and application
restarts.

**Database-backed treatment recommendations**\
The AI selects from allowed treatment IDs. Treatment metadata comes from
PostgreSQL rather than being treated as authoritative AI-generated
content.

**JSONB recommendation snapshots**\
Structured recommended treatment details are stored with the
recommendation while preserving their ordered AI-selected presentation.

**Persisted recommendation retrieval**\
Recommendation generation is explicit. Later GET requests return the
stored result rather than making another OpenAI request.

**AI provider abstraction**\
Application services are isolated from provider SDK details and can use
either the OpenAI or deterministic mock provider.

**TanStack Query for server state**\
Frontend API state, caching, mutation handling, and invalidation are
centralized rather than duplicated in local/global application state.

------------------------------------------------------------------------