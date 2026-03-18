# Pitfalls Research: Visual Rebrand

**Domain:** Visual Rebranding (Brownfield)
**Researched:** 2026-03-19
**Confidence:** HIGH (based on codebase analysis and domain knowledge)

---

## Critical Pitfalls

### Pitfall 1: Incomplete Dark Mode Rebrand

**What goes wrong:**
Only light mode CSS variables are updated to Brand Victoria colors. Dark mode retains original Databricks-inspired colors, creating an inconsistent brand experience when users switch themes.

**Why it happens:**
Dark mode is often treated as an afterthought. The existing `index.css` has a well-structured dark mode section that mirrors the light mode variables, but developers focus on the visible light mode during initial work and forget to update both.

**How to avoid:**
- Update BOTH `:root` AND `.dark` sections in `index.css` simultaneously
- Create a mapping table before starting: for each Brand Victoria color, define its dark mode equivalent
- Test theme toggle after EVERY color variable change

**Warning signs:**
- `index.css` shows changes in `:root` but `.dark` section unchanged
- Visual review only conducted in one theme
- Color contrast issues appearing only in dark mode

**Phase to address:**
Phase 1 (Color System Update) - must complete both themes before declaring phase done

---

### Pitfall 2: Hardcoded Color Values Remain in Components

**What goes wrong:**
While CSS variables are updated, 269+ instances of `dark:bg-`, `dark:text-`, and `dark:border-` classes with hardcoded Tailwind colors (e.g., `bg-gray-100`, `bg-slate-800`, `dark:bg-slate-800`) remain scattered across 64 files. These hardcoded values don't use the new brand colors, creating visual inconsistency.

**Why it happens:**
Shadcn UI components use CSS variables correctly, but custom components and views often use direct Tailwind color classes. During rebrand, developers focus on the central theme file and miss distributed hardcoded values.

**How to avoid:**
- Audit ALL files for hardcoded color classes BEFORE starting rebrand
- Use grep/search for patterns: `bg-gray-`, `bg-slate-`, `bg-zinc-`, `bg-neutral-`, `text-gray-`, `text-slate-`, etc.
- Either replace with CSS variable equivalents OR extend Tailwind config with brand-specific colors
- Create a "deprecated colors" linter rule if possible

**Warning signs:**
- Search results show `bg-gray-` or `bg-slate-` patterns after rebrand declared complete
- Visual QA finds elements that don't match brand guidelines
- Components look correct in isolation but inconsistent in context

**Phase to address:**
Phase 2 (Component Audit & Update) - systematic replacement of hardcoded colors

---

### Pitfall 3: Brand Victoria Intersection Device Misimplementation

**What goes wrong:**
The Brand Victoria intersection device (25.3-degree gradient from the triangle logo) is implemented incorrectly. Common mistakes: wrong angle, wrong colors, wrong positioning, or using it as a background where it creates readability issues.

**Why it happens:**
The intersection device is a distinctive but unusual element. Developers may not fully understand the brand guidelines or may implement it as a simple gradient without the precise angle specification. The existing codebase has `bg-gradient-to-br from-violet-500 to-purple-600` patterns that could be mistakenly copied.

**How to avoid:**
- Reference official Brand Victoria guidelines PDF for exact specifications
- Create a dedicated CSS class/component for the intersection device
- Document the exact CSS: `background: linear-gradient(25.3deg, [brand-color-1], [brand-color-2])`
- Test against brand guidelines visual examples
- Limit usage to appropriate contexts (headers, hero sections - not everywhere)

**Warning signs:**
- Intersection device appears on every page element
- Angle looks "off" compared to official materials
- Text becomes hard to read over the gradient
- Gradient uses non-brand colors

**Phase to address:**
Phase 3 (Intersection Device Implementation) - dedicated phase with explicit specs

---

### Pitfall 4: VIC Font Loading Failures

