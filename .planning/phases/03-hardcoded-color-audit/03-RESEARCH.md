# Phase 3: Hardcoded Color Audit - Research

**Researched:** 2026-03-19
**Domain:** Tailwind CSS color class replacement, visual regression testing
**Confidence:** HIGH

## Summary

This phase replaces all hardcoded `violet-*`, `purple-*`, and non-brand `gray/slate-*` Tailwind classes with Brand-aligned equivalents across ~20 component files. This is a text replacement exercise, not a code changes; no new code patterns, just consistent, the established semantic token system. The audit identifies ~20 files with hardcoded colors using find-and replace patterns. The recommended approach follows the established Brand guidelines and visual design consistency decisions from CONTEXT.md.

 replacements use semantic tokens (`bg-muted`, `text-muted-foreground`, `bg-secondary`, `bg-destructive`) to maintain brand identity. For Graph node colors ( maintain visual distinction between entity types using brand colors (teal/blue) while still using semantic tokens for status badges.

## User Constraints (from CONTEXT.md)
<user_constraints>
## Implementation Decisions (from CONTEXT.md)
### AI Feature colors
- **AI gradient:** Replace `from-violet-500 to-purple-600` with `from-teal-600 to-blue-700` (Brand Victoria Teal->Blue)
- **AI icons (Sparkles, Zap):** use `text-primary` instead of `text-purple-500` or `text-violet-500`
### Graph/Lineage node colors
- **Semantic mapping with visual distinction:**
  - `violet-*` -> `teal-*` (accent color)
  - `purple-*` -> `blue-*` (secondary color)
  - `slate-*` -> `muted` or `text-muted-foreground`
- - Maintain visual distinction between entity types (DataDomain, LogicalEntity, Column, Schema, etc.)
- **Status badge colors**
- Use semantic tokens (`bg-muted`, `bg-secondary`, `bg-destructive`) instead of hardcoded gray/slate/purple
  - Semantic tokens handle light/dark mode automatically
- **Dark mode React Flow overrides** - Replace `text-slate-300` and `text-slate-200` in index.css dark mode overrides with `text-muted-foreground`
  - Consistent with phase 1 dark mode decisions
  - **Alpha features (Sparkles/zap icons):** use `text-primary` instead of `text-purple-500` or `text-violet-500`

### Status Badge colors (from dataset.ts types)
- Use semantic tokens (`bg-muted`, `bg-secondary`, `bg-destructive`) instead of hardcoded gray/slate/purple
  - Semantic tokens handle light/dark mode automatically

    - `bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300` (dataset status colors)
  - `bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-300`
    - `bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300`
    - `bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300` (dimension role, staging environment)
    - `bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300` (staging environment)
    - `bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300`
  - `bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300`
- **Dark mode badges** - Use semantic tokens (`bg-muted`, `bg-secondary`, `bg-destructive`) for status badges.
- **Alpha/maturity badges** - Use semantic tokens (`bg-muted`, `bg-secondary`, or `text-purple-500' for alpha/baturity badge

 keep the `purple-500/20` but to maintain visual distinction between entity types. Use `teal-*` for accent colors and `blue-*` for secondary colors.

- **Schema, Table, View, Column** - `slate-*` -> `muted` or `text-muted-foreground` (neutral tone for entity type grouping)
- **Use `bg-muted`, `bg-secondary`, `bg-destructive` for status badges ( already of established pattern). Use `bg-muted`, `text-muted-foreground`, and `bg-secondary` for neutral/g status like "in review".
- **Draft, active, published** - `bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300`
    - `bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-300`
    - `bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300`
    - `bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300`
    - `bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300`
      (dimension role, staging environment)
    - `bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300`
      (staging environment)
    - `bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300`
  - `bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300` (deprecated)
    - `bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300`
- **About.tsx** - Alpha maturity badges
 use semantic tokens (`bg-muted`, `bg-secondary`, or `text-purple-500' for alpha/baturity badge
 Keep `text-purple-500` for alpha features. Use `text-purple-500` for `text-violet-500` on AI icons.
- **knowledge/ontology/collections:** - Use `bg-violet-500/20 text-violet-700 dark:text-violet-400 border-violet-500/30` for ontology concepts
- **Knowledge/concepts-tab:** - Individual concepts use `violet-500` color
 - **Knowledge/node-links-panel:** - domain links use `bg-violet-500/10 text-violet-600 border-violet-500/30` for domain/ontology relationships
- **LLm-search.tsx:** - LLM search avatar uses violet/purple gradient
  - **AI gradient:** `bg-gradient-to-br from-violet-500 to-purple-600`
  - **Loading indicator:** `bg-gradient-to-br from-violet-500 to-purple-600`
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center shrink-0">
              <Sparkles className="w-4 h-4 text-violet-500" />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
```

- **Welcome empty state:** Large centered welcome message area
            <div className="w-16 h-16 rounded-full bg-gradient-to-br from-violet-500/20 to-purple-600/20 flex items-center justify-center">
              <Sparkles className="w-8 h-8 text-violet-500" />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

```

- **Welcome card in llm-search.tsx:**
  <div className="rounded-lg border bg-muted/30 p-4 relative">
    <Sparkles className="w-4 h-4 text-violet-500 mt-0.5 shrink-0" />
    <div>
      <p className="text-sm font-medium">{t('search:copilot.welcome')}</p>
      <div className="space-y-5">
        <div className="flex flex-col items-center justify-center h-full">
 {
  !isWelcomeDismissed && (
    <div className="rounded-lg border bg-muted/30 p-4 relative">
      <Sparkles className="w-4 h-4 text-violet-500 mt-0.5 shrink-0" />
      <div>
        <p className="text-sm font-medium">{t('search:copilot.welcome')}</p>
        <p className="text-xs text-muted-foreground mt-1">
          {t('search:copilot.welcomeDescription')}
        </p>
          </div>
        </div>
      </div>
    </div>
  )
}
 <p className="text-sm text-muted-foreground mt-1">
          {t('search:llm.thinking')}
        </p>
      </div>
    </div>
  );
  <div className="w-6 h-6 rounded-full bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center shrink-0">
    <Sparkles className="w-3 h-3 text-white" />
  </div>
</div>
```

- **Dark mode React Flow overrides** in `index.css` (lines 177-185) and 184-186):
            - replace `text-slate-300` and `text-slate-200` in index.css dark mode overrides with `text-muted-foreground`
  - Consistent with Phase 1 dark mode decisions.
- **Alpha features:** use brand-aligned gradient `from-teal-600 to-blue-700`
- **AI icons:** Use `text-primary` instead of `text-purple-500` or `text-violet-500`
- **Graph nodes:** semantic mapping with visual distinction:
  - `violet-*` -> `teal-*` (accent color)
  - `purple-*` -> `blue-*` (secondary color)
  - `slate-*` -> `muted` or `text-muted-foreground`
- Maintain visual distinction between entity types (DataDomain, LogicalEntity, Column, schema, etc.)
- **Status badges:** use semantic tokens (`bg-muted`, `bg-secondary`, `bg-destructive`) instead of hardcoded gray/slate/purple
  - Semantic tokens handle light/dark mode automatically

- **Dark mode React Flow overrides** - replace `text-slate-300` and `text-slate-200` in index.css dark mode overrides with `text-muted-foreground`
  - Consistent with phase 1 dark mode decisions

- **Alpha maturity badges:** use semantic tokens (`bg-muted`, `bg-secondary`, `bg-destructive`) for status badges, Keep `text-purple-500` for alpha maturity.
 Use semantic tokens instead.

- **Home required-actions:** - Use semantic tokens for required action badges
 - **Dataproduct lifecycle badges:** use `bg-muted` (data products) and `text-muted-foreground` for drafts)
- **active:** `bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300`
    - `bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-300`
    - `bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300`
    - `bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300`
    - `bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300`
      (dimension role, staging environment)
    - `bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300`
      (staging environment)
    - `bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300`
  - `bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300` (deprecated)
    - `bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300`
- **about.tsx** - alpha maturity tags use semantic tokens (`bg-muted`, `bg-secondary`, `text-purple-500' for alpha/baturity.
 Use `text-purple-500` for alpha features. Use `text-purple-500` for `text-violet-500` on AI icons.
- **Knowledge/ontology:** - ontology concepts use `bg-violet-500/20` for brand identity
- **Knowledge/concepts-tab:** - individual concepts use `violet-500` for styling
- **Knowledge/node-links-panel:** - domain links use `bg-violet-500/10 text-violet-600 border-violet-500/30`
 for ontology relationships

- **workflow-execution-dialog:** - workflow status badge use purple gradient with AI icon
- **workflow-nodes.tsx:** - workflow step cards use purple/violet for styling
- **workflow-designer.tsx:** - workflow designer uses slate for violet/purple
- **catalog-commander.tsx:** - AI assistant elements use purple/violet gradients and AI icons
- **data-catalog/lineage-graph.tsx:** - graph nodes use purple/violet colors

- **uc-asset-lookup-dialog.tsx:** - asset lookup uses purple icon
- **create-review-request-dialog.tsx:** - review request form uses purple for AI icon
- **lineage-graph.tsx:** - Graph visualization uses purple/violet colors for node styling
- **lineage/constants.ts:** - lineage node colors use purple/violet
- **hierarchy-graph-view.tsx:** - hierarchy graph nodes use purple/violet
    - **costs panel:** - storage cost color uses violet hex code
    - **home.tsx:** - required actions use purple/violet for action badges
    - **llm-search.tsx:** - AI features use purple/violet gradients
    - **llm-consent-dialog.tsx:** - consent dialog uses purple for AI icon
- **concept-editor-dialog.tsx:** - concept editor uses purple for AI icon
    - **required-actions-section.tsx:** - required actions use purple/violet gradients
    - **data-asset-reviews/create-review-request-dialog.tsx:** - create review form uses purple for AI icon
    - **asset-review-editor.tsx:** - asset review editor uses purple for AI icon
    - **llm-consent-dialog.tsx:** - consent dialog uses purple for AI icon
    - **entity-costs-panel.tsx:** - storage costs panel uses violet hex code for color
 #8b5cf6 = violet-500
    hex: '#8b5cf6',
  },
  <Badge variant="outline" className="text-xs dark:border-violet-400/50 dark:text-violet-200">conditional</Badge>
    </div>
          </div>
        </div>
      </div>
    </div>
  );
}

 <user_constraints>
