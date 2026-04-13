"""
Regenerates section hub pages (docs/<Section>.md with “Contents - …” lists) and
overwrites repo-root mkdocs.yml from ``PART1_BASE`` + dynamic ``not_in_nav`` + a dynamic ``nav`` block (Biobanks, then other tabs).

Top-level tabs use a fixed order (`_NAV_TAB_ORDER`). **Major databases** is not a tab: hub and
continent listing pages are listed under ``not_in_nav`` (home page links; pages still build). Journals, Catalog statistics, and
Trending are omitted from the tab bar (home page cards link to Journals / Catalog statistics;
Trending uses `not_in_nav` so those pages still build). Rows with
SECTION=Tools and TOPIC=Population_Genetics are emitted as a separate **Population Genetics**
tab (`Population_Genetics.md` hub; pages remain `Tools_Population_Genetics_*.md`). The Tools
section tab and hub heading are labeled **GWAS Tools** (`Tools.md` unchanged).

Change site config in `PART1_BASE` / ``build_mkdocs_part1_yaml_header()`` below — hand-editing mkdocs.yml is lost on the next
`write_mkdcos()` run (e.g. `python main.py` from src/). After editing
`docs/stylesheets/extra.css`, run `python scripts/minify_extra_css.py` (see `deploy.sh`).
"""
import os
import re

import pandas as pd
import yaml

from load_data import load_table_and_ref
from process_major_databases import major_databases_not_in_nav_paths
from tag_pages import write_tag_pages


def _load_biobanks_world_map_snippet():
    path = os.path.join(os.path.dirname(__file__), "templates", "biobanks_world_map.html")
    with open(path, encoding="utf-8") as f:
        return f.read()


PART1_BASE='''site_name: CTGCatalog
site_url: https://cloufield.github.io/CTGCatalog/
site_description: >-
  Curated index of complex trait genetics resources—biobanks, GWAS summary statistics,
  software tools, references, single-cell methods, major projects, and AI-related tooling.
site_author: HE Yunye
repo_name: 'GitHub'
repo_url: https://github.com/Cloufield/CTGCatalog/
edit_uri: ""
copyright: "CTGCatalog is licensed under the MIT license"

extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/Cloufield/CTGCatalog
      name: CTGCatalog on GitHub

theme:
  name: material
  custom_dir: docs/overrides
  features:
      - navigation.tabs
      - navigation.top
      - navigation.path
      - navigation.prune
      - toc.follow
      - search.highlight
      - search.suggest
      - search.share
  font: false
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: blue
      accent: blue
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: blue
      accent: blue
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  logo:
      assets/logo.png
  favicon:
      assets/logo.png

extra_css:
  - stylesheets/extra.min.css

markdown_extensions:
  - md_in_html
  - toc:
      toc_depth: 3
  - admonition
  - tables
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.arithmatex:
      generic: true

extra_javascript:
  - javascripts/mathjax.js
  - https://unpkg.com/tablesort@5.3.0/dist/tablesort.min.js
  - javascripts/tablesort.js

plugins:
  - meta
  - tags
  - search
  - mkdocs-jupyter

'''

def build_mkdocs_part1_yaml_header(*, major_db_not_in_nav: list[str] | None = None) -> str:
    """Site YAML head + ``not_in_nav`` (Trending + Major databases; neither is a top tab)."""
    lines = [
        PART1_BASE.rstrip(),
        "",
        "not_in_nav: |",
        "  Trending/index.md",
        "  Trending/Trending_PubMed_GWAS.md",
    ]
    for rel in major_db_not_in_nav or ():
        lines.append(f"  {rel}")
    return "\n".join(lines) + "\n\n"


# Top tabs (Material navigation.tabs). Not listed here: Journals, Catalog statistics, Trending (home cards only).
_NAV_TAB_ORDER = [
    "Biobanks",
    "Sumstats",
    "Tools",
    "Coding",
    "Population_Genetics",
    "References",
    "Single_Cell",
    "Projects",
    "AI",
]

# Catalog rows still use SECTION=Tools, TOPIC=Population_Genetics; split into its own Material tab.
_POPGEN_TOPIC = "Population_Genetics"
_POPGEN_NAV_TITLE = "Population Genetics"
_POPGEN_HUB_BASENAME = "Population_Genetics"

# SECTION stays "Tools" in JSON; Material tab and hub heading use this label (page remains Tools.md).
_TOOLS_NAV_TITLE = "GWAS Tools"

