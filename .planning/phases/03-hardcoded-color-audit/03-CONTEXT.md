# Phase 3: Hardcoded Color Audit - Context

**Gathered:** 2026-03-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Replace all hardcoded `violet-*`, `purple-*`, and non-brand `gray/slate-*` Tailwind classes with Brand Victoria equivalents across ~20 component files. This phase does ONLY Tailwind class names in component code — no CSS variable changes, no backend changes.

</domain>

<decisions>
## Implementation Decisions

### AI Feature Colors
- **AI gradient:** Replace `from-violet-500 to-purple-600` with `from-teal-600 to-blue-700` (Brand Victoria Teal→Blue)
- **AI icons (Sparkles, Zap):** Use `text-primary` instead of `text-purple-500` or `text-violet-500`

### Graph/Lineage Node Colors
- **Semantic mapping with visual distinction:**
  - `violet-*` → `teal-*` (accent color)
  - `purple-*` → `blue-*` (secondary color)
  - `slate-*` → `muted` or `text-muted-foreground`
- **Maint visual distinction** between entity types (DataDomain, LogicalEntity, Column, Schema, etc.)

### Status Badge Colors
- Use semantic tokens (`bg-muted`, `bg-secondary`, `bg-destructive`, etc.) instead of hardcoded gray/slate/purple
- Semantic tokens handle light/dark mode automatically

### Dark Mode React Flow Overrides
- Replace `text-slate-300` and `text-slate-200` in index.css with `text-muted-foreground`
- Consistent with Phase 1 dark mode decisions

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Brand Victoria Guidelines
- `https://www.vic.gov.au/sites/default/files/2018-11/brand-victoria-guidelines.pdf` — Official Brand Victoria Guidelines (Version 2, 2018). Defines color palette, typography, logo usage, intersection device.

### Project Research
- `.planning/research/ARCHITECTURE.md` — Lists 11 files with hardcoded colors to be addressed in Phase 3

### Prior Phase Context
- `.planning/phases/01-color-system/01-CONTEXT.md` — Color decisions, semantic token mapping (Phase 1 complete)
- `.planning/phases/02-typography-logo/02-CONTEXT.md` — Typography decisions (Phase 2 complete)

### Existing Code
- `src/frontend/src/index.css` — CSS variables with Brand Victoria values (Phase 1 complete)
- `src/frontend/tailwind.config.cjs` — Tailwind config with VIC font family (Phase 2 complete)
- `src/frontend/src/components/copilot/copilot-panel.tsx` — AI gradient usage
- `src/frontend/src/components/search/llm-search.tsx` — AI gradient usage
- `src/frontend/src/views/catalog-commander.tsx` — AI gradient usage
- `src/frontend/src/components/lineage/constants.ts` — Graph node colors
- `src/frontend/src/components/hierarchy/hierarchy-graph-view.tsx` — Graph node colors
- `src/frontend/src/types/dataset.ts` — Status badge colors

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **CSS Variable System:** Established in Phase 1 — semantic tokens (`primary`, `secondary`, `accent`, `muted`, `destructive`) ready to use
- **Tailwind Config:** CommonJS format with `fontFamily` extension

### Established Patterns
- **Tailwind utility classes:** Direct color classes like `bg-violet-500`, `text-purple-600` — need replacement
- **Gradient pattern:** `bg-gradient-to-br from-violet-500 to-purple-600` — standard Tailwind gradient syntax
- **Dark mode classes:** `.dark` prefix for dark mode variants

### Integration Points
- All 11+ files identified in `.planning/research/ARCHITECTURE.md` need color class replacement
- React Flow components use index.css dark mode overrides

</code_context>

<specifics>
## Specific Ideas

- AI features should feel cohesive with Brand Victoria identity — use Teal→Blue gradient as brand accent
- Graph nodes should remain visually distinct to maintain UX clarity
- Status badges should be consistent across all views using semantic tokens

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 03-hardcoded-color-audit*
*Context gathered: 2026-03-19*
