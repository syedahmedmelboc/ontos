# Feature Research

**Domain:** Government Visual Brand Implementation (Brand Victoria)
**Researched:** 2026-03-19
**Confidence:** HIGH (based on official Brand Victoria Guidelines PDF)

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist. Missing these = product feels incomplete or non-compliant.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Brand Victoria color palette | Government users expect official department colors; non-compliance signals inauthenticity | LOW | CSS variable replacement in `index.css`. Primary: Navy #201547, Blue #004c97, Teal #00b2a9. Supporting: Grey #53565a, Light Grey #d9d9d6 |
| DTP Victoria logo | Users need to see their department identity; missing logo breaks trust | LOW | Replace `ontos-logo.svg` with DTP logo, update `customLogoUrl` in store |
| VIC font family typography | Official brand guidelines mandate VIC fonts for all communications | MEDIUM | Self-host font files in `public/fonts/`, update Tailwind config. Weights: Light, Book, Medium, SemiBold, Bold |
| Accessible color contrast | WCAG 2.1 AA compliance required for government sites; Brand Victoria provides accessible palette | LOW | Use accessible combinations from guidelines page 26-27. Navy text on white, white on navy, etc. |
| Favicon update | Browser tab must show department identity | LOW | Replace favicon files with DTP/Brand Victoria favicon |
| Browser title update | Users expect government site branding in window title | LOW | Update `<title>` in `index.html` and dynamic title handling |

### Differentiators (Competitive Advantage)

Features that set the product apart. Not required, but valuable.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Intersection device accent | Distinctive Brand Victoria visual language; creates professional government aesthetic | MEDIUM | CSS gradient at +/- 25.3deg angle derived from triangle logo. Can frame headers, cards, section dividers |
| Dark mode with Brand Victoria colors | Consistent brand experience across themes; most apps ignore dark mode branding | MEDIUM | Adapt primary palette for dark backgrounds. Navy becomes background, teal/blue become accents |
| Custom font loading with fallbacks | Resilient typography that degrades gracefully if fonts fail to load | LOW | Use Arial as fallback (official Brand Victoria alternative). Set up `font-display: swap` |
| Brand Victoria secondary colors for charts | Consistent data visualization palette; charts look cohesive with overall design | LOW | Use secondary palette: Orange #ff9e1b, Red #af272f, Purple #87189d, Green #78be20, etc. for chart series |
| Intersection device on loading states | Premium feel during async operations; reinforces brand even during wait states | LOW | Use angle pattern in skeleton loaders or spinner designs |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem good but create problems.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Multiple Brand Victoria logos per page | "We need to show partnership with multiple departments" | Brand Victoria guidelines explicitly prohibit more than one triangle logo visible per page. Creates visual clutter and brand dilution | Use Victoria State Government logo as endorser in footer only. Lead with single department logo in header |
| VIC Display font for body copy | "It looks official and branded" | VIC Display is ONLY for logo development, never for body text. Illegible at small sizes, violates brand guidelines | Use VIC Book/Regular for body, VIC Bold/SemiBold for headings. VIC Display restricted to logo creation only |
| Custom color palette "inspired by" Brand Victoria | "We want to be unique while still being official" | Creates brand inconsistency; government users recognize non-compliance immediately. May require re-approval from DPC | Use exact Brand Victoria palette. Use intersection device and photography for differentiation instead |
| Removing dark mode to "ensure consistency" | "Dark mode makes branding harder" | Excludes users who need dark mode for accessibility or preference. Many government users work in varied lighting conditions | Implement dark mode with adapted Brand Victoria colors. Navy works well as dark background base |
| Using Chronicle Display for "prestigious" feel | "It looks more formal and government-like" | Chronicle Display is secondary font only for traditional/historic contexts. Never for body copy. Inappropriate for digital products | Use VIC fonts throughout. Chronicle only for special print materials with heritage context |
| Gradient overlays on intersection device with photos | "It looks more dynamic" | Brand Victoria explicitly prohibits gradient colors over images for intersection device. Creates muddy, unprofessional appearance | Use solid colors or opacities over images. Use gradients only with solid colors, never combined with photography |