# Short intro under "## Contents - …" on each top-level section hub (nav tab landing pages).
_SECTION_HUB_LEADS: dict[str, str] = {
    "Biobanks": (
        "Regional cohorts and biobanks with ancestry scope, sample context, and pointers to data access."
    ),
    "Sumstats": (
        "Public summary statistics and omics summary-level resources—GWAS, QTL, imaging, proteomics, and more."
    ),
    "Tools": (
        "GWAS-centric software and pipelines: association tests, fine mapping, PRS, MR, imputation, and visualization."
    ),
    "Coding": (
        "Languages, environments, containers, docs tooling, and workflow engines used day to day for analysis and the site."
    ),
    "Population_Genetics": (
        "Population-genetics methods: ancestry and admixture, genealogies and ARGs, phylogeny, and selection."
    ),
    "References": (
        "Curated reading by theme—genome biology, variants, phenotypes, methods, and related topics."
    ),
    "Single_Cell": (
        "Single-cell genomics tools: QC, annotation, harmonization, trajectories, and gene networks."
    ),
    "Projects": (
        "Major programs and reference resources (e.g. 1000 Genomes, UK Biobank, GTEx) with phased or versioned pages."
    ),
    "AI": (
        "Genomic models, agents, and AI-assisted tooling for genomics and variant interpretation."
    ),
}


#part2+='''    - Sumstats:
#      - Sumstats: Sumstats_Sumstats_README.md
#      - Biobanks_Cohorts: Sumstats_Biobanks_Cohorts_README.md
#      - Metabolomics: Metabolomics_Metabolomics_README.md
#      - Proteomics: Proteomics_Proteomics_README.md
#      - Imaging: Imaging_Imaging_README.md\n'''

## TAB_TOPIC_SUBTOPIC.md 

