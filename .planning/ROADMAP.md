# Roadmap: Ontos DTP Victoria Rebrand

## Overview

A visual rebranding project to transform the Ontos data governance platform into an authentic Victorian Government product for the Department of Transport and Planning (DTP). The journey progresses from foundational CSS color variables through typography and identity updates, followed by a systematic audit of hardcoded colors, and concludes with the distinctive Brand Victoria intersection device accent.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Color System** - Apply Brand Victoria color palette to CSS variables for both light and dark modes
- [ ] **Phase 2: Typography & Logo** - Self-host VIC fonts and replace Ontos branding with DTP Victoria identity
- [ ] **Phase 3: Hardcoded Color Audit** - Replace all hardcoded violet/purple/gray Tailwind classes with Brand Victoria equivalents
- [ ] **Phase 4: Intersection Device** - Add distinctive Brand Victoria gradient accent element

## Phase Details

### Phase 1: Color System
**Goal**: All UI components use Brand Victoria colors through CSS variable propagation
**Depends on**: Nothing (first phase)
**Requirements**: COLOR-01, COLOR-02, COLOR-03, COLOR-04
**Success Criteria** (what must be TRUE):
  1. User sees Navy (#201547), Blue (#004c97), and Teal (#00b2a9) as primary interface colors in light mode
  2. User sees appropriately adjusted Brand Victoria colors in dark mode with accessible contrast
  3. All Shadcn UI components (buttons, inputs, cards) render with Brand Victoria palette
  4. Charts and data visualizations use Brand Victoria color scheme
**Plans**: 1 plan

Plans:
- [x] 01-01-PLAN.md — Update CSS variables in index.css with Brand Victoria HSL values (light + dark modes)

### Phase 2: Typography & Logo
**Goal**: DTP Victoria brand identity is visible in fonts, logo, and browser chrome
**Depends on**: Phase 1
**Requirements**: TYPE-01, TYPE-02, TYPE-03, LOGO-01, LOGO-02, LOGO-03
**Success Criteria** (what must be TRUE):
  1. User sees VIC font family (Book, SemiBold, Bold) rendered in all UI text
  2. User sees DTP Victoria logo in the sidebar header
  3. Browser tab shows DTP Victoria favicon and "DTP Data Governance" title
  4. Text falls back to Arial if VIC fonts fail to load (per Brand Victoria guidelines)
**Plans**: TBD

Plans:
- [ ] 02-01: Add VIC font files and @font-face declarations
- [ ] 02-02: Update Tailwind config and apply typography
- [ ] 02-03: Replace logo, favicon, and browser title

### Phase 3: Hardcoded Color Audit
**Goal**: No violet, purple, or non-brand gray colors remain in component code
**Depends on**: Phase 2
**Requirements**: HARD-01, HARD-02, HARD-03
**Success Criteria** (what must be TRUE):
  1. User sees consistent Brand Victoria colors across all pages (no stray purple/violet)
  2. Dark mode components use brand-aligned gray/slate alternatives
  3. All identified files (11 feature files with hardcoded colors) render with semantic tokens
**Plans**: TBD

Plans:
- [ ] 03-01: Replace violet-* and purple-* Tailwind classes
- [ ] 03-02: Replace dark:bg-gray-* and dark:text-slate-* patterns

### Phase 4: Intersection Device
**Goal**: Distinctive Brand Victoria visual accent enhances key UI elements
**Depends on**: Phase 3
**Requirements**: INT-01, INT-02
**Success Criteria** (what must be TRUE):
  1. User sees a 25.3-degree gradient accent (Navy to Blue to Teal) on header dividers
  2. Intersection device CSS utility class is reusable for future brand elements
**Plans**: TBD

Plans:
- [ ] 04-01: Create intersection device CSS utility and apply to UI

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 4

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Color System | 1/1 | Complete | 2026-03-19 |
| 2. Typography & Logo | 0/3 | Not started | - |
| 3. Hardcoded Color Audit | 0/2 | Not started | - |
| 4. Intersection Device | 0/1 | Not started | - |
