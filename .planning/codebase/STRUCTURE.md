# Codebase Structure

**Analysis Date:** 2026-03-17

## Directory Layout

```
ontos/
├── src/
│   ├── backend/
│   │   ├── src/
│   │   │   ├── app.py                      # FastAPI application entry point
│   │   │   ├── routes/                     # API route handlers (53+ route modules)
│   │   │   ├── controller/                 # Manager classes (55+ managers)
│   │   │   ├── repositories/               # Data access layer (42+ repositories)
│   │   │   ├── models/                     # Pydantic API models (50+ files)
│   │   │   ├── db_models/                  # SQLAlchemy database models (42+ files)
│   │   │   ├── common/                     # Cross-cutting utilities (38+ modules)
│   │   │   ├── workflows/                  # Databricks workflow/job definitions (15+)
│   │   │   ├── data/                       # Demo data, taxonomies, schemas (28+ files)
│   │   │   ├── tests/                      # Unit & integration tests
│   │   │   ├── schemas/                    # JSON schemas (validation)
│   │   │   ├── connectors/                 # External system connectors (8 files)
│   │   │   ├── tools/                      # Utility scripts and tools (15+)
│   │   │   ├── file_models/                # File-based model definitions
│   │   │   ├── owl/                        # OWL/RDF processing utilities
│   │   │   └── utils/                      # Startup tasks, utilities
│   │   ├── alembic/                        # Database migrations
│   │   ├── alembic.ini                     # Alembic configuration
│   │   ├── requirements.txt                # Python dependencies
│   │   └── run.sh                          # Development run script
│   ├── frontend/
│   │   ├── src/
│   │   │   ├── app.tsx                     # React app root component
│   │   │   ├── views/                      # Page-level components (60+ views)
│   │   │   ├── components/                 # Reusable UI components (35+ dirs)
│   │   │   │   ├── ui/                     # Base Shadcn UI components
│   │   │   │   ├── common/                 # App-specific common components
│   │   │   │   ├── layout/                 # Navigation, sidebar, header
│   │   │   │   └── [feature]/              # Feature-specific components
│   │   │   ├── stores/                     # Zustand global state (8+ stores)
│   │   │   ├── hooks/                      # Custom React hooks (15+)
│   │   │   ├── types/                      # TypeScript type definitions
│   │   │   ├── utils/                      # Utility functions
│   │   │   ├── config/                     # Feature flags, configuration
│   │   │   ├── lib/                        # Library functions (8+ files)
│   │   │   ├── i18n/                       # Internationalization
│   │   │   │   └── locales/                # Locale files (ja, it, nl, etc.)
│   │   │   └── tests/                      # React component tests
│   │   ├── public/                         # Static assets
│   │   ├── tests/                          # E2E tests
│   │   ├── index.html                      # HTML entry point
│   │   ├── vite.config.ts                  # Vite build configuration
│   │   ├── tailwind.config.js              # Tailwind CSS configuration
│   │   ├── tsconfig.json                   # TypeScript configuration
│   │   └── package.json                    # Node dependencies
│   ├── app.yaml                            # Databricks App configuration
│   ├── databricks.yaml                     # Databricks Asset Bundle config
│   ├── manifest.yaml                       # App manifest
│   ├── pyproject.toml                      # Python project config (hatch)
│   ├── requirements.txt                    # Python dependencies
│   └── package.json                        # Root package.json
├── docs/                                   # Project documentation
│   ├── images/                             # Documentation images
│   ├── notes/                              # Development notes
│   │   └── TODOS/                          # TODO tracking
│   └── user-journeys/                      # User journey documentation
├── website/                                # Docusaurus documentation site
│   └── ontos/
│       ├── docs/                           # User/admin/dev guides
│       └── src/                            # Website components
├── .planning/codebase/                     # GSD analysis documents (THIS FOLDER)
├── .github/workflows/                      # CI/CD workflows
├── .claude/                                # Claude Code configuration
│   ├── agents/                             # Agent definitions
│   ├── commands/                           / Custom commands (gsd/)
│   ├── hooks/                              # Hooks
│   └── get-shit-done/                      # GSD workflows
├── .cursor/                                # Cursor IDE config
├── .cursorrules                            # Cursor rules
└── .gsd/                                   # GSD milestones
```

