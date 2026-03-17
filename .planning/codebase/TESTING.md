# Testing Patterns

**Analysis Date:** 2026-03-17

## Test Framework

**Backend (Python):**
- Runner: pytest 7.0+
- Config: `src/pyproject.toml` under `[tool.pytest.ini_options]`
- Assertion Library: pytest built-in assertions
- Coverage Tool: pytest-cov 4.0+ with HTML, XML, and term-missing reports

**Frontend (TypeScript/React):**
- Runner: Vitest 3.2+
- Config: `src/frontend/vitest.config.ts`
- Assertion Library: Vitest built-in + `@testing-library/jest-dom/vitest`
- Testing Library: `@testing-library/react` 16.3+, `@testing-library/user-event` 14.6+
- Coverage Tool: v8 provider with text, json, html, lcov reporters
- E2E Testing: Playwright 1.55+

**Run Commands:**

Backend:
```bash
hatch -e dev run test              # Run all tests
hatch -e dev run test-unit         # Run unit tests only
hatch -e dev run test-integration  # Run integration tests only
hatch -e dev run test-cov          # Run with HTML coverage report
hatch -e dev run test-cov-xml      # Run with XML coverage report
```

Frontend:
```bash
cd src/frontend
yarn test                          # Run in watch mode (vitest)
yarn test:run                      # Run once
yarn test:coverage                 # Generate coverage report
yarn test:ui                       # Vitest UI mode
yarn test:e2e                      # Playwright E2E tests
yarn test:e2e:ui                   # Playwright interactive mode
yarn test:e2e:debug                # Playwright debug mode
yarn test:all                      # Run both unit and E2E tests
```

## Test File Organization

**Location:**

Backend:
- Path: `src/backend/tests/`
- Files: `test_*.py`
- Example files:
  - `src/backend/tests/test_compliance_dsl.py`
  - `src/backend/tests/test_compliance_actions.py`
  - `src/backend/tests/test_catalog_commander_manager.py`

Frontend (Vitest):
- Path: Co-located with source files
- Pattern: `**/*.test.ts`, `**/*.test.tsx`
- Example files:
  - `src/frontend/src/hooks/use-api.test.ts`
  - `src/frontend/src/stores/permissions-store.test.ts`
  - `src/frontend/src/components/data-products/data-product-form-dialog.test.tsx`

Frontend (Playwright E2E):
- Path: `src/frontend/src/tests/` and `src/frontend/tests/`
- Pattern: `*.spec.ts`
- Example files:
  - `src/frontend/src/tests/contract-outputport-mapping.spec.ts`
  - `src/frontend/src/tests/domain-edit.spec.ts`
  - `src/frontend/tests/team-assignment.spec.ts`

## Test Structure

**Backend Test Suite Organization:**

```python
"""Unit tests for Compliance DSL Parser and Evaluator."""
import pytest
from unittest.mock import MagicMock

from src.common.compliance_dsl import (
    Lexer,
    Parser,
    Evaluator,
    TokenType,
    evaluate_rule_on_object,
)


class TestLexer:
    """Test DSL lexer."""

    def test_tokenize_simple_assertion(self):
        """Test tokenizing a simple assertion."""
        lexer = Lexer("obj.name = 'test'")
        tokens = lexer.tokenize()

        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == 'obj'

    def test_tokenize_regex_match(self):
        """Test tokenizing MATCHES operator."""
        lexer = Lexer("obj.name MATCHES '^[a-z]+$'")
        tokens = lexer.tokenize()

        assert any(t.type == TokenType.MATCHES for t in tokens)


class TestEvaluator:
    """Test DSL evaluator."""

    def test_evaluate_property_access(self):
        """Test evaluating property access."""
        obj = {'name': 'test_table'}
        evaluator = Evaluator(obj)
        ast = PropertyAccess('obj', 'name')

        result = evaluator.evaluate(ast)
        assert result == 'test_table'


class TestRuleEvaluation:
    """Test complete rule evaluation."""

    def test_simple_naming_convention(self):
        """Test naming convention rule."""
        rule = "ASSERT obj.name MATCHES '^[a-z][a-z0-9_]*$'"

        # Valid name
        obj1 = {'name': 'valid_table_name'}
        passed, msg = evaluate_rule_on_object(rule, obj1)
        assert passed is True
        assert msg is None

        # Invalid name
        obj2 = {'name': 'InvalidName'}
        passed, msg = evaluate_rule_on_object(rule, obj2)
        assert passed is False
        assert msg is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
```

