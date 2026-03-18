# Project Research Summary

**Project:** Ontos DTP Victoria Rebrand
**Domain:** Government Visual Brand Implementation (Brownfield)
**Researched:** 2026-03-19
**Confidence:** HIGH

## Executive Summary

This is a visual rebranding project for an existing Databricks App (Ontos) to adopt the Victorian Government's Brand Victoria identity. The project involves updating colors, typography, logo, and visual elements to comply with official government brand guidelines while maintaining the existing Shadcn UI + Tailwind CSS architecture.

The recommended approach is a phased implementation starting with CSS variable replacement in `index.css`, which propagates automatically to all Shadcn UI components. This is followed by typography (self-hosted VIC fonts), logo replacement, and a systematic audit to replace 269+ instances of hardcoded colors across 64 files. The Brand Victoria intersection device (25.3-degree gradient) adds distinctive government visual language as a polish element.

Key risks include incomplete dark mode rebranding (updating only light mode colors), VIC font loading failures (licensing requires self-hosting), and accessibility contrast failures with certain Brand Victoria colors. All three must be addressed during implementation to avoid brand non-compliance and poor user experience.

## Key Findings

### Recommended Stack

The rebrand uses the existing Tailwind CSS 3.4.x + Shadcn UI stack with no new package dependencies. All implementation relies on CSS variables (HSL format without `hsl()` wrapper) for color tokens, enabling automatic propagation to Shadcn components and proper opacity modifier support.

**Core technologies:**
- **Tailwind CSS 3.4.x (existing):** CSS framework with CSS variable theming - stay on v3 stable for production government project
- **Shadcn UI (existing):** Component library using `hsl(var(--name))` pattern - theming via CSS variables is built-in
- **VIC Font Family (self-hosted):** Brand Victoria primary typography - must self-host in `public/fonts/` per licensing constraints
- **CSS Variables (HSL):** Theme tokens stored as `H S L%` channels (not `hsl()` wrapped) for Tailwind opacity modifier support

### Expected Features

