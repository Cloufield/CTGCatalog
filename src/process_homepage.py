import html

import pandas as pd
import yaml

from catalog_sources import HOMEPAGE_SUMSTATS_SHEETS
from print_level import _SECTION_DEFAULT_BADGES


def _stats_counts_table_html(df: pd.DataFrame) -> str:
    """HTML table with Count column bars (length ∝ value, anchored to the right)."""
    if df.empty or "Count" not in df.columns:
        return "<p><em>No entries in this section.</em></p>\n"

    counts = pd.to_numeric(df["Count"], errors="coerce").fillna(0)
    max_c = float(counts.max())
    if max_c <= 0:
        max_c = 1.0

    cols = list(df.columns)
    lines = [
        '<table class="catalog-stats-table">',
        "<thead><tr>",
    ]
    for c in cols:
        lines.append(f"<th>{html.escape(str(c))}</th>")
    lines.append("</tr></thead><tbody>")

    for (_, row), num in zip(df.iterrows(), counts):
        lines.append("<tr>")
        for c in cols:
            raw = row[c]
            if c == "Count":
                pct = min(100.0, (float(num) / max_c) * 100.0)
                val = int(num) if pd.notna(raw) else 0
                lines.append(
                    f'<td class="catalog-stats-count" '
                    f'style="--catalog-count-pct:{pct:.2f}%">{val}</td>'
                )
            else:
                lines.append(f"<td>{html.escape(str(raw))}</td>")
        lines.append("</tr>")

    lines.append("</tbody></table>")
    return "\n".join(lines) + "\n"

