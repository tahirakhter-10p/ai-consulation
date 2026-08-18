# AI Consultation Platform

# Frontend Architecture

Version: 1.0

Status: Draft

---

# 1. Overview

## Purpose

This document defines the frontend architecture of the AI Consultation Platform.

It describes:

- Application structure
- Technology stack
- Routing
- Component organization
- State management
- API communication
- UI design principles

The frontend is responsible for providing an intuitive and responsive user interface while communicating with the FastAPI backend through REST APIs.

The frontend architecture implements the requirements defined in:

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
| React | User Interface |
| TypeScript | Type Safety |
| Vite | Build Tool |
| Material UI (MUI) | UI Components |
| React Router | Client-side Routing |
| TanStack Query | Server State Management |
| Axios | HTTP Client |

---

# 3. Architecture Overview

The frontend follows a feature-oriented component architecture with clear separation between presentation, state management, and API communication.

```text
Pages

↓

Components / Hooks

↓

API Services

↓

REST APIs

↓

FastAPI Backend
```

Each layer has a defined responsibility.

---

# 4. Project Structure

```text
frontend/
│
├── public/
│
├── src/
│   │
│   ├── api/
│   │   ├── axios.ts
│   │   ├── dashboard.ts
│   │   ├── consultations.ts
│   │   ├── recommendations.ts
│   │   └── appointments.ts
│   │
│   ├── assets/
│   │
│   ├── components/
│   │   ├── common/
│   │   ├── dashboard/
│   │   ├── consultation/
│   │   ├── recommendation/
│   │   └── appointment/
│   │
│   ├── hooks/
│   │
│   ├── layouts/
│   │
│   ├── pages/
│   │   ├── DashboardPage.tsx
│   │   ├── ConsultationListPage.tsx
│   │   ├── ConsultationDetailPage.tsx
│   │   ├── ConsultationSummaryPage.tsx
│   │   └── AppointmentPage.tsx
│   │
│   ├── routes/
│   │
│   ├── types/
│   │
│   ├── utils/
│   │
│   ├── App.tsx
│   └── main.tsx
│
├── package.json
└── vite.config.ts
```

---

# 5. Routing

The application consists of five primary screens.

| Route | Screen |
|--------|--------|
| `/dashboard` | Dashboard |
| `/consultations` | Consultation Records |
| `/consultations/:id` | Consultation Detail |
| `/consultations/:id/recommendation` | Consultation Summary |
| `/consultations/:id/appointment` | Appointment Booking |

The route:

```text
/consultations/:id/recommendation
```

uses the Recommendation API resource but renders the:

**Consultation Summary** screen.

This maintains the distinction between the backend Recommendation domain entity and the frontend Consultation Summary presentation.

---

# 6. Pages

## 6.1 Dashboard

### Purpose

Displays overall consultation statistics.

### API

```http
GET /dashboard
```

### Components

- Sidebar
- Header
- Statistics Cards

### Displayed Information

- Total consultations
- Booked appointments
- Conversion rate

---

## 6.2 Consultation Records

### Purpose

Displays consultation records and their current status.

### API

```http
GET /consultations
```

### Features

- Search consultations
- Filter by status
- Display patient information
- Display primary concern
- Display recommended procedure
- Display consultation status
- Open consultation

### Components

- Search Bar
- Status Filter
- Consultation Table

---

## 6.3 Consultation Detail

### Purpose

Allows administrators to interact with the AI assistant during an active consultation.

### APIs

```http
GET /consultations/{id}

GET /consultations/{id}/messages

POST /consultations/{id}/messages
```

### Features

- View consultation information
- View conversation history
- Send messages
- Receive AI responses
- Maintain conversation context

### Components

- Chat Window
- Message Bubble
- Chat Input
- Send Button

---

## 6.4 Consultation Summary

### Purpose

Displays the persisted Recommendation generated from the consultation conversation.

The Recommendation is the backend/domain resource.

The Consultation Summary is the frontend presentation of that resource.

### APIs