**Must have (table stakes):**
- Brand Victoria color palette (Navy #201547, Blue #004c97, Teal #00b2a9, Grey #53565a, Light Grey #d9d9d6) - users expect official department colors
- DTP Victoria logo - users need to see their department identity
- VIC font family typography - mandatory per Brand Victoria guidelines
- Accessible color contrast (WCAG 2.1 AA) - required for government sites
- Favicon and browser title update - basic browser chrome branding

**Should have (competitive):**
- Intersection device accent (25.3deg gradient) - distinctive Brand Victoria visual language
- Dark mode with Brand Victoria colors - consistent brand across themes
- Brand Victoria secondary colors for charts - cohesive data visualization

**Defer (v2+):**
- Intersection device on loading states - premium polish
- Brand Victoria photography guidelines - if app adds hero images

### Architecture Approach

The rebrand follows a layered CSS architecture: `index.css` defines CSS variables, `tailwind.config.cjs` maps them to Tailwind semantic tokens (`primary`, `accent`, etc.), and Shadcn UI components consume these tokens. The critical finding is that 11 feature files contain hardcoded `violet-*` and `purple-*` colors that bypass the theme system and need manual replacement.

**Major components:**
1. **`index.css` CSS Variables** - Single source of truth for brand colors in `:root` (light) and `.dark` (dark) sections
2. **`tailwind.config.cjs`** - Maps CSS vars to semantic tokens and extends with `victoria-*` palette for direct brand color access
3. **VIC Fonts in `public/fonts/`** - Self-hosted WOFF2 files with `@font-face` declarations
4. **`UnityCatalogLogo` component** - Logo rendering with Zustand store for runtime customization

### Critical Pitfalls

1. **Incomplete Dark Mode Rebrand** - Only updating `:root` and ignoring `.dark` creates inconsistent brand experience. Solution: Update BOTH sections simultaneously and test theme toggle after every change.

2. **Hardcoded Colors Remain** - 269+ instances of `bg-gray-`, `bg-slate-`, `violet-*` classes in 64 files don't use CSS variables. Solution: Systematic grep audit and replacement with semantic tokens or `victoria-*` colors.

3. **VIC Font Loading Failures** - Wrong `@font-face` paths, missing formats, or CORS issues cause fallback to system fonts. Solution: Use absolute paths `/fonts/VIC-Regular.woff2`, include woff2 format, add `font-display: swap`.

4. **Color Contrast Accessibility Failures** - Teal #00b2a9 and Light Grey #d9d9d6 can fail WCAG AA contrast requirements. Solution: Test every color combination, define accessible text variants if needed.

5. **Intersection Device Misimplementation** - Wrong angle or colors. Solution: Use exact `25.3deg` angle, reference Brand Victoria Guidelines PDF for specifications.

## Implications for Roadmap

Based on research, suggested phase structure:

### Phase 1: Color System Update
**Rationale:** CSS variables are the foundation - all other changes depend on brand colors being defined first. Must complete both light and dark modes.
**Delivers:** Brand Victoria color palette in both themes, accessible contrast verified
**Addresses:** Color palette, accessible contrast (table stakes)
**Avoids:** Incomplete dark mode, contrast failures

### Phase 2: Typography & Logo
**Rationale:** Typography requires font files to be in place before Tailwind config references them. Logo replacement is independent but logically grouped with brand identity.
**Delivers:** VIC fonts self-hosted and loading, DTP logo in header/sidebar/favicon, browser title updated
**Uses:** Self-hosted font files, CSS `@font-face` declarations
**Avoids:** Font loading failures, missing logo identity

### Phase 3: Hardcoded Color Audit
**Rationale:** Only after Phases 1-2 can we properly audit and replace hardcoded colors, as the target palette and typography are now defined.
**Delivers:** All `violet-*`, `purple-*`, `bg-gray-*`, `bg-slate-*` patterns replaced with Brand Victoria equivalents
**Implements:** Semantic token usage across 11 identified files (layout.tsx, copilot-panel.tsx, llm-search.tsx, catalog-commander.tsx, workflow-nodes.tsx, lineage/constants.ts, knowledge tabs, hierarchy-graph-view.tsx, entity-costs-panel.tsx)
**Avoids:** Visual inconsistency, hidden brand violations

### Phase 4: Intersection Device
**Rationale:** Polish element that adds distinctive Brand Victoria visual language. Requires all core branding complete first to ensure cohesion.
**Delivers:** Reusable intersection device CSS component/utility at 25.3deg angle
**Uses:** Teal/blue brand colors in gradient
**Implements:** Header accents, section dividers, loading state enhancements

### Phase Ordering Rationale

- Phase 1 must come first because CSS variables propagate to all Shadcn components automatically - this is the "80% of the work for 20% of the effort" phase
- Phase 2 (Typography/Logo) can partially parallelize with Phase 1 but requires testing after Phase 1 is stable
- Phase 3 must wait until Phases 1-2 are complete because hardcoded colors need to be replaced with the now-defined semantic tokens
- Phase 4 is last because it's a polish element that depends on all core branding being stable

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 2 (Typography):** VIC font file procurement - need to confirm licensing terms and obtain WOFF2 files from DPC before implementation

Phases with standard patterns (skip research-phase):
- **Phase 1 (Color System):** Well-documented CSS variable patterns in Tailwind and Shadcn UI
- **Phase 3 (Hardcoded Audit):** Standard grep/search and replace workflow
- **Phase 4 (Intersection Device):** Straightforward CSS gradient implementation with documented 25.3deg spec

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Existing Tailwind/Shadcn architecture well-understood; official docs confirm CSS variable patterns |
| Features | HIGH | Brand Victoria Guidelines PDF provides explicit color/typography specifications |
| Architecture | HIGH | Codebase analysis identified exact files needing updates (11 files with hardcoded colors) |
| Pitfalls | HIGH | Based on codebase grep analysis (269 instances in 64 files) and domain knowledge of rebranding patterns |

**Overall confidence:** HIGH

### Gaps to Address

- **VIC Font File Procurement:** Research identified that VIC fonts must be self-hosted, but actual font files need to be obtained from DPC. This is a prerequisite for Phase 2 and should be confirmed before implementation begins.
- **Brand Victoria Color Accessibility Testing:** While guidelines mention accessible combinations, actual contrast testing with the app's specific text sizes and backgrounds should be done during Phase 1.

## Sources

### Primary (HIGH confidence)
- [Brand Victoria Guidelines PDF (Version 2, 2018)](https://www.vic.gov.au/sites/default/files/2018-11/brand-victoria-guidelines.pdf) - Official color palette, typography, intersection device specs
- [Tailwind CSS Customizing Colors](https://tailwindcss.com/docs/customizing-colors) - CSS variable patterns for opacity modifiers
- [Shadcn UI Theming](https://ui.shadcn.com/docs/theming) - CSS variable convention and semantic tokens

### Secondary (MEDIUM confidence)
- [Tailwind CSS Dark Mode](https://tailwindcss.com/docs/dark-mode) - Class-based dark mode switching
- [Australian Government Design System](https://designsystem.gov.au/) - Accessibility patterns reference

### Tertiary (Codebase Analysis)
- `src/frontend/src/index.css` - Current CSS variable structure
- `src/frontend/tailwind.config.cjs` - Tailwind configuration
- Grep analysis of hardcoded color patterns across codebase
- `src/frontend/src/components/layout/unity-catalog-logo.tsx` - Logo component

---
*Research completed: 2026-03-19*
*Ready for roadmap: yes*