**What goes wrong:**
VIC font files are placed in `public/fonts/` but don't load correctly, causing fallback to system fonts. This breaks brand compliance. Common causes: wrong `@font-face` paths, missing font formats, CORS issues, or incorrect font-weight mappings.

**Why it happens:**
Self-hosted fonts require precise `@font-face` declarations. The existing codebase uses system fonts (Inter) without explicit `@font-face`, so there's no existing pattern to follow. Font licensing requirements may also be unclear.

**How to avoid:**
- Include multiple font formats (woff2, woff, ttf) for browser compatibility
- Use absolute paths from public root: `/fonts/VIC-Regular.woff2`
- Define all font weights used: Book (400), Medium (500), SemiBold (600), Bold (700), Light (300)
- Test font loading in Network tab and with browser dev tools
- Add `font-display: swap` to prevent invisible text during load

**Warning signs:**
- Browser console shows 404 for font files
- Text renders in Times New Roman or system font
- Font weights don't change when specified
- FOUT (Flash of Unstyled Text) is severe

**Phase to address:**
Phase 2 (Typography & Font Implementation) - test font loading before moving on

---

### Pitfall 5: Color Contrast Accessibility Failures

**What goes wrong:**
Brand Victoria colors, especially when applied to both themes, fail WCAG 2.1 AA contrast requirements (4.5:1 for normal text, 3:1 for large text). Navy `#201547` on certain backgrounds or Teal `#00b2a9` text may be unreadable.

**Why it happens:**
Brand guidelines prioritize aesthetics over accessibility. Navy is dark enough for most backgrounds, but Teal and Light Grey (`#d9d9d6`) can fail contrast requirements. Dark mode variants may also have insufficient contrast.

**How to avoid:**
- Test EVERY color combination with a contrast checker before implementation
- For text: ensure all foreground/background combinations meet 4.5:1
- May need to create "accessible variants" of brand colors for text use
- Document which brand colors are safe for text vs. decorative use
- Consider using brand colors for accents/backgrounds but maintaining accessible text colors

**Warning signs:**
- Lighthouse accessibility score drops after rebrand
- Text is hard to read, especially in dark mode
- Grey text on colored backgrounds fails contrast
- Small text becomes illegible

**Phase to address:**
Phase 1 (Color System Update) - contrast testing is a completion gate

---

## Technical Debt Patterns

Shortcuts that seem reasonable but create long-term problems.

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Update CSS variables only, skip hardcoded colors | Faster initial implementation | Inconsistent UI, hidden brand violations | Never - must audit all colors |
| Copy existing violet gradient patterns for intersection device | Quick visual result | Wrong angle, wrong brand | Never - use exact 25.3deg spec |
| Skip dark mode testing initially | Faster light mode completion | Double work when dark mode fails | Never - test both simultaneously |
| Use CDN for VIC fonts | Simpler setup | Licensing violation, offline fails, vendor lock-in | Never - requirement says self-host |
| Only test in Chrome | Faster QA | Safari/Firefox font loading issues, CSS differences | Never - cross-browser testing required |

---

## Integration Gotchas

Common mistakes when connecting to external services or systems.

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Databricks Apps deployment | Forgetting to include font files in bundle | Add fonts to `app.yaml` includes or verify `public/` is bundled |
| Theme persistence | Assuming theme state is server-synced | Theme is localStorage-only (`vite-ui-theme` key) - brand applies to both themes equally |
| Logo customization | Overwriting `customLogoUrl` mechanism | Set DTP logo as default, keep customization for future flexibility |
| Browser title | Only updating visible title | Update `<title>` in `index.html` AND any dynamic title setters |
| Favicon | Only updating SVG favicon | Provide multiple formats (ico, png) for different contexts |

---

## Performance Traps

Patterns that work at small scale but fail as usage grows.

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Multiple font file formats | Slow initial load with 5 weights x 3 formats = 15 files | Use `font-display: swap`, preload critical weights only, subset fonts | On slow connections |
| Large intersection device images | Background images cause layout shift | Use CSS gradients, not images | On mobile data |
| CSS variable proliferation | Theme switching causes re-render cascade | Keep variable count minimal, group related values | With 50+ variables |

