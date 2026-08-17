# Salesforce Health Check Report Structure

This file defines report content and ordering. It is not the source of Salesforce best-practice knowledge.

The final DOCX is rendered from the schema-valid JSON assessment.

## Cover

Include when available:
- Salesforce Org Health Check
- Organisation
- Org/environment
- Salesforce edition
- Org ID
- Evidence date
- Assessment date
- Prepared by
- Version
- Classification

## 1. Executive Summary

For senior stakeholders:
- overall qualitative assessment;
- concise summary;
- 3–5 key themes;
- recommended next actions.

Do not introduce new findings.

## 2. Assessment Overview

Include:
- assessment scope;
- methodology summary;
- evidence reviewed;
- official Salesforce guidance basis;
- key assessment limitations.

## 3. Org Health Snapshot

Show one row per assessed domain:
- area;
- Well-Architected lens;
- qualitative rating;
- Critical / High / Medium / Low counts;
- concise summary.

Counts are derived from `findings`.

`Not Assessed` / `Insufficient Evidence` areas must remain visibly distinct from healthy areas.

## 4. Key Risks & Findings

Show all Critical and High findings plus selected systemic Medium findings.

Columns:
- ID
- Finding
- Severity
- Confidence
- Area
- Impact
- Priority

## 5. Detailed Assessment

Group findings by category.

For each category:
- category assessment summary;
- findings.

Each finding must display:
- ID + title;
- severity;
- confidence;
- guidance basis;
- affected area/components;
- Observation;
- Org Evidence;
- Salesforce Guidance;
- Gap / Alignment;
- Risk / Impact;
- Recommendation;
- Priority;
- Effort.

If an area was adequately assessed and no material issue was found, state so.
If evidence was incomplete, state `Not Assessed / Insufficient Evidence`.

## 6. Remediation Roadmap

Group accepted findings into:
- Phase 1 — Immediate Risk Reduction
- Phase 2 — Stabilisation
- Phase 3 — Optimisation & Modernisation

Do not invent delivery dates.

## 7. Positive Findings

List evidence-supported strengths.

## 8. Selected Component Deep Dives

Optional.

Only include components explicitly listed in `componentHighlights`.

Use when a component:
- supports a material finding;
- is architecturally important;
- benefits from a visual or detailed breakdown.

Do not document every Flow/Apex class/object at this depth.

## 9. Assessment Limitations

Mandatory.

State that:
- the assessment reflects the evidence available as of the evidence date;
- static review cannot prove the absence of defects, vulnerabilities or runtime issues;
- unreviewed/inaccessible areas are not implicitly healthy.

## Appendices

### A. Detailed Finding Register
### B. Org Inventory / Metrics
### C. Evidence Sources
### D. Official Salesforce Guidance References

The inventory belongs primarily in the appendix rather than dominating the executive report.
