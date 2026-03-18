---
phase: 01-color-system
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - src/frontend/src/index.css
autonomous: false
requirements:
  - COLOR-01
  - COLOR-02
  - COLOR-03
  - COLOR-04

must_haves:
  truths:
    - "User sees Navy (#201547), Blue (#004c97), and Teal (#00b2a9) as primary interface colors in light mode"
    - "User sees Teal (#00b2a9) as primary color in dark mode with accessible contrast"
    - "All Shadcn UI components render with Brand Victoria palette in both light and dark modes"
    - "Charts use Brand Victoria color scheme (Teal, Blue, Navy, Orange, Purple)"
  artifacts:
    - path: "src/frontend/src/index.css"
      provides: "CSS variable definitions for entire UI color system"
      contains: ":root"
      contains: ".dark"
      min_lines: 90
  key_links:
    - from: "src/frontend/src/index.css :root"
      to: "Shadcn UI components"
      via: "Tailwind hsl(var(--name)) pattern"
      pattern: "--primary:.*--secondary:.*--accent:"
    - from: "src/frontend/src/index.css .dark"
      to: "Dark mode components"
      via: ".dark class toggle"
      pattern: "\\.dark\\s*\\{"
---

<objective>
Replace all CSS variable values in `src/frontend/src/index.css` with Brand Victoria color palette HSL values for both light mode (`:root`) and dark mode (`.dark`) blocks. This propagates automatically to all Shadcn UI components via Tailwind's `hsl(var(--name))` pattern.

**Purpose:** Establish Brand Victoria as the visual identity for the DTP data governance platform. Users must see official Victorian Government colors throughout the interface.

**Output:** Updated `index.css` with Brand Victoria HSL values in both theme blocks.
</objective>

<execution_context>
@/Users/syedahmed/repos/newrepos/ontos/.claude/get-shit-done/workflows/execute-plan.md
@/Users/syedahmed/repos/newrepos/ontos/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/01-color-system/01-CONTEXT.md

<interfaces>
<!-- Current CSS variable structure in index.css - executor must preserve this exact format -->
<!-- Values are HSL channels without hsl() wrapper to enable Tailwind opacity modifiers -->

From src/frontend/src/index.css current structure:
```css
@layer base {
  :root {
    --background: 0 0% 100%;           /* Format: H S% L% */
    --foreground: 0 0% 3.9%;
    --primary: 0 0% 9%;
    --primary-foreground: 0 0% 98%;
    --secondary: 0 0% 96.1%;
    --secondary-foreground: 0 0% 9%;
    --muted: 0 0% 96.1%;
    --muted-foreground: 0 0% 45.1%;
    --accent: 0 0% 96.1%;
    --accent-foreground: 0 0% 9%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 0 0% 98%;
    --border: 0 0% 89.8%;
    --input: 0 0% 89.8%;
    --ring: 0 0% 3.9%;
    --chart-1: 12 76% 61%;
    --chart-2: 173 58% 39%;
    --chart-3: 197 37% 24%;
    --chart-4: 43 74% 66%;
    --chart-5: 27 87% 67%;
    --sidebar-background: 0 0% 98%;
  }

  .dark {
    /* Same variables with dark mode values */
  }
}
```
</interfaces>
</context>

<tasks>

