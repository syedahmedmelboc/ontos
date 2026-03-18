# Architecture Research

**Domain:** Visual Rebrand (Tailwind CSS + Shadcn UI)
**Researched:** 2026-03-19
**Confidence:** HIGH

## Standard Architecture

### System Overview

```
+------------------------------------------------------------------+
|                        CSS Variables Layer                        |
|  src/frontend/src/index.css                                       |
|  --primary, --secondary, --accent, --destructive, --chart-*       |
|  Light mode (:root) and Dark mode (.dark)                         |
+------------------------------------------------------------------+
                                |
                                v
+------------------------------------------------------------------+
|                     Tailwind Config Layer                         |
|  src/frontend/tailwind.config.cjs                                 |
|  Maps CSS variables to Tailwind semantic tokens                   |
|  colors: { primary: 'hsl(var(--primary))', ... }                  |
+------------------------------------------------------------------+
                                |
                                v
+------------------------------------------------------------------+
|                     Shadcn UI Components                          |
|  src/frontend/src/components/ui/                                  |
|  Button, Dialog, Form, etc. use Tailwind semantic classes         |
|  className="bg-primary text-primary-foreground"                   |
+------------------------------------------------------------------+
                                |
                                v
+------------------------------------------------------------------+
|                      Feature Components                           |
|  src/frontend/src/components/[feature]/                           |
|  src/frontend/src/views/                                          |
|  Mix of semantic tokens + HARDCODED brand colors (violet/purple)  |
+------------------------------------------------------------------+
```

### Component Responsibilities

| Component | Responsibility | Implementation |
|-----------|----------------|----------------|
| `index.css` | CSS custom properties (HSL values) | `:root` for light mode, `.dark` for dark mode |
| `tailwind.config.cjs` | Map CSS vars to Tailwind tokens | `colors: { primary: 'hsl(var(--primary))' }` |
| Shadcn UI components | Reusable UI primitives | Use semantic tokens (`bg-primary`, `text-muted-foreground`) |
| Feature components | Business UI | Mix: semantic + hardcoded colors (needs audit) |
| `UnityCatalogLogo` | Logo rendering | Zustand store for `customLogoUrl`, fallback to `/ontos-logo.svg` |
| `ui-customization-store` | Runtime customization | Fetches settings from `/api/settings/ui-customization` |

## Recommended Project Structure for Rebrand

```
src/frontend/
+-- public/
|   +-- fonts/                    # NEW: VIC font files (self-hosted)
|   |   +-- VIC-Regular.woff2
|   |   +-- VIC-SemiBold.woff2
|   |   +-- VIC-Bold.woff2
|   |   +-- VIC-Medium.woff2
|   |   +-- VIC-Light.woff2
|   +-- dtp-victoria-logo.svg     # NEW: DTP logo
|   +-- favicon.ico               # UPDATE: DTP favicon
+-- src/
|   +-- index.css                 # UPDATE: CSS variables with Brand Victoria HSL
|   +-- index.tsx                 # Font face declarations
|   +-- components/
|   |   +-- ui/                   # No changes (uses semantic tokens)
|   |   +-- layout/
|   |   |   +-- layout.tsx        # UPDATE: Copilot tab gradient (violet->teal)
|   |   +-- unity-catalog-logo.tsx # UPDATE: Default to DTP logo
|   +-- views/                    # AUDIT: Hardcoded violet/purple
+-- tailwind.config.cjs           # UPDATE: Extend with Brand Victoria palette
+-- index.html                    # UPDATE: Title, favicon link
```

### Structure Rationale

- **`public/fonts/`**: VIC fonts must be self-hosted per licensing constraints. WOFF2 format for optimal web performance.
- **`index.css`**: Single source of truth for color tokens. Updating here propagates to ALL Shadcn components automatically.
- **`tailwind.config.cjs`**: Add Brand Victoria specific colors as extended palette for cases where semantic tokens don't apply.
- **Hardcoded color audit**: Components using `violet-*` or `purple-*` need conversion to Brand Victoria accent colors.

## Architectural Patterns

### Pattern 1: CSS Variable Propagation

**What:** All UI colors flow from CSS variables defined in `index.css`. Shadcn UI components reference these via `hsl(var(--name))` in Tailwind classes.

**When to use:** This is the primary pattern. Use for ALL color decisions.

**Trade-offs:**
- (+) Single point of change for theme updates
- (+) Automatic dark mode support via `.dark` class
- (-) Requires HSL color format (Brand Victoria uses HEX)
- (-) Indirect: must convert Brand Victoria HEX to HSL