# Homepage: hide left nav + TOC so the article spans the full main row (same width as all three
# columns on Biobanks, etc.). Top tabs / header unchanged; mobile drawer still opens site nav.
# `tags` + `hide: tags` align Material search filters with catalog sections without duplicating badges in the hero.
def _dump_front_matter(fm: dict) -> str:
    return (
        "---\n"
        + yaml.safe_dump(
            fm,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
        + "---\n\n"
    )

# Same pattern as GWASQuiz (https://cloufield.github.io/GWASQuiz/): Markdown hero first so
# Material parses headings/links in .md-typeset; only the card deck is raw HTML.
_HOMEPAGE_INTRO = """# Complex Trait Genetics Catalog

<div class="catalog-home-hero">
<p><strong>Hi there, and welcome to CTGCatalog.</strong></p>
<p>I'm Yunye, and I study complex trait genomics. I created this collection to bring together resources that I personally find useful for my work.</p>
<p>CTGCatalog is a GWAS-focused collection for complex trait genetics, including reference data, public summary statistics, software tools, related literature, and AI-related resources. It is a personal curated collection rather than an exhaustive or official resource. AI assists with curation, while all entries are reviewed and maintained manually.</p>
</div>

<div class="grid cards catalog-home-cards">
<ul>
<li>
<a class="catalog-home-card-link" href="Biobanks/">
<p><span class="catalog-card-icon" aria-hidden="true">🏥</span> <strong>Biobanks &amp; cohorts</strong></p>
<hr>
<p>Population studies and biobanks by world region.</p>
</a>
</li>
<li>
<a class="catalog-home-card-link" href="Sumstats/">
<p><span class="catalog-card-icon" aria-hidden="true">📊</span> <strong>Summary statistics</strong></p>
<hr>
<p>Public GWAS and omics sumstats (imaging, proteomics, transcriptomics, etc.).</p>
</a>
</li>
<li>
<a class="catalog-home-card-link" href="Tools/">
<p><span class="catalog-card-icon" aria-hidden="true">🛠️</span> <strong>GWAS Tools</strong></p>
<hr>
<p>Association tests, fine mapping, PRS, visualization, MR, and more.</p>
</a>
</li>
<li>
<a class="catalog-home-card-link" href="Coding/">
<p><span class="catalog-card-icon" aria-hidden="true">💻</span> <strong>Coding</strong></p>
<hr>
<p>Python stack, Conda, containers, Linux shell, workflows, and docs/site tooling.</p>
</a>
</li>
<li>
<a class="catalog-home-card-link" href="References/">
<p><span class="catalog-card-icon" aria-hidden="true">📚</span> <strong>References</strong></p>
<hr>
<p>Key papers and resources by topic (genome, variant, phenotype, and more).</p>
</a>
</li>
<li>
<a class="catalog-home-card-link" href="Single_Cell/">
<p><span class="catalog-card-icon" aria-hidden="true">🧬</span> <strong>Single cell</strong></p>
<hr>
<p>scRNA-seq tools: QC, annotation, trajectory, networks, harmonization.</p>
</a>
</li>
<li>
<a class="catalog-home-card-link" href="Projects/">
<p><span class="catalog-card-icon" aria-hidden="true">🗂️</span> <strong>Projects</strong></p>
<hr>
<p>Large programs (e.g. 1000 Genomes, UK Biobank, GTEx): one page per project, one card per phase.</p>
</a>
</li>
<li>
<a class="catalog-home-card-link" href="AI/">
<p><span class="catalog-card-icon" aria-hidden="true">🤖</span> <strong>AI</strong></p>
<hr>
<p>Biomedical AI agents and related tooling.</p>
</a>
</li>
<li>
<a class="catalog-home-card-link" href="Journals/">
<p><span class="catalog-card-icon" aria-hidden="true">📰</span> <strong>Journals</strong></p>
<hr>
<p>Publication venues cited by the catalog, with links and metadata.</p>
</a>
</li>
<li>
<a class="catalog-home-card-link" href="tags/">
<p><span class="catalog-card-icon" aria-hidden="true">🏷️</span> <strong>Tags</strong></p>
<hr>
<p>Tag hub and one page per tag (entries from every section). Click a tag on any card to open its page.</p>
</a>
</li>
<li>
<a class="catalog-home-card-link" href="Catalog_statistics/">
<p><span class="catalog-card-icon" aria-hidden="true">📈</span> <strong>Catalog statistics</strong></p>
<hr>
<p>Item counts by biobank region, sumstats field, AI, GWAS tools, and more.</p>
</a>
</li>
<li>
<a class="catalog-home-card-link" href="Trending/">
<p><span class="catalog-card-icon" aria-hidden="true">🔥</span> <strong>Trending</strong></p>
<hr>
<p>Literature trends from PubMed baseline: GWAS-related terms and journal rankings.</p>
</a>
</li>
<li id="about">
<div class="catalog-home-card-link catalog-home-card-link--static" markdown="block">
<p><span class="catalog-card-icon" aria-hidden="true">ℹ️</span> <strong>About</strong></p>
<hr>
<p>For more complex trait genomics content, see <a href="https://cloufield.github.io/GWASTutorial/">GWASTutorial</a></p>
<p>Contact: <a href="mailto:gwaslab@gmail.com">gwaslab@gmail.com</a></p>
</div>
</li>
</ul>
</div>

"""


def write_catalog_statistics_page(t: pd.DataFrame) -> None:
    """Write docs/Catalog_statistics.md (counts by section)."""
    if "FIELD" not in t.columns:
        t = t.copy()
        t["FIELD"] = ""

    path = "../docs/Catalog_statistics.md"
    stats_tags = sorted(set(_SECTION_DEFAULT_BADGES.values()) | {"Statistics"})
    with open(path, "w") as f:
        f.write(
            _dump_front_matter(
                {"hide": ["navigation", "tags"], "tags": stats_tags}
            )
        )
        f.write("# Catalog statistics\n\n")
        f.write(
            "The tables below summarize how many items are indexed in each part of the catalog. "
            "Counts change as the catalog is updated.\n\n"
        )

    biobanks = t.loc[t["SECTION"] == "Biobanks", :]
    if biobanks.empty:
        counts = pd.DataFrame(columns=["Location", "Count"])
    else:
        counts = (
            biobanks[["NAME", "CONTINENT"]]
            .groupby(["CONTINENT"])
            .count()
            .reset_index()
        )
        counts = counts.rename(columns={"CONTINENT": "Location", "NAME": "Count"})

    with open(path, "a") as f:
        f.write("## Biobanks and cohorts\n\n")
        f.write(_stats_counts_table_html(counts))
        f.write("\n")

    sumstats_like = t.loc[t["FIELD"].isin(HOMEPAGE_SUMSTATS_SHEETS), :].copy()
    if sumstats_like.empty:
        counts = pd.DataFrame(columns=["Field", "Category", "Count"])
    else:
        sumstats_like["CATEGORY"] = sumstats_like["CATEGORY"].fillna("MISC")
        counts = (
            sumstats_like[["TOPIC", "NAME", "CATEGORY"]]
            .groupby(["TOPIC", "CATEGORY"])
            .count()
            .reset_index()
        )
        counts = counts.rename(
            columns={"TOPIC": "Field", "NAME": "Count", "CATEGORY": "Category"}
        )

    with open(path, "a") as f:
        f.write("## Sumstats\n\n")
        f.write(_stats_counts_table_html(counts))
        f.write("\n")

    ai_sec = t.loc[t["SECTION"] == "AI", :].copy()
    if ai_sec.empty:
        counts = pd.DataFrame(columns=["Field", "Category", "Count"])
    else:
        ai_sec["CATEGORY"] = ai_sec["CATEGORY"].fillna("MISC")
        counts = (
            ai_sec[["TOPIC", "NAME", "CATEGORY"]]
            .groupby(["TOPIC", "CATEGORY"])
            .count()
            .reset_index()
        )
        counts = counts.rename(
            columns={"TOPIC": "Field", "NAME": "Count", "CATEGORY": "Category"}
        )

    with open(path, "a") as f:
        f.write("## AI\n\n")
        f.write(_stats_counts_table_html(counts))
        f.write("\n")

    tools = t.loc[t["SECTION"] == "Tools", :].copy()
    if tools.empty:
        counts = pd.DataFrame(columns=["Field", "Category", "Count"])
    else:
        tools["CATEGORY"] = tools["CATEGORY"].fillna("MISC")
        counts = (
            tools[["TOPIC", "NAME", "CATEGORY"]]
            .groupby(["TOPIC", "CATEGORY"])
            .count()
            .reset_index()
        )
        counts = counts.rename(
            columns={"TOPIC": "Field", "NAME": "Count", "CATEGORY": "Category"}
        )

    with open(path, "a") as f:
        f.write("## GWAS Tools\n\n")
        f.write(_stats_counts_table_html(counts))
        f.write("\n")

    coding = t.loc[t["SECTION"] == "Coding", :].copy()
    if coding.empty:
        counts = pd.DataFrame(columns=["Field", "Count"])
    else:
        counts = (
            coding[["TOPIC", "NAME"]]
            .groupby(["TOPIC"])
            .count()
            .reset_index()
        )
        counts = counts.rename(columns={"TOPIC": "Field", "NAME": "Count"})

    with open(path, "a") as f:
        f.write("## Coding\n\n")
        f.write(_stats_counts_table_html(counts))
        f.write("\n")


def write_homepage(table_and_ref: pd.DataFrame):
    write_catalog_statistics_page(table_and_ref)

    index_path = "../docs/index.md"
    with open(index_path, "w") as homepage:
        homepage.write(
            _dump_front_matter(
                {
                    "hide": ["navigation", "toc", "tags"],
                    "tags": ["Catalog", "Home"],
                }
            )
        )
        homepage.write(_HOMEPAGE_INTRO)
