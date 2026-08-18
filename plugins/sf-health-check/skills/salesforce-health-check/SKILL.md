---
name: salesforce-health-check
description: Generate an evidence-based Salesforce Org Health Check, validate material best-practice claims against current official Salesforce guidance, produce schema-valid JSON, and render a professional DOCX report.
disable-model-invocation: true
---

# Salesforce Org Health Check

Generate, inside the **current project** (the org being assessed), not inside this plugin:

1. `health-check/health-check-report.json` — canonical validated assessment.
2. `health-check/Salesforce-Health-Check.docx` — client-facing report rendered from the JSON.

The JSON is the source of truth. DOCX generation is presentation-only and must not introduce new findings, severities, recommendations, metrics, or Salesforce claims.

## Operating Mode

Run in **Assessment Mode**.

- Do not modify Salesforce metadata.
- Do not deploy.
- Do not assume the default authenticated org is the assessment target.
- Retrieve live metadata only when explicitly requested or required by the agreed assessment scope, and only after verifying the target org.
- A Health Check does not authorise remediation.

If the current project defines its own Assessment Mode / Implementation Mode rules (e.g. in `CLAUDE.md` or `.claude/rules/`), follow those in addition to this skill — they take precedence on project-specific policy (deployment approval, target org selection, etc.).

## Metadata Baseline

If the user explicitly requests the latest/current/live org metadata,
or the agreed assessment scope requires a fresh retrieval:

1. Identify and verify the target org.
2. Determine the metadata scope required for the assessment.
3. Generate the Health Check retrieval manifest at:

   `manifest/package-health-check-<YYYYMMDD>.xml`

   where `<YYYYMMDD>` is the current local date when the assessment
   is performed.

   Example:

   `manifest/package-health-check-20260818.xml`

4. If a Health Check manifest already exists for the current date:
   - inspect it first;
   - reuse it when it matches the agreed assessment scope;
   - update it when the scope has changed;
   - do not create duplicate same-day manifests unnecessarily.
5. Retrieve the required metadata from the verified target org using
   that manifest.
6. Start Health Check analysis only after the retrieval completes.
7. Record the following in the assessment evidence:
   - target org/environment;
   - retrieval date/time;
   - manifest path;
   - retrieval scope;
   - retrieval result;
   - any metadata that could not be retrieved.

If retrieval fails or is incomplete:
- do not silently rely on stale local metadata;
- report the limitation;
- mark affected assessment areas as `Insufficient Evidence`
  where appropriate.

Prefer targeted retrieval over an unnecessary full-org retrieval.

Do not overwrite or reuse an unrelated deployment manifest.
The Health Check retrieval manifest must use the `package-health-check-<YYYYMMDD>.xml` naming convention.

## Required Outcome

The Health Check must:

1. Resolve the assessment target, scope, evidence set, and evidence date.
2. Analyse the supplied Salesforce evidence.
3. Identify evidence-backed candidate findings and positive observations.
4. Consolidate duplicate occurrences and common root causes.
5. Validate material Salesforce best-practice claims against current applicable official Salesforce guidance.
6. Distinguish confirmed findings from project standards, design recommendations, and items requiring validation.
7. Produce `health-check-report.json`.
8. Validate the JSON against `schema/health-check.schema.json` and the quality gates below.
9. Generate the final DOCX using the supplied Word template and generator.
10. Perform document QA before delivery.

## Execution Strategy

Choose the most efficient execution strategy for the assessment.

- Handle straightforward analysis directly when delegation would add little value.
- Use available specialist subagents (`salesforce-org-evidence-analyst`, `salesforce-guidance-validator`, bundled with this plugin) when they materially improve context isolation, parallelism, expertise, or token efficiency.
- Let subagent selection be driven by their descriptions and the current task; do not invoke a subagent merely because it exists.
- Do not require a fixed number or fixed sequence of subagent calls.
- Avoid duplicating the same analysis in the main context and a subagent.
- Keep large repository exploration and large documentation research out of the main context when delegation is beneficial.
- Do not create agent teams unless explicitly required by the user.

The quality requirements in this skill apply regardless of whether work is performed directly or delegated.

## Evidence Rules

Every actionable finding must start from evidence in the assessed org/project.

Acceptable evidence can include:
- Salesforce metadata or source code;
- configuration exports;
- native Salesforce Health Check output;
- validated static-analysis output;
- runtime/log evidence;
- dependency/usage evidence;
- other assessment artifacts explicitly supplied or retrieved for the assessment.

Rules:

- Claude/model knowledge may suggest what to investigate, but it is not evidence.
- Do not infer missing metadata, runtime behaviour, usage, data volume, or security impact without evidence.
- Missing evidence means `Not Assessed` / `Insufficient Evidence`, not `Healthy`.
- Static-analysis warnings are candidates until validated in context.
- Consolidate repeated occurrences when they share the same root cause and remediation pattern.
- Preserve evidence-supported strengths as positive findings.

## Finding Model

Keep these concepts separate:

1. **Observation** — what was actually found.
2. **Org Evidence** — traceable support for the observation.
3. **Salesforce Guidance** — applicable external authority, when required.
4. **Gap / Alignment** — how the org differs from or aligns with that guidance.
5. **Risk / Impact** — org-specific consequence.
6. **Recommendation** — proportionate remediation or next action.

Do not collapse evidence, guidance, risk, and recommendation into one unsupported statement.

## Salesforce Guidance Validation

A finding described as a Salesforce best-practice issue requires:

```text
Org Evidence
    +
Applicable Current Official Salesforce Guidance
    +
Org-Specific Gap / Risk
    =
Validated Salesforce Best-Practice Finding
```

Use these guidance-basis labels:

