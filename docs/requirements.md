# AI Consultation Platform

# Software Requirements Specification (SRS)

Version: 1.0

Status: Draft

---

# 1. Project Overview

## 1.1 Purpose

The purpose of this project is to build a web-based AI-powered consultation workflow that enables clinic administrators to manage consultation records, interact with an AI assistant, generate treatment recommendations, and schedule appointments through a complete end-to-end workflow.

The application should demonstrate a production-style architecture while fulfilling all functional and technical requirements defined in the assessment.

---

# 2. Project Goals

The system shall allow users to:

- View consultation statistics.
- Manage consultation records.
- Conduct AI-assisted consultations.
- Generate consultation summaries.
- Identify appropriate treatments based on the consultation.
- Book patient appointments.
- Persist consultation data throughout the workflow.

Treatment recommendations shall be based on the available treatment data stored in the database.

---

# 3. Project Scope

## In Scope

- Dashboard
- Consultation Records
- Consultation Detail (AI Chat)
- Consultation Summary
- Appointment Booking
- REST APIs
- PostgreSQL Database
- Persistent Chat History
- AI Integration
- Search
- Status Filtering
- Treatment Catalog
- Treatment Recommendations

## Out of Scope

The following features are intentionally excluded from this implementation.

- Authentication
- Authorization
- User Management
- Notifications
- Email Integration
- SMS Integration
- Payment Processing
- Multi-language Support
- Audit Logs
- Analytics beyond the required dashboard metrics
- Mobile Application

---

# 4. Actors

## Primary User

Clinic Administrator

Responsibilities

- View consultations
- Chat with AI
- Review recommendations
- Book appointments
- Track consultation status

---

# 5. User Journey

The system shall support the following workflow.

Dashboard

↓

Consultation Records

↓

Consultation Detail

↓

AI Consultation

↓

Consultation Summary

↓

Appointment Booking

↓

Consultation Records (Updated Status)

---

# 6. Functional Requirements

---

## Module A — Dashboard

### FR-001

Display total consultations.

Priority

High

Acceptance Criteria

- Total consultation count is displayed.

---

### FR-002

Display booked appointments.

Priority

High

Acceptance Criteria

- Total booked appointments are displayed.

---

### FR-003

Display conversion rate.

Priority

High

Acceptance Criteria

- Conversion rate is calculated and displayed.

---

### FR-004

Provide navigation to Consultation Records.

Priority

High

Acceptance Criteria

- User can navigate to Consultation Records.

---

## Module B — Consultation Records

### FR-005

Display consultation list.

Acceptance Criteria

Each consultation shall display:

- Patient Name
- Primary Concern
- Recommended Treatment
- Status

---

### FR-006

Search consultations.

Acceptance Criteria

- User can search consultations using keywords.

---

### FR-007

Filter consultations.

Acceptance Criteria

Support filters.

- Pending
- Booked
- Completed

---

### FR-008

Open consultation details.

Acceptance Criteria

Selecting a consultation opens the Consultation Detail page.

---

## Module C — Consultation Detail

### FR-009

Start AI conversation.

Acceptance Criteria

Administrator can send messages.

---

### FR-010

Receive AI responses.

Acceptance Criteria

AI generates responses for each message.

---

### FR-011

Persist conversation.

Acceptance Criteria

Messages remain available after refresh or navigation.

---

### FR-012

Support multiple messages.

Acceptance Criteria

Conversation history remains intact throughout the consultation.

---

### FR-013

Support structured AI output.

Acceptance Criteria

AI may return

- Tables
- Lists
- Structured recommendations

---

## Module D — Consultation Summary

### FR-014

Generate consultation summary.

Acceptance Criteria

Summary is generated from the completed conversation.

The generated recommendation shall identify appropriate treatment(s) based on the consultation.

The AI shall use the available treatment information when identifying recommended treatments.

---

### FR-015

Display recommended treatments.

Acceptance Criteria

Treatment recommendations are visible.

Recommended treatments shall correspond to treatments available in the treatment database.

Treatment information such as:

- Treatment name
- Description
- Duration
- Price
- Location

shall be retrieved from the treatment database rather than being generated or hardcoded by the frontend.