---

## UX Pitfalls

Common user experience mistakes in visual rebranding.

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Drastic visual change without transition | Users think app is broken, lose trust | Maintain layout/structure, change colors/typography gradually |
| Logo placement change | Users can't find "home" navigation | Keep logo in same position, just swap the image |
| Removing familiar visual cues | Users feel lost | Keep interaction patterns identical, only change surface appearance |
| Over-applying intersection device | Visual overwhelm, looks unprofessional | Use as accent in headers/hero only, not on every component |
| Dark mode too dark or too light | Eye strain, unreadable text | Test with real users, aim for comfortable reading contrast |

---

## "Looks Done But Isn't" Checklist

Things that appear complete but are missing critical pieces.

- [ ] **Color Variables:** All variables updated in BOTH `:root` AND `.dark` sections - verify by grepping for old HSL values
- [ ] **Hardcoded Colors:** No `bg-gray-`, `bg-slate-`, `text-gray-` patterns remain (except intentional)
- [ ] **Font Loading:** VIC fonts load in Network tab, Computed styles show "VIC" not fallback
- [ ] **Font Weights:** All 5 weights (Light, Book, Medium, SemiBold, Bold) render differently
- [ ] **Dark Mode Toggle:** Switching themes shows brand colors in both, no flash of wrong colors
- [ ] **Logo:** DTP logo appears in header, sidebar, and favicon (not Ontos logo)
- [ ] **Browser Title:** Tab shows "DTP Victoria" or similar (not "Ontos")
- [ ] **Contrast:** All text passes WCAG AA contrast in both themes
- [ ] **Intersection Device:** Angle is 25.3 degrees (measure with design tool overlay)
- [ ] **Cross-browser:** Tested in Chrome, Firefox, Safari (font loading especially)
- [ ] **Deployment:** Font files included in Databricks bundle, not just local

---

## Recovery Strategies

When pitfalls occur despite prevention, how to recover.

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Incomplete dark mode | MEDIUM | Update `.dark` section, test all pages in dark mode |
| Hardcoded colors remain | HIGH | Grep for all color patterns, systematic replacement per file |
| Wrong intersection angle | LOW | Update CSS `linear-gradient()` angle value |
| Font loading failure | MEDIUM | Check paths, add formats, verify `@font-face` syntax |
| Contrast failures | MEDIUM | Define accessible text variants, update affected components |
| Logo not updated | LOW | Replace SVG file, clear browser cache, verify all logo refs |

---

## Pitfall-to-Phase Mapping

How roadmap phases should address these pitfalls.

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Incomplete Dark Mode | Phase 1: Color System | Toggle test in all major views |
| Hardcoded Colors | Phase 2: Component Audit | Grep search returns 0 results for deprecated patterns |
| Intersection Device | Phase 3: Intersection Device | Design review against Brand Victoria PDF |
| Font Loading | Phase 2: Typography | Network tab shows fonts loaded, computed styles correct |
| Contrast Failures | Phase 1: Color System | Lighthouse accessibility score >= 90 |

---

## Sources

- Codebase analysis of `/src/frontend/src/index.css` - CSS variable structure
- Codebase analysis of `/src/frontend/tailwind.config.cjs` - Tailwind configuration
- Grep analysis of dark mode class usage across codebase - 269 instances in 64 files
- Grep analysis of hardcoded color patterns - gray/slate/zinc usage found
- Brand Victoria Guidelines (referenced in PROJECT.md): https://www.vic.gov.au/sites/default/files/2018-11/brand-victoria-guidelines.pdf
- WCAG 2.1 Contrast Requirements - domain knowledge
- Tailwind CSS Dark Mode documentation - domain knowledge

---

*Pitfalls research for: Ontos DTP Victoria Rebrand*
*Researched: 2026-03-19*