**Example:**
```css
/* index.css - Light mode */
:root {
  --primary: 260 85% 35%;      /* Brand Victoria Purple #87189d converted to HSL */
  --primary-foreground: 0 0% 100%;
}

/* index.css - Dark mode */
.dark {
  --primary: 260 85% 45%;      /* Lighter purple for dark mode visibility */
  --primary-foreground: 0 0% 100%;
}
```

### Pattern 2: Extended Tailwind Palette

**What:** Add Brand Victoria specific colors to `tailwind.config.cjs` for use outside Shadcn components.

**When to use:** When semantic tokens (primary, secondary) don't fit the context (e.g., chart colors, lineage node colors, intersection device gradient).

**Trade-offs:**
- (+) Direct access to brand colors
- (+) Can use alongside semantic tokens
- (-) More colors to maintain
- (-) Risk of inconsistent usage

**Example:**
```javascript
// tailwind.config.cjs
theme: {
  extend: {
    colors: {
      // ... existing semantic tokens ...
      victoria: {
        navy: '#201547',
        blue: '#004c97',
        teal: '#00b2a9',
        orange: '#ff9e1b',
        red: '#af272f',
        purple: '#87189d',
        grey: '#53565a',
        lightGrey: '#d9d9d6',
      }
    }
  }
}
```

### Pattern 3: Logo Customization Store

**What:** Existing `useUICustomizationStore` allows runtime logo swap via `customLogoUrl` setting.

**When to use:** For admin-configurable branding. NOT recommended for DTP rebrand (should be default, not configurable).

**Trade-offs:**
- (+) No code change needed for logo swap
- (-) Requires backend configuration
- (-) Falls back to Ontos logo if unset

**Recommendation:** Update default fallback in `UnityCatalogLogo` component directly.

## Data Flow

### Brand Color Propagation

```
Brand Victoria Guidelines (HEX colors)
    |
    v [Manual conversion]
CSS Variables (HSL in index.css)
    |
    v [Tailwind config reference]
Tailwind Semantic Tokens (hsl(var(--primary)))
    |
    v [Component classes]
Shadcn UI Components (bg-primary, text-primary)
    |
    v [DOM rendering]
User Interface
```

### Logo Flow

```
app.tsx (initialization)
    |
    v
useUICustomizationStore.fetchSettings()
    |
    v [API call]
GET /api/settings/ui-customization
    |
    v [Response]
{ custom_logo_url: string | null }
    |
    v
UnityCatalogLogo component
    |
    +-- customLogoUrl exists? --> Render custom logo
    |                                  |
    +-- customLogoUrl null/errored --> Render /ontos-logo.svg
```

### Theme Toggle Flow

```
ThemeToggle component
    |
    v [User click]
toggleTheme() from ThemeProvider
    |
    v [DOM mutation]
document.documentElement.classList.toggle('dark')
    |
    v [CSS cascade]
.dark selector activates in index.css
    |
    v
All CSS variables update to dark mode values
```

## Hardcoded Color Audit

Files using `violet-*` or `purple-*` Tailwind classes that need updating:

| File | Lines | Context | Recommended Replacement |
|------|-------|---------|------------------------|
| `layout.tsx` | 44-46 | Copilot tab gradient | `from-victoria-teal to-victoria-blue` |
| `copilot-panel.tsx` | 41, 266, 354, 392 | AI assistant branding | Use victoria-teal |
| `llm-search.tsx` | 74, 722, 748-749, 774 | AI search branding | Use victoria-teal |
| `catalog-commander.tsx` | 942, 972-973, 1007, 1059 | AI assistant elements | Use victoria-teal |
| `workflow-nodes.tsx` | 66-68, 389 | Workflow node styling | Use victoria-blue or victoria-teal |
| `lineage/constants.ts` | 16, 27 | LogicalEntity/Schema node colors | Use victoria-purple |
| `knowledge/concepts-tab.tsx` | 54, 62 | Individual concept styling | Use victoria-teal |
| `knowledge/collections-tab.tsx` | 63 | Ontology collection styling | Use victoria-purple |
| `knowledge/node-links-panel.tsx` | 49 | Domain link styling | Use victoria-blue |
| `hierarchy-graph-view.tsx` | 46 | Schema node styling | Use victoria-purple |
| `entity-costs-panel.tsx` | 24 | Storage cost color | Use victoria-purple |

