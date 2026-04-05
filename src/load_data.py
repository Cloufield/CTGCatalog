import json
import pandas as pd
from pathlib import Path

from catalog_sources import is_catalog_json_file, normalize_folder_field, repo_json_dir

# Populated from PubMed via ``sync_json_bibliography.py`` (or manually in JSON).
BIBLIO_COLUMNS = [
    "TITLE",
    "ISO",
    "JOURNAL",
    "YEAR",
    "VOLUME",
    "ISSUE",
    "PAGE",
    "Authors",
    "ABSTRACT",
    "DOI",
    "PMC ID",
    "CITATION",
    "FIRST_AUTHOR",
]


def _ensure_biblio_columns(df: pd.DataFrame) -> pd.DataFrame:
    for col in BIBLIO_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA
    return df


def _fill_biblio_derivatives(df: pd.DataFrame) -> pd.DataFrame:
    df = _ensure_biblio_columns(df)
    has_auth = df["Authors"].notna() & (df["Authors"].astype(str).str.strip() != "")
    need_fa = has_auth & (
        df["FIRST_AUTHOR"].isna()
        | (df["FIRST_AUTHOR"].astype(str).str.strip() == "")
    )
    if need_fa.any():
        df.loc[need_fa, "FIRST_AUTHOR"] = (
            df.loc[need_fa, "Authors"].astype(str).str.split(",").str[0].str.strip()
        )
    # Do not synthesize CITATION from PMID + Authors + TITLE here; use explicit JSON
    # CITATION (e.g. from sync_json_bibliography) or MANUAL_CITATION via format_table.
    return df


def _load_json_catalog(json_dir: Path) -> pd.DataFrame:
    rows = []
    for path in sorted(json_dir.rglob("*.json")):
        if not is_catalog_json_file(json_dir, path):
            continue
        with open(path, encoding="utf-8") as f:
            rec = json.load(f)
        meta = rec.pop("_meta", None) or {}
        if "source_sheet" in meta:
            rec["FIELD"] = meta["source_sheet"]
        rows.append(rec)
    if not rows:
        raise FileNotFoundError(
            f"No catalog JSON files found under {json_dir}. "
            "Add UTF-8 .json entries under json/ (see .design/SCHEMA.md)."
        )
    return pd.DataFrame(rows)


def load_table_and_ref():
    json_dir = repo_json_dir()
    print(f"Loading catalog from JSON: {json_dir}")
    pop = _load_json_catalog(json_dir)

    for col in ["SECTION", "TOPIC", "SUBTOPIC"]:
        if col not in pop.columns:
            pop[col] = ""
        else:
            pop[col] = pop[col].fillna("")

    if "PMID" not in pop.columns:
        pop["PMID"] = pd.NA
    # JSON numbers become float in DataFrame; astype("string") yields "26773131.0".
    # Coerce to int digit string for consistent PMID keys and citations.
    pm = pd.to_numeric(pop["PMID"], errors="coerce")
    pop["PMID"] = pm.map(lambda x: pd.NA if pd.isna(x) else str(int(x)))
    pop["PMID"] = pop["PMID"].astype("string")

    pop_pmid = _fill_biblio_derivatives(pop)

    # When PubMed-derived YEAR is absent, use MANUAL_YEAR (e.g. preprint-only MANUAL_CITATION).
    if "MANUAL_YEAR" in pop_pmid.columns:

        def _manual_year_to_str(v):
            if v is None or (isinstance(v, float) and pd.isna(v)):
                return pd.NA
            if isinstance(v, bool):
                return pd.NA
            if isinstance(v, (int, float)):
                try:
                    return str(int(v))
                except (TypeError, ValueError):
                    pass
            s = str(v).strip()
            return s if s else pd.NA

        my = pop_pmid["MANUAL_YEAR"].map(_manual_year_to_str)
        if "YEAR" not in pop_pmid.columns:
            pop_pmid["YEAR"] = pd.NA
        y_blank = pop_pmid["YEAR"].isna() | (
            pop_pmid["YEAR"].astype(str).str.strip() == ""
        )
        pop_pmid.loc[y_blank & my.notna(), "YEAR"] = my.loc[y_blank & my.notna()]

    has_pmid = pop_pmid["PMID"].notna() & (pop_pmid["PMID"].astype(str).str.strip() != "")
    if "MANUAL_CITATION" in pop_pmid.columns:
        has_manual = pop_pmid["MANUAL_CITATION"].notna() & (
            pop_pmid["MANUAL_CITATION"].astype(str).str.strip() != ""
        )
    else:
        has_manual = pd.Series(False, index=pop_pmid.index)
    has_biblio = pop_pmid["Authors"].notna() & (
        pop_pmid["Authors"].astype(str).str.strip() != ""
    )
    missing = pop_pmid.loc[has_pmid & ~has_manual & ~has_biblio, "PMID"]
    missing.dropna().drop_duplicates().to_csv(
        "../not_in_lib.pmidlist", index=None, header=None
    )

    for i in ["SECTION", "TOPIC", "SUBTOPIC"]:
        pop_pmid[i] = normalize_folder_field(pop_pmid[i])

    return pop_pmid


def load_biobanks():
    json_dir = repo_json_dir() / "biobanks"
    if not json_dir.is_dir():
        return pd.DataFrame()
    rows = []
    for path in sorted(json_dir.rglob("*.json")):
        with open(path, encoding="utf-8") as f:
            rec = json.load(f)
        rec.pop("_meta", None)
        rows.append(rec)
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    for col in ["SECTION", "TOPIC", "SUBTOPIC"]:
        if col in df.columns:
            df[col] = normalize_folder_field(df[col].fillna(""))
    return df
