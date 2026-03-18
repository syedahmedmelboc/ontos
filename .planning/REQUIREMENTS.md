# Requirements: Ontos DTP Victoria Rebrand

**Defined:** 2026-03-19
**Core Value:** The platform must feel like an authentic Victorian Government product, building trust and recognition for DTP staff using the data governance tools.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Color System

- [ ] **COLOR-01**: Brand Victoria palette applied to CSS variables in `:root` block (Navy, Blue, Teal, Grey)
- [ ] **COLOR-02**: Dark mode variants in `.dark` block with accessible contrast ratios
- [ ] **COLOR-03**: Semantic color mapping (primary=Navy, secondary=Blue, accent=Teal, destructive=Red)
- [ ] **COLOR-04**: Chart colors (`--chart-1` through `--chart-5`) updated to Brand Victoria palette

### Typography

- [ ] **TYPE-01**: VIC font files self-hosted in `public/fonts/` (Book, SemiBold, Bold weights)
- [ ] **TYPE-02**: `@font-face` declarations added to `index.css` with WOFF2 format
- [ ] **TYPE-03**: Arial as fallback font in font-family stack per Brand Victoria guidelines

### Logo & Identity

- [ ] **LOGO-01**: DTP Victoria logo replaces default logo in sidebar (`UnityCatalogLogo` component)
- [ ] **LOGO-02**: Favicon updated to DTP Victoria icon (SVG format)
- [ ] **LOGO-03**: Browser title updated to "DTP Data Governance" in `index.html`

### Hardcoded Colors

- [ ] **HARD-01**: Replace `violet-*` Tailwind classes with Brand Victoria equivalents (Teal/Blue)
- [ ] **HARD-02**: Replace `purple-*` Tailwind classes with Brand Victoria equivalents
- [ ] **HARD-03**: Update hardcoded `dark:bg-gray-*`, `dark:text-slate-*` patterns in identified files

### Intersection Device

- [ ] **INT-01**: CSS utility class for +/-25.3 degree gradient accent (Navy->Blue->Teal)
- [ ] **INT-02**: Intersection device applied to header divider or key UI element

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Typography Extended

- **TYPE-EXT-01**: VIC Display font for large headings (logo-only usage per guidelines)
- **TYPE-EXT-02**: VIC Light weight for subtle text elements

### Visual Polish

- **VIS-01**: Animated intersection device transitions on scroll
- **VIS-02**: Print stylesheet with Brand Victoria styling
- **VIS-03**: Loading skeleton colors updated to brand palette

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Backend changes | Visual rebrand only - frontend styling changes |
| Feature changes | No new functionality, only visual identity update |
| Content/terminology | Keeping "Ontos" naming in code, API, and internal references |
| Mobile app | Web platform only - no mobile app changes |
| VIC font CDN | Licensing requires self-hosting - no external font services |
| Real-time theme toggle | No runtime theme switching - build-time brand application |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| COLOR-01 | Phase 1 | Pending |
| COLOR-02 | Phase 1 | Pending |
| COLOR-03 | Phase 1 | Pending |
| COLOR-04 | Phase 1 | Pending |
| TYPE-01 | Phase 2 | Pending |
| TYPE-02 | Phase 2 | Pending |
| TYPE-03 | Phase 2 | Pending |
| LOGO-01 | Phase 2 | Pending |
| LOGO-02 | Phase 2 | Pending |
| LOGO-03 | Phase 2 | Pending |
| HARD-01 | Phase 3 | Pending |
| HARD-02 | Phase 3 | Pending |
| HARD-03 | Phase 3 | Pending |
| INT-01 | Phase 4 | Pending |
| INT-02 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 15 total
- Mapped to phases: 15
- Unmapped: 0

---
*Requirements defined: 2026-03-19*
*Last updated: 2026-03-19 after roadmap creation*