## Directory Purposes

**`src/backend/src/`** (Main backend source)
- Purpose: Implement FastAPI application with RORO pattern and manager/repository abstraction
- Contains: Python source code, database models, API schemas, Pydantic validators
- Key files: `app.py` (server entry), 53+ route modules, 55+ manager classes

**`src/backend/src/routes/`** (HTTP API Endpoints)
- Purpose: FastAPI routers exposing HTTP endpoints grouped by feature
- Contains: One route module per feature (e.g., `data_product_routes.py`, `compliance_routes.py`)
- Pattern: Each imports a Manager, uses FastAPI's dependency injection for auth/DB
- Examples: `data_product_routes.py`, `data_contracts_routes.py`, `search_routes.py`, `assets_routes.py`

**`src/backend/src/controller/`** (Business Logic)
- Purpose: Manager classes implementing domain logic, coordinating repositories and services
- Contains: 55+ manager classes with `_manager.py` suffix
- Examples: `DataProductsManager`, `DataContractsManager`, `ComplianceManager`, `SearchManager`, `OntologySchemaManager`
- Pattern: Each manager handles one feature domain; many implement `SearchableAsset` for indexing
- Subdirectory: `ontology_handlers/` -- Format-specific ontology parsers (FIBO, GS1, OBO, Schema.org, SimpleOWL)

**`src/backend/src/repositories/`** (Data Access Layer)
- Purpose: Abstract database operations, map between API (Pydantic) and DB (SQLAlchemy) models
- Contains: 42+ repository classes
- Pattern: Each class extends `CRUDBase[DBModel, CreateModel, UpdateModel]` generic base
- Examples: `DataProductRepository`, `DataContractRepository`, `ComplianceRepository`, `AssetsRepository`

**`src/backend/src/models/`** (Pydantic API Models)
- Purpose: Define request/response schema for API, validate inputs
- Contains: 50+ Pydantic model files
- Pattern: Classes with `Create`, `Update`, `Response` suffixes (RORO pattern)
- Examples: `data_products.py` (has `DataProductCreate`, `DataProductUpdate`, `DataProduct`)
- Key: ODPS-compliant structure (`apiVersion`, `kind`, `spec`, `status`) with Databricks extensions

**`src/backend/src/db_models/`** (SQLAlchemy Database Models)
- Purpose: Define database table schemas and relationships
- Contains: 42+ SQLAlchemy model files
- Pattern: Classes extending SQLAlchemy Base, with `__tablename__` and column definitions
- Examples: `data_products.py`, `data_contracts.py`, `compliance.py`, `assets.py`, `entity_relationships.py`

**`src/backend/src/common/`** (Cross-Cutting Utilities)
- Purpose: Shared utilities, configuration, middleware, authorization
- Contains: 38+ utility modules
- Key modules:
  - `database.py` -- Session factory, DB initialization, Alembic migrations
  - `config.py` -- Settings loader (Pydantic BaseSettings)
  - `authorization.py` -- Permission checking, user fetching from Databricks SDK
  - `dependencies.py` -- FastAPI dependency providers (managers, sessions, users)
  - `manager_dependencies.py` -- Manager getter functions for DI
  - `middleware.py` -- Logging, error handling middleware
  - `search_interfaces.py` -- `SearchableAsset` interface
  - `search_registry.py` -- `@searchable_asset` decorator, manager registry
  - `logging.py` -- Structured logger setup
  - `workspace_client.py` -- Databricks SDK client instantiation
  - `git.py` -- Git service for indirect delivery
  - `delivery_mixin.py` -- Mixin for automatic delivery triggers

