# Coding Conventions

**Analysis Date:** 2026-03-17

## Backend Conventions (Python/FastAPI)

### Naming Patterns

**Files and Directories:**
- Use lowercase with underscores: `data_products_manager.py`, `data_product_routes.py`
- Manager files: `*_manager.py` (e.g., `src/backend/src/controller/data_products_manager.py`)
- Repository files: `*_repository.py` (e.g., `src/backend/src/repositories/data_products_repository.py`)
- Route files: `*_routes.py` (e.g., `src/backend/src/routes/data_product_routes.py`)
- DB models: snake_case in `src/backend/src/db_models/`
- API models: snake_case in `src/backend/src/models/`

**Classes:**
- Managers: PascalCase with `Manager` suffix: `DataProductsManager`
- Repositories: PascalCase with `Repository` suffix: `DataProductRepository`
- DB Models: PascalCase with `Db` suffix for SQLAlchemy models: `DataProductDb`, `OutputPortDb`
- API Models: PascalCase, no suffix: `DataProduct`, `DataProductCreate`, `DataProductUpdate`

**Functions:**
- Use snake_case: `get_data_products_manager()`, `fetch_permissions()`
- Async functions: `async def` for route handlers, SDK calls, DB operations
- Sync functions: `def` for pure functions, validation helpers
- Helper functions prefixed with underscore if module-private: `_is_valid_uuid()`

**Variables:**
- Use snake_case: `data_product`, `is_active`, `has_permission`
- Boolean variables: `is_`, `has_`, `should_` prefixes
- Private/unused variables: prefix with underscore: `_is_valid_uuid`, `_init_attempted`

**Constants:**
- UPPER_SNAKE_CASE at module level: `SOURCE_ID_PROPERTY`, `DATA_PRODUCTS_FEATURE_ID`

### Code Style (Python)

**Formatting:**
- Tool: Ruff (configured in `src/pyproject.toml`)
- Line length: 100 characters
- Quote style: double quotes
- Indent: spaces (2 spaces)
- Target version: 3.11

**Linting (Ruff rules):**
- Selected: E (pycodestyle errors), W (pycodestyle warnings), F (pyflakes), I (isort), B (bugbear), C4 (comprehensions), UP (pyupgrade), SIM (simplify)
- Ignored: E501 (line length handled by formatter), B008 (FastAPI Depends pattern), B904 (raise without from - too noisy)

**Type Hints:**
- Use Python type hints extensively from `typing`: `List`, `Optional`, `Dict`, `Any`, `Union`
- Pydantic models for API validation and serialization
- SQLAlchemy models for DB interaction
- `Annotated` types for FastAPI dependency injection

### Import Organization

**Order:**
1. Standard library imports (e.g., `import os`, `from datetime import datetime`)
2. Third-party imports (Pydantic, SQLAlchemy, FastAPI, Databricks SDK)
3. Local imports from `src.*`

**Isort Configuration:**
- First-party package: `src`
- Known first-party: `["src"]`

**Example:**
```python
import asyncio
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any

import yaml
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session, selectinload
from fastapi import APIRouter, HTTPException, Depends

from databricks.sdk import WorkspaceClient
from databricks.sdk.errors import NotFound, PermissionDenied

from src.models.data_products import DataProduct, DataProductCreate
from src.repositories.data_products_repository import data_product_repo
from src.common.logging import get_logger
```

### Error Handling

**Patterns:**
```python
# Route-level error handling with HTTPException
from fastapi import HTTPException

if not product:
    raise HTTPException(status_code=404, detail="Data Product not found")

# Repository-level error handling with logging
try:
    db.add(db_obj)
    db.flush()
    db.refresh(db_obj)
    logger.info(f"Successfully created product: {db_obj.id}")
    return db_obj
except Exception as e:
    logger.error(f"Database error: {e}", exc_info=True)
    db.rollback()
    raise

# Databricks SDK error handling
from databricks.sdk.errors import NotFound, PermissionDenied

try:
    result = ws.catalogs.get(name=catalog_name)
except NotFound:
    logger.warning(f"Catalog {catalog_name} not found")
    return None
except PermissionDenied as e:
    logger.error(f"Permission denied: {e}")
    raise HTTPException(status_code=403, detail="Access denied")
```

### Logging