```http
POST /consultations/{id}/recommendation

GET /consultations/{id}/recommendation
```

### Displayed Information

- Patient summary
- Recommended treatments
- Optional AI reasoning

### Components

- Summary Card
- Recommendation Card
- AI Reasoning Panel
- Book Appointment Button
- Restart Consultation Button

### Flow

```text
Consultation Detail
        ↓
Generate Recommendation
        ↓
Persist Recommendation
        ↓
Consultation Summary
        ↓
Book Appointment
```

---

## 6.5 Appointment Booking

### Purpose

Allows the administrator to book an appointment based on the consultation recommendation.

### API

```http
POST /consultations/{id}/appointment
```

### Features

- Select treatment
- Select date
- Select time
- Enter location
- Confirm appointment

### Components

- Appointment Form
- Date Picker
- Time Picker
- Location Input
- Submit Button

### After Successful Booking

```text
Appointment Created
        ↓
Consultation Status = Booked
        ↓
Return to Consultation Records
```

---

# 7. Layout

The application uses a common layout across the primary screens.

```text
+---------------------------------------------+
| Header                                      |
+------------+--------------------------------+
| Sidebar    |                                |
|            |                                |
|            |        Page Content            |
|            |                                |
|            |                                |
+------------+--------------------------------+
```

The sidebar remains available while navigating between the application screens.

---

# 8. Component Architecture

Reusable components are organized by feature.

## Common Components

- Header
- Sidebar
- Loading Spinner
- Error Message
- Empty State
- Confirmation Dialog

---

## Dashboard Components

- Statistics Card

---

## Consultation Components

- Consultation Table
- Search Bar
- Status Filter
- Chat Window
- Chat Message
- Chat Input

---

## Recommendation Components

These components render the Recommendation data on the Consultation Summary screen.

- Summary Card
- Recommendation Card
- AI Reasoning Panel

---

## Appointment Components

- Appointment Form
- Date Picker
- Time Picker
- Location Input

---

# 9. State Management

## Local State

React local state will manage UI-specific state such as:

- Form values
- Search input
- Filters
- Dialog visibility
- Temporary form state

---

## Server State

TanStack Query will manage server-side data such as:

- Dashboard statistics
- Consultation list
- Consultation details
- Conversation history
- Recommendation
- Appointment data where required

---

## Queries

Examples:

```text
useDashboardQuery
useConsultationsQuery
useConsultationQuery
useMessagesQuery
useRecommendationQuery
```

---

## Mutations

Examples:

```text
useSendMessageMutation
useGenerateRecommendationMutation
useBookAppointmentMutation
```

Mutations should invalidate or update related queries when server state changes.

For example:

```text
Book Appointment
      ↓
Update Consultation Status
      ↓
Invalidate Consultation Records Query
      ↓
Records display "Booked"
```

---

## Routing State

React Router manages navigation between pages.

---

# 10. API Layer

All HTTP communication is isolated in the API layer.

Example structure:

```text
api/
├── axios.ts
├── dashboard.ts
├── consultations.ts
├── recommendations.ts
└── appointments.ts
```

### Responsibilities

- Perform HTTP requests
- Configure the HTTP client
- Define API request functions
- Return typed responses
- Handle common HTTP configuration

The UI components do not communicate directly with Axios.

---

# 11. Data Flow

## 11.1 Sending a Chat Message

```text
User
  ↓
Chat Input
  ↓
useSendMessageMutation
  ↓
messages API service
  ↓
POST /consultations/{id}/messages
  ↓
FastAPI Backend
  ↓
AI Response
  ↓
API Response
  ↓
Update Conversation State
  ↓
Render Chat Window
```

Both user and assistant messages are persisted by the backend.

---

## 11.2 Recommendation Flow

```text
Consultation Detail
        ↓
Generate Recommendation
        ↓
useGenerateRecommendationMutation
        ↓
POST /consultations/{id}/recommendation
        ↓
FastAPI Backend
        ↓
AI Service
        ↓
LLM
        ↓
Persist Recommendation
        ↓
Return Recommendation
        ↓
Consultation Summary
```