<task type="auto">
  <name>Task 1: Update light mode CSS variables in :root block</name>
  <files>src/frontend/src/index.css</files>
  <read_first>
    <file>src/frontend/src/index.css</file>
  </read_first>
  <action>
    Update the `:root` block in `src/frontend/src/index.css` with Brand Victoria HSL values. Replace ALL variable values using these exact HSL conversions:

    **Brand Victoria Light Mode Palette:**
    ```
    --background: 0 0% 100%;                    /* White - unchanged */
    --foreground: 248 48% 18%;                  /* Navy #201547 for text */
    --card: 0 0% 100%;                          /* White - unchanged */
    --card-foreground: 248 48% 18%;             /* Navy #201547 */
    --popover: 0 0% 100%;                       /* White - unchanged */
    --popover-foreground: 248 48% 18%;          /* Navy #201547 */
    --primary: 248 48% 18%;                     /* Navy #201547 */
    --primary-foreground: 0 0% 100%;            /* White */
    --secondary: 212 100% 30%;                  /* Blue #004c97 */
    --secondary-foreground: 0 0% 100%;          /* White */
    --muted: 40 3% 85%;                         /* Light Grey #d9d9d6 */
    --muted-foreground: 210 4% 35%;             /* Grey #53565a */
    --accent: 177 100% 35%;                     /* Teal #00b2a9 */
    --accent-foreground: 0 0% 100%;             /* White */
    --destructive: 356 62% 42%;                 /* Red #af272f */
    --destructive-foreground: 0 0% 100%;        /* White */
    --border: 40 3% 85%;                        /* Light Grey #d9d9d6 */
    --input: 40 3% 85%;                         /* Light Grey #d9d9d6 */
    --ring: 212 100% 30%;                       /* Blue #004c97 for focus rings */
    --sidebar-background: 248 48% 18%;          /* Navy #201547 */
    ```

    **Chart Colors (Brand Victoria palette):**
    ```
    --chart-1: 177 100% 35%;                    /* Teal #00b2a9 */
    --chart-2: 212 100% 30%;                    /* Blue #004c97 */
    --chart-3: 248 48% 18%;                     /* Navy #201547 */
    --chart-4: 38 100% 55%;                     /* Orange #ff9e1b */
    --chart-5: 292 83% 36%;                     /* Purple #87189d */
    ```

    **IMPORTANT:**
    - Keep the exact CSS structure (order, comments, @layer base wrapper)
    - Only change the VALUES, not variable names
    - Preserve the --radius: 0.5rem; unchanged
    - HSL format: `H S% L%` (no hsl() wrapper, space-separated)
  </action>
  <acceptance_criteria>
    - grep verifies `--primary: 248 48% 18%;` in :root block
    - grep verifies `--secondary: 212 100% 30%;` in :root block
    - grep verifies `--accent: 177 100% 35%;` in :root block
    - grep verifies `--sidebar-background: 248 48% 18%;` in :root block
    - grep verifies all chart variables updated to Brand Victoria colors
    - File contains `@layer base` wrapper unchanged
    - File contains `:root {` block opener unchanged
  </acceptance_criteria>
  <verify>
    <automated>grep -E "^\s*--primary:\s*248 48% 18%;" src/frontend/src/index.css && grep -E "^\s*--secondary:\s*212 100% 30%;" src/frontend/src/index.css && grep -E "^\s*--accent:\s*177 100% 35%;" src/frontend/src/index.css</automated>
  </verify>
  <done>
    Light mode CSS variables updated with Brand Victoria colors. Primary=Navy, Secondary=Blue, Accent=Teal, Sidebar=Navy background. All chart colors use Brand Victoria palette.
  </done>
</task>

