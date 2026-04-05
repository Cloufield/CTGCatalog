"""Validate json/ against .design/catalog-entry.schema.json (used by main.py and CLI)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from catalog_sources import is_catalog_json_file

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCHEMA = REPO_ROOT / ".design" / "catalog-entry.schema.json"
DEFAULT_JSON_ROOT = REPO_ROOT / "json"


def validate_catalog(
    schema_path: Path | None = None,
    json_root: Path | None = None,
    *,
    quiet: bool = False,
) -> int:
    """
    Return 0 if every catalog JSON file validates, 1 on failure or missing jsonschema.
    """
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        print(
            "Missing dependency: jsonschema (required for catalog schema check)\n"
            "  pip install -r requirements-dev.txt",
            file=sys.stderr,
        )
        return 1

    schema_path = (schema_path or DEFAULT_SCHEMA).resolve()
    json_root = (json_root or DEFAULT_JSON_ROOT).resolve()

    if not schema_path.is_file():
        print(f"Schema not found: {schema_path}", file=sys.stderr)
        return 1
    if not json_root.is_dir():
        print(f"JSON root not found: {json_root}", file=sys.stderr)
        return 1

    with open(schema_path, encoding="utf-8") as f:
        schema = json.load(f)

    try:
        Draft202012Validator.check_schema(schema)
    except Exception as e:
        print(f"Invalid schema file {schema_path}: {e}", file=sys.stderr)
        return 1

    validator = Draft202012Validator(schema)
    paths = sorted(
        p for p in json_root.rglob("*.json") if is_catalog_json_file(json_root, p)
    )

    if not paths:
        print(f"No .json files under {json_root}", file=sys.stderr)
        return 1

    errors: list[tuple[Path, str]] = []
    for path in paths:
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            errors.append((path, f"invalid JSON: {e}"))
            continue
        if not isinstance(data, dict):
            errors.append((path, f"root must be object, got {type(data).__name__}"))
            continue
        errs = sorted(validator.iter_errors(data), key=lambda e: e.path)
        for err in errs:
            loc = ".".join(str(p) for p in err.path) if err.path else "(root)"
            errors.append((path, f"{loc}: {err.message}"))

    if not quiet:
        print(f"Schema check: {len(paths)} file(s) under {json_root.relative_to(REPO_ROOT)}/")

    if errors:
        print(f"\n{len(errors)} schema error(s):\n", file=sys.stderr)
        for path, msg in errors:
            try:
                rel = path.relative_to(REPO_ROOT)
            except ValueError:
                rel = path
            print(f"  {rel}: {msg}", file=sys.stderr)
        return 1

    if not quiet:
        print("Schema check: OK.")
    return 0