**Framework:** Python logging via `src/backend/src/common/logging.py`

**Usage:**
```python
from src.common.logging import get_logger
logger = get_logger(__name__)

# Log levels
logger.debug(f"Fetching product: {id}")
logger.info(f"Successfully created product: {db_obj.id}")
logger.warning(f"Product not found: {id}")
logger.error(f"Database error: {e}", exc_info=True)
logger.critical("Settings not found in application state!")
```

**Format:** `%(asctime)s - %(name)s - %(levelname)s - %(message)s`

### Comments and Documentation

**Module-level docstrings:**
```python
"""
ODPS v1.0.0 Data Products Manager

This module implements the business logic layer for ODPS v1.0.0 Data Products.
Handles product creation, updates, versioning, contract integration, and search indexing.
"""
```

**Function docstrings:**
```python
def get_visible_products(
    self,
    db: Session,
    current_user: str,
    user_projects: List[str]
) -> List[DataProductDb]:
    """Get products visible to user based on three-tier visibility model.

    Visibility tiers:
    - Tier 3: Published to marketplace (everyone can see)
    - Tier 2: Team/project versions (no personal owner, in user's projects)
    - Tier 1: User's own personal drafts

    Args:
        db: Database session
        current_user: Username of current user
        user_projects: List of project IDs the user has access to

    Returns:
        List of visible DataProductDb objects
    """
```

### Function Design

**Size:** Functions should be focused; manager methods often orchestrate multiple operations

**Parameters:**
- Use type hints for all parameters
- Use `Optional[T]` for nullable parameters with defaults
- Manager constructors use optional parameters with warnings if not provided

**Return Values:**
- Return Pydantic API models from managers
- Return SQLAlchemy models from repositories
- Use tuples for multiple return values with clear naming

**Dependency Injection Pattern:**
```python
# Define Annotated type alias in dependencies.py
from fastapi import Depends, Annotated
DBSessionDep = Annotated[Session, Depends(get_db)]
CurrentUserDep = Annotated[UserInfo, Depends(get_current_user)]
DataProductsManagerDep = Annotated[DataProductsManager, Depends(get_data_products_manager)]

# Use in route
@router.get("/products")
async def list_products(
    db: DBSessionDep,
    current_user: CurrentUserDep,
    manager: DataProductsManagerDep
):
    ...
```

### Module Design

**Exports:**
- Managers and repositories instantiated as singletons at app startup, stored in `app.state`
- Access via dependency injection functions in `src/common/dependencies.py`
- Manager getters defined in `src/common/manager_dependencies.py`

---

## Frontend Conventions (TypeScript/React)

### Naming Patterns

**Files and Directories:**
- Use lowercase with dashes: `data-product-form-dialog.tsx`, `use-api.ts`
- Components: kebab-case: `data-products.tsx` in `src/frontend/src/views/`
- Hooks: kebab-case with `use-` prefix: `use-api.ts` in `src/frontend/src/hooks/`
- Types: kebab-case: `data-product.ts` in `src/frontend/src/types/`
- Stores: kebab-case with `-store` suffix: `permissions-store.ts` in `src/frontend/src/stores/`

**Components:**
- React components: PascalCase: `DataProductFormDialog`
- Functional components only (no class components)

**Functions:**
- Use camelCase: `fetchPermissions()`, `hasPermission()`
- Event handlers: `handle` prefix: `handleSubmit`, `handleClick`

**Variables:**
- Use camelCase: `isLoading`, `dataProduct`, `hasPermission`
- Boolean variables: `is`, `has`, `should` prefixes
- Private state: prefix with underscore: `_isInitializing`, `_initAttempted`

**Types:**
- Interfaces: PascalCase: `DataProduct`, `ApiResponse<T>`
- Enums: PascalCase with UPPER_SNAKE_CASE values:
  ```typescript
  export enum DataProductStatus {
    DRAFT = 'draft',
    ACTIVE = 'active',
    RETIRED = 'retired'
  }
  ```

### Code Style (TypeScript)

**Formatting (Prettier in `src/frontend/.prettierrc`):**
- Semi-colons: required (`semi: true`)
- Single quotes for strings (`singleQuote: true`)
- Tab width: 2 spaces
- Trailing commas: ES5
- Print width: 100 characters
- Bracket spacing: true
- Arrow parens: always
- End of line: LF