<task type="auto">
  <name>Task 2: Update dark mode CSS variables in .dark block</name>
  <files>src/frontend/src/index.css</files>
  <read_first>
    <file>src/frontend/src/index.css</file>
  </read_first>
  <action>
    Update the `.dark` block in `src/frontend/src/index.css` with Brand Victoria dark mode HSL values. Per CONTEXT.md decision: "Primary swaps to Teal — Navy (#201547) has insufficient contrast on dark backgrounds."

    **Brand Victoria Dark Mode Palette:**
    ```
    --background: 248 48% 8%;                   /* Very dark Navy */
    --foreground: 0 0% 95%;                     /* Off-white for text */
    --card: 248 48% 10%;                        /* Slightly lighter dark Navy */
    --card-foreground: 0 0% 95%;                /* Off-white */
    --popover: 248 48% 12%;                     /* Dark Navy for popovers */
    --popover-foreground: 0 0% 95%;             /* Off-white */
    --primary: 177 100% 45%;                    /* Teal #00b2a9 lightened for dark mode contrast */
    --primary-foreground: 248 48% 18%;          /* Navy for contrast on Teal */
    --secondary: 212 100% 45%;                  /* Blue lightened for dark mode */
    --secondary-foreground: 0 0% 100%;          /* White */
    --muted: 248 30% 20%;                       /* Muted dark Navy */
    --muted-foreground: 0 0% 65%;               /* Muted text */
    --accent: 212 100% 45%;                     /* Blue for dark mode accent */
    --accent-foreground: 0 0% 100%;             /* White */
    --destructive: 356 62% 55%;                 /* Red lightened for dark mode */
    --destructive-foreground: 0 0% 100%;        /* White */
    --border: 248 30% 25%;                      /* Dark Navy border */
    --input: 248 30% 25%;                       /* Dark Navy input borders */
    --ring: 177 100% 45%;                       /* Teal for focus rings in dark mode */
    --sidebar-background: 248 48% 12%;          /* Dark Navy for sidebar */
    ```

    **Chart Colors (10-15% lighter for dark mode per CONTEXT.md):**
    ```
    --chart-1: 177 100% 45%;                    /* Teal lightened */
    --chart-2: 212 100% 45%;                    /* Blue lightened */
    --chart-3: 248 48% 35%;                     /* Navy lightened */
    --chart-4: 38 100% 65%;                     /* Orange lightened */
    --chart-5: 292 83% 50%;                     /* Purple lightened */
    ```

    **IMPORTANT:**
    - Keep the exact CSS structure (order, comments, .dark block wrapper)
    - Only change the VALUES, not variable names
    - HSL format: `H S% L%` (no hsl() wrapper, space-separated)
    - Dark mode uses Teal as primary (not Navy) for accessible contrast
  </action>
  <acceptance_criteria>
    - grep verifies `--primary: 177 100% 45%;` in .dark block (Teal, not Navy)
    - grep verifies `--primary-foreground: 248 48% 18%;` in .dark block
    - grep verifies `--secondary: 212 100% 45%;` in .dark block
    - grep verifies `--accent: 212 100% 45%;` in .dark block (Blue in dark mode)
    - grep verifies `--sidebar-background: 248 48% 12%;` in .dark block
    - grep verifies all dark mode chart variables have lighter lightness values
    - File contains `.dark {` block opener unchanged
  </acceptance_criteria>
  <verify>
    <automated>grep -A 50 "\.dark {" src/frontend/src/index.css | grep -E "^\s*--primary:\s*177 100% 45%;" && grep -A 50 "\.dark {" src/frontend/src/index.css | grep -E "^\s*--accent:\s*212 100% 45%;"</automated>
  </verify>
  <done>
    Dark mode CSS variables updated with Brand Victoria colors adapted for dark backgrounds. Primary=Teal (for contrast), Secondary=Blue, Accent=Blue, Sidebar=dark Navy background. Charts use 10-15% lighter variants.
  </done>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <name>Task 3: Visual verification of Brand Victoria colors</name>
  <files>src/frontend/src/index.css</files>
  <action>
    This is a checkpoint task for human visual verification. No code changes required.
    The executor will pause and prompt the user to verify the Brand Victoria colors are applied correctly.
  </action>
  <what_built>
    Updated `src/frontend/src/index.css` with Brand Victoria color palette in both light and dark modes. All Shadcn UI components now use these colors automatically via CSS variable propagation.
  </what_built>
  <how_to_verify>
    1. Open the app in browser (localhost:3000)
    2. Verify light mode shows:
       - Navy (#201547) as primary button/action color
       - Blue (#004c97) as secondary elements
       - Teal (#00b2a9) as accent/highlight color
       - Navy sidebar background
    3. Toggle to dark mode (use theme toggle in UI)
    4. Verify dark mode shows:
       - Teal (#00b2a9 lightened) as primary color (NOT Navy)
       - Blue for secondary and accent elements
       - Dark Navy background
    5. Check a chart or data visualization (if available on home page)
    6. Verify chart uses Teal, Blue, Navy, Orange, Purple palette
  </how_to_verify>
  <verify>
    <automated>echo "Checkpoint: Human visual verification required"</automated>
  </verify>
  <done>
    User has verified Brand Victoria colors are correctly applied in both light and dark modes. Primary, secondary, accent, and chart colors match Brand Victoria palette.
  </done>
  <resume_signal>Type "approved" if colors look correct, or describe issues if any Brand Victoria colors are missing or incorrect</resume_signal>
</task>

</tasks>

<verification>
## Automated Verification

1. **Light mode primary color:** `grep -E "^\s*--primary:\s*248 48% 18%;" src/frontend/src/index.css`
2. **Dark mode primary color:** `grep -A 50 "\.dark {" src/frontend/src/index.css | grep -E "^\s*--primary:\s*177 100% 45%;"`
3. **Chart colors updated:** `grep -E "^\s*--chart-1:\s*177 100% 35%;" src/frontend/src/index.css`
4. **CSS structure preserved:** File contains `@layer base`, `:root {`, `.dark {` blocks

## Manual Verification

See Task 3 checkpoint for visual verification steps.
</verification>

<success_criteria>
1. User sees Navy (#201547), Blue (#004c97), and Teal (#00b2a9) as primary interface colors in light mode
2. User sees appropriately adjusted Brand Victoria colors in dark mode with Teal as primary (accessible contrast)
3. All Shadcn UI components (buttons, inputs, cards) render with Brand Victoria palette
4. Charts and data visualizations use Brand Victoria color scheme (Teal, Blue, Navy, Orange, Purple)
5. CSS file structure preserved (no broken Tailwind compilation)
</success_criteria>

<output>
After completion, create `.planning/phases/01-color-system/01-color-system-01-SUMMARY.md`
</output>