## Feature Dependencies

```
[Brand Victoria Color Palette]
    └──required by──> [Dark Mode Rebranding]
                           └──requires──> [Accessible Color Contrast Verification]

[DTP Victoria Logo]
    └──required by──> [Favicon Update]
                           └──requires──> [Browser Title Update]

[VIC Font Files Self-Hosted]
    └──required by──> [VIC Typography in Tailwind]
                           └──required by──> [Font Fallback Configuration]

[Intersection Device]
    └──enhances──> [Header Component]
    └──enhances──> [Card Components]
    └──enhances──> [Loading States]
```

### Dependency Notes

- **Dark Mode requires Color Palette:** Cannot define dark mode theme without establishing base Brand Victoria colors first. The palette informs which colors adapt to dark backgrounds.
- **Logo requires Favicon:** Logo establishes primary visual identity; favicon must match for consistency across browser tabs and bookmarks.
- **VIC Typography requires Font Files:** VIC is not a system font or available via CDN (licensing). Must self-host `.woff2` files in `public/fonts/` before Tailwind can reference them.
- **Intersection Device enhances multiple components:** Once the CSS pattern is defined (25.3deg angle gradient), it can be applied to headers, cards, dividers, and loading states for cohesive brand language.

## MVP Definition

### Launch With (v1)

Minimum viable product — what's needed to validate the concept.

- [ ] **Brand Victoria Color Palette** — Core identity; without this, nothing else matters. Replace all CSS variables in `index.css` with Brand Victoria HSL values.
- [ ] **DTP Victoria Logo** — Users must see their department identity. Replace `ontos-logo.svg` in `public/` and verify `UnityCatalogLogo` component displays it.
- [ ] **VIC Typography** — Official font family is mandatory per guidelines. Self-host VIC font files and update Tailwind config with new font stack.
- [ ] **Favicon + Browser Title** — Basic browser chrome branding. Create favicon from DTP logo, update `index.html` title.

### Add After Validation (v1.x)

Features to add once core is working.

- [ ] **Intersection Device** — Adds distinctive Brand Victoria visual language. Implement as reusable CSS component/utility class.
- [ ] **Dark Mode Rebranding** — Consistent brand across themes. Adapt palette for dark backgrounds using Navy as base.
- [ ] **Chart Color Palette** — Consistent data visualization. Replace `--chart-1` through `--chart-5` with Brand Victoria secondary colors.

### Future Consideration (v2+)

Features to defer until product-market fit is established.

- [ ] **Intersection Device on Loading States** — Premium polish; skeleton loaders with angle pattern.
- [ ] **Brand Victoria Photography Guidelines** — If app adds hero images or photography, follow eclectic contrasts guidance.

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Brand Victoria Color Palette | HIGH | LOW | P1 |
| DTP Victoria Logo | HIGH | LOW | P1 |
| VIC Typography | HIGH | MEDIUM | P1 |
| Favicon + Browser Title | HIGH | LOW | P1 |
| Accessible Color Contrast | HIGH | LOW | P1 |
| Dark Mode Rebranding | MEDIUM | MEDIUM | P2 |
| Intersection Device | MEDIUM | MEDIUM | P2 |
| Chart Color Palette | LOW | LOW | P3 |
| Loading State Branding | LOW | LOW | P3 |

**Priority key:**
- P1: Must have for launch (brand compliance)
- P2: Should have, add when possible (brand polish)
- P3: Nice to have, future consideration (brand extension)

## Implementation Complexity Notes

### Brand Victoria Color Palette (LOW)
- **Location:** `src/frontend/src/index.css`
- **Approach:** Replace existing HSL values with Brand Victoria colors
- **Mapping:**
  - `--primary`: Navy #201547 (HSL: 256, 67%, 20%)
  - `--accent`: Teal #00b2a9 (HSL: 177, 100%, 35%)
  - `--secondary`: Blue #004c97 (HSL: 212, 100%, 30%)
  - `--muted`: Grey #53565a (HSL: 240, 4%, 35%)
  - `--border`: Light Grey #d9d9d6 (HSL: 60, 1%, 85%)

