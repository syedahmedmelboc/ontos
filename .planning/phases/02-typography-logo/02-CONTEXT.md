# Phase 2: Typography & Logo - Context

**Gathered:** 2026-03-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Self-host VIC font family (Book, SemiBold, Bold weights) and replace Ontos branding with DTP Victoria identity. This phase touches:
- Font files: Copy from `.planning/WEBFONT/` to `src/frontend/public/fonts/`
- CSS: Add `@font-face` declarations to `src/frontend/src/index.css`
- Tailwind: Update font-family in `tailwind.config.cjs`
- Logo: Replace `src/frontend/public/ontos-logo.svg` with DTP placeholder
- Favicon: Replace `src/frontend/public/favicon.ico` with placeholder
- Browser title: Update `src/frontend/index.html` title to "DTP Data Governance"

No backend changes required. Logo uses direct SVG replacement (not customLogoUrl API).

</domain>

<decisions>
## Implementation Decisions

### Font Procurement

| Source | Location | Format |
|--------|----------|--------|
| VIC-Regular.woff2 | `.planning/WEBFONT/Regular/` | WOFF2 (Book/400) |
| VIC-SemiBold.woff2 | `.planning/WEBFONT/SemiBold/` | WOFF2 (600) |
| VIC-Bold.woff2 | `.planning/WEBFONT/Bold/` | WOFF2 (700) |

**Why WOFF2:** Best compression, supported by all modern browsers. EOT/TTT/WOFF not needed.

### Font Weights

| Weight | File | CSS font-weight | Usage |
|--------|------|-----------------|-------|
| Book | VIC-Regular.woff2 | 400 | Body text, labels |
| SemiBold | VIC-SemiBold.woff2 | 600 | Headings, emphasis |
| Bold | VIC-Bold.woff2 | 700 | Strong emphasis, buttons |

**Why Essential 3:** Covers 95% of UI needs. Light/Medium weights add minimal value for data governance interface.

### @font-face Declaration Pattern

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
  src: url('/fonts/VIC-SemiBold.woff2') format('woff2');
  font-weight: 600;
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
```

**Why font-display: swap:** Prevents FOIT (Flash of Invisible Text). Arial fallback displays immediately, VIC fonts swap in when loaded.

### Font Stack

```css
font-family: 'VIC', Arial, sans-serif;
```

**Why Arial fallback:** Official Brand Victoria alternative font per guidelines page 32.

### Logo Implementation Strategy

| Approach | Choice | Rationale |
|----------|--------|-----------|
| Replace default SVG | ✓ Selected | Simpler, no backend changes, logo always shows |
| Use customLogoUrl API | ✗ Not chosen | Requires backend default setting, more complex |

**Implementation:** Replace `src/frontend/public/ontos-logo.svg` directly. The `UnityCatalogLogo` component will automatically display the new logo via `getAssetPath('/ontos-logo.svg')`.

### Logo & Favicon Assets

| Asset | Status | Notes |
|-------|--------|-------|
| DTP Logo (SVG) | Placeholder | Create simple placeholder with "DTP" text in Navy |
| Favicon (ICO) | Placeholder | Create simple placeholder |
| Favicon (SVG) | Optional | Modern browsers support SVG favicons |

**Placeholder approach:** User will replace placeholder files with real DTP Victoria assets later.

### Browser Title

Update `index.html`:
```html
<title>DTP Data Governance</title>
```

### Claude's Discretion

- Exact placement of @font-face declarations (before @layer base in index.css)
- Placeholder logo design (simple "DTP" text in Brand Victoria Navy)
- Whether to include SVG favicon alongside ICO

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Brand Victoria Guidelines
- `https://www.vic.gov.au/sites/default/files/2018-11/brand-victoria-guidelines.pdf` — Official guidelines (pages 29-32 for typography, Arial fallback)

### Project Research
- `.planning/research/STACK.md` — VIC font self-hosting pattern, @font-face declarations
- `.planning/research/FEATURES.md` — Typography weights, logo requirements

### Prior Phase Context
- `.planning/phases/01-color-system/01-CONTEXT.md` — Color decisions (Phase 1 complete)

### Existing Code
- `src/frontend/src/index.css` — CSS variables (updated in Phase 1), where @font-face goes
- `src/frontend/tailwind.config.cjs` — Tailwind config (no fontFamily yet)
- `src/frontend/src/components/unity-catalog-logo.tsx` — Logo component using `/ontos-logo.svg`
- `src/frontend/index.html` — Current title "Ontos", favicon link

### Font Files
- `.planning/WEBFONT/Regular/VIC-Regular.woff2` — Book weight
- `.planning/WEBFONT/SemiBold/VIC-SemiBold.woff2` — SemiBold weight
- `.planning/WEBFONT/Bold/VIC-Bold.woff2` — Bold weight

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **Font files ready:** VIC WOFF2 files exist in `.planning/WEBFONT/` — just need copying
- **CSS Variable System:** Established in Phase 1 — `@layer base` pattern ready for font declarations
- **Logo Component:** `UnityCatalogLogo` already uses `/ontos-logo.svg` — direct replacement works

### Established Patterns
- **CSS Layer Structure:** `@layer base { :root { ... } .dark { ... } }` — fonts go before or within
- **Tailwind Config:** Uses CommonJS format (`module.exports`) — add `fontFamily` to `theme.extend`
- **Asset Path:** `getAssetPath()` helper handles base path — logo just needs to be in `public/`

### Integration Points
- All text in Shadcn UI components will automatically use VIC font via body inheritance
- `font-semibold` (Tailwind default 600) maps perfectly to VIC-SemiBold
- `font-bold` (Tailwind default 700) maps perfectly to VIC-Bold
- `font-normal` (Tailwind default 400) maps perfectly to VIC-Regular (Book)

</code_context>

<specifics>
## Specific Ideas

- VIC Regular is named "Regular" in file but represents "Book" weight per Brand Victoria terminology
- Tailwind's `font-semibold` (600) and `font-bold` (700) align exactly with available weights
- Logo placeholder should use Brand Victoria Navy (#201547) for consistency
- Favicon placeholder can be simple square with "D" in Navy

</specifics>

<deferred>
## Deferred Ideas

- Light weight (300) for large body copy blocks — not essential for data governance UI
- Medium weight (500) — SemiBold covers emphasis needs
- Italic variants — not needed for data governance interface
- VIC Display font — explicitly prohibited for body text per guidelines
- Logo with text label ("DTP Data Governance") — sidebar already has text below logo area
- SVG favicon — ICO sufficient for now, can add SVG variant later
- customLogoUrl API configuration — direct replacement is simpler

</deferred>

---

*Phase: 02-typography-logo*
*Context gathered: 2026-03-19*
