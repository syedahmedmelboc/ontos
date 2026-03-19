---
phase: 4
slug: intersection-device
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-19
---

# Phase 4 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | vitest (visual regression via Playwright MCP) |
| **Config file** | vitest.config.ts |
| **Quick run command** | `cd src/frontend && yarn test --run` |
| **Full suite command** | `cd src/frontend && yarn test` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Visual inspection in browser (light + dark mode)
- **After every plan wave:** Visual comparison screenshots via Playwright MCP
- **Before `/gsd:verify-work`:** Full visual verification complete
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 04-01-01 | 01 | 1 | INT-01 | visual | `mcp__playwright__browser_snapshot` | ❌ W0 | ⬜ pending |
| 04-01-02 | 01 | 1 | INT-02 | visual | `mcp__playwright__browser_snapshot` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] Visual verification capability via Playwright MCP (already available)
- [ ] Light/dark mode toggle accessible for testing

*Existing infrastructure covers all phase requirements. No new test files needed - CSS-only change verified visually.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Gradient renders correctly | INT-01 | Visual regression | 1. Open app in browser 2. Verify gradient bar below header 3. Check colors flow Navy→Blue→Teal |
| Dark mode gradient | INT-01 | Visual regression | 1. Toggle dark mode 2. Verify gradient uses semantic tokens (Teal→Blue→Blue) |
| Header divider visible | INT-02 | Visual regression | 1. Navigate to any page 2. Confirm intersection device bar appears below header |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