**`src/backend/src/connectors/`** (External System Connectors)
- Purpose: Pluggable asset connectors for external data platforms
- Contains: Base connector class, registry, platform-specific implementations
- Platforms: Databricks (primary), BigQuery, Snowflake, Kafka, PowerBI
- Files: `base.py`, `registry.py`, `databricks.py`, `bigquery.py`, `snowflake.py`, `kafka.py`, `powerbi.py`

**`src/backend/src/workflows/`** (Databricks Jobs/Workflows)
- Purpose: Define long-running or scheduled tasks (separate from API)
- Contains: 15+ workflow definitions, each in its own directory
- Examples: `compliance_checks/`, `data_quality_checks/`, `data_product_sync/`
- Pattern: Each workflow has its own `task.py` (Databricks task) and optional config

**`src/backend/src/data/`** (Demo Data & Static Config)
- Purpose: Store seed data, demo fixtures, ontology definitions
- Contains: 28+ data files
  - `taxonomies/` -- RDF ontologies (e.g., `ontos-ontology.ttl`)
  - Demo data files (loaded via POST /api/settings/demo-data/load)
  - YAML configurations for data products, contracts, etc.

**`src/backend/src/tools/`** (Utility Scripts)
- Purpose: Standalone utility scripts for maintenance and operations
- Contains: 15+ tool scripts
- Examples: Schema migration, data import, cleanup scripts

**`src/backend/src/tests/`** (Test Suite)
- Purpose: Unit and integration tests
- Pattern: pytest-based; one test file per feature
- Co-located tests also exist in `src/frontend/src/**/*.test.tsx`

**`src/frontend/src/`** (React Application)
- Purpose: Single-page application for user interface
- Contains: React components, stores, hooks, types, utilities

**`src/frontend/src/views/`** (Page-Level Components)
- Purpose: Full page components corresponding to routes
- Contains: 60+ view components (one per major feature)
- Examples: `data-products.tsx`, `data-contracts.tsx`, `compliance.tsx`, `settings-general.tsx`, `asset-explorer.tsx`
- Pattern: Import feature-specific components and layout components; manage page-level state

**`src/frontend/src/components/`** (Reusable Components)
- Purpose: Reusable UI components organized by feature and type
- Contains: 35+ subdirectories
- Structure:
  - `ui/` -- Base Shadcn UI components (button, dialog, form, etc.)
  - `common/` -- App-specific common components (RelativeDate, UserInfo, etc.)
  - `layout/` -- Navigation (sidebar, header, breadcrumbs)
  - `[feature]/` -- Feature-specific components (e.g., `data-products/`, `compliance/`, `concepts/`, `assets/`)
- Pattern: Each feature may have multiple components (list, form, detail, card, etc.)

**`src/frontend/src/stores/`** (Global State - Zustand)
- Purpose: Centralized state management for cross-component concerns
- Contains: 8+ Zustand stores
- Examples:
  - `permissions-store.ts` -- User permissions, role overrides
  - `user-store.ts` -- Current user info
  - `notifications-store.ts` -- Toast notifications
  - `breadcrumb-store.ts` -- Page breadcrumb navigation
- Pattern: Create stores with `create()`, expose via custom hooks like `usePermissions()`

**`src/frontend/src/hooks/`** (Custom React Hooks)
- Purpose: Reusable hook logic for data fetching and interactions
- Contains: 15+ custom hooks
- Examples:
  - `use-api.ts` -- Wraps fetch with error/loading handling
  - `use-comments.ts` -- Comment management
  - `use-toast.ts` -- Toast notifications
  - `use-domains.ts` -- Domain list fetching
  - `use-teams.ts` -- Team management
- Pattern: Each hook manages a specific data flow or interaction

**`src/frontend/src/types/`** (TypeScript Type Definitions)
- Purpose: Define interfaces/types for API responses, components
- Contains: One file per feature domain
- Examples: `data-product.ts`, `settings.ts`, `compliance.ts`, `assets.ts`

**`src/frontend/src/lib/`** (Library Functions)
- Purpose: Utility functions and constants
- Contains: `utils.ts`, `permissions.ts`, `odps-lifecycle.ts`, `odcs-lifecycle.ts`, `ontology-utils.ts`, etc.

