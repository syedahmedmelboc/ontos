# Stack Research

**Domain:** Government Brand Identity Implementation (Tailwind CSS + Shadcn UI)
**Researched:** 2026-03-19
**Confidence:** HIGH

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Tailwind CSS | 3.4.x (existing) | CSS framework with CSS variables for theming | Already in use; CSS variable pattern established in index.css. Tailwind v4 is in beta (Nov 2024) - stay on stable v3 for production government project. |
| Shadcn UI | Current (existing) | Component library built on Radix UI | Already integrated; uses `hsl(var(--name))` pattern for all colors. Theming via CSS variables is built-in and well-documented. |
| VIC Font Family | Self-hosted | Brand Victoria primary typography | Required for brand compliance. Must self-host in `public/fonts/` per project constraints - no CDN for licensing control. |
| CSS Variables (HSL) | Native | Theme tokens for colors | Shadcn UI convention; enables runtime theme switching without rebuild. Store values as `H S L%` without `hsl()` wrapper for opacity modifier support. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `@fontsource/variable` pattern | N/A | Self-hosted font loading | Use as reference for @font-face declarations in index.css. VIC fonts require manual @font-face setup. |
| `tailwindcss-animate` | Existing | Animation utilities | Already installed; continue using for intersection device animations. |
| `@tailwindcss/typography` | Existing | Prose utilities | Already installed; ensure brand colors apply to prose content. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| CSS Variables DevTools | Inspect theme tokens | Chrome/FF show computed CSS variables; helpful for debugging brand color application |
| Color contrast checker | WCAG 2.0 AA compliance | Brand Victoria guidelines require accessible color combinations - verify all text/background pairs |

## Implementation Patterns

### 1. CSS Variable Structure for Brand Victoria Colors

The existing `index.css` uses HSL values without the `hsl()` wrapper. This pattern must continue:

```css
@layer base {
  :root {
    /* Brand Victoria Primary Colors */
    --vic-navy: 263 59% 18%;        /* #201547 */
    --vic-blue: 210 100% 30%;       /* #004c97 */
    --vic-teal: 176 100% 35%;       /* #00b2a9 */

    /* Brand Victoria Supporting Colors */
    --vic-grey: 210 4% 35%;         /* #53565a */
    --vic-light-grey: 40 3% 85%;    /* #d9d9d6 */

    /* Brand Victoria Accent Colors */
    --vic-orange: 36 100% 54%;      /* #ff9e1b */
    --vic-red: 356 62% 42%;         /* #af272f */
    --vic-purple: 287 74% 34%;      /* #87189d */
  }
}
```

