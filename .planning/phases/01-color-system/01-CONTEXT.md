# Phase 1: Color System - Context

**Gathered:** 2026-03-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Apply Brand Victoria color palette to CSS variables in `src/frontend/src/index.css` for both light (`:root`) and dark (`.dark`) modes. This phase touches ONLY the CSS variable definitions — no component code changes, no logo, no fonts. All UI components automatically inherit the new colors through Tailwind's `hsl(var(--name))` pattern.

</domain>

<decisions>
## Implementation Decisions

### Color Mapping (Semantic)

| Semantic Token | Light Mode | Dark Mode | Hex |
|----------------|------------|-----------|-----|
| `--primary` | Navy | Teal | #201547 / #00b2a9 |
| `--primary-foreground` | White | Navy | #ffffff / #201547 |
| `--secondary` | Blue | Blue | #004c97 |
| `--secondary-foreground` | White | White | #ffffff |
| `--accent` | Teal | Blue | #00b2a9 / #004c97 |
| `--accent-foreground` | White | White | #ffffff |
| `--destructive` | Red | Red | #af272f |
| `--destructive-foreground` | White | White | #ffffff |
| `--sidebar-background` | Navy | Darker Navy | #201547 |

### Dark Mode Strategy

- **Primary swaps to Teal** — Navy (#201547) has insufficient contrast on dark backgrounds; Teal (#00b2a9) maintains brand recognition while being accessible
- **Secondary stays Blue** — Blue (#004c97) works on both light and dark with appropriate foreground
- **Charts use lighter variants** — 10-15% lighter HSL lightness for dark mode chart colors

### Chart Colors (Brand Victoria Palette)

| Token | Color | Light HSL | Dark HSL |
|-------|-------|-----------|----------|
| `--chart-1` | Teal | 177 100% 35% | 177 100% 45% |
| `--chart-2` | Blue | 212 100% 30% | 212 100% 45% |
| `--chart-3` | Navy | 248 48% 18% | 248 48% 35% |
| `--chart-4` | Orange | 38 100% 55% | 38 100% 65% |
| `--chart-5` | Purple | 292 83% 36% | 292 83% 50% |

### CSS Variable Format

- **HSL without wrapper** — Store as `H S L%` (e.g., `248 48% 18%`) to enable Tailwind opacity modifiers like `bg-primary/50`
- **No new Tailwind utilities** — Use semantic tokens only; direct Brand Victoria colors (vic-navy, vic-teal) deferred to future if needed

### Claude's Discretion

- Exact HSL conversion values for all Brand Victoria colors
- Specific lightness adjustments for dark mode variants (10-15% lighter)
- Border and input color values

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Brand Victoria Guidelines
- `https://www.vic.gov.au/sites/default/files/2018-11/brand-victoria-guidelines.pdf` — Official Brand Victoria Guidelines (Version 2, 2018). Defines color palette, typography, logo usage, intersection device.

### Project Research
- `.planning/research/STACK.md` — Tailwind CSS variable patterns, dark mode strategy, font self-hosting approach
- `.planning/research/FEATURES.md` — Brand Victoria feature requirements, table stakes vs differentiators
- `.planning/research/ARCHITECTURE.md` — CSS variable propagation pattern, 11 files with hardcoded colors (Phase 3)

### Existing Code
- `src/frontend/src/index.css` — Current CSS variables to be updated
- `src/frontend/tailwind.config.cjs` — Tailwind config referencing CSS variables

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **CSS Variable System**: Already established in `index.css` with `:root` and `.dark` blocks — just need value updates
- **Tailwind Config**: Already references `hsl(var(--name))` pattern — no changes needed
- **Shadcn UI Components**: All use semantic tokens — will auto-inherit new colors

### Established Patterns
- **HSL format**: Current variables use `H S L%` format (correct for Tailwind opacity)
- **Dark mode**: `.dark` class toggles between theme blocks
- **Sidebar**: Uses `--sidebar-background` for distinct sidebar color

### Integration Points
- All Shadcn UI components in `src/frontend/src/components/ui/` reference semantic tokens
- Charts in `src/frontend/src/views/home.tsx` use `--chart-*` variables
- Dark mode classes throughout codebase reference semantic tokens

</code_context>

<specifics>
## Specific Ideas

- "Navy on dark backgrounds has low contrast" — from research analysis
- Charts should use Brand Victoria palette: Teal, Blue, Navy, Orange, Purple
- Sidebar should be Navy (#201547) to reinforce brand identity

</specifics>

<deferred>
## Deferred Ideas

- Direct Tailwind utilities (vic-navy, vic-teal) — not needed for Phase 1; semantic tokens sufficient
- Hardcoded color replacement — Phase 3
- Logo replacement — Phase 2

</deferred>

---

*Phase: 01-color-system*
*Context gathered: 2026-03-19*
