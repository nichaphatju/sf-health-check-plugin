# Salesforce Health Check — Claude Code Plugin

Private marketplace + plugin bundling the Salesforce Org Health Check workflow so it can be installed into any Salesforce DX project, instead of being copy-pasted per repo.

## What's bundled

Plugin `sf-health-check` (`plugins/sf-health-check/`):

- **Skills**
  - `salesforce-health-check` — evidence-based assessment, schema-valid JSON, DOCX report generation.
  - `health-check-to-confluence` — publishes the canonical JSON to Confluence without re-running the assessment.
- **Agents**
  - `salesforce-org-evidence-analyst` — read-only evidence gathering from project metadata/artifacts.
  - `salesforce-guidance-validator` — validates candidate findings against official Salesforce documentation.

## What is NOT bundled (stays per-project)

- `CLAUDE.md` operating-mode instructions (Assessment Mode / Implementation Mode) — these are project policy, not plugin logic. Copy the relevant section from an existing project's `CLAUDE.md` into any new project.
- `.claude/rules/*` — project implementation conventions.
- `.mcp.json` Salesforce DX MCP server entry — add per project so Claude Code has org/metadata/data access:

  ```json
  {
    "mcpServers": {
      "Salesforce DX": {
        "command": "npx",
        "args": ["-y", "@salesforce/mcp", "--orgs", "DEFAULT_TARGET_ORG",
          "--toolsets", "orgs,metadata,data,users,code-analysis,experts-validation",
          "--tools", "run_apex_test,retrieve_metadata", "--allow-non-ga-tools"]
      }
    }
  }
  ```
- Confluence/Atlassian MCP access — configured at the user level, not per project.

## Prerequisites

- Python 3.9+ with `python-docx` installed for DOCX generation:

  ```bash
  pip install python-docx
  ```

## Installing into a project

This is a **private** repo — installers need git access to it (SSH key or HTTPS credentials with read access).

```
/plugin marketplace add <owner>/sf-health-check-plugin
/plugin install sf-health-check@sf-health-check-marketplace
```

(or the full URL form: `/plugin marketplace add https://github.com/<owner>/sf-health-check-plugin.git`)

## Updating

Edit the skill/agent files under `plugins/sf-health-check/`, bump `version` in both `plugin.json` and `marketplace.json`, commit, and push. Installed projects pick up the update the next time they refresh the marketplace (`/plugin marketplace update` or reinstall).

## Output location

Both skills read/write `health-check/health-check-report.json` and `health-check/Salesforce-Health-Check.docx` **inside the project being assessed** — never inside this plugin's own directory.