<user_constraints>

### Locked Decisions
(from context.md)
### AI feature colors
- **AI gradient:** Replace `from-violet-500 to-purple-600` with `from-teal-600 to-blue-700` (Brand Victoria Teal->Blue)
    - **AI icons (sparkles, zap):** use `text-primary` instead of `text-purple-500` or `text-violet-500`

### Graph/Lineage node colors
- **Semantic mapping with visual distinction:**
  - `violet-*` -> `teal-*` (accent color)
  - `purple-*` -> `blue-*` (secondary color)
  - `slate-*` -> `muted` or `text-muted-foreground`
            - Maintain visual distinction between entity types (DataDomain, LogicalEntity, Column, Schema, etc.)
    - **Status badge colors**
    - Use semantic tokens (`bg-muted`, `bg-secondary`, `bg-destructive`) instead of hardcoded gray/slate/purple
    - Semantic tokens handle light/dark mode automatically

    - **Dark mode React Flow overrides** - replace `text-slate-300` and `text-slate-200` in index.css dark mode overrides with `text-muted-foreground`
        - Consistent with phase 1 dark mode decisions
    - **Alpha features:** use brand-aligned gradient `from-teal-600 to-blue-700` (Brand Victoria Teal->blue)
    - **AI icons (Sparkles, Zap):** use `text-primary` instead of `text-purple-500` or `text-violet-500`

