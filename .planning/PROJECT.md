# Ontos DTP Victoria Rebrand

## What This Is

A visual rebrand of the Ontos data governance platform to align with the Victorian Government's Brand Victoria guidelines for the Department of Transport and Planning (DTP). This involves updating the color palette, typography, logo, and visual accents while preserving all existing functionality.

## Core Value

The platform must feel like an authentic Victorian Government product, building trust and recognition for DTP staff using the data governance tools.

## Requirements

### Validated

- ✓ Data governance platform for Databricks — existing
- ✓ FastAPI backend with React frontend — existing
- ✓ Tailwind CSS + Shadcn UI component system — existing
- ✓ CSS variable-based theming with light/dark modes — existing
- ✓ Custom logo support via UI customization store — existing

### Active

- [ ] Apply Brand Victoria color palette to all UI elements
- [ ] Replace Ontos logo with DTP Victoria logo
- [ ] Implement VIC font family typography
- [ ] Add Brand Victoria intersection device accent
- [ ] Update favicon and browser title
- [ ] Ensure dark mode uses Brand Victoria colors appropriately

### Out of Scope

- Feature changes or new functionality — visual rebrand only
- Content/terminology changes — keeping "Ontos" naming in code and API
- Backend changes — frontend styling only
- Mobile app — web platform only

## Context

**Existing Architecture:**
- Frontend uses Tailwind CSS with CSS variables defined in `src/frontend/src/index.css`
- Shadcn UI components reference these CSS variables via `hsl(var(--name))`
- Dark mode toggles `.dark` class on root element
- Logo component (`UnityCatalogLogo`) supports custom logo via `customLogoUrl` in Zustand store
- Default logo is `ontos-logo.svg` in `public/`

**Brand Victoria Guidelines:**
- Primary colors: Navy `#201547`, Blue `#004c97`, Teal `#00b2a9`
- Supporting: Grey `#53565a`, Light Grey `#d9d9d6`
- Accent colors: Orange `#ff9e1b`, Red `#af272f`, Purple `#87189d`
- Typography: VIC font family (Book, SemiBold, Bold, Medium, Light)
- Logo: Division name LEFT of Victoria triangle
- Intersection device: ±25.3° angle gradient from triangle logo

**Source:** https://www.vic.gov.au/sites/default/files/2018-11/brand-victoria-guidelines.pdf

## Constraints

- **Tech Stack:** Must use existing Tailwind CSS + Shadcn UI system — no new styling libraries
- **Compatibility:** Must maintain dark mode support — both themes need rebranding
- **Font Licensing:** VIC font files must be self-hosted in `public/fonts/` — no CDN

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| VIC font files over Arial | Exact brand compliance per user request | — Pending |
| DTP Victoria logo | Department-specific branding for DTP | — Pending |
| Rebrand dark mode too | Consistent brand experience across themes | — Pending |
| Include intersection device | Adds distinctive Brand Victoria visual language | — Pending |

---
*Last updated: 2026-03-19 after initialization*