**Frontend Test Suite Organization:**

```typescript
import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import { act, renderHook, waitFor } from '@testing-library/react';
import usePermissionsStore, { usePermissions } from './permissions-store';
import { FeatureAccessLevel } from '@/types/settings';

// Mock fetch globally
global.fetch = vi.fn();

describe('Permissions Store', () => {
  beforeEach(() => {
    // Reset store state before each test
    act(() => {
      usePermissionsStore.setState({
        permissions: {},
        isLoading: false,
        error: null,
        availableRoles: [],
      });
    });
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('Initial State', () => {
    it('has correct initial state', () => {
      const { result } = renderHook(() => usePermissionsStore());
      expect(result.current.permissions).toEqual({});
      expect(result.current.isLoading).toBe(false);
    });
  });

  describe('fetchPermissions', () => {
    it('fetches and sets permissions successfully', async () => {
      // Arrange
      const mockPermissions = {
        'data-products': FeatureAccessLevel.READ_WRITE,
        'data-contracts': FeatureAccessLevel.READ_ONLY,
      };
      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockPermissions,
      });

      const { result } = renderHook(() => usePermissionsStore());

      // Act
      await act(async () => {
        await result.current.fetchPermissions();
      });

      // Assert
      expect(result.current.permissions).toEqual(mockPermissions);
      expect(result.current.error).toBeNull();
    });
  });

  describe('hasPermission', () => {
    it('returns true when user has sufficient permission', () => {
      const { result } = renderHook(() => usePermissionsStore());

      act(() => {
        usePermissionsStore.setState({
          permissions: {
            'data-products': FeatureAccessLevel.READ_WRITE,
          },
        });
      });

      expect(result.current.hasPermission('data-products', FeatureAccessLevel.READ_ONLY)).toBe(true);
      expect(result.current.hasPermission('data-products', FeatureAccessLevel.READ_WRITE)).toBe(true);
    });
  });
});
```

**Patterns:**
- Arrange-Act-Assert (AAA) pattern for test structure
- Descriptive test names: `test_feature_scenario_expected_result`
- Group related tests with nested describe blocks or class test organization
- Use `describe`/`it` (not `test`) for frontend tests
- Use `class Test*` with `def test_*` for backend tests

## Mocking

**Framework:**
- Python: `unittest.mock` (MagicMock, Mock, patch)
- TypeScript: Vitest mocking (`vi.fn()`, `vi.mock()`, `vi.spyOn()`)

**Patterns:**

Python:
```python
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_ws_client(self):
    """Create a mocked Databricks WorkspaceClient."""
    mock = MagicMock()
    mock.clusters.list.return_value = []
    mock.catalogs.list.return_value = []
    return mock
```

TypeScript:
```typescript
// Mock fetch globally in test setup
global.fetch = vi.fn();

// Arrange - set mock return value
(global.fetch as any).mockResolvedValueOnce({
  ok: true,
  json: async () => mockData,
});

// Clean up
afterEach(() => {
  vi.clearAllMocks();
  vi.restoreAllMocks();
});
```

**What to Mock:**
- External SDK clients (Databricks WorkspaceClient)
- HTTP requests (via `fetch`)
- Dependent managers (NotificationsManager, TagsManager)
- Global browser APIs (localStorage, fetch, ResizeObserver, IntersectionObserver)

**What NOT to Mock:**
- Repository/CRUD logic - test with real in-memory SQLite
- Zustand store mutations - test state changes directly
- Custom hooks internal logic - test via renderHook

## Fixtures and Factories

**Test Data (Python):**

```python
@pytest.fixture
def sample_product_data(self):
    """Sample data product data for testing."""
    return {
        "id": str(uuid.uuid4()),
        "name": "Test Data Product",
        "version": "1.0.0",
        "status": "draft",
    }
```

