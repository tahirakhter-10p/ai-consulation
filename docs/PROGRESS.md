# Implementation Progress

This file tracks implementation against the milestones in [development-roadmap.md](development-roadmap.md).

| Milestone | Status | Notes |
| --- | --- | --- |
| 1. Project Initialization | Complete | Backend and frontend foundations, configuration, logging, CORS, async SQLAlchemy/Alembic setup, health check, and application shell are in place. |
| 2. Database Foundation | Complete | SQLAlchemy models, enums, relationships, the Treatment catalog, and seven ordered Alembic revisions are implemented. |
| 3. Repository Layer | Complete | Async SQLAlchemy repositories for consultations, messages, recommendations, and appointments are implemented and verified. |
| 4. Service Layer | Complete | Dashboard, consultation/chat, recommendation, and appointment business services are implemented with repository constructor injection. |
| 5. AI Integration | Complete | AIService, provider adapters, prompt templates, structured AI schemas, and service-layer integration are implemented. |
| 6. REST APIs | Complete | Versioned dashboard, consultation/chat, recommendation, and appointment APIs with Pydantic contracts and Swagger are implemented. |
| 7. Frontend Implementation | Complete with documented follow-ups | Dashboard, consultation records/detail and chat, DB-backed recommendation selection, appointment booking, and booked confirmation are integrated with the current `/api/v1` contracts. The M7.7 audit identified a requirements decision for FR-025 and an ambiguity in FR-017. |

## Milestone 1 Completion Record

Completed on 2026-08-04.

- Created the FastAPI package structure and runtime configuration.
- Added environment-based settings, console logging, CORS, exception-handler skeletons, and `GET /health`.
- Configured async SQLAlchemy session infrastructure and async Alembic scaffolding without models or migrations.
- Created the React/Vite TypeScript application, Material UI layout, React Router, Axios client, and TanStack Query provider.
- Initialized the Git repository.
- Verified the frontend with `npm run build` and `npm run lint`.
- Verified backend source with Python static compilation.

## Milestone 2 Completion Record

Completed on 2026-08-05.

- Added UUID-based `BaseModel` with UTC creation timestamps.
- Added `ConsultationStatus` and `MessageRole` enums with the documented values.
- Added the `Consultation`, `ConsultationMessage`, `Recommendation`, and `Appointment` ORM entities.
- Implemented one-to-many and one-to-one relationships, foreign keys, unique constraints, indexes, non-empty checks, and cascading deletes as specified.
- Added ordered Alembic revisions `0001` through `0004`, one for each table in the documented migration order.
- Verified SQLAlchemy metadata, relationship mapping, source syntax, and the Alembic migration head.

The database foundation was subsequently expanded by revisions `0005` through `0007` to
update recommendation/appointment storage, create the authoritative Treatment catalog, and
expand its seeded treatment data.

The original Milestone 2 completion occurred before live PostgreSQL verification. Subsequent
backend work added and exercised the later migrations and Treatment seeding workflow against
the configured `ai_consultation` database.

## Milestone 3 Completion Record

Completed on 2026-08-06.

- Added `ConsultationRepository` with create, retrieve, list/search/filter, and status-update operations.
- Added `MessageRepository` with message persistence and chronological conversation retrieval.
- Added `RecommendationRepository` with recommendation persistence and consultation lookup.
- Added `AppointmentRepository` with appointment persistence, scheduled-list retrieval, and consultation lookup.
- All repositories use `AsyncSession`, flush changes without committing transactions, and contain no service, router, or AI logic.
- Verified imports and representative asynchronous repository operations with an async-session test double.

## Milestone 4 Completion Record

Completed on 2026-08-10.

- Added `DashboardService` with total consultation count, booked appointment count, and zero-safe conversion-rate calculation.
- Added `ConsultationService` with consultation creation, retrieval, search/status listing, status updates, and chronological chat persistence/retrieval.
- Added `RecommendationService` with consultation existence checks, one-recommendation-per-consultation enforcement, recommendation persistence, and retrieval.
- Added `AppointmentService` with consultation existence and duplicate-booking checks, appointment creation, appointment listing, and automatic status transition to `Booked`.
- All services use constructor-based repository injection; no router or API layer was added.
- Added service-level invalid-operation and conflict errors for invalid text/input and duplicate one-to-one workflow records.
- AI response and recommendation generation remain deferred to Milestone 5. The chat and recommendation services persist AI-generated content supplied by a future AI integration.
- Verified backend source with `python3 -m compileall -q backend/app`. Runtime imports and Ruff could not be run because the active interpreter does not have the backend dependencies installed.

## Milestone 5 Completion Record

Completed on 2026-08-10.

