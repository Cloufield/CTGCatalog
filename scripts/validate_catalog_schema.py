#!/usr/bin/env python3
"""
Validate all catalog JSON files under json/ against .design/catalog-entry.schema.json.

Usage (from repository root):
  pip install -r requirements-dev.txt
  python3 scripts/validate_catalog_schema.py

Same logic as the check run at the start of src/main.py. Exit code 0 if all pass, 1 otherwise.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from validate_catalog import (  # noqa: E402
    DEFAULT_JSON_ROOT,
    DEFAULT_SCHEMA,
    validate_catalog,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA,
        help=f"path to JSON Schema (default: {DEFAULT_SCHEMA})",
    )
    parser.add_argument(
        "--json-dir",
        type=Path,
        default=DEFAULT_JSON_ROOT,
        help=f"root directory of catalog JSON (default: {DEFAULT_JSON_ROOT})",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="print only errors"
    )
    args = parser.parse_args()
    return validate_catalog(
        schema_path=args.schema,
        json_root=args.json_dir,
        quiet=args.quiet,
    )


if __name__ == "__main__":
    raise SystemExit(main())