- `Verified — Official Salesforce`
- `Verified — Organisation Standard`
- `Requires Guidance Verification`
- `Design Recommendation — Not a Salesforce Requirement`

If official guidance cannot be verified:
- do not say Salesforce recommends or requires the pattern;
- do not present it as a confirmed Salesforce best-practice violation.

Project conventions in the current project's `CLAUDE.md`, `.claude/rules/`, or project documentation may support an organisation-standard finding, but they are not automatically Salesforce requirements.

## Official Source Policy

For Salesforce best-practice validation, prioritise current official sources:

1. `architect.salesforce.com`
2. `developer.salesforce.com`
3. `help.salesforce.com`
4. `trust.salesforce.com` when directly relevant

Prefer:
- Salesforce Well-Architected for architecture principles and patterns;
- Architect Decision Guides for design trade-offs;
- Developer Guides for coding/platform behaviour;
- Salesforce Help for product/configuration behaviour;
- current Release Notes and Limits documentation for version-sensitive behaviour.

Do not use forums, consultancy blogs, Stack Exchange, Reddit, search snippets, or model memory as authority for a confirmed Salesforce best-practice finding when applicable official guidance is available.

Research only topics that survive evidence triage. Reuse authoritative sources where they genuinely apply and avoid repeatedly fetching the same page.

## Important Assessment Safeguards

Do not apply simplistic rules such as:

- Flow is always preferable to Apex.
- Aura's existence is automatically technical debt.
- `without sharing` alone proves a security defect.
- system-mode execution alone proves a security defect.
- metadata is unused because no reference was found in one checkout.
- scanner severity equals Health Check severity.

Native Salesforce Security Health Check:
- preserve Salesforce's reported score when supplied;
- preserve the baseline type;
- do not invent or recompute Salesforce's scoring formula;
- do not extrapolate that score to unrelated Health Check domains.

Do not invent a numeric Salesforce Well-Architected score.

## Canonical JSON

Before producing the final JSON, read:

- `${CLAUDE_PLUGIN_ROOT}/skills/salesforce-health-check/schema/health-check.schema.json`
- `${CLAUDE_PLUGIN_ROOT}/skills/salesforce-health-check/templates/report-structure.md`

Create, in the current project (not in this plugin):

```text
health-check/health-check-report.json
```

The JSON contains only final assessment data.

Do not store redundant computed totals when they can be derived from `findings`.

Use stable finding IDs such as:

```text
HC-SEC-001
HC-AUT-002
HC-APX-003
```

The JSON should preserve enough traceability to support later remediation without requiring the Word report to be parsed.

## JSON Validation

Run:

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/salesforce-health-check/scripts/validate-report.py \
  health-check/health-check-report.json
```

Do not generate the DOCX if validation fails.

Fix the JSON first.

## DOCX Generation

Generate:

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/salesforce-health-check/scripts/generate-docx.py \
  health-check/health-check-report.json \
  --template ${CLAUDE_PLUGIN_ROOT}/skills/salesforce-health-check/templates/health-check-template.docx \
  --output health-check/Salesforce-Health-Check.docx
```

The generator may derive:
- severity totals;
- category totals;
- snapshot tables;
- roadmap grouping;
- finding registers;
- source lists.

The generator must not perform new Salesforce analysis.

## Report Structure

Use `${CLAUDE_PLUGIN_ROOT}/skills/salesforce-health-check/templates/report-structure.md`.

The report should be executive-first:

1. Executive Summary
2. Assessment Overview
3. Org Health Snapshot
4. Key Risks & Findings
5. Detailed Assessment
6. Remediation Roadmap
7. Positive Findings
8. Selected Component Deep Dives, when useful
9. Assessment Limitations
10. Appendices

Keep detailed inventory primarily in appendices.

Generate component deep dives selectively for architecturally important or materially risky components; do not document every Flow, Apex class, object, or integration at that level.

## Final Quality Gate

Before delivery, confirm:

- assessment target and evidence date are clear;
- every actionable finding has traceable org evidence;
- every Critical/High/Medium item presented as Salesforce best practice has applicable verified official guidance;
- project conventions are not misrepresented as Salesforce requirements;
- unsupported candidates were excluded or clearly labelled;
- duplicate/root-cause-equivalent findings are consolidated;
- severity reflects org-specific impact rather than scanner severity alone;
- limitations and unassessed areas are explicit;
- no invented scores, metrics, usage, or runtime behaviour exist;
- JSON validates against the schema and quality checks;
- report counts are derived from the canonical findings;
- DOCX content matches the JSON;
- no secrets, credentials, session IDs, private keys, or unnecessary customer data are exposed.

## Document QA

Render and visually inspect the generated DOCX before delivery using the available project/document rendering workflow.

Check every page for:
- clipped or overlapping text;
- broken tables;
- bad page breaks;
- orphaned finding headings;
- inconsistent widths/spacing;
- unreadable URLs;
- header/footer problems;
- visible placeholders.

Fix the generator/template or JSON as appropriate, regenerate, and repeat QA until clean.

## Token Efficiency

Unless the user explicitly requests exhaustive analysis:

- inspect likely evidence locations before broad repository traversal;
- use targeted search before reading large files;
- avoid loading the same evidence repeatedly;
- research only surviving candidate topics;
- prefer one strong applicable official source over several generic sources;
- consolidate systemic occurrences;
- keep raw scanner output and verbose research out of the final report;
- use subagents only when delegation is expected to reduce context pressure or improve execution quality.

## Implementation Handoff

If the user later requests remediation:

1. Exit Assessment Mode.
2. Enter Implementation Mode.
3. Retrieve/revalidate the latest affected metadata.
4. Confirm the original finding still applies.
5. Follow the project's implementation rules.
6. Do not deploy unless explicitly requested.

Assessment evidence may be stale by the time remediation begins.