**Test Data (TypeScript):**

```typescript
const mockPermissions = {
  'data-products': FeatureAccessLevel.READ_WRITE,
  'data-contracts': FeatureAccessLevel.READ_ONLY,
};

const mockRoles = [
  {
    id: 'role-1',
    name: 'Admin',
    feature_permissions: {
      'data-products': FeatureAccessLevel.ADMIN,
    },
  },
];
```

**Location:**
- Backend: Inline in test files as fixtures
- Frontend: Inline in test files

## Test Setup (Frontend)

**File:** `src/frontend/src/test/setup.ts`

```typescript
import '@testing-library/jest-dom/vitest';
import { cleanup } from '@testing-library/react';
import { afterEach, beforeEach, vi } from 'vitest';

// Cleanup after each test
afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

// Mock IntersectionObserver
class MockIntersectionObserver implements IntersectionObserver {
  readonly root: Element | Document | null = null;
  readonly rootMargin: string = '';
  readonly thresholds: ReadonlyArray<number> = [];

  constructor(_callback: IntersectionObserverCallback, _options?: IntersectionObserverInit) {}

  observe(): void {}
  disconnect(): void {}
  unobserve(): void {}
  takeRecords(): IntersectionObserverEntry[] { return []; }
}
global.IntersectionObserver = MockIntersectionObserver;

// Mock ResizeObserver
global.ResizeObserver = class ResizeObserver {
  constructor() {}
  observe() { return null; }
  disconnect() { return null; }
  unobserve() { return null; }
};

// Mock scrollIntoView
Element.prototype.scrollIntoView = vi.fn();

// Mock getBoundingClientRect
Element.prototype.getBoundingClientRect = vi.fn(() => ({
  x: 0, y: 0, width: 0, height: 0, top: 0, right: 0, bottom: 0, left: 0,
  toJSON: vi.fn(),
}));

// Mock matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock localStorage
const localStorageMock = (() => {
  let store: Record<string, string> = {};
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => { store[key] = value.toString(); },
    removeItem: (key: string) => { delete store[key]; },
    clear: () => { store = {}; },
    get length() { return Object.keys(store).length; },
    key: (index: number) => Object.keys(store)[index] || null,
  };
})();
global.localStorage = localStorageMock as any;
```

## Coverage

**Requirements:** Not enforced via thresholds (disabled in configs)

**View Coverage:**

Backend:
```bash
hatch -e dev run test-cov          # Generates htmlcov/index.html
open src/backend/htmlcov/index.html
```

Frontend:
```bash
cd src/frontend
yarn test:coverage                  # Generates coverage/
open coverage/index.html
```

**Configuration:**

Backend (`src/pyproject.toml`):
```toml
[tool.coverage.run]
source = ["backend/src"]
omit = [
    "*/tests/*",
    "*/test_*.py",
    "*/__init__.py",
    "*/migrations/*",
    "*/alembic/*",
]

[tool.coverage.report]
precision = 2
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "@abstractmethod",
]
```

Frontend (`src/frontend/vitest.config.ts`):
```typescript
coverage: {
  provider: 'v8',
  reporter: ['text', 'json', 'html', 'lcov'],
  exclude: [
    'node_modules/',
    'src/test/',
    '**/*.d.ts',
    '**/*.config.*',
    '**/mockData',
    'src/components/ui/**',  // Exclude Shadcn base components
    '**/*.test.{ts,tsx}',
    '**/*.spec.{ts,tsx}',
  ],
  all: true,
  // Coverage thresholds disabled for now
  // lines: 80,
  // functions: 80,
  // branches: 80,
  // statements: 80,
}
```

## Test Types

**Unit Tests:**
- Scope: Single function/method in isolation
- Approach: Mock all external dependencies
- Backend: Manager methods with mocked repository and SDK
- Frontend: Store actions, hook behavior, utility functions

**Integration Tests:**
- Scope: Multiple components working together
- Approach: Real database (in-memory SQLite), mocked external APIs
- Backend: Manager + Repository + Database

**E2E Tests (Frontend):**
- Scope: Full user workflows (navigate, interact, assert)
- Approach: Real browser via Playwright, real API endpoints
- Location: `src/frontend/src/tests/*.spec.ts` and `src/frontend/tests/*.spec.ts`

