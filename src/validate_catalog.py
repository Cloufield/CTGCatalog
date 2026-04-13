"""Validate json/ against .design/catalog-entry.schema.json (used by main.py and CLI)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from catalog_sources import is_catalog_json_file, repo_databases_dir

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCHEMA = REPO_ROOT / ".design" / "catalog-entry.schema.json"
DATABASE_SCHEMA = REPO_ROOT / ".design" / "database-entry.schema.json"
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


def validate_databases_json(
    schema_path: Path | None = None,
    databases_root: Path | None = None,
    *,
    quiet: bool = False,
) -> int:
    """Validate ``json/databases/<country>/*.json`` against database-entry.schema.json."""
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        print(
            "Missing dependency: jsonschema (required for database schema check)\n"
            "  pip install -r requirements-dev.txt",
            file=sys.stderr,
        )
        return 1

    schema_path = (schema_path or DATABASE_SCHEMA).resolve()
    databases_root = (databases_root or repo_databases_dir()).resolve()

    if not databases_root.is_dir():
        if not quiet:
            print("Schema check (databases): skipped (no json/databases/).")
        return 0

    if not schema_path.is_file():
        print(f"Database schema not found: {schema_path}", file=sys.stderr)
        return 1

    with open(schema_path, encoding="utf-8") as f:
        schema = json.load(f)

    try:
        Draft202012Validator.check_schema(schema)
    except Exception as e:
        print(f"Invalid database schema file {schema_path}: {e}", file=sys.stderr)
        return 1

    validator = Draft202012Validator(schema)
    paths = sorted(p for p in databases_root.rglob("*.json") if p.is_file())
    if not paths:
        if not quiet:
            print("Schema check (databases): 0 file(s) (OK).")
        return 0

    errors: list[tuple[Path, str]] = []
    for path in paths:
        try:
            rel = path.relative_to(databases_root)
        except ValueError:
            errors.append((path, "path must be under databases root"))
            continue
        if len(rel.parts) < 2:
            errors.append(
                (path, "expected json/databases/<country>/<file>.json (missing country folder)")
            )
            continue
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            errors.append((path, f"invalid JSON: {e}"))
            continue
        if not isinstance(data, dict):
            errors.append((path, f"root must be object, got {type(data).__name__}"))
            continue
        desc = data.get("DESCRIPTION", "")
        if isinstance(desc, str) and "|" in desc:
            errors.append(
                (path, "DESCRIPTION must not contain '|' (breaks Markdown tables); use a comma or rephrase")
            )
        name_zh = data.get("NAME_ZH", "")
        if isinstance(name_zh, str) and "|" in name_zh:
            errors.append(
                (path, "NAME_ZH must not contain '|' (breaks Markdown tables); use a comma or rephrase")
            )
        kdb = data.get("KEY_DATABASES")
        if kdb is not None:
            if not isinstance(kdb, list):
                errors.append((path, "KEY_DATABASES must be an array"))
            else:
                for i, item in enumerate(kdb):
                    if not isinstance(item, dict):
                        errors.append((path, f"KEY_DATABASES[{i}] must be an object"))
                        continue
                    for fld in ("NAME", "NAME_ZH", "URL", "DESCRIPTION"):
                        v = item.get(fld, "")
                        if isinstance(v, str) and "|" in v:
                            errors.append(
                                (
                                    path,
                                    f"KEY_DATABASES[{i}].{fld} must not contain '|' (breaks Markdown tables)",
                                )
                            )
        errs = sorted(validator.iter_errors(data), key=lambda e: e.path)
        for err in errs:
            loc = ".".join(str(p) for p in err.path) if err.path else "(root)"
            errors.append((path, f"{loc}: {err.message}"))

    if not quiet:
        print(f"Schema check (databases): {len(paths)} file(s) under json/databases/")

    if errors:
        print(f"\n{len(errors)} database schema error(s):\n", file=sys.stderr)
        for path, msg in errors:
            try:
                rel = path.relative_to(REPO_ROOT)
            except ValueError:
                rel = path
            print(f"  {rel}: {msg}", file=sys.stderr)
        return 1

    if not quiet:
        print("Schema check (databases): OK.")
    return 0
