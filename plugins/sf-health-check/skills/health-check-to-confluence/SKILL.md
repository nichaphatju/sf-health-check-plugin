---
name: health-check-to-confluence
description: Publish or update a Confluence page from the canonical Salesforce Health Check JSON without re-running or changing the assessment.
disable-model-invocation: true
---

# Health Check to Confluence

Publish a Salesforce Health Check to Confluence using:

`health-check/health-check-report.json`

(read from the **current project**, the org that was assessed) as the canonical source of truth.

This skill is a publishing transformation, not a Salesforce assessment.

## Core Rules

1. Do not re-run the Salesforce Health Check.
2. Do not create, remove, reinterpret, upgrade, or downgrade findings.
3. Do not change finding severity, confidence, guidance basis, risk, recommendation, priority, or effort.
4. Do not add new Salesforce best-practice claims.
5. Do not use model knowledge to fill missing Health Check content.
6. Preserve finding IDs and source traceability.
7. Calculate display counts from `findings`; do not invent totals.
8. If required source data is missing, state that it is unavailable rather than guessing.

## Input

Default:

`health-check/health-check-report.json`

Use another JSON path only when supplied in `$ARGUMENTS`.

Before publishing:
- confirm the file exists;
- parse it;
- ensure it is the intended assessment;
- run the Health Check JSON validator (bundled with this plugin) before publication:

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/salesforce-health-check/scripts/validate-report.py \
  health-check/health-check-report.json
```

Do not publish invalid JSON.

## Confluence Connection

Use the available Confluence/Atlassian integration or MCP tools discovered in the current Claude Code environment.

Do not assume a specific MCP server name or tool identifier.

If no writable Confluence integration is available:
- generate a local publication preview;
- clearly state that publication could not be performed;
- do not claim the page was created.

## Publication Target

Use `$ARGUMENTS` when provided for:
- Confluence space;
- parent page;
- page title;
- existing page to update;
- publish mode;
- inclusion/exclusion of appendices.

Do not guess a target space or parent when multiple plausible destinations exist.

If the user identifies an existing page, update it rather than creating a duplicate when the available integration supports safe page updates.

## Default Page Title

When no title is supplied:

`Salesforce Health Check — <Organisation>`

If an assessment date is useful for distinguishing multiple assessments:

`Salesforce Health Check — <Organisation> — <Assessment Date>`

## Content Structure

Create an executive-first Confluence page.

### Header / Document Control

Include when available:
- Organisation
- Salesforce org/environment
- Edition
- Assessment date
- Evidence date
- Version
- Prepared by
- Classification

### 1. Executive Summary

Use only:
- `executiveSummary.overallAssessment`
- `executiveSummary.summary`
- `executiveSummary.keyThemes`
- `executiveSummary.recommendedNextActions`

Do not create new conclusions.

### 2. Assessment Overview

Include:
- scope;
- evidence reviewed;
- assessment limitations;
- methodology summary.

Methodology wording may explain that material Salesforce best-practice findings were validated against current official Salesforce guidance, but must not introduce new assessment claims.

### 3. Org Health Snapshot

Create a compact table from:
- `coverage`
- derived finding counts by category/severity.

Suggested columns:

| Area | Assessment | Critical | High | Medium | Low | Summary |
|---|---|---:|---:|---:|---:|---|

`Not Assessed` and `Insufficient Evidence` must remain visibly distinct from healthy areas.

### 4. Key Risks & Findings

Include:
- all Critical findings;
- all High findings;
- systemic Medium findings where useful for the summary.

Do not omit Critical/High findings merely to shorten the page.

Suggested table:

| ID | Finding | Severity | Confidence | Area | Priority |
|---|---|---|---|---|---|

### 5. Detailed Assessment

Group by `category`.

For each finding preserve:
- ID and title
- Severity
- Confidence
- Guidance Basis
- Affected Components
- Observation
- Org Evidence
- Salesforce Guidance
- Gap / Alignment
- Risk / Impact
- Recommendation
- Priority
- Effort

Keep source IDs or source links visible where practical.

### 6. Remediation Roadmap

Derive phase grouping from existing `priority` values:
- Immediate → Phase 1 — Immediate Risk Reduction
- Near-term → Phase 2 — Stabilisation
- Backlog / Advisory → Phase 3 — Optimisation & Modernisation

Do not change the recommendation while formatting the roadmap.

### 7. Positive Findings

Render `positiveFindings`.

### 8. Assessment Limitations

Render all `limitations`.

### 9. Official Salesforce References

Render `salesforceSources`:
- source ID;
- title;
- URL;
- finding IDs supported.

### 10. Evidence Sources

Render `evidenceSources` when useful for auditability.

## Page Design

Prefer native Confluence constructs that remain maintainable after publication:
- headings;
- tables;
- panels/callouts;
- status labels when supported;
- expandable sections for verbose evidence;
- links to official Salesforce sources.

Avoid fragile formatting, raw HTML, or elaborate generated markup when native Confluence formatting can express the same structure.

Keep the first screen useful to leadership. Put detailed technical evidence later on the page.

## Large Reports

Do not create dozens of child pages automatically.

For a normal Health Check, prefer one page.

Consider a parent page plus child pages only when:
- the report is too large to navigate effectively;
- the user explicitly requests a page hierarchy; or
- the existing Confluence structure clearly expects it.

If splitting:
- parent: executive summary, snapshot, roadmap;
- children: detailed assessment by major domain or technical appendix.

Preserve finding IDs across all pages.

## Preview and Write Behaviour

### Preview-only request

If the user asks to preview, draft, format, or prepare:
- do not publish;
- produce the proposed page structure/content locally or in the response.

### Explicit publish/update request

When the user explicitly asks to publish/create/update the Confluence page:
- use the writable Confluence integration;
- publish the content;
- return the resulting page title/location/link/reference when available.

Do not perform unrelated Confluence changes.

## Update Behaviour

When updating an existing Health Check page:
- preserve the target page identity;
- replace/update Health Check content from the canonical JSON;
- do not merge stale findings from the old page back into the JSON;
- do not treat manually edited Confluence wording as a new Salesforce assessment;
- avoid duplicating sections.

If material manual content exists outside the generated Health Check sections, preserve it where practical or alert the user before destructive replacement.

## Token Efficiency

- Read the JSON once where practical.
- Do not load Salesforce metadata or code.
- Do not browse Salesforce documentation; validation already belongs to the Health Check workflow.
- Do not invoke Health Check analysis subagents.
- Derive tables/counts programmatically where tooling is available.
- Summarise verbose evidence for page readability without changing its meaning.

## Final Check

Before publishing confirm:
- organisation and assessment date match the intended report;
- finding IDs are unchanged;
- severity/confidence/priority values match JSON;
- no new findings were introduced;
- Critical/High findings were not accidentally omitted;
- official Salesforce references correspond to JSON source records;
- limitations are included;
- no credentials/secrets are published;
- page target is correct.

## Final Response

Report:
- whether the page was previewed, created, or updated;
- page title;
- target space/parent when available;
- page link/reference when available;
- number of findings published;
- any sections intentionally omitted by user request.
