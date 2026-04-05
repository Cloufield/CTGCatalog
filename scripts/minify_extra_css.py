#!/usr/bin/env python3
"""Minify docs/stylesheets/extra.css -> docs/stylesheets/extra.min.css (requires rcssmin)."""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import rcssmin
except ImportError:
    print("Install rcssmin: pip install rcssmin", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "docs" / "stylesheets" / "extra.css"
dst = ROOT / "docs" / "stylesheets" / "extra.min.css"
if not src.is_file():
    print(f"Missing {src}", file=sys.stderr)
    sys.exit(1)
css = src.read_text(encoding="utf-8")
out = rcssmin.cssmin(css)
dst.write_text(out, encoding="utf-8")
print(f"Wrote {dst} ({len(css)} -> {len(out)} bytes)")