**Why HSL without wrapper:** Tailwind opacity modifiers (`bg-primary/50`) require the variable to contain just the color channels, not the `hsl()` function. Reference: [Tailwind CSS Customizing Colors](https://tailwindcss.com/docs/customizing-colors).

### 2. Tailwind Config Brand Color Mapping

Map Brand Victoria colors to semantic Shadcn UI variables:

```javascript
// tailwind.config.cjs
module.exports = {
  theme: {
    extend: {
      colors: {
        // Semantic mappings to Brand Victoria
        primary: {
          DEFAULT: 'hsl(var(--vic-navy))',
          foreground: 'hsl(var(--vic-light-grey))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--vic-blue))',
          foreground: 'hsl(var(--vic-light-grey))',
        },
        accent: {
          DEFAULT: 'hsl(var(--vic-teal))',
          foreground: 'hsl(var(--vic-navy))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--vic-red))',
          foreground: 'hsl(var(--vic-light-grey))',
        },
        // Direct brand color access
        vic: {
          navy: 'hsl(var(--vic-navy))',
          blue: 'hsl(var(--vic-blue))',
          teal: 'hsl(var(--vic-teal))',
          grey: 'hsl(var(--vic-grey))',
          'light-grey': 'hsl(var(--vic-light-grey))',
          orange: 'hsl(var(--vic-orange))',
          red: 'hsl(var(--vic-red))',
          purple: 'hsl(var(--vic-purple))',
        },
      },
    },
  },
}
```

**Why semantic mapping:** Shadcn components use `primary`, `secondary`, `accent`, etc. Mapping brand colors to these semantics ensures all existing components receive brand colors without code changes.

### 3. Dark Mode Brand Color Strategy

Brand Victoria colors need dark mode variants that maintain brand identity:

```css
@layer base {
  .dark {
    /* Dark mode uses lighter/tinted brand colors */
    --vic-navy: 263 30% 25%;        /* Lighter navy for dark bg */
    --vic-blue: 210 80% 50%;        /* Brighter blue for contrast */
    --vic-teal: 176 70% 45%;        /* Slightly muted teal */

    /* Background uses brand dark tones */
    --background: 263 59% 8%;       /* Very dark navy */
    --foreground: 40 3% 95%;        /* Off-white */

    /* Primary in dark mode */
    --primary: 40 3% 95%;           /* Light text on dark */
    --primary-foreground: 263 59% 18%; /* Navy for contrast */
  }
}
```

**Why this approach:** Dark mode must still feel like Brand Victoria. Using dark navy as the base background maintains brand recognition while ensuring accessibility.

### 4. VIC Font Self-Hosting Pattern

Place font files in `public/fonts/` and declare in `index.css`:

```css
@font-face {
  font-family: 'VIC';
  src: url('/fonts/VIC-Regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'VIC';
  src: url('/fonts/VIC-Bold.woff2') format('woff2');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}

/* Additional weights: SemiBold (600), Medium (500), Light (300) */

@layer base {
  body {
    font-family: 'VIC', Arial, sans-serif;
  }
}
```

**Why self-hosting:**
- VIC font is a licensed government asset - no public CDN exists
- Project constraint explicitly requires self-hosting
- `font-display: swap` prevents FOIT (Flash of Invisible Text)
- Arial fallback per Brand Victoria alternative font guidelines

### 5. Intersection Device Implementation

The Brand Victoria intersection device uses a +/- 25.3 degree angle derived from the triangle logo:

```css
/* Intersection device angle constant */
:root {
  --vic-angle: 25.3deg;
}

/* CSS utility for intersection device */
.vic-intersection {
  background: linear-gradient(
    calc(var(--vic-angle) * -1),
    hsl(var(--vic-teal) / 0.8) 0%,
    hsl(var(--vic-teal) / 0.8) 50%,
    transparent 50%
  );
}
```

**Tailwind plugin approach (optional):**

```javascript
// tailwind.config.cjs
module.exports = {
  theme: {
    extend: {
      backgroundImage: {
        'vic-intersection': `linear-gradient(-25.3deg, hsl(var(--vic-teal) / 0.8) 0%, hsl(var(--vic-teal) / 0.8) 50%, transparent 50%)`,
      },
    },
  },
}
```

## Installation

No new packages required - all implementation uses existing Tailwind CSS + Shadcn UI infrastructure.

**Font files needed:**
- Obtain VIC font files (WOFF2 format preferred) from DTP/DPC
- Place in `src/frontend/public/fonts/`
- Add @font-face declarations to `src/frontend/src/index.css`

## Alternatives Considered

| Recommended | Alternative | Why Not |
|-------------|-------------|---------|
| CSS Variables (HSL) | CSS Variables (OKLCH) | Shadcn UI uses HSL convention; OKLCH support is newer. Tailwind v4 beta supports OKLCH but project is on stable v3. |
| Self-hosted VIC fonts | Google Fonts / Adobe Fonts | VIC is not available on any CDN. Government licensing requires self-hosting. |
| Semantic color mapping | Direct brand color usage | Semantic mapping (`primary`, `accent`) ensures all Shadcn components get brand colors automatically. Direct usage would require updating every component. |
| Tailwind v3.4.x | Tailwind v4.x | v4 is in beta (Nov 2024). Government projects should use stable releases. Migration can be considered after v4 stable release. |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| `hsl()` in CSS variable values | Breaks Tailwind opacity modifiers (`bg-primary/50`) | Store as `H S L%` channels only |
| RGB/HEX in CSS variables | Inconsistent with Shadcn UI convention; opacity modifiers won't work | Use HSL format consistently |
| `!important` for color overrides | Breaks cascade; makes debugging harder | Use proper CSS layer ordering and specificity |
| Tailwind v4 `@theme` directive | Not available in v3; requires v4 upgrade | Continue with `tailwind.config.cjs` + CSS variables |
| External font CDNs | Licensing and availability concerns; network dependency | Self-host in `public/fonts/` |

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| Tailwind CSS 3.4.x | Shadcn UI (current) | Full compatibility via CSS variables |
| Tailwind CSS 3.4.x | Vite 6.x | Existing setup works; no changes needed |
| React 18.x | Shadcn UI | Full compatibility |
| VIC Font (WOFF2) | All modern browsers | IE11 not supported (not a concern for Databricks Apps) |

## Key Decisions for Roadmap

1. **Semantic color mapping first:** Map Brand Victoria colors to Shadcn's `primary`, `secondary`, `accent`, etc. This gets 80% of components rebranded with minimal changes.

2. **Direct brand colors for special cases:** Add `vic-*` colors for intersection device, charts, and components that need specific brand colors beyond the semantic palette.

3. **Dark mode requires brand adaptation:** Navy (#201547) cannot be the primary color on dark backgrounds. Use inverted/lighter variants while maintaining brand recognition.

4. **Font loading performance:** Use `font-display: swap` and preload critical weights to avoid layout shift during font load.

## Sources

- [Tailwind CSS Customizing Colors](https://tailwindcss.com/docs/customizing-colors) - CSS variable patterns for opacity modifiers (HIGH confidence)
- [Shadcn UI Theming](https://ui.shadcn.com/docs/theming) - CSS variable convention, `@theme inline` directive for new colors (HIGH confidence)
- [Tailwind CSS Dark Mode](https://tailwindcss.com/docs/dark-mode) - Class-based dark mode switching with `.dark` class (HIGH confidence)
- [Tailwind CSS v4 Beta Blog](https://tailwindcss.com/blog/tailwindcss-v4-beta) - v4 status, stay on v3 for production (HIGH confidence)
- [Brand Victoria Guidelines PDF](https://www.vic.gov.au/sites/default/files/2018-11/brand-victoria-guidelines.pdf) - Official color palette (#201547, #004c97, #00b2a9, etc.), VIC font family, intersection device angle (+/- 25.3deg) (HIGH confidence)

---

*Stack research for: Brand Victoria Visual Rebrand*
*Researched: 2026-03-19*