- Added the `AIService` as the sole provider-invocation boundary for chat responses, consultation summaries, and treatment recommendations.
- Added typed AI contracts for conversation messages, chat responses, consultation summaries, and recommendations.
- Added separate prompt builders for consultation chat, summary generation, and treatment-routing recommendations.
- Added an injectable `AIProvider` contract, deterministic `MockAIProvider` for local development/tests, and an optional `OpenAIProvider` using the asynchronous Responses API.
- Added AI provider configuration (`AI_PROVIDER`, `AI_MODEL`, and `OPENAI_API_KEY`) plus a cached AI-service dependency factory. The default provider is `mock`, so no credentials are required locally.
- Updated `ConsultationService` to persist the user message, call only `AIService`, and persist the generated assistant reply.
- Updated `RecommendationService` to use only `AIService` to generate and persist a summary and recommendation from the consultation conversation.
- Added `AIServiceError` to isolate provider and malformed-model-output failures from business services.
- No routers or APIs were added.

## Milestone 6 Completion Record

Completed on 2026-08-11.

- Added all documented `/api/v1` dashboard, consultation, chat, recommendation-summary, and appointment endpoints.
- Added Pydantic request and response contracts, including the standardized `{success, message, data}` success envelope and documented validation-error envelope.
- Added request-scoped service dependency factories that inject repositories sharing one database session and the configured `AIService` where required.
- Kept routers limited to request parsing, service calls, response serialization, and HTTP status selection; workflow logic remains in services.
- Updated the async database-session dependency to commit successful request transactions and roll back failed ones.
- Configured Swagger UI at `/docs` and the OpenAPI document at `/openapi.json`.
- Updated request-validation responses to use the API specification's HTTP 400 status.

## Milestone 7 Completion Record

Completed on 2026-08-17.

- Implemented the responsive dashboard with live total consultations, booked appointments,
  and conversion rate, plus Consultation Records and New Consult actions.
- Implemented Consultation Records, search/status filtering, consultation detail, persistent
  AI chat, recommendation generation, and booked-workflow routing.
- Integrated the Recommendation screen with `recommended_treatments`, displaying DB-backed
  treatment ID, specialty, description, target area, duration, price/range, and location.
- Integrated Appointment Booking with Treatment UUID selection, catalog-backed defaults,
  required date/time and location, complete booking metadata, confirmation state, and cache
  refreshes for consultations and dashboard metrics.
- Preserved legacy treatment-name fallback for migrated recommendations while preferring
  Treatment UUIDs for current records.
- Completed the PDF-aligned application shell with responsive sidebar navigation and active
  Dashboard/Consultation Records states. Unsupported PDF navigation entries are visual-only
  and do not create routes or backend dependencies.
- Added clearly isolated, typed frontend demo data for Monthly Revenue, Consultation Trends,
  Recent Activity, and Pending Clinical Reviews. The three required dashboard metrics remain
  connected to `GET /api/v1/dashboard`.
- Refined the Recent Activity panel into a compact, responsive activity list.
- Verified the frontend with `npm run lint` and `npm run build`.

## Milestone 7.7 Frontend Workflow Audit

Completed on 2026-08-17 as a read-only audit.

- Cross-checked frontend API calls, payloads, response types, routes, and workflow state against
  the implemented backend and the documentation under `docs/`.
- Confirmed that Recommendation uses only the current
  `/consultations/{consultation_id}/recommendation` endpoints and consumes
  `recommended_treatments`; no obsolete `/summary` calls remain.
- Confirmed that recommendation treatment metadata originates from authoritative Treatment
  database snapshots returned by the backend, and Appointment Booking submits the selected
  Treatment UUID to the documented appointment endpoint.
- Confirmed persisted chat, recommendation, appointment, booked-status, query invalidation,
  refresh behavior, loading states, error states, and empty states through code/contract review.
- Confirmed that the dashboard's three required metrics remain backend-backed and its PDF demo
  sections remain frontend-only.
- Frontend verification passed: ESLint, TypeScript compilation, and Vite production build.
- Backend verification passed: `13 passed` with `pytest`.
- The backend was not listening on port 8000 during the audit, so live HTTP/browser workflow
  verification was not performed in that audit session.

### Audit Follow-ups

- **FR-025 decision required:** the SRS says booking should redirect to Consultation Records,
  while the currently implemented, previously requested behavior remains on the Appointment
  screen and displays the confirmed appointment details with navigation actions.
- **FR-017 clarification required:** the current Return to Consultation action resumes the
  persisted conversation; the SRS does not define whether Restart Consultation means resume,
  clear local state, or create a new consultation.
- Opening the frontend at `http://127.0.0.1:5173` may not match the configured CORS origin;
  use `http://localhost:5173` with the current configuration.

## Environment Note

The backend declares Python 3.13 as required. The current dependency-managed environment can
run the backend test suite successfully. Runtime verification still requires the PostgreSQL
service and FastAPI process to be running.

## Update Rules

When beginning a milestone, set its status to **In progress**. Mark it **Complete** only after its deliverables and relevant verification have been finished. Record material deviations, deferred work, and verification results in that milestone's completion record.