**`src/frontend/src/i18n/`** (Internationalization)
- Purpose: Multi-language support
- Contains: Locale files for Japanese, Italian, Dutch, etc.
- Pattern: i18next configuration with locale JSON files

## Key File Locations

**Entry Points:**
- Backend: `src/backend/src/app.py` -- FastAPI application bootstrap
- Frontend: `src/frontend/src/app.tsx` -- React app root and routing
- Frontend HTML: `src/frontend/index.html` -- DOM anchor point

**Configuration:**
- Backend settings: `src/backend/src/common/config.py` -- Pydantic BaseSettings (loads `.env`)
- Environment example: `src/backend/.env.example` -- Environment variable template
- Frontend config: `src/frontend/src/config/features.ts` -- Feature flags
- Database: `src/backend/src/common/database.py` -- Session factory and models
- Migrations: `src/backend/alembic/` -- Alembic migration scripts
- Build (Frontend): `src/frontend/vite.config.ts`, `src/frontend/tailwind.config.js`
- Build (Backend): `src/pyproject.toml` -- Hatch configuration
- Build (App): `src/app.yaml` -- Databricks App Bundle format

**Core Logic:**
- Data Products: `src/backend/src/controller/data_products_manager.py`, `src/backend/src/models/data_products.py`
- Data Contracts: `src/backend/src/controller/data_contracts_manager.py`, `src/backend/src/models/data_contracts.py`
- Assets (Ontology-driven): `src/backend/src/controller/assets_manager.py`, `src/backend/src/models/assets.py`
- Search: `src/backend/src/controller/search_manager.py`, `src/backend/src/common/search_interfaces.py`
- Compliance: `src/backend/src/controller/compliance_manager.py`, `src/backend/src/models/compliance.py`
- Ontology: `src/backend/src/controller/ontology_schema_manager.py`, `src/backend/src/models/ontology_schema.py`
- Authentication/Authorization: `src/backend/src/common/authorization.py`

**Startup & Initialization:**
- Startup tasks: `src/backend/src/utils/startup_tasks.py`
- Database init: `src/backend/src/common/database.py` (`init_db()`)
- Manager init: `src/backend/src/utils/startup_tasks.py` (`initialize_managers()`)

**Testing:**
- Backend tests: `src/backend/src/tests/` directory
- Frontend tests: `src/frontend/src/**/*.test.tsx` (co-located)
- Test config: `src/backend/pyproject.toml` (pytest config)

## Naming Conventions

**Files:**

**Backend Python:**
- Routes: `{feature}_routes.py` (e.g., `data_product_routes.py`)
- Managers: `{feature}_manager.py` (e.g., `data_products_manager.py`)
- Repositories: `{entity}_repository.py` (e.g., `data_products_repository.py`)
- Models (API): `{entity}.py` (e.g., `data_products.py`)
- Models (DB): `{entity}.py` (e.g., `data_products.py`)
- Tests: `test_{module}_routes.py` or `test_{module}_repository.py`
- Utilities: `{utility_name}.py` (e.g., `workspace_client.py`)

**Frontend TypeScript:**
- Views: `{view-name}.tsx` (e.g., `data-products.tsx`, `data-product-details.tsx`)
- Components: `{component-name}.tsx` (e.g., `data-product-form.tsx`)
- Stores: `{store-name}-store.ts` (e.g., `permissions-store.ts`)
- Hooks: `use-{hook-name}.ts` (e.g., `use-api.ts`, `use-comments.ts`)
- Types: `{entity-name}.ts` (e.g., `data-product.ts`)
- Utils: `{utility-name}.ts` (e.g., `utils.ts`)

**Directories:**

**Backend:**
- Pluralized: `routes/`, `models/`, `repositories/`, `db_models/`, `workflows/`, `connectors/`
- Singular: `controller/`, `common/`, `utils/`, `data/`, `tools/`, `owl/`