---

### FR-016

Display AI reasoning.

Priority

Optional

Acceptance Criteria

Reasoning is displayed when available.

---

### FR-017

Restart consultation.

Acceptance Criteria

Administrator can restart the consultation.

---

### FR-018

Navigate to Appointment Booking.

Acceptance Criteria

Book Appointment button opens the booking page.

---

## Module E — Appointment Booking

### FR-019

Capture selected treatment.

---

### FR-020

Capture appointment date.

---

### FR-021

Capture appointment time.

---

### FR-022

Capture appointment location.

---

### FR-023

Save appointment.

Acceptance Criteria

Appointment is stored successfully.

---

### FR-024

Update consultation status.

Acceptance Criteria

Status changes to Booked.

---

### FR-025

Redirect to Consultation Records.

Acceptance Criteria

Administrator returns to the consultation list after booking.

---

# 7. Technical Requirements

## TR-001

Use REST APIs.

---

## TR-002

Persist consultations.

---

## TR-003

Persist messages.

---

## TR-004

Persist recommendations.

---

## TR-005

Persist appointments.

---

## TR-006

Maintain relationships between

- Consultation
- Messages
- Recommendation
- Appointment

---

## TR-007

Maintain state across the workflow.

---

## TR-008

Support context-aware AI responses.

---

## TR-009

Provide structured AI output.

---

## TR-010

Provide graceful error handling.

---

## TR-011

Maintain a persistent treatment catalog in PostgreSQL.

---

## TR-012

Use the treatment catalog when generating treatment recommendations.

The AI shall identify appropriate treatments based on the consultation, and the application shall resolve those treatments against the available treatment records.

---

## TR-013

Treatment details displayed to the user shall come from persisted treatment records.

Treatment information such as:

- Price
- Duration
- Description
- Location

shall not be hardcoded in the frontend.

---

## TR-014

Validate structured AI recommendation output before it is persisted or used by the application.

---

# 8. Non-Functional Requirements

## NFR-001

Responsive web application.

---

## NFR-002

Clean and modular architecture.

---

## NFR-003

Readable code.

---

## NFR-004

Consistent REST API design.

---

## NFR-005

Database normalization.

---

## NFR-006

Proper validation.

---

## NFR-007

Error handling.

---

## NFR-008

Maintainable project structure.

---

# 9. Success Criteria

The project shall be considered complete when

✓ All required screens are implemented.

✓ All REST APIs are functional.

✓ AI conversation persists.

✓ Appointment booking updates consultation status.

✓ Dashboard metrics are correct.

✓ Database persistence is verified.

✓ Complete workflow functions without data loss.

✓ Recommended treatments are resolved against the treatment catalog.

✓ Treatment details displayed in the recommendation UI come from the treatment database.

✓ Recommendation data is persisted.

---

# 10. Requirement Traceability Matrix

| ID | Module | Priority | Status |
|----|----------|----------|--------|
| FR-001 | Dashboard | High | Pending |
| FR-002 | Dashboard | High | Pending |
| FR-003 | Dashboard | High | Pending |
| FR-004 | Dashboard | High | Pending |
| FR-005 | Consultation Records | High | Pending |
| FR-006 | Consultation Records | High | Pending |
| FR-007 | Consultation Records | High | Pending |
| FR-008 | Consultation Records | High | Pending |
| FR-009 | AI Chat | High | Pending |
| FR-010 | AI Chat | High | Pending |
| FR-011 | AI Chat | High | Pending |
| FR-012 | AI Chat | High | Pending |
| FR-013 | AI Chat | High | Pending |
| FR-014 | Summary | High | Pending |
| FR-015 | Summary | High | Pending |
| FR-016 | Summary | Optional | Pending |
| FR-017 | Summary | High | Pending |
| FR-018 | Summary | High | Pending |
| FR-019 | Booking | High | Pending |
| FR-020 | Booking | High | Pending |
| FR-021 | Booking | High | Pending |
| FR-022 | Booking | High | Pending |
| FR-023 | Booking | High | Pending |
| FR-024 | Booking | High | Pending |
| FR-025 | Booking | High | Pending |