def write_mkdcos(
    *,
    tag_buckets=None,
    tag_slug_map=None,
    tag_card_rows=None,
):

    ##################################################################################################################################################################################################################

    def format_path(series):
        path_list=[]
        for i in series:
            if i!="" and i is not None:
                path_list.append(i)
        return "_".join(path_list)

    def format_level(series):
        level = 1
        for i in series:
            if i!="":
                level+=1
        return level

    def append_section_nav_lines(
        out,
        hub_basename,
        path_df,
        level_root_dic,
        *,
        nav_label=None,
    ):
        """Append mkdocs nav YAML lines for one catalog section (same structure as before).

        hub_basename: docs/{hub_basename}.md (e.g. Population_Genetics).
        nav_label: tab/sidebar title (e.g. Population Genetics); defaults to hub_basename.
        """
        spaces = " " * 2 * (1 + 1)
        label = nav_label or hub_basename
        value = "{}.md".format(hub_basename)
        single_line = "{}- {}: \n".format(spaces, label)
        out.append(single_line)

        spaces = " " * 2 * (1 + 2)
        single_line = "{}- {}: {} \n".format(spaces, label, value)
        out.append(single_line)

        added_topic = []
        for index, row in path_df.iterrows():

            spaces = " " * 2 * (1 + row["LEVEL"] - 1)
            if row["LEVEL"] == 3:
                col = "TOPIC"
            if row["LEVEL"] == 4:
                col = "SUBTOPIC"
            key = row[col]

            value = "{}.md".format(row["PATH"])

            if row["SUBTOPIC"] == "" and row["TOPIC"] in level_root_dic["TOPIC"]:
                added_topic.append(row["TOPIC"])
                single_line = "{}- {}:\n".format(spaces, key)
                out.append(single_line)
                spaces = " " * 2 * (1 + row["LEVEL"])
                single_line = "{}- {}: {}\n".format(spaces, key, value)
                out.append(single_line)

            elif (
                row["SUBTOPIC"] != ""
                and row["TOPIC"] in level_root_dic["TOPIC"]
                and row["TOPIC"] not in added_topic
            ):
                added_topic.append(row["TOPIC"])
                col = "TOPIC"
                spaces = " " * 2 * (1 + row["LEVEL"] - 2)
                single_line = "{}- {}:\n".format(spaces, row["TOPIC"])
                out.append(single_line)

                spaces = " " * 2 * (1 + row["LEVEL"] - 1)
                single_line = "{}- {}: {}\n".format(spaces, key, value)
                out.append(single_line)
            else:
                single_line = "{}- {}: {}\n".format(spaces, key, value)
                out.append(single_line)

    ##################################################################################################################################################################################################################

    table = load_table_and_ref()
    folder_cols = ["SECTION", "TOPIC", "SUBTOPIC"]
    table.loc[:, folder_cols ] = table.loc[:, folder_cols].fillna("")
    table["TYPE"] = table["TYPE"].fillna("MISC")
    table = table.sort_values(by=["SECTION","TOPIC","SUBTOPIC"])

    nav_by_section = {}

    def emit_catalog_section(
        nav_map_key,
        raw_dir,
        *,
        hub_basename,
        contents_title,
        nav_label=None,
        biobanks_world_map=False,
    ):
        if raw_dir.empty:
            return
        raw_dir = raw_dir.copy()
        raw_dir["PATH"] = raw_dir[folder_cols].apply(lambda x: format_path(x), axis=1)

        df_dir = raw_dir.loc[:, folder_cols].dropna(subset=folder_cols[0]).fillna("")
        path_df = df_dir.groupby(folder_cols).count().reset_index()
        path_df["PATH"] = path_df[folder_cols].apply(lambda x: format_path(x), axis=1)
        path_df["LEVEL"] = path_df[folder_cols].apply(lambda x: format_level(x), axis=1)

        level_root_dic = {col: [] for col in folder_cols}
        level_count = path_df.loc[path_df["LEVEL"] == 4, :].groupby("TOPIC")["PATH"].count()
        level_root_dic["TOPIC"] += list(level_count[level_count >= 1].index.values)

        main_file = "../docs/" + hub_basename + ".md"
        hub_fm = {"class": f"catalog-section-{nav_map_key}"}
        with open(main_file, "w") as file:
            file.write("---\n")
            file.write(
                yaml.safe_dump(
                    hub_fm,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                )
            )
            file.write("---\n\n")

        with open(main_file, "a") as file:
            # Same order as other section hubs: intro rail first so page h1 + .catalog-nav-lead
            # share the continuous accent rail (map would break that if placed above the lead).
            hub_lead = _SECTION_HUB_LEADS.get(nav_map_key)
            if hub_lead:
                file.write(
                    '<div class="catalog-nav-lead" markdown="block">\n\n'
                    + hub_lead.strip()
                    + "\n\n</div>\n\n"
                )
            if biobanks_world_map:
                file.write(_load_biobanks_world_map_snippet())
                file.write("\n\n")
            file.write("## {} - {} \n".format("Contents", contents_title))
            file.write("\n")
            file.write('<div class="catalog-section-contents" markdown="block">\n\n')

            added_topic = []
            for index, row in path_df.iterrows():
                type_dir = raw_dir.loc[
                    raw_dir["PATH"] == row["PATH"], :
                ].groupby("TYPE")["NAME"].count()
                string_list = []
                for k, v in type_dir.items():
                    string_list.append("{} - {}".format(k, v))
                type_line = " , ".join(string_list)

                spaces = " " * 2 * (row["LEVEL"] - 2)
                if row["LEVEL"] == 3:
                    col = "TOPIC"
                if row["LEVEL"] == 4:
                    col = "SUBTOPIC"
                string = row[col]
                link_string = "{}.md".format(row["PATH"])

                if (
                    row["SUBTOPIC"] != ""
                    and row["TOPIC"] in level_root_dic["TOPIC"]
                    and row["TOPIC"] not in added_topic
                ):
                    added_topic.append(row["TOPIC"])
                    single_line = "{}- {} :\n".format(
                        " " * 2 * (row["LEVEL"] - 3), row["TOPIC"], type_line
                    )
                    file.write(single_line)
                else:
                    added_topic.append(row["TOPIC"])

                link_key = "[{}]({})".format(string, link_string)
                single_line = "{}- {} : {}\n".format(spaces, link_key, type_line)
                file.write(single_line)

            file.write("\n</div>\n\n")

        nav_lines = []
        append_section_nav_lines(
            nav_lines,
            hub_basename,
            path_df,
            level_root_dic,
            nav_label=nav_label,
        )
        nav_by_section[nav_map_key] = "".join(nav_lines)

    for dirname in table["SECTION"].dropna().unique():
        if dirname == "":
            continue
        # Journals: single page from process_md; not a top tab (linked from home only).
        if dirname == "Journals":
            continue

        raw_dir = table.loc[table["SECTION"] == dirname, :].copy()
        if dirname == "Tools":
            raw_dir = raw_dir.loc[raw_dir["TOPIC"] != _POPGEN_TOPIC]

        if dirname == "Tools":
            tools_title = _TOOLS_NAV_TITLE
            tools_nav = _TOOLS_NAV_TITLE
        else:
            tools_title = dirname
            tools_nav = None

        emit_catalog_section(
            dirname,
            raw_dir,
            hub_basename=dirname,
            contents_title=tools_title,
            nav_label=tools_nav,
            biobanks_world_map=(dirname == "Biobanks"),
        )

    popgen = table.loc[
        (table["SECTION"] == "Tools") & (table["TOPIC"] == _POPGEN_TOPIC)
    ].copy()
    if not popgen.empty:
        emit_catalog_section(
            "Population_Genetics",
            popgen,
            hub_basename=_POPGEN_HUB_BASENAME,
            contents_title=_POPGEN_NAV_TITLE,
            nav_label=_POPGEN_NAV_TITLE,
        )

    part2_parts: list[str] = ["nav: \n", "    - Home : index.md\n"]
    if "Biobanks" in nav_by_section:
        part2_parts.append(nav_by_section["Biobanks"])
    for s in _NAV_TAB_ORDER:
        if s == "Biobanks":
            continue
        if s in nav_by_section:
            part2_parts.append(nav_by_section[s])
    part2 = "".join(part2_parts)

    if tag_buckets is not None and tag_slug_map is not None:
        write_tag_pages(tag_buckets, tag_slug_map, tag_card_rows)

    with open("../mkdocs.yml", mode="w") as file:
        file.write(
            build_mkdocs_part1_yaml_header(
                major_db_not_in_nav=major_databases_not_in_nav_paths(),
            )
            + part2
        )