---

## 11.3 Appointment Flow

```text
Consultation Summary
        ↓
Book Appointment
        ↓
useBookAppointmentMutation
        ↓
POST /consultations/{id}/appointment
        ↓
FastAPI Backend
        ↓
Create Appointment
        ↓
Update Consultation Status
        ↓
Return Success
        ↓
Consultation Records
        ↓
Status = Booked
```

---

# 12. Error Handling

The frontend shall handle:

- Validation errors
- Network failures
- API errors
- AI generation errors
- Appointment booking errors
- Unexpected server errors

User-friendly messages shall be displayed whenever an error occurs.

The frontend should use the common API error response defined in:

```text
api-specification.md
```

---

# 13. Loading States

Loading indicators shall be displayed while:

- Loading dashboard statistics
- Loading consultation records
- Loading consultation details
- Loading conversation history
- Sending AI messages
- Generating recommendations
- Loading recommendations
- Booking appointments

The UI should prevent duplicate actions while a mutation is in progress where appropriate.

---

# 14. Empty States

Appropriate empty states should be displayed when:

- No consultations exist
- No search results are found
- No messages exist
- No recommendation has been generated yet

Empty states should clearly explain what the user can do next.

---

# 15. TypeScript Models

The frontend will define TypeScript types/interfaces for:

- Consultation
- ConsultationMessage
- Recommendation
- RecommendedTreatment
- Appointment
- DashboardStatistics
- APIResponse
- APIError

These types should align with the backend API response schemas.

---

## Recommendation Type

Conceptually:

```typescript
interface Recommendation {
  id: string;
  consultation_id: string;
  patient_summary: string;
  recommended_treatments: RecommendedTreatment[];
  ai_reasoning?: string | null;
}
```

The frontend should treat the Recommendation as the data resource and the Consultation Summary as the screen that presents it.

---

# 16. UI Design Principles

The application follows these principles:

- Clean interface
- Consistent spacing
- Responsive layout
- Accessible components
- Reusable UI
- Minimal navigation
- Clear visual hierarchy
- Clear loading and error feedback
- Consistent status presentation

---

# 17. Component Reusability

The frontend emphasizes reusable components.

| Component | Reusable |
|-----------|----------|
| Sidebar | Yes |
| Header | Yes |
| Statistics Card | Yes |
| Search Bar | Yes |
| Status Filter | Yes |
| Consultation Table | Yes |
| Chat Window | Yes |
| Chat Message | Yes |
| Chat Input | Yes |
| Summary Card | Yes |
| Recommendation Card | Yes |
| AI Reasoning Panel | Yes |
| Appointment Form | Yes |
| Loading Spinner | Yes |
| Error Message | Yes |

---

# 18. Frontend Development Principles

The frontend implementation follows:

- Component-based architecture
- Separation of concerns
- Strong TypeScript typing
- Reusable UI components
- Feature-focused organization
- Consistent API integration
- Responsive design
- Maintainable codebase
- Clear separation between server state and local UI state

---

# 19. End-to-End Navigation Flow

The primary user journey is:

```text
Dashboard
    ↓
Consultation Records
    ↓
Consultation Detail
    ↓
AI Conversation
    ↓
Consultation Summary
    ↓
Appointment Booking
    ↓
Consultation Records
    ↓
Updated Status: Booked
```

The frontend must preserve the consultation ID throughout this workflow so that the correct consultation, recommendation, and appointment remain connected.

---

# 20. Implementation Order

1. Initialize React project
2. Configure Material UI
3. Configure React Router
4. Configure Axios
5. Configure TanStack Query
6. Create Application Layout
7. Build Dashboard
8. Build Consultation Records
9. Build Consultation Detail
10. Build Consultation Summary
11. Build Appointment Booking
12. Integrate Backend APIs
13. Implement loading and error states
14. Verify complete consultation workflow
15. Final Testing
