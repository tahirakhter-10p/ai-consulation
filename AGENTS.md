# AGENTS.md

This file defines repository-wide instructions for coding agents working on the AI Consultation
Platform. These rules apply to every file under this directory unless a more specific
`AGENTS.md` exists in a subdirectory.

## Project Overview

This repository contains:

- `backend/`: Python 3.13, FastAPI, Pydantic, SQLAlchemy, Alembic, PostgreSQL, and OpenAI.
- `frontend/`: React 18, TypeScript, Vite, Material UI, TanStack Query, and Axios.
- `docs/`: requirements, API contracts, architecture, database design, and roadmap documents.

Preserve the primary dependency directions:

```text
Frontend page -> query/API module -> Axios -> FastAPI endpoint
FastAPI router -> service -> repository -> SQLAlchemy/PostgreSQL
                         -> AI service -> AI provider
```

## Safety and Scope

- Never read, display, copy, edit, delete, or commit `backend/.env`, `frontend/.env`, or any
  other real environment file. Use and update `.env.example` files when configuration
  documentation changes.
- Never expose API keys, database credentials, tokens, patient information, or other secrets in
  code, tests, logs, fixtures, documentation, commits, or command output.
- Do not overwrite or revert unrelated user changes. The worktree may already be dirty.
- Do not run destructive Git or filesystem commands unless the user explicitly requests them.
- Keep changes within the requested scope. Do not perform opportunistic rewrites or dependency
  upgrades.
- Do not edit generated artifacts such as `dist/`, `coverage/`, Python caches, Vite caches, or
  `*.egg-info` files. Remove generated artifacts created during verification when they are not
  ignored.
- Do not commit lockfile changes unless dependencies actually changed. When dependencies change,
  update and retain the appropriate lockfile.

## Code Design Rules

- Prefer small, single-purpose functions and components with descriptive names.
- If a function grows beyond roughly 40 lines of executable logic, has more than three levels of
  nesting, or handles multiple responsibilities, split it into focused helpers.
- Do not split code mechanically when doing so would make the flow harder to understand. Extract
  cohesive behavior, not arbitrary line ranges.
- Avoid duplicated business rules. Backend services own workflow rules; repositories own data
  access; routers own HTTP concerns; frontend API modules own transport calls.
- Use early returns and explicit validation instead of deeply nested conditionals.
- Add type annotations to Python public APIs and keep TypeScript in strict mode. Avoid `Any`,
  unsafe casts, and untyped dictionaries unless an external boundary makes them necessary.
- Preserve existing public API behavior unless the requested task explicitly changes it.
- Prefer clear code over comments. Add comments only for non-obvious constraints, invariants, or
  decisions.
- Do not leave debug prints, console logs, commented-out code, TODO placeholders, or dead code.

## Backend Rules

- Keep FastAPI routers thin: validate HTTP input, call a service, and return the documented
  response envelope.
- Put business workflows and domain validation in `backend/app/services/`.
- Put database queries and persistence only in `backend/app/repositories/`.
- Keep provider-specific OpenAI code behind the AI provider abstraction. Services must not call
  the OpenAI SDK directly.
- Validate AI output with Pydantic before using or persisting it. Never trust model-generated IDs
  or structured data without checking them against database records.
- Use the shared application exceptions and central error handlers. Do not create ad hoc HTTP
  error shapes in individual endpoints.
- Keep async operations async throughout routers, services, repositories, and tests. Do not add
  blocking I/O to async request paths.
- Do not create or alter database tables directly. Add an Alembic migration for every schema
  change and keep SQLAlchemy models aligned with it.
- Migrations must be forward-safe and must not silently discard existing data. Destructive or
  irreversible migrations require explicit user approval and documentation.
- Do not connect automated unit tests to a developer or production database.

## Frontend Rules

- Keep route-level orchestration in `frontend/src/pages/` and reusable UI in
  `frontend/src/components/`.
- Put HTTP calls in typed modules under `frontend/src/api/`; components must not create ad hoc
  Axios clients.
- Use TanStack Query for server state, caching, mutations, and invalidation. Do not duplicate
  server state into unnecessary local state.
- Reuse domain and API types from `frontend/src/types/`. Keep API payloads and backend schemas in
  sync.
- Follow existing Material UI patterns and theme-compatible styling. Avoid introducing a second
  component or styling system without explicit approval.
- Preserve accessibility: use semantic elements, associated labels, keyboard-operable controls,
  meaningful accessible names, and visible loading/error/empty states.
- Do not place tests inside `frontend/src/`; keep them in `frontend/tests/`.

## Testing Requirements

- Every behavior change or bug fix must include a focused regression test.
- Test observable behavior and contracts rather than implementation details.
- Keep backend tests separated by scope:
  - `backend/tests/unit/`: isolated service, domain, validation, and transformation tests.
  - `backend/tests/e2e/`: HTTP-level FastAPI application and API contract tests.
- Keep frontend tests under `frontend/tests/unit/` and use Vitest with React Testing Library.
- Mock external AI and network calls. Tests must be deterministic and must not require an OpenAI
  key, internet access, or production services.
- Do not weaken, skip, or delete an existing test merely to make a change pass. Update a test only
  when the intended contract has genuinely changed.
- Cover success, validation, empty-state, error, and important boundary paths in proportion to the
  risk of the change.

## Required Verification

Run the smallest relevant checks while developing, then run all checks affected by the change.

Backend checks (from `backend/`):

```bash
PYTHONPATH=. .venv/bin/pytest
PYTHONPATH=. .venv/bin/ruff check app tests
```

Backend coverage when coverage tooling is available:

```bash
uv run --with pytest-cov pytest --cov=app --cov-branch --cov-report=term-missing
```

Frontend checks (from `frontend/`):

```bash
npm test
npm run lint
npm run build
```

Frontend coverage:

```bash
npm run test:coverage
```

Do not claim a check passed unless it was actually run successfully. If a check cannot run,
report the exact reason and which checks did run.

## Documentation and API Contracts

- Update the README or relevant file in `docs/` when setup, commands, architecture, configuration,
  routes, schemas, or user-visible workflows change.
- Treat `docs/api-specification.md`, backend schemas, frontend types, and tests as one contract.
  Keep them synchronized when request or response shapes change.
- Prefer examples with fake values. Never paste real `.env` contents into documentation.
- Keep documentation concise and accurate; remove statements made obsolete by a change.

## Dependency Changes

- Prefer the existing libraries and patterns before adding a dependency.
- Add a dependency only when it provides clear value that is difficult to implement safely with
  the current stack.
- Use `uv` for backend dependency resolution and `npm` for frontend dependency resolution.
- Keep dependency changes scoped, update lockfiles, and report security or compatibility warnings.
- Never run automatic audit fixes or major-version upgrades without reviewing their impact and
  receiving approval when they exceed the requested scope.

## Completion Checklist

Before handing work back:

1. Confirm the requested behavior is implemented.
2. Review the diff for secrets, unrelated edits, generated files, and accidental formatting churn.
3. Run relevant tests, lint checks, type checks, and builds.
4. Confirm migrations, API schemas, frontend types, and documentation agree where applicable.
5. Summarize the changed files, verification results, and any remaining risks or follow-up work.
