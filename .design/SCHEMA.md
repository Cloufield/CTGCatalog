# Catalog JSON schema

One UTF-8 **object per file** under `json/`. The build loads every `*.json` recursively (no manifest). See also [DESIGN.md](./DESIGN.md).

**On this page:** [Quick reference](#quick-reference) · [Example](#minimal-example) · [Routing](#routing) · [Pipeline quirks](#pipeline-quirks) · [Field catalog](#field-catalog) · [JSON Schema file](#json-schema-file)

---

## Quick reference

| Item | Rule |
|------|------|
| **Required** | `NAME`, `SECTION`, `TOPIC` (non-empty strings) |
| **Optional nav** | `SUBTOPIC` — omit or `""` for two-level paths |
| **Provenance** | `_meta.source_sheet` → becomes column `FIELD` (sumstats stats, traceability) |
| **Schema style** | Open: extra keys are allowed; values are usually strings or numbers |
| **Citations** | **Display** uses explicit `CITATION` in JSON (from `sync_json_bibliography.py` or hand). No auto-generated cite string at load. `MANUAL_YEAR` can still set `YEAR` when missing. |
| **Site tags** | `TAGS` (preferred) or `TAG` → MkDocs Material `tags` + entry card badges (`process_md` / `print_level`) |

## Minimal example

```json
{
  "NAME": "Example tool",
  "SECTION": "Tools",
  "TOPIC": "Visualization",
  "SUBTOPIC": "GWAS",
  "TYPE": "R package",
  "URL": "https://example.org",
  "DESCRIPTION": "One-line summary.",
  "TAGS": ["GWAS", "Visualization"],
  "PMID": 12345678,
  "_meta": {
    "source_sheet": "Tools"
  }
}
```

## Routing

These control **MkDocs nav** and the generated page path (`process_md.add_path()`):

`docs/{SECTION}_{TOPIC}_{SUBTOPIC}.md` — empty segments dropped (e.g. `docs/Tools_Visualization.md` when `SUBTOPIC` is absent).

`SECTION` / `TOPIC` / `SUBTOPIC` are normalized at load time (spaces and hyphens → underscores) in `load_data.py`.

| Field | Role |
|-------|------|
| `SECTION` | Top tab (MkDocs label may differ): `Biobanks`, `Sumstats`, `Tools` (nav **GWAS Tools**), `Coding`, `References`, `Single_Cell`, `Projects`, `AI`; `Tools`+`Population_Genetics` → **Population Genetics** tab; `Journals` is home-linked only |
| `TOPIC` | Second level (e.g. biobank region `EUROPE`) |
| `SUBTOPIC` | Third level when needed |

## `_meta`

| Key | Use |
|-----|-----|
| `source_sheet` | String label stored as `FIELD`. Must match an entry in `HOMEPAGE_SUMSTATS_SHEETS` (in `catalog_sources.py`) if the row should count toward the Sumstats block on `Catalog_statistics.md`. |

## Pipeline quirks

- **Missing keys** — absent properties are not written; the DataFrame gets sparse columns.
- **`PMID`** — often a JSON number; loader coerces to string digits; bibliography fields are read from the same JSON object.
- **Display flags** — `ADD_PREFIX`, `ADD_SUFFIX`, `USE_FIRST_AUTHOR`: use integer `0`/`1`; `format_table` normalizes for name building.
- **`SAMPLE_SIZE` vs `SAMPLE SIZE`** — underscore key tends to be numeric; spaced key tends to be human text (e.g. `~500k`).

## Field catalog

Open schema: **any** top-level string/number field may appear. The groups below describe fields commonly present in the current tree (~920 catalog JSON files under `json/`, excluding `json/tags/`); they are documentation only, not validation.

*Routing fields are listed in [Routing](#routing) only.*

### Bibliography & naming

| Field | Typical type | Notes |
|-------|--------------|--------|
| `SHORT NAME` | string | Card title / abbreviation |
| `FULL NAME` | string | Longer label |
| `PMID` | number | With PubMed-derived keys in the same JSON → `CITATION`, `TITLE`, `Authors`, … (from `sync_json_bibliography.py`) |
| `CITATION` | string | **Main citation** text on the site. Must be present in JSON (sync or hand); the loader does not build it from PMID + authors + title. |
| `MANUAL_CITATION` | string | Optional note; not copied into the displayed citation. Prefer `CITATION` for what readers should see. |
| `MANUAL_YEAR` | number | Year when not from CSV |
| `PREPRINT_DOI`, `PREPRINT_SERVER` | string | |
| `DOI` | string | Rare in JSON; often from merge |

### Classification & discovery

| Field | Typical type | Notes |
|-------|--------------|--------|
| `TYPE` | string | Hub counts, display name rules |
| `CATEGORY` | string | Summary tables; blank → `MISC` |
| `KEYWORDS`, `USE` | string | |
| `TAGS` | string or list | **Preferred** for site tags: MkDocs page `tags`, card badges. JSON array of strings, or one string with `;`-separated values |
| `TAG` | string | Single tag or `;`-separated list (same parsing as `TAGS`) |
| `BADGES` | string or list | Legacy alias for tags (same behavior as `TAGS` if `TAG` / `TAGS` absent) |
| `BADGE` | string | Legacy single-tag alias |

### Content & links

| Field | Typical type | Notes |
|-------|--------------|--------|
| `DESCRIPTION` | string | |
| `URL` | string | Multiple URLs: whitespace-separated → markdown links |
| `SERVER`, `SOURCE`, `NOTE` | string | |
| `DATA_REQUIRED`, `DATA ACCESS`, `FILE` | string | |
| `ARROW_SUMMARY` | string | |
| `AI_GENERATED`, `LAST_CHECK` | number | Flags / metadata |

### Sumstats / cohort-style

| Field | Typical type | Notes |
|-------|--------------|--------|
| `MAIN_ANCESTRY`, `ANCESTRY` | string | |
| `TRAIT`, `COHORT`, `PLATFORM` | string | |
| `SAMPLE_SIZE` | number or string | |
| `RELATED_BIOBANK` | string | Comma-separated; linked via `json/biobanks` |
| `ARRAY`, `WGS/WES`, `TRANSCRIPTOME`, `METABOLOME`, `PROTEOME`, `METHYLOME`, `METAGENOME` | string | Coverage text |
| `IMAGAING` | string | Legacy spelling of “imaging” |
| `STUDY TYPE` | string | |

### Projects (`json/projects/<project>/`)

Large programs are split by **page** (`SECTION` + `TOPIC` = one Markdown file) and by **card** (one JSON file per phase/stage).

| Field | Typical type | Notes |
|-------|--------------|--------|
| `TOPIC` | string | Project name; normalized to path segment (e.g. `1000 Genomes` → `Projects_1000_Genomes.md`) |
| `STAGE_ORDER` | number | Sort key for cards and summary table on that page |
| `STAGE_PERIOD` | string | Human-readable era (e.g. `2012–2015`, `ongoing`) |
| `DESCRIPTION` | string | Body text for that phase |

### Biobanks

| Field | Typical type | Notes |
|-------|--------------|--------|
| `CONTINENT` | string | `Catalog_statistics.md` biobank counts |
| `REGION` | string | |
| `SAMPLE SIZE` | string | Human-readable size (≠ `SAMPLE_SIZE`) |
| `PARTICIPANTS` | string | Short prose on who was enrolled (see also `catalog-entry.schema.json` description) |

### Name overrides (display)

| Field | Type | Effect when `1` |
|-------|------|------------------|
| `ADD_PREFIX` | number | Prefix `NAME` with `TYPE` |
| `ADD_SUFFIX` | number | Suffix with `PMID` |
| `USE_FIRST_AUTHOR` | number | Use merged `FIRST_AUTHOR` as display name |

**Often from PubMed sync:** `TITLE`, `CITATION`, `JOURNAL`, `Authors`, `FIRST_AUTHOR`, … may be written into JSON by `src/sync_json_bibliography.py`.

## JSON Schema file

For editors and validators, a draft-2020-12 fragment lives in [`catalog-entry.schema.json`](./catalog-entry.schema.json). It enforces `NAME` / `SECTION` / `TOPIC` and documents common keys; **`additionalProperties: true`** keeps the catalog extensible. The build does **not** run this schema—it only loads JSON into pandas.

### Validate from the CLI

The same check runs automatically at the start of **`python main.py`** (from `src/`). To run it alone:

```bash
pip install -r requirements-dev.txt
python3 scripts/validate_catalog_schema.py
```

Options: `--schema PATH`, `--json-dir PATH`, `-q` / `--quiet` (errors only). Exit code **1** if any file fails or dependencies are missing.

## Related code

| Module | Responsibility |
|--------|------------------|
| `src/validate_catalog.py` | Schema validation (`validate_catalog`), used by `main.py` |
| `src/load_data.py` | `_load_json_catalog`, `load_biobanks`, PMID coercion |
| `src/catalog_sources.py` | `repo_json_dir`, `slugify_segment`, `HOMEPAGE_SUMSTATS_SHEETS`, tag slug helpers |
| `src/format_table.py` | URLs, citations, name flags, related biobanks |
| `src/process_md.py` | Output path, page-level `tags` front matter from `_badges_for_row` |
| `src/print_level.py` | `TAG` / `TAGS` → MkDocs tags + card badges (`_badges_for_row`); optional `TAG_SLUG_MAP` for badge links |
| `src/tag_pages.py` | Per-tag listing pages under `docs/tags/`, shared bucket data for `write_mkdcos` |

### Refreshing the field inventory

Key frequencies drift as entries change. To list top-level keys and counts:

```bash
python3 -c "
import json
from pathlib import Path
from collections import Counter
c = Counter()
for p in Path('json').rglob('*.json'):
    with open(p, encoding='utf-8') as f:
        c.update(json.load(f).keys())
for k, n in c.most_common():
    print(f'{n:4d}  {k}')
"
```

Run from the **repository root**.