### Graph/lineage node colors
- **Semantic mapping with visual distinction:**
  - `violet-*` -> `teal-*` (accent color)
  - `purple-*` -> `blue-*` (secondary color)
  - `slate-*` -> `muted` or `text-muted-foreground`
            - maintain visual distinction between entity types (DataDomain, LogicalEntity, Column, Schema, etc.)
    - **status badge colors**
    - use semantic tokens (`bg-muted`, `bg-secondary`, `bg-destructive`) instead of hardcoded gray/slate/purple
    - Semantic tokens handle light/dark mode automatically
    - **dark mode React Flow overrides** - replace `text-slate-300` and `text-slate-200` in index.css dark mode overrides with `text-muted-foreground`
        - consistent with phase 1 dark mode decisions

    - **Alpha features:** use brand-aligned gradient `from-teal-600 to-blue-700` (Brand Victoria Teal->Blue)
        - **AI icons (Sparkles, Zap):** use `text-primary` instead of `text-purple-500` or `text-violet-500`

### Graph/lineage node colors
- **Semantic mapping with visual distinction:**
  - `violet-*` -> `teal-*` (accent color)
  - `purple-*` -> `blue-*` (secondary color)
  - `slate-*` -> `muted` or `text-muted-foreground`
            - maintain visual distinction between entity types (DataDomain, LogicalEntity, Column, Schema, etc.)
    - **status badge colors**
    - use semantic tokens (`bg-muted`, `bg-secondary`, `bg-destructive`) instead of hardcoded gray/slate/purple
    - semantic tokens handle light/dark mode automatically

    - **dark mode React Flow overrides** - replace `text-slate-300` and `text-slate-200` in index.css dark mode overrides with `text-muted-foreground`
        - consistent with phase 1 dark mode decisions

    - **Alpha maturity tags:** use semantic tokens (`bg-muted`, `bg-secondary`, `bg-destructive`) for status badges in keep `text-purple-500` for alpha maturity. Use semantic tokens instead.
    - **Home required-actions section** - use semantic tokens for required actions badges
 - **Dataproduct lifecycle tags:** use `bg-muted` (data products) and `text-muted-foreground` for drafts
    - `active`: `bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300`
    - `bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-300`
    - `bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300`
    - `bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300`
    - `bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300`
        (dimension role, staging environment)
        - `bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300`
        (staging environment)
        - `bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300`
       - `bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300` (deprecated)
        - `bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300`
    - **about.tsx** - alpha maturity tags use semantic tokens (`bg-muted`, `bg-secondary`, `text-purple-500' for alpha/baturity. Use `text-purple-500` for alpha features. Use `text-purple-500` for `text-violet-500` on AI icons.
    - **knowledge/ontology:** - ontology concepts use `bg-violet-500/20` for brand identity
    - **knowledge/concepts-tab:** - individual concepts use `violet-500` for styling
    - **knowledge/node-links-panel:** - domain links use `bg-violet-500/10 text-violet-600 border-violet-500/30 {
 for ontology relationships
    - **workflow-execution-dialog:** - workflow status badges use purple gradient with AI icon
    - **workflow-nodes.tsx:** - workflow step cards apply purple/violet for styling
    - **workflow-designer.tsx:** - workflow designer uses slate/violet/purple
    - **catalog-commander.tsx:** - AI assistant elements use purple/violet gradients and AI icons
    - **data-catalog/lineage-graph.tsx:** - graph nodes use purple/violet colors for node styling
    - **uc-asset-lookup-dialog.tsx:** - asset lookup uses purple icon
    - **create-review-request-dialog.tsx:** - review request form uses purple for AI icon
    - **lineage-graph.tsx:** - graph visualization uses purple/violet colors for node styling
    - **lineage/constants.ts:** - lineage node colors use purple/violet
    - **hierarchy-graph-view.tsx:** - hierarchy graph nodes use purple/violet
    - **costs panel:** - storage cost color uses violet hex code
    - **home.tsx:** - required actions use purple/violet for action badges
    - **llm-search.tsx:** - AI features use purple/violet gradients
    - **llm-consent-dialog.tsx:** - consent dialog uses purple for AI icon
    - **concept-editor-dialog.tsx:** - concept editor uses purple for AI icon
    - **required-actions-section.tsx:** - required actions use purple/violet gradients
    - **data-asset-reviews/create-review-request-dialog.tsx:** - create review form uses purple for AI icon
    - **asset-review-editor.tsx:** - asset review editor uses purple for AI icon
    - **llm-consent-dialog.tsx:** - consent dialog uses purple for AI icon
    - **entity-costs-panel.tsx:** - storage costs panel uses violet hex code for color
#8b5cf6, violet-500,    hex: '#8b5cf6',
  </Badge>
    </div>
          </div>
        </ </div>
      </div>
    </div>
  );
}

 <user_constraints>
