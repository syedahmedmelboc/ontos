# Phase 4: Intersection Device - Research

**Researched:** 2026-03-19
**Domain:** CSS gradients, Tailwind utility patterns, Brand Victoria visual identity
**Confidence:** HIGH

## Summary

This phase implements the Brand Victoria "intersection device" - a distinctive visual accent element featuring a +/-25.3 degree gradient transitioning from Navy (#201547) through Blue (#004c97) to Teal (#00b2a9). The intersection device is derived from the Victoria triangle logo and provides brand recognition when applied to key UI dividers and accents.

**Primary recommendation:** Create a reusable CSS utility class `.intersection-device` in index.css using a 3-stop linear-gradient at 25.3deg, applied to header dividers and other key brand elements.

<phase_requirements>

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| INT-01 | CSS utility class for +/-25.3 degree gradient accent (Navy->Blue->Teal) | CSS linear-gradient syntax, Tailwind @layer utilities, existing gradient patterns in codebase |
| INT-02 | Intersection device applied to header divider or key UI element | Header component structure, sidebar divider location, Separator component pattern |

</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| CSS linear-gradient | Native | Gradient rendering | Browser-native, no dependencies |
| Tailwind @layer utilities | 3.x | CSS utility organization | Already in use via tailwind.config.cjs |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| CSS Variables | Native | Color value reuse | For HSL values from Phase 1 |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| CSS utility class | Tailwind arbitrary value `bg-[linear-gradient(...)]` | Utility class is reusable, maintainable, self-documenting |
| Inline style | Utility class | Utility class integrates with Tailwind layering, can be themed |

**Installation:**
No new packages required - uses existing CSS and Tailwind infrastructure.

## Architecture Patterns

### Recommended Implementation Location

```
src/frontend/src/
├── index.css                    # Add .intersection-device utility class
├── components/
│   ├── layout/
│   │   ├── header.tsx           # Apply to border-b divider
│   │   └── sidebar.tsx          # Apply to border-b divider (logo area)
│   └── ui/
│       └── separator.tsx        # Optional variant with intersection device
```

### Pattern 1: CSS Utility Class (Recommended)

**What:** A reusable CSS class that applies the Brand Victoria intersection device gradient as a decorative element.

**When to use:** On dividers, section separators, or any UI element requiring brand accent.

**Syntax:**
```css
/* Source: Brand Victoria Guidelines - +/-25.3 degree gradient from triangle logo */
.intersection-device {
  background: linear-gradient(
    25.3deg,
    hsl(var(--primary)) 0%,        /* Navy #201547 in light, Teal in dark */
    hsl(var(--secondary)) 50%,     /* Blue #004c97 */
    hsl(var(--accent)) 100%        /* Teal #00b2a9 in light, Blue in dark */
  );
}

/* For horizontal dividers - 2px height bar */
.intersection-device-bar {
  height: 2px;
  background: linear-gradient(
    25.3deg,
    hsl(var(--primary)) 0%,
    hsl(var(--secondary)) 50%,
    hsl(var(--accent)) 100%
  );
}
```

**Example usage in Header:**
```tsx
// header.tsx - replace border-b with intersection device bar
<header className="sticky top-0 z-40 flex h-16 items-center gap-4 bg-sidebar/95 px-6 backdrop-blur">
  {/* ... header content ... */}
</header>
{/* Intersection device bar below header */}
<div className="intersection-device-bar" />
```

### Pattern 2: Pseudo-element Approach

**What:** Use ::after pseudo-element to add intersection device without extra DOM element.

**When to use:** When you want to add the accent to existing elements without changing HTML structure.

**Example:**
```css
.header-with-intersection::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(
    25.3deg,
    hsl(var(--primary)) 0%,
    hsl(var(--secondary)) 50%,
    hsl(var(--accent)) 100%
  );
}
```

### Pattern 3: Separator Component Variant

**What:** Add an `intersection` variant to the existing Separator component.

**When to use:** When using Separator component for brand accent sections.

**Example:**
```tsx
// separator.tsx - add variant prop
interface SeparatorProps extends React.ComponentPropsWithoutRef<typeof SeparatorPrimitive.Root> {
  variant?: 'default' | 'intersection';
}

// Usage
<Separator variant="intersection" className="h-0.5" />
```

### Anti-Patterns to Avoid

- **Anti-pattern: Using hex color values directly** - Bypasses theme system, breaks dark mode.
  Instead: Use CSS variables `hsl(var(--primary))` for automatic light/dark mode support.

- **Anti-pattern: Applying gradient to border-color** - CSS gradients cannot be used with border-color.
  Instead: Use a separate div element or pseudo-element with background gradient.

- **Anti-pattern: Arbitrary angle variations** - Brand Victoria specifies +/-25.3 degrees.
  Instead: Use exactly 25.3deg (or -25.3deg for opposite direction).

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Gradient utility | Inline styles or arbitrary Tailwind values | CSS utility class in @layer utilities | Reusable, maintainable, self-documenting |
| Brand accent colors | Hardcoded hex values | CSS variables from Phase 1 | Automatic dark mode support, consistency |
| Divider styling | border-bottom with gradient | Separate div with gradient background | CSS gradients don't work on border-color |

**Key insight:** The intersection device should use semantic tokens (--primary, --secondary, --accent) which already swap values for dark mode in Phase 1. This ensures the gradient looks correct in both themes.

## Common Pitfalls

### Pitfall 1: Incorrect Angle Interpretation

**What goes wrong:** Using 25.3deg when the design calls for -25.3deg (or vice versa), causing the gradient to flow in the wrong direction.

**Why it happens:** The Brand Victoria guidelines specify "+/-25.3 degrees" meaning either direction is valid, but consistency matters.

**How to avoid:** Choose one direction (25.3deg for left-to-right gradient) and use consistently. Document the choice.

**Warning signs:** Gradient flows opposite to logo triangle direction, inconsistent gradient direction across UI elements.

### Pitfall 2: Using Hardcoded Hex Colors

**What goes wrong:** Gradient uses `#201547, #004c97, #00b2a9` directly instead of CSS variables.

**Why it happens:** Direct hex values seem simpler than variable syntax.

**How to avoid:** Always use `hsl(var(--primary))`, `hsl(var(--secondary))`, `hsl(var(--accent))` to inherit Phase 1's dark mode adaptations.

**Warning signs:** Dark mode shows Navy gradient instead of Teal-based gradient (Navy has poor contrast on dark backgrounds).

### Pitfall 3: Applying to Wrong Elements

**What goes wrong:** Intersection device applied to too many elements, diluting brand impact.

**Why it happens:** The gradient looks good and developers want to use it everywhere.

**How to avoid:** Reserve intersection device for key brand moments: header dividers, section separators in hero areas, footer accents. Not for every card border.

**Warning signs:** Visual clutter, brand accent loses distinction.

### Pitfall 4: Height/Size Inconsistency

**What goes wrong:** Intersection device bars have varying heights (1px, 2px, 4px) across the application.

**Why it happens:** No standardized sizing defined.

**How to avoid:** Define standard heights: 2px for dividers, 4px for prominent accents.

**Warning signs:** Inconsistent visual weight across intersection device instances.

## Code Examples

### Intersection Device CSS Utility (Primary Pattern)

```css
/* Source: Brand Victoria Guidelines + MDN linear-gradient documentation */
/* Add to index.css in @layer utilities section */

@layer utilities {
  /* Intersection device gradient - Brand Victoria +/-25.3 degree accent */
  .intersection-device {
    background: linear-gradient(
      25.3deg,
      hsl(var(--primary)) 0%,
      hsl(var(--secondary)) 50%,
      hsl(var(--accent)) 100%
    );
  }

  /* Intersection device as horizontal bar (for dividers) */
  .intersection-device-bar {
    height: 2px;
    width: 100%;
    background: linear-gradient(
      25.3deg,
      hsl(var(--primary)) 0%,
      hsl(var(--secondary)) 50%,
      hsl(var(--accent)) 100%
    );
  }

  /* Intersection device - opposite direction variant */
  .intersection-device-reverse {
    background: linear-gradient(
      -25.3deg,
      hsl(var(--primary)) 0%,
      hsl(var(--secondary)) 50%,
      hsl(var(--accent)) 100%
    );
  }
}
```

### Application to Header Divider

```tsx
// Source: header.tsx current structure
// BEFORE:
<header className="sticky top-0 z-40 flex h-16 items-center gap-4 border-b bg-sidebar/95 px-6 backdrop-blur">

// AFTER (Option A - replace border-b with gradient bar below):
<header className="sticky top-0 z-40 flex h-16 items-center gap-4 bg-sidebar/95 px-6 backdrop-blur supports-[backdrop-filter]:bg-sidebar/60">
  {/* ... header content ... */}
</header>
<div className="intersection-device-bar" />

// AFTER (Option B - add class to header with ::after):
<header className="sticky top-0 z-40 flex h-16 items-center gap-4 bg-sidebar/95 px-6 backdrop-blur header-with-intersection">
```

### Application to Sidebar Logo Divider

```tsx
// Source: sidebar.tsx current structure
// BEFORE:
<div className="flex h-16 items-center justify-center border-b px-4 shrink-0">

// AFTER:
<div className="flex h-16 items-center justify-center px-4 shrink-0">
  <Link to="/" className="flex items-center gap-2 font-semibold">
    <UnityCatalogLogo className={cn("h-8 w-8 transition-all", isCollapsed ? "h-10 w-10" : "h-10 w-10")} />
  </Link>
</div>
<div className="intersection-device-bar" />
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Single-color dividers | Gradient intersection device | Brand Victoria guidelines | Distinctive brand recognition |
| Hardcoded colors | CSS variable semantic tokens | Phase 1 | Automatic dark mode support |
| Border-bottom styling | Separate gradient element | CSS limitation | Gradients require background, not border |

**Deprecated/outdated:**
- Using `border-image` for gradient borders: Poor browser support for gradient border-image, use background element instead.
- SVG gradient backgrounds: Unnecessary complexity when CSS linear-gradient is sufficient.

## Open Questions

1. **Should intersection device be visible in dark mode with the same angle?**
   - What we know: Phase 1 swapped primary from Navy to Teal for dark mode contrast.
   - What's unclear: Whether the intersection device angle should also invert in dark mode.
   - Recommendation: Keep the same 25.3deg angle; color swap via semantic tokens is sufficient. The gradient will show Teal->Blue->Blue (since accent also becomes Blue in dark mode).

2. **Should Separator component have an `intersection` variant?**
   - What we know: Separator component exists and is used for dividers.
   - What's unclear: Whether to extend it or use standalone div elements.
   - Recommendation: Start with standalone `.intersection-device-bar` divs. Add Separator variant only if pattern becomes common enough to warrant component abstraction.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | vitest (see vitest.config.ts) |
| Config file | vitest.config.ts |
| Quick run command | `cd src/frontend && yarn test --run` |
| Full suite command | `cd src/frontend && yarn test` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| INT-01 | CSS utility class produces correct gradient | visual regression | N/A - manual verification | No |
| INT-02 | Intersection device visible on header divider | visual regression | N/A - manual verification | No |

### Sampling Rate
- **Per task commit:** Visual inspection in browser (light + dark mode)
- **Per wave merge:** Visual comparison screenshots
- **Phase gate:** Manual verification that gradient appears on target elements

### Wave 0 Gaps
- No existing tests for CSS utility classes - visual verification is appropriate
- No component tests for decorative elements - manual verification sufficient

*Note: This is a CSS-only change. Visual verification in both light and dark modes is the appropriate validation method.*

## Sources

### Primary (HIGH confidence)
- PROJECT.md - Brand Victoria intersection device specification (+/-25.3 degree gradient from triangle logo)
- Phase 1 CONTEXT.md - Color palette (Navy #201547, Blue #004c97, Teal #00b2a9) and semantic token mapping
- MDN linear-gradient documentation - https://developer.mozilla.org/en-US/docs/Web/CSS/gradient/linear-gradient

### Secondary (MEDIUM confidence)
- index.css - Existing CSS variable system established in Phase 1
- tailwind.config.cjs - Existing Tailwind configuration patterns
- header.tsx, sidebar.tsx - Current divider implementation locations

### Tertiary (LOW confidence)
- Brand Victoria Guidelines PDF (referenced in PROJECT.md) - https://www.vic.gov.au/sites/default/files/2018-11/brand-victoria-guidelines.pdf

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - CSS linear-gradient is native, well-documented, already used in codebase
- Architecture: HIGH - Clear pattern from existing gradient usage (see layout.tsx copilot button)
- Pitfalls: HIGH - CSS gradient behavior is well-understood, dark mode handled by semantic tokens

**Research date:** 2026-03-19
**Valid until:** 30 days (stable CSS patterns)