**Linting (ESLint in `src/frontend/eslint.config.js`):**
- React recommended + jsx-runtime rules
- React Hooks recommended
- TypeScript recommended
- Custom rules:
  - `@typescript-eslint/no-unused-vars`: warn (ignore `_` prefix)
  - `@typescript-eslint/no-explicit-any`: warn
  - `no-console`: warn (allow `warn`, `error`)

**TypeScript Configuration (`src/frontend/tsconfig.json`):**
- Strict mode enabled
- `noUnusedLocals`: true
- `noUnusedParameters`: true
- `noFallthroughCasesInSwitch`: true

### Import Organization

**Order:**
1. React and framework imports
2. Third-party library imports (React Router, Zustand, etc.)
3. UI component imports (Shadcn, Radix)
4. Local imports (hooks, types, components)

**Path Aliases:**
- `@/*` maps to `./src/*` (configured in `tsconfig.json`)

**Example:**
```typescript
import { useState, useCallback, useEffect } from 'react';
import { create } from 'zustand';

import { Button } from '@/components/ui/button';
import { Dialog, DialogContent } from '@/components/ui/dialog';

import { useApi } from '@/hooks/use-api';
import { usePermissions } from '@/stores/permissions-store';
import type { DataProduct } from '@/types/data-product';
```

### Error Handling

**Patterns:**
```typescript
// API error handling with useApi hook
const { data, error } = await api.get<DataProduct>('/api/data-products/123');
if (error) {
  toast({ title: 'Error', description: error, variant: 'destructive' });
  return;
}

// Store error handling
try {
  const response = await fetch('/api/user/permissions');
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  const data = await response.json();
  setPermissions(data);
} catch (error: any) {
  console.error("Failed to fetch permissions:", error);
  setError(error.message || 'Failed to load');
}
```

### Logging

**Framework:** Console with prefixes for identification

**Usage:**
```typescript
console.error("[useApi] GET error from", url, ":", error);
console.warn("[Component] Warning message");
```

### Function Design

**React Patterns:**
```typescript
// Use useCallback for stable function references
const handleSubmit = useCallback(async (data: FormData) => {
  await api.post('/api/endpoint', data);
}, [api]);

// Use useMemo for expensive computations
const filteredProducts = useMemo(() => {
  return products.filter(p => p.status === 'active');
}, [products]);

// Custom hook pattern
export const useApi = () => {
  const [loading, setLoading] = useState(false);

  const get = useCallback(async <T>(url: string): Promise<ApiResponse<T>> => {
    // ...
  }, []);

  return { get, post, put, delete: delete_, loading };
};
```

### State Management (Zustand)

**Pattern:**
```typescript
import { create } from 'zustand';

interface PermissionsState {
  permissions: UserPermissions;
  isLoading: boolean;
  error: string | null;
  fetchPermissions: () => Promise<void>;
  hasPermission: (featureId: string, level: FeatureAccessLevel) => boolean;
}

const usePermissionsStore = create<PermissionsState>((set, get) => ({
  permissions: {},
  isLoading: false,
  error: null,

  fetchPermissions: async () => {
    set({ isLoading: true });
    try {
      const response = await fetch('/api/user/permissions');
      const data = await response.json();
      set({ permissions: data, error: null });
    } catch (error: any) {
      set({ error: error.message });
    } finally {
      set({ isLoading: false });
    }
  },

  hasPermission: (featureId, level) => {
    const { permissions } = get();
    return permissions[featureId] === level;
  },
}));
```

### Component Design

**Structure:**
```typescript
// 1. Imports
import { useState } from 'react';

// 2. Types
interface DataProductFormProps {
  productId?: string;
  onSubmit: (data: DataProduct) => void;
}

// 3. Component
export function DataProductForm({ productId, onSubmit }: DataProductFormProps) {
  // 3a. Hooks
  const { data, isLoading } = useApi();

  // 3b. State
  const [isOpen, setIsOpen] = useState(false);

  // 3c. Effects
  useEffect(() => { /* ... */ }, []);

  // 3d. Handlers
  const handleSubmit = () => { /* ... */ };

  // 3e. Render
  return ( /* ... */ );
}
```

---

*Convention analysis: 2026-03-17*