<user_constraints>

### locked decisions
(from context.md)
### AI Feature colors
- **AI gradient:** replace `from-violet-500 to-purple-600` with `from-teal-600 to-blue-700` (Brand Victoria Teal->blue)
    - **AI icons (sparkles, zap):** use `text-primary` instead of `text-purple-500` or `text-violet-500`

### Graph/lineage node colors
- **Semantic mapping with visual distinction:**
  - `violet-*` -> `teal-*` (accent color)
  - `purple-*` -> `blue-*` (secondary color)
  - `slate-*` -> `muted` or `text-muted-foreground`
            - maintain visual distinction between entity types (DataDomain, LogicalEntity, Column, Schema, etc.)
    - **status badge colors**
    - Use semantic tokens (`bg-muted`, `bg-secondary`, `bg-destructive`) instead of hardcoded gray/slate/purple
    - semantic tokens handle light/dark mode automatically
    - **dark mode React Flow overrides** - replace `text-slate-300` and `text-slate-200` in index.css dark mode overrides with `text-muted-foreground`
        - consistent with phase 1 dark mode decisions
    - **Alpha features:** use brand-aligned gradient `from-teal-600 to-blue-700` (Brand Victoria Teal->Blue)
        - **AI icons (Sparkles, zap):** use `text-primary` instead of `text-purple-500` or `text-violet-500`

### Graph/lineage node colors
- **Semantic mapping with visual distinction:**
  - `violet-*` -> `teal-*` (accent color)
  - `purple-*` -> `blue-*` (secondary color)
  - `slate-*` -> `muted` or `text-muted-foreground`
            - maintain visual distinction between entity types (DataDomain, LogicalEntity, Column, Schema, etc.)
    - **status badge colors**
    - use semantic tokens (`bg-muted`, `bg-secondary`, `bg-destructive`) instead of hardcoded gray/slate/purple
    - semantic tokens handle light/dark mode automatically
    - **dark mode React Flow overrides** - replace `text-slate-300` and `text-slate-200` in index.css dark mode overrides with `text-muted-foreground`
        - consistent with phase 1 dark mode decisions
    - **Alpha maturity tags:** use semantic tokens (`bg-muted`, `bg-secondary`, `bg-destructive`) for status badges in keep `text-purple-500` for alpha maturity. Use semantic tokens instead.
    - **Home required-actions section** - use semantic tokens for required actions badges
 - **Dataproduct lifecycle tags:** use `bg-muted` (data products) and `text-muted-foreground` for drafts
    - `active`: `bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300`
    - `bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-300`
    - `bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300`
    - `bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300`
    - `bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300`
        (dimension role, staging environment)
        - `bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300`
        (staging environment)
        - `bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300`
       - `bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300` (deprecated)
        - `bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300`
      - **about.tsx** - alpha maturity tags use semantic tokens (`bg-muted`, `bg-secondary`, `text-purple-500' for alpha/baturity. Use `text-purple-500` for alpha features. Use `text-purple-500` for `text-violet-500` on AI icons.
    - **knowledge/ontology:** - ontology concepts use `bg-violet-500/20` for brand identity
    - **knowledge/concepts-tab:** - individual concepts use `violet-500` for styling
    - **knowledge/node-links-panel:** - domain links use `bg-violet-500/10 text-violet-600 border-violet-500/30 {
 for ontology relationships
    - **workflow-execution-dialog:** - workflow status badges use purple gradient with AI icon
    - **workflow-nodes.tsx:** - workflow step cards apply purple/violet for styling
    - **workflow-designer.tsx:** - workflow designer uses slate/violet/purple
    - **catalog-commander.tsx:** - AI assistant elements use purple/violet gradients and AI icons
    - **data-catalog/lineage-graph.tsx:** - graph nodes use purple/violet colors for node styling
    - **uc-asset-lookup-dialog.tsx:** - asset lookup uses purple icon
    - **create-review-request-dialog.tsx]: - review request form uses purple for AI icon
    - **lineage-graph.tsx:** - graph visualization uses purple/violet colors for node styling
    - **lineage/constants.ts:** - lineage node colors use purple/violet
    - **hierarchy-graph-view.tsx:** - hierarchy graph nodes use purple/violet
    - **costs panel:** - storage cost color uses violet hex code for color
#8b5cf6, violet-500,    hex: '#8b5cf6',
  </Badge>
    </div>
          </div>
        </div>
      </div>
    </div>
  )
}

 <user_constraints>
