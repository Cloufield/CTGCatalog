#!/usr/bin/env python3
"""Regenerate src/templates/biobanks_world_map.html from Natural Earth 110m countries.

Downloads GeoJSON to a temp file if needed. Run from repo root:
  python3 scripts/generate_biobanks_map.py
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request

W, H = 800, 400
NE_URL = (
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
    "master/geojson/ne_110m_admin_0_countries.geojson"
)


def project(lon: float, lat: float) -> tuple[float, float]:
    return (lon + 180) / 360 * W, (90 - lat) / 180 * H


def ring_to_d(ring: list) -> str:
    pts = [project(lon, lat) for lon, lat in ring]
    if not pts:
        return ""
    d = f"M {pts[0][0]:.1f},{pts[0][1]:.1f}"
    for x, y in pts[1:]:
        d += f" L {x:.1f},{y:.1f}"
    d += " Z"
    return d


def geom_to_path_strings(geom: dict) -> list[str]:
    out: list[str] = []
    t = geom["type"]
    if t == "Polygon":
        rings = geom["coordinates"]
        if rings:
            out.append(" ".join(ring_to_d(r) for r in rings))
    elif t == "MultiPolygon":
        for poly in geom["coordinates"]:
            if poly:
                out.append(" ".join(ring_to_d(r) for r in poly))
    return out


def main() -> int:
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_path = os.path.join(root, "src", "templates", "biobanks_world_map.html")

    cache = os.path.join(root, ".cache", "natural-earth")
    os.makedirs(cache, exist_ok=True)
    geo_path = os.path.join(cache, "ne_110m_admin_0_countries.geojson")
    if not os.path.isfile(geo_path):
        print("Downloading", NE_URL, file=sys.stderr)
        urllib.request.urlretrieve(NE_URL, geo_path)

    with open(geo_path, encoding="utf-8") as f:
        fc = json.load(f)

    groups = {k: [] for k in ("AFRICA", "AMERICA", "ASIA", "EUROPE", "OCEANIA")}
    for feat in fc["features"]:
        cont = feat["properties"].get("CONTINENT")
        if cont in ("Antarctica", "Seven seas (open ocean)", None):
            continue
        if cont in ("North America", "South America"):
            key = "AMERICA"
        elif cont.upper() in groups:
            key = cont.upper()
        else:
            continue
        groups[key].extend(geom_to_path_strings(feat["geometry"]))

    hrefs = {
        "AFRICA": "../Biobanks_AFRICA/",
        "AMERICA": "../Biobanks_AMERICA/",
        "ASIA": "../Biobanks_ASIA/",
        "EUROPE": "../Biobanks_EUROPE/",
        "OCEANIA": "../Biobanks_OCEANIA/",
    }
    labels = {
        "AFRICA": "Africa",
        "AMERICA": "America",
        "ASIA": "Asia",
        "EUROPE": "Europe",
        "OCEANIA": "Oceania",
    }
    label_xy = {
        "AMERICA": (200.0, 168.0),
        "OCEANIA": (698.0, 258.0),
        "AFRICA": (437.0, 197.0),
        "ASIA": (592.0, 142.0),
        "EUROPE": (428.0, 88.0),
    }
    order = ["AMERICA", "OCEANIA", "AFRICA", "ASIA", "EUROPE"]

    lines = [
        '<div class="biobanks-world-map" id="biobanks-world-map" role="navigation" aria-label="Biobanks by continent">',
        '<p class="biobanks-world-map-hint">Click a continent to open its biobank list.</p>',
        '<p class="biobanks-world-map-note">Continent zones on this map are a <strong>loose navigational grouping</strong> (often by study geography), not strict geography. <strong>MAIN ANCESTRY</strong> usually uses <strong>1000 Genomes super-population codes</strong> (AFR, AMR, EAS, EUR, SAS) when they fit; otherwise it uses a short accurate label. See <strong>PARTICIPANTS</strong>, <strong>MAIN ANCESTRY</strong>, and <strong>CONTINENT</strong> in the summary table and entry cards.</p>',
        '<div class="biobanks-world-map-frame">',
        '<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" role="img" aria-label="World map by continent">',
        '<rect class="biobanks-world-map-ocean" width="800" height="400" rx="12"/>',
    ]

    for key in order:
        href = hrefs[key]
        cls = f"biobanks-world-map-land biobanks-world-map-{key.lower()}"
        lines.append(
            f'<a class="biobanks-world-map-hit" xlink:href="{href}" href="{href}">'
        )
        lines.append(f"<title>{labels[key]}</title>")
        for d in groups[key]:
            lines.append(
                f'<path class="{cls}" fill-rule="evenodd" d="{d}"/>'
            )
        lines.append("</a>")

    lines.append('<g class="biobanks-world-map-labels" pointer-events="none" fill="currentColor">')
    for key in order:
        x, y = label_xy[key]
        lines.append(
            f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" class="biobanks-world-map-label">{labels[key]}</text>'
        )
    lines.append("</g>")
    lines.append("</svg>")
    lines.append("</div>")
    lines.append(
        '<p class="biobanks-world-map-credit">Geography: <a href="https://www.naturalearthdata.com/">Natural Earth</a> (public domain), 110m countries.</p>'
    )
    lines.append("</div>")
    lines.append("")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("Wrote", out_path, os.path.getsize(out_path), "bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