**Playwright Configuration (`src/frontend/playwright.config.ts`):**
```typescript
export default defineConfig({
  timeout: 90_000,
  expect: { timeout: 10_000 },
  testDir: './src/tests',
  retries: 0,
  reporter: 'list',
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
  webServer: {
    command: 'yarn dev:frontend --port 3000',
    url: 'http://localhost:3000',
    reuseExistingServer: true,
  },
});
```

## Common Patterns

**Async Testing (Python):**
```python
@pytest.mark.asyncio
async def test_async_operation(self, manager):
    """Test async operation."""
    result = await manager.async_method()
    assert result is not None
```

**Async Testing (TypeScript):**
```typescript
it('fetches and sets permissions successfully', async () => {
  const mockData = { 'data-products': FeatureAccessLevel.READ_WRITE };
  (global.fetch as any).mockResolvedValueOnce({
    ok: true,
    json: async () => mockData,
  });

  const { result } = renderHook(() => usePermissionsStore());

  await act(async () => {
    await result.current.fetchPermissions();
  });

  expect(result.current.permissions).toEqual(mockData);
});
```

**Error Testing (Python):**
```python
def test_create_product_validation_error(self, manager, db_session):
    """Test error handling for invalid product data."""
    invalid_data = {"name": "Test"}  # Missing required fields

    with pytest.raises(ValueError, match="Invalid ODPS product data"):
        manager.create_product(invalid_data, db=db_session)
```

**Error Testing (TypeScript):**
```typescript
it('handles fetch errors gracefully', async () => {
  (global.fetch as any).mockResolvedValueOnce({
    ok: false,
    status: 500,
    json: async () => ({ detail: 'Server error' }),
  });

  const { result } = renderHook(() => usePermissionsStore());

  try {
    await act(async () => {
      await result.current.fetchPermissions();
    });
  } catch (e) {
    // Expected to throw
  }

  const storeState = usePermissionsStore.getState();
  expect(storeState.error).toBeTruthy();
});
```

**Waiting for State (TypeScript):**
```typescript
// Use waitFor for async state updates
await waitFor(() => {
  expect(result.current.appliedRoleId).toBe('role-1');
});

// Use waitFor with expect for assertions
await waitFor(() => {
  expect(global.fetch).toHaveBeenCalledWith(
    '/api/user/role-override',
    expect.objectContaining({ method: 'POST' })
  );
});
```

**E2E Testing (Playwright):**
```typescript
import { test, expect } from '@playwright/test';

test.describe('Contract-OutputPort Mapping', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('should link existing contract to output port from product side', async ({ page }) => {
    await page.click('text=Data Products');
    await page.waitForURL('**/data-products');

    const productCard = page.locator('.border').first();
    await productCard.click();

    await page.waitForSelector('text=Output Ports');

    const linkButton = page.locator('button[title="Link contract"]').first();
    if (await linkButton.isVisible()) {
      await linkButton.click();
    }

    await page.waitForSelector('text=Link Contract to Output Port');

    await page.click('[id="contract"]');
    await page.waitForSelector('role=option');
    await page.click('role=option >> nth=0');

    await page.click('button:has-text("Link Contract")');

    await page.waitForSelector('text=Contract Linked', { timeout: 10000 });
    await expect(page.locator('text=Contract:')).toBeVisible();
  });
});
```

## Known Limitations

**Component Testing:**
- Complex Radix UI components (Select, Combobox) may hang in jsdom
- These are better tested with Playwright E2E tests
- Example: `DataProductFormDialog` is skipped for this reason

**Pattern for Skipped Tests:**
```typescript
/**
 * NOTE: This test file is skipped because the component uses complex Radix UI
 * components (Select, Combobox) that don't work reliably in jsdom and cause
 * infinite render loops. These interactions are better tested with Playwright E2E tests.
 */
import { describe, it, expect } from 'vitest';

describe.skip('DataProductFormDialog', () => {
  it('renders correctly', () => {
    expect(true).toBe(true);
  });
});
```

---

*Testing analysis: 2026-03-17*