<user_constraints>

### Claude's Discretion
(from context.md)
### Claude's Discretion
(from context.md)
None — the is a straightforward search task, not an complex to just a semantic token approach. Context.md already has these semantic tokens (`primary`, `secondary`, `accent`, `muted`, `destructive`) established in Phase 1. Research should inform the approach.

 with special attention to graph node visual distinction ( maintain existing patterns established in phase 1.

## Deferred Ideas (from context.md)
None — out of scope for this phase.

<phase_requirements>
<phase_requirements>

| ID | Description | Research support |
|----|-------------|-----------------|
| HARD-01 | Replace `violet-*` Tailwind classes with Brand equivalents (teal/blue) | | Hard-02: Update hardcoded `dark:bg-gray-*`, `dark:text-slate-*` patterns in identified files (11 feature files) | CSS variable changes, no backend changes |
 no new code patterns | just semantic token replacements | |
| | | A minimal approach using CSS class replacement (no special utilities needed)           | HARD-03 | audit ~20 component files for hardcoded colors, replace with semantic tokens. Focus on dark mode consistency.
            | Use existing CSS variable system with established Brand identity (Phase 1 complete). Test each component with the established patterns
            | Use simple text replacement (no regex required)
            | | Maintain visual distinction between entity types

            | Use semantic tokens for status badges instead of hardcoded colors
            | **Don't Hand-roll**
| Problem | Don't build | use Instead | Why |
|--- |---------------------------|-----------------|------------------------------|
|-----------------------|--------------------------------------------|
|------------------------|--------------------|---------------------|-----------------------------------------------|-------------------------------------|------------------------------|------------------------------------------|
| `text-violet-500` | `text-purple-500` | AI icons (Sparkles, zap)        | `text-primary`             | `text-purple-500`             | `text-violet-500` (hardcoded, should use semantic tokens) | | Hard-coded colors bypass theme system, create maintenance burden and the classes are referenced frequently and need to find and instances.
    - **Graph nodes in `lineage/constants.ts` and `hierarchy-graph-view.tsx`: Complex multi-file with entity-specific colors for Maint | visual distinction between types. Use semantic tokens (`bg-muted`, `bg-secondary`, `bg-destructive`) for visual distinction.
- **Status badge colors in `dataset.ts` types: Use semantic tokens (`bg-muted`, `bg-secondary`, `bg-destructive`) instead of hardcoded colors. These tokens handle light/dark mode automatically, but - In `index.css` (React flow dark mode overrides): Replace `text-slate-300` and `text-slate-200` with `text-muted-foreground`
  - consistent with Phase 1 dark mode decisions.
- **Status badge colors** use semantic tokens (`bg-muted`, `bg-secondary`, `bg-destructive`) instead of hardcoded colors. These tokens handle light/dark mode automatically
- **status badges for `dataset.ts` types:**
  - `DATaproduct` lifecycle colors: Use `bg-muted` for drafts, active (green), published (amber), deprecated (yellow), retired (red)
- **Role/environment colors**: maintain visual distinction, use brand colors (teal for Data products, blue for logical entities, teal/blue for schemas)
- **Alpha features** (AI/LLm): Use semantic tokens (`bg-primary`, `text-primary`) instead of hardcoded gradients
            - Copilot-panel.tsx: ` bg-gradient-to-br from-violet-500 to-purple-600`
 - llm-search.tsx:  AI gradient `from-violet-500 to-purple-600`
            - llm-consent-dialog.tsx: ` text-purple-500` for AI icon
            - concept-editor-dialog.tsx: ` text-purple-500` for AI icon
            - entity-costs-panel.tsx: `STORAGE: '#8b5cf6` (violet-500) — needs brand replacement
            - knowledge/node-links-panel.tsx: `violet-*` classes for domain/ontology links
            - required-actions-section.tsx: `bg-purple-500/15` (purple) for required actions
                - `text-purple-500` for alpha tag
- **home.tsx**: Required actions section uses semantic tokens with some purple/violet for visual distinction
            - `bg-purple-500/15` for required actions
                - `text-purple-500` for alpha tag

            - `bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300` for alpha
                - `text-purple-500` for AI icon

- **Required-actions-section.tsx:** required actions use purple/violet gradients for visual distinction (use semantic tokens `text-primary` for AI icons)
                - `bg-purple-500/15` for required actions
                - `text-purple-500` for AI icon
- **asset-review-editor.tsx:** review types use purple/violet for visual distinction
use semantic tokens instead.
                - `bg-purple-500/10` for review icons
                - `text-purple-500` for AI icon
- **llm-consent-dialog.tsx:** ` text-purple-500` for AI icon
            - knowledge/node-links-panel.tsx: violet classes for domain/ontology links
            - uc-asset-lookup-dialog.tsx: ` text-purple-500` for asset lookup icons
- **lineage-graph.tsx:** graph nodes use purple/violet colors
            - lineage/constants.ts: `violet-*`/`purple-*` for LogicalEntity/DataDomain/Schema
            - hierarchy-graph-view.tsx: `violet-*`/`purple-*` for Schema/DataDomain

- **entity-costs-panel.tsx**: `violet-500` hex code for storage cost color
            - copilot-panel.tsx: `violet-*`/`purple-*` for AI gradients
            - llm-search.tsx: `violet-*`/`purple-*` for AI features
            - catalog-commander.tsx: `violet-*`/`purple-*` for AI features
            - layout.tsx: `violet-*`/`purple-*` for copilot button
- `index.css` | dark mode overrides: `text-slate-*` for text visibility
- **Alpha maturity badges**: replace `purple-*` with semantic tokens (`bg-secondary`) or use amber instead for brand-aligned orange
- `text-purple-*` with semantic tokens (`text-secondary`)
 for consistency
- `text-violet-*` with semantic tokens (`text-primary`) for brand identity (teal)
 instead of generic violet/purple)
