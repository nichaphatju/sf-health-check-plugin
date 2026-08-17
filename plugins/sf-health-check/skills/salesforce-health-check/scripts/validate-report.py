#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("report")
    parser.add_argument("--schema", default=None)
    args = parser.parse_args()

    report_path = Path(args.report)
    schema_path = Path(args.schema) if args.schema else Path(__file__).resolve().parent.parent / "schema" / "health-check.schema.json"

    report = json.loads(report_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    errors = sorted(Draft202012Validator(schema).iter_errors(report), key=lambda e: list(e.path))
    if errors:
        print(f"INVALID: {len(errors)} schema error(s)")
        for err in errors:
            loc = ".".join(str(p) for p in err.path) or "<root>"
            print(f"- {loc}: {err.message}")
        sys.exit(1)

    ids = [f["id"] for f in report.get("findings", [])]
    duplicates = sorted({x for x in ids if ids.count(x) > 1})
    if duplicates:
        print("INVALID: duplicate finding IDs: " + ", ".join(duplicates))
        sys.exit(1)

    source_ids = {s["id"] for s in report.get("salesforceSources", [])}
    evidence_ids = {s["id"] for s in report.get("evidenceSources", [])}

    failures = []
    for f in report.get("findings", []):
        if f["severity"] in {"Critical", "High", "Medium"} and f["guidanceBasis"] == "Verified — Official Salesforce":
            guidance = f.get("guidance") or {}
            refs = guidance.get("sourceIds") or []
            if not refs:
                failures.append(f'{f["id"]}: verified official finding has no Salesforce source reference')
            for ref in refs:
                if ref not in source_ids:
                    failures.append(f'{f["id"]}: unknown Salesforce source ID {ref}')
        for ev in f.get("evidence", []):
            sid = ev.get("sourceId")
            if sid and sid not in evidence_ids:
                failures.append(f'{f["id"]}: unknown evidence source ID {sid}')

    if failures:
        print("INVALID: quality-gate error(s)")
        for failure in failures:
            print("- " + failure)
        sys.exit(1)

    print(f"VALID: {report_path}")
    print(f"Findings: {len(ids)}")
    print(f"Salesforce sources: {len(source_ids)}")
    print(f"Evidence sources: {len(evidence_ids)}")

if __name__ == "__main__":
    main()