**Total files requiring updates:** 11

## Brand Victoria Color Mappings

### Primary Palette (Semantic Tokens)

| Semantic Token | Light Mode | Dark Mode | Brand Victoria Source |
|----------------|------------|-----------|----------------------|
| `--primary` | Purple `#87189d` | Lighter purple | Accent: Purple |
| `--secondary` | Grey `#53565a` | Light grey | Supporting: Grey |
| `--accent` | Teal `#00b2a9` | Lighter teal | Primary: Teal |
| `--destructive` | Red `#af272f` | Lighter red | Accent: Red |
| `--background` | White `#ffffff` | Navy `#201547` | Primary: Navy (dark mode) |
| `--sidebar-background` | Light Grey `#d9d9d6` | Navy variant | Supporting: Light Grey |

### Chart Palette

| Token | Brand Victoria Color |
|-------|---------------------|
| `--chart-1` | Navy `#201547` |
| `--chart-2` | Blue `#004c97` |
| `--chart-3` | Teal `#00b2a9` |
| `--chart-4` | Orange `#ff9e1b` |
| `--chart-5` | Red `#af272f` |

## Intersection Device Implementation

The Brand Victoria intersection device uses a +/- 25.3 degree angle derived from the triangle logo. For web implementation:

```css
/* Intersection device gradient */
.intersection-device {
  background: linear-gradient(
    -25.3deg,
    hsl(var(--victoria-teal)) 0%,
    hsl(var(--victoria-blue)) 100%
  );
}
```

**Recommended locations:**
1. Header accent line (thin gradient bar)
2. Loading states / skeletons
3. Feature announcement banners

## Anti-Patterns

### Anti-Pattern 1: Hardcoded HEX Colors in Components

**What people do:** Use `#87189d` directly in Tailwind classes or inline styles.

**Why it's wrong:** Bypasses theme system, breaks dark mode, creates maintenance burden.

**Do this instead:** Convert to CSS variable or extended Tailwind palette color.

### Anti-Pattern 2: Ignoring Dark Mode

**What people do:** Only update light mode CSS variables, leaving dark mode unchanged.

**Why it's wrong:** Dark mode users see inconsistent branding (old Ontos/Databricks colors).

**Do this instead:** Update BOTH `:root` and `.dark` sections in `index.css` with appropriate Brand Victoria values.

### Anti-Pattern 3: Skipping Font Face Declarations

**What people do:** Reference VIC font in Tailwind config without `@font-face` declarations.

**Why it's wrong:** Font won't load, falls back to system font, brand compliance fails.

**Do this instead:** Add `@font-face` rules at top of `index.css` before Tailwind directives.

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| VIC Font Files | Self-hosted in `/public/fonts/` | No CDN allowed per licensing |
| Brand Victoria Guidelines | Reference document | https://www.vic.gov.au/brand-victoria |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| `index.css` <-> `tailwind.config.cjs` | CSS variables via `hsl(var(--))` | Single direction: CSS vars are source of truth |
| `tailwind.config.cjs` <-> Components | Tailwind class names | Components consume tokens |
| `ui-customization-store` <-> `UnityCatalogLogo` | Zustand state | Runtime customization (optional) |

## Build Order Implications

Phase dependencies for rebrand implementation:

```
Phase 1: CSS Variables (index.css)
    |
    v [No build dependency]
Phase 2: Tailwind Config (tailwind.config.cjs)
    |
    v [Requires Phase 1+2 for testing]
Phase 3: Font Files (@font-face in index.css)
    |
    v [Requires Phase 1-3 for visual testing]
Phase 4: Logo & Favicon (public/, components)
    |
    v [Requires Phase 1-4 for visual testing]
Phase 5: Hardcoded Color Audit (11 files)
    |
    v [Full visual regression testing]
Phase 6: Intersection Device (CSS patterns)
```

**Critical path:** CSS Variables -> Tailwind Config -> Visual Testing

**Parallel work:** Logo/Favicon preparation can happen independently of code changes.

## Sources

- Brand Victoria Guidelines (official PDF): https://www.vic.gov.au/sites/default/files/2018-11/brand-victoria-guidelines.pdf
- Tailwind CSS theming documentation: https://tailwindcss.com/docs/customizing-colors#using-css-variables
- Shadcn UI theming guide: https://ui.shadcn.com/docs/theming

---
*Architecture research for: Visual Rebrand (Tailwind CSS + Shadcn UI)*
*Researched: 2026-03-19*