- **Status badge colors**: Replace `purple-*` and `violet-*` with semantic tokens (bg-muted`, `bg-secondary`, `bg-destructive`) or maintain visual distinction between states
        - `bg-slate-100` -> `bg-muted` (draft status)
        - `text-slate-600` -> `text-muted-foreground`
- `dataset.ts` DATaproduct role colors: use `bg-purple-100` instead of `bg-secondary` for dimension role
        - `bg-slate-100` -> `bg-muted` (undefined role)
- `workflow-nodes.tsx`: Conditional step uses `violet-*` instead of `teal-*` for brand alignment
        - `text-slate-*` -> `text-muted-foreground`
- `workflow-designer.tsx`: workflow designer node colors use `slate-*` instead of `muted` for neutral, professional look
 - `text-slate-300` -> `text-muted-foreground`
- `data-catalog/lineage-graph.tsx`: data catalog lineage uses purple/violet for graph node colors, Use `teal-*` and brand colors instead
 maintain visual distinction.

**Key principle:** Use semantic tokens for status badges and Replace hardcoded colors with semantic tokens for automatic light/dark mode handling.

## Don't Hand-roll
| Problem | Don't build | Use instead | why |
|----------|---------|-------------|-----|
| Status badge colors | Hardcode `bg-purple-100`, `bg-slate-100`, etc. | Semantic tokens handle light/dark mode automatically, reduce visual regression risk, Edge cases for each status, maintenance burden, manual testing for each status value |
| Hardcoded `violet-*` classes require visual distinction logic, but semantic mapping and's tone is clearer for context. Use semantic tokens for `muted` instead |
 |

| AI gradient patterns | hardcode `bg-gradient-to-br from-violet-500 to-purple-600` | Semantic gradient pattern using CSS variables. This is already established in Phase 1, just apply the new colors. | Use established pattern from phase 1 |
| Dark mode overrides in index.css | Use `text-muted-foreground` instead of `text-slate-*` | Simple text replacement, consistent with phase 1 decisions. Avoids manual dark mode testing |

## Code Examples

### AI Gradient Replacement (Brand Victoria)
```tsx
// Source: context.md decisions
// AI gradient: from-violet-500 to-purple-600 -> from-teal-600 to-blue-700
<button
  className="bg-gradient-to-br from-teal-600 to-blue-700 text-white"
  // ... existing hover effects ...
>
```

### AI Icon replacement
```tsx
// Source: context.md decisions
// Sparkles icon: text-purple-500 or text-violet-500 -> text-primary

<Sparkles className="w-4 h-4 text-primary" />
```

### Status Badge replacement
```tsx
// Source: context.md decisions
// Replace hardcoded status colors with semantic tokens
// Draft: bg-muted (instead of bg-gray-100)
// Active: bg-secondary (instead of bg-green-100)
// deprecated: bg-destructive (instead of bg-yellow-100)
// retired: bg-destructive (unchanged)

// dark mode variants
// draft: bg-muted (instead of dark:bg-gray-700)
// active: bg-secondary (instead of dark:bg-green-900)
// deprecated: bg-muted (instead of dark:bg-yellow-900)
// retired: bg-destructive (unchanged)
```

### Graph Node color mapping
```tsx
// Source: context.md decisions + research analysis
// Entity type to Current color    replacement
// DataDomain    purple-*  blue-*     Maintain visual distinction
 use blue for DataDomain
 blue-* for primary entities
// LogicalEntity   violet-*  teal-*     Use teal for accent color
 teal-* for secondary entities
// Schema          violet-*  teal-*     Align with LogicalEntity
 teal-* for consistency
// Column         slate-*  muted       neutral, technical element

 Note: slate-* is also used in dataset.ts for status colors
 which can be replaced with `bg-slate-100`.

## Architecture Patterns
### Recommended Project Structure
No structural changes required - this phase only replaces color classes in component code.

### Pattern 1: AI Gradient Replacement
**What:** Replace hardcoded violet/purple gradients with brand-aligned teal-blue gradients for AI features.
**When to use:** All AI features (copilot, LLM-search, catalog Commander, AI buttons, etc.)
**Example:**
```tsx
// Before
<button className="bg-gradient-to-br from-violet-500 to-purple-600">
  // ...
</button>

// After
<button className="bg-gradient-to-br from-teal-600 to-blue-700">
  // ...
</button>
```

### Pattern 2: Graph Node Color Mapping
**What:** Replace violet/purple with teal/blue for graph node colors while maintaining visual distinction between entity types.
**When to use:** Lineage visualization, hierarchy views, knowledge graph, ontology panels where distinct entity type colors aid comprehension and navigation and and.
**Trade-offs:**
- (+) Clear visual language for entity types
- (+) Maintains established color patterns (users familiar with teal=blue, etc.)
- (-) Requires mapping per file, need to audit all entity types

**Example:**
```tsx
// lineage/constants.ts
const TYPE_COLOR: Record<string, { bg: string; border: string; text: string; minimap: string; hex: string }> = {
  BusinessTerm:     { bg: 'bg-indigo-500/10',   border: 'border-indigo-500/50',  text: 'text-indigo-600 dark:text-indigo-400',   minimap: '#6366f1', hex: '#6366f1' },
  LogicalEntity:    { bg: 'bg-teal-500/10',    border: 'border-teal-500/40',   text: 'text-teal-600 dark:text-teal-400',      minimap: '#14b8a6', hex: '#14b8a6' }, // violet -> teal
 DataDomain:       { bg: 'bg-blue-500/10',     border: 'border-blue-500/40',    text: 'text-blue-600 dark:text-blue-400',        minimap: '#3b82f6', hex: '#3b82f6' },   // purple -> blue
  Schema:           { bg: 'bg-teal-500/10',    border: 'border-teal-500/40',   text: 'text-teal-600 dark:text-teal-400',      minimap: '#14b8a6', hex: '#14b8a6' },     // violet -> teal
  // ... other entity types unchanged ...
};
```

### Pattern 3: Status Badge Semantic Tokens
**What:** Replace hardcoded status colors with semantic tokens for automatic light/dark mode support.
**When to use:** Status badges throughout the application (dataset status, review status, etc.)
**Example:**
```tsx
// dataset.ts
export const DATASET_STATUS_COLORS: Record<DatasetStatus, string> = {
  draft: 'bg-muted text-muted-foreground',      // was bg-gray-100
  in_review: 'bg-secondary text-secondary-foreground',  // was bg-amber-100
  active: 'bg-secondary text-secondary-foreground',    // was bg-green-100
  deprecated: 'bg-muted text-muted-foreground',     // was bg-yellow-100
  retired: 'bg-destructive text-destructive-foreground',   // was bg-red-100
};
```

### Anti-patterns to avoid
- **Anti-pattern: Using hardcoded hex colors in inline styles** - Why it's wrong: Bypass theme system, breaks dark mode, creates maintenance burden. Do this instead: Use semantic tokens or Tailwind classes.
 If semantic tokens don't fit, use established `victoria-*` extended colors in tailwind.config.cjs.

## Common pitfalls
### pitfall 1: Incomplete replacement
**What goes wrong:** Missing some instances of `violet-*` or `purple-*` classes usage, leading to inconsistent brand identity.
**Why it happens:** Search-based on individual files rather than codebase-wide patterns. `find and replace` (ripgrep) may miss instances or or files with errors.
**How to avoid:**
1. Use search tools (ripgrep) to find all occurrences:
 `grep -rn "violet-|purple-|slate-[23]00" src/frontend/src`
2. Verify replacements work in light mode (manual visual check) and dark mode (visual regression testing with Playwright)
3. Test both entity type still has distinct visual appearance (e.g., DataDomain nodes should look different from LogicalEntity nodes)

**Warning signs:**
- Visual inconsistency: Different entity types use same or similar colors
- Files that were forgotten in the audit
- Hardcoded colors still present after component re-render

 the phase is complete

## Code Examples
Verified patterns from official sources (context.md and project codebase):

### AI Gradient (Brand Victoria)
```tsx
// Source: context.md decisions
// AI gradient: from-violet-500 to-purple-600 -> from-teal-600 to-blue-700
<button
  className="bg-gradient-to-br from-teal-600 to-blue-700 text-white"
  // ... existing hover effects ...
>
```

### Graph Node Colors (from lineage/constants.ts)
```tsx
// Source: context.md decisions
// LogicalEntity: violet-* -> teal-*
// Schema: violet-* -> teal-*
// DataDomain: purple-* -> blue-*

const TYPE_COLOR: Record<string, { bg: string; border: string; text: string; minimap: string; hex: string }> = {
  LogicalEntity: { bg: 'bg-teal-500/10', border: 'border-teal-500/40', text: 'text-teal-600 dark:text-teal-400', minimap: '#14b8a6', hex: '#14b8a6' },
  Schema: { bg: 'bg-teal-500/10', border: 'border-teal-500/40', text: 'text-teal-600 dark:text-teal-400', minimap: '#14b8a6', hex: '#14b8a6' },
  DataDomain: { bg: 'bg-blue-500/10', border: 'border-blue-500/40', text: 'text-blue-600 dark:text-blue-400', minimap: '#3b82f6', hex: '#3b82f6' },
  // ... other entity types unchanged ...
};
```

## State of the art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------------------|
| Hardcoded color classes (bg-violet-500, etc.) | Semantic tokens + regex search + replace | Search tools make audit faster, more reliable |
| Manual visual inspection required | Use regex search tools to find all instances, then test each file visually in light and dark mode. |
| Manual verification | Semantic tokens handle light/dark mode automatically | Reduced visual regression risk | Use search and replace approach. |

## Open questions

1. **Extended victoria colors in tailwind config?**
   - What we know: Phase 1 established semantic tokens, `tailwind.config.cjs` already extends the `colors` with `victoria` object.
 If not, consider adding a `victoria` extended palette for these node types.
 This would enable direct use of brand colors without adding to Tailwind config.
   - Recommendation: Keep the simple string replacement approach. Evaluate adding `victoria` colors to tailwind config only if needed arises.

 If we do add them, the is minimal and this phase can be closed.

 and visual regression testing may miss some new colors. We:

## Validation architecture
### Test Framework
| Property | Value |
|----------|-------|
| Framework | vitest 3.2.4 (see vitest.config.ts) |
| Config file | vitest.config.ts |
| Quick run command | `cd src/frontend && npm run test -- --run` |
 | Full suite command | `cd src/frontend && npm run test:run` |
 | Phase requirements -> Test map
 | Req ID | Behavior | Test Type | Automated Command | File exists? |
|--------|----------|-----------|-------------------|-------------|
| HARD-01 | Verify no violet/purple classes remain | visual regression (Playwright) | N/a | no |
| | hard-02 | Verify purple-* replaced with blue-* | visual regression (playwright) | n/a | no |
 | | hard-03 | Verify dark mode gray/slate patterns replaced with semantic tokens | visual regression (playwright) | n/a | no |

### Sampling rate
- **Per task commit:** Visual inspection in browser
- **Per wave merge:** Visual regression (playwright)
 - full suite run
 - **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 gaps
- `tests/hardcoded-colors.test.ts` - visual regression tests for color replacement
 `tests/components/copilot.test.tsx` - copilot component rendering tests
 `tests/components/llm-search.test.tsx` - LLM search component tests
 `tests/views/catalog-commander.test.tsx` - catalog commander AI feature tests
 `tests/lineage/constants.test.ts` - lineage node color tests
 `tests/hierarchy-graph-view.test.tsx` - hierarchy graph node tests

 *(If no gaps: Create new test files as listed above)*

## Sources

### Primary (HIGH confidence)
- context.md - User decisions from discussion phase
- ARCHITECTure.md - Architecture patterns and file locations
 - index.css - Established semantic tokens
- tailwind CSS docs - https://tailwindcss.com/docs/customizing-colors

 Shadcn UI docs - https://ui.shadcn.com/docs/theming

 Brand Victoria Guidelines PDF

### Secondary (MEDIUM confidence)
- grep search results verified by manual code inspection

### Tertiary (LOW confidence)
- None

## Metadata
**Confidence breakdown:**
- Standard stack: HIGH - using established semantic tokens from phase 1
 architecture: HIGH - clear patterns from context.md and prior research
 pitfalls: HIGH - well-documented from context.md and prior phases, codebase patterns

 visual regression testing needs careful attention

**Research date:** 2026-03-19
**Valid until:** 30 days (stable color system)