### VIC Typography (MEDIUM)
- **Location:** Font files in `public/fonts/`, Tailwind config in `tailwind.config.cjs`
- **Approach:**
  1. Obtain VIC font files (WOFF2 format) from DPC or authorized source
  2. Add `@font-face` declarations in `index.css`
  3. Update Tailwind `fontFamily` config
  4. Set Arial as fallback (official Brand Victoria alternative)
- **Font Stack:** `VIC, Arial, sans-serif`

### Intersection Device (MEDIUM)
- **Location:** New CSS utility classes or component
- **Approach:** Create reusable CSS pattern using 25.3deg angle
- **Implementation:**
  ```css
  .intersection-device {
    background: linear-gradient(25.3deg, var(--bv-navy) 50%, var(--bv-teal) 50%);
  }
  ```
- **Usage:** Header backgrounds, card accents, section dividers

### Dark Mode Rebranding (MEDIUM)
- **Location:** `src/frontend/src/index.css` `.dark` class
- **Approach:** Adapt Brand Victoria palette for dark backgrounds
- **Mapping:**
  - `--background`: Navy #201547 (same as light mode primary)
  - `--primary`: White #ffffff (for text on dark)
  - `--accent`: Teal #00b2a9 (remains accent)
  - `--secondary`: Lighter navy tint

## Brand Victoria Specification Reference

### Primary Color Palette (from guidelines page 24)

| Color | HEX | RGB | Usage |
|-------|-----|-----|-------|
| Navy | #201547 | 32, 21, 71 | Primary text, headers, logos |
| Blue | #004c97 | 0, 76, 151 | Secondary, links, interactive |
| Teal | #00b2a9 | 0, 178, 169 | Accent, highlights, CTAs |
| Grey | #53565a | 83, 86, 90 | Body text, muted elements |
| Light Grey | #d9d9d6 | 217, 217, 214 | Backgrounds, borders |
| Orange | #ff9e1b | 255, 158, 27 | Accent, warnings |
| Red | #af272f | 175, 39, 47 | Destructive, errors |
| Purple | #87189d | 135, 24, 157 | Accent, special elements |

### Typography Specification (from guidelines pages 29-32)

| Font Weight | Usage |
|-------------|-------|
| VIC Bold | Headlines, brochure titles |
| VIC SemiBold | Major headings, sub-headings |
| VIC Medium | Sub-headings, emphasis |
| VIC Book | Body copy (primary) |
| VIC Light | Large body copy blocks |
| VIC Display | LOGO DEVELOPMENT ONLY |

### Intersection Device (from guidelines pages 33-35)

- **Angle:** +/- 25.3 degrees (derived from triangle logo geometry)
- **Usage:** Frame imagery, create visual language, lock up with primary logo
- **Allowed:** Solid colors, tints, opacities, gradients (without images), multiply effect on overlapping colors
- **Prohibited:** Gradient colors over images, striping, use without color

### Accessibility Requirements (from guidelines pages 26-27, 41)

- WCAG 2.1 AA compliance required
- Accessible color palette provided with contrast ratios
- Normal text vs Large text contrast requirements
- Alternative formats for communications (Easy English, audio)
- Captioning for videos
- Digital content must meet Web Content Accessibility Guidelines 2.0 AA

## Sources

- [Brand Victoria Guidelines PDF (Version 2, 2018)](https://www.vic.gov.au/sites/default/files/2018-11/brand-victoria-guidelines.pdf) - HIGH confidence - Official Victorian Government brand guidelines
- [Australian Government Design System](https://designsystem.gov.au/) - HIGH confidence - Reference for accessibility and component patterns
- Existing codebase analysis: `src/frontend/src/index.css`, `tailwind.config.cjs`, `unity-catalog-logo.tsx`

---

*Feature research for: Brand Victoria Visual Rebrand*
*Researched: 2026-03-19*