**Frontend:**
- Pluralized: `views/`, `components/`, `stores/`, `hooks/`, `types/`, `utils/`, `tests/`
- Singular: `lib/`, `config/`, `i18n/`
- Feature-grouped components: `components/{feature-name}/` (hyphenated)

## Where to Add New Code

**New Feature (Full Feature Lifecycle):**
1. **Database schema:** `src/backend/src/db_models/{entity}.py` (SQLAlchemy model)
2. **API models:** `src/backend/src/models/{entity}.py` (Pydantic models with Create/Update/Response)
3. **Repository:** `src/backend/src/repositories/{entity}_repository.py` (extends CRUDBase)
4. **Manager:** `src/backend/src/controller/{entity}_manager.py` (business logic, optionally implement SearchableAsset)
5. **Routes:** `src/backend/src/routes/{entity}_routes.py` (FastAPI endpoints, register in `app.py`)
6. **Frontend types:** `src/frontend/src/types/{entity}.ts` (TypeScript interfaces)
7. **Frontend views:** `src/frontend/src/views/{entity}.tsx` (page component)
8. **Frontend components:** `src/frontend/src/components/{entity}/` directory (form, list, detail components)
9. **Tests:** `src/backend/src/tests/integration/test_{entity}_routes.py` (API tests)

**New Component/Module (UI Only):**
- Implementation: `src/frontend/src/components/{feature}/{component-name}.tsx`
- Use existing patterns (Shadcn UI + Tailwind, react-hook-form for forms)

**New Utility Function:**
- Backend: `src/backend/src/common/{utility_name}.py` or `src/backend/src/utils/{utility_name}.py`
- Frontend: `src/frontend/src/lib/` or `src/frontend/src/utils/`

**New API Endpoint:**
- Add method to Manager class: `src/backend/src/controller/{manager}.py`
- Add route in corresponding route file: `src/backend/src/routes/{feature}_routes.py`
- Register route in `app.py` if new router: `{feature}_routes.register_routes(app)`

**New Permission/Feature:**
- Define in: `src/backend/src/common/features.py` (add to `APP_FEATURES` dict)
- Use in route: `dependencies=[Depends(PermissionChecker('feature-id', FeatureAccessLevel.READ_WRITE))]`
- Check in UI: `hasPermission('feature-id', FeatureAccessLevel.READ_WRITE)` from `usePermissions()`

**New Connector:**
- Create in: `src/backend/src/connectors/{platform}.py` (extend `BaseConnector`)
- Register in: `src/backend/src/utils/startup_tasks.py` (`initialize_managers()` function)

## Special Directories

**`src/backend/src/workflows/`** (Generated/Managed)
- Purpose: Databricks Workflow/Job definitions
- Generated: Partially (managed by SettingsManager; users create via UI)
- Committed: Yes (stored as task.py and config files)
- Examples: `compliance_checks/`, `data_quality_checks/`, `data_product_sync/`

**`src/frontend/src/components/ui/`** (Generated/Third-Party)
- Purpose: Shadcn UI components (generated via CLI)
- Generated: Yes (via `npx shadcn-ui add`)
- Committed: Yes (checked in as source)
- Contains: Base components (Button, Dialog, Form, Input, Tooltip, etc.)

**`src/backend/src/data/`** (Static Content)
- Purpose: Demo data, ontologies, seed data
- Generated: No (hand-curated)
- Committed: Yes
- Examples: `taxonomies/ontos-ontology.ttl`, demo data YAML/SQL files

**`src/backend/alembic/`** (Database Migrations)
- Purpose: Schema migration version control
- Generated: Yes (via `alembic revision --autogenerate`)
- Committed: Yes
- Contains: Migration scripts and configuration

**`.planning/codebase/`** (GSD Analysis - THIS FOLDER)
- Purpose: Codebase analysis documents for GSD planner/executor
- Generated: By gsd:map-codebase command
- Committed: Yes
- Files: ARCHITECTURE.md, STRUCTURE.md, CONVENTIONS.md, TESTING.md, STACK.md, INTEGRATIONS.md, CONCERNS.md

---

*Structure analysis: 2026-03-17*
