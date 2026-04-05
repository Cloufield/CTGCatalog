#!/usr/bin/env python3
"""
Set biobank PARTICIPANTS to a short prose description of who was enrolled
(not counts — use SAMPLE SIZE for scale).

Run from repo root:
  python3 scripts/set_biobank_participants_descriptions.py
"""
from __future__ import annotations

import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BIOBANKS = os.path.join(ROOT, "json", "biobanks")

# Short participant description (no numbers)
PARTICIPANTS_BY_REL: dict[str, str] = {
    "africa/awi-gen.json": "Sub-Saharan African adults (multi-site East/West/South)",
    "africa/h3africa.json": "African participants (H3Africa consortium studies)",
    "africa/nigerian-100k-genome-project.json": "Nigerian participants (national genome project)",
    "africa/the-egypt-genome-project.json": "Egyptian participants (national reference effort)",
    "africa/uganda-genome-resource.json": "Ugandan participants (genome resource)",
    "america/all-of-us.json": "US residents (nationally diverse recruitment)",
    "america/aric.json": "US Black and white adults (community-based cohorts)",
    "america/biobank-of-the-americas.json": "US and Latin American clinical / biopharma-linked participants",
    "america/biome.json": "New York City area health-system patients",
    "america/bioportal.json": "Montreal-area Canadian research participants",
    "america/biovu.json": "Vanderbilt University Medical Center patients",
    "america/canpath-ontario-health-study.json": "Canadian adults (Ontario; CanPath)",
    "america/cartagene-biobank.json": "Quebec residents (CartaGENE)",
    "america/colorado-center-for-personalized-medicine.json": "University of Colorado health-system patients",
    "america/elsa-brasil.json": "Brazilian civil servants and families (longitudinal aging)",
    "america/hchs-sol.json": "Hispanic/Latino adults (US community sites)",
    "america/massachusetts-general-brigham-biobank.json": "Mass General Brigham patients",
    "america/mesa-study.json": "US adults (Black, white, Hispanic/Latino, Chinese cohorts)",
    "america/mexico-city-prospective-study.json": "Mexico City metropolitan adults",
    "america/michigan-genomics-initiative.json": "Michigan Medicine patients",
    "america/million-veteran-program.json": "US military veterans (VA healthcare)",
    "america/page-study.json": "US minority cohorts (NH Black, Hispanic/Latino, Asian, Native American)",
    "america/penn-medicine-biobank.json": "University of Pennsylvania Health System patients",
    "america/the-canadian-longitudinal-study-on-aging.json": "Canadian adults (national aging cohort)",
    "america/ucla-precision-health-biobank.json": "UCLA Health patients",
    "america/womens-health-initiative.json": "US postmenopausal women (multi-ethnic)",
    "asia/biobank-japan.json": "Japanese adults (hospital and population network)",
    "asia/born-in-guangzhou-cohort-study.json": "Han Chinese mothers and infants (Guangzhou birth cohort)",
    "asia/cebu-longitudinal-health-and-nutrition-survey.json": "Filipino mothers and offspring (Cebu)",
    "asia/china-kadoorie-biobank.json": "Chinese adults (10 regions; prospective cohort)",
    "asia/chinese-millionome-database.json": "Chinese individuals (aggregated genome database)",
    "asia/han-chinese-genome-initiative-phase-1-the-han100k-project.json": "Han Chinese adults (reference genomes)",
    "asia/indigenomes.json": "Indian subcontinent individuals (genome resource)",
    "asia/koges.json": "Korean adults (population-based sub-cohorts)",
    "asia/korean-genome-project-phase-1.json": "Korean individuals (reference genomes)",
    "asia/korean-genome-project-phase-2.json": "Korean individuals (Korea4K reference)",
    "asia/national-biobank-of-korea.json": "Korean participants (linked with KoGES / national program)",
    "asia/national-center-biobank-network.json": "Japanese patients (national hospital biobank network)",
    "asia/nyuwa-genome-resource.json": "Han Chinese individuals (NyuWa reference genomes)",
    "asia/qatar-biobank.json": "Consenting adults in Qatar (national biobank)",
    "asia/qatar-genome-program.json": "Qatari individuals (national sequencing; linked with Qatar Biobank)",
    "asia/sg10k_health.json": "Singapore residents (Chinese, Malay, Indian, other)",
    "asia/taiwan-biobank.json": "Han Chinese adults (general-population recruitment)",
    "asia/taiwan-precision-medicine-initiative.json": "Han Chinese adults (precision medicine initiative)",
    "asia/taizhou-imaging-study.json": "Han Chinese adults (Taizhou imaging cohort)",
    "asia/the-china-metabolic-analytics-project.json": "Chinese adults (metabolic disease cohort)",
    "asia/the-hisayama-study.json": "Japanese adults (Hisayama town)",
    "asia/the-japan-covid-19-task-force-study.json": "Japanese individuals (COVID-19 host genetics)",
    "asia/the-japan-prospective-studies-collaboration-for-aging-and-dementia.json": "Japanese adults (aging and dementia collaboration)",
    "asia/the-malaysian-cohort.json": "Malaysian adults (multi-ethnic national cohort)",
    "asia/the-nagahama-study.json": "Japanese adults (Nagahama City, Shiga)",
    "asia/the-stromics-genome-study.json": "Chinese adults (acute ischemic stroke registry)",
    "asia/tohoku-medical-megabank.json": "Japanese adults (Tōhoku region; megabank)",
    "asia/westlake-biobank-for-chinese.json": "Han Chinese adults (Westlake biobank)",
    "europe/alspac.json": "UK pregnant women and children (Bristol area; Children of the 90s)",
    "europe/biobank-graz.json": "Austrian clinical and research participants (Graz)",
    "europe/biobank-russia.json": "Russian adults (Almazov Centre biobank)",
    "europe/colaus-study.json": "Swiss adults (Lausanne population cohort)",
    "europe/danish-blood-donor-study.json": "Danish blood donors",
    "europe/danish-national-biobank.json": "Danish national biobank participants",
    "europe/decode-genetics.json": "Icelandic participants (population and genealogy)",
    "europe/east-london-genes-health.json": "British Bangladeshi and Pakistani adults (East London)",
    "europe/estonian-biobank.json": "Estonian adults (national biobank)",
    "europe/fenland-study.json": "English adults (Cambridgeshire Fenland)",
    "europe/finngen.json": "Finnish adults (national FinnGen)",
    "europe/generation-scotland.json": "Scottish adults and families",
    "europe/gutenberg-health-study.json": "German adults (population-based Mainz region)",
    "europe/interval-study.json": "English blood donors (INTERVAL)",
    "europe/lifelines.json": "Dutch residents (three-generation cohort)",
    "europe/nako-gesundheitsstudie.json": "German adults (NAKO national cohort)",
    "europe/rotterdam-study.json": "Dutch adults (Rotterdam Study)",
    "europe/sapaldia.json": "Swiss adults (respiratory population cohort)",
    "europe/the-international-agency-for-research-on-cancer-iarc-biobank.json": "Participants from many international IARC-led studies",
    "europe/the-trndelag-health-study.json": "Norwegian adults (HUNT, Trøndelag)",
    "europe/twinsuk.json": "UK adult female twins",
    "europe/uk-biobank.json": "UK adults (aged ~40–69 at baseline)",
    "oceania/forty-five-and-up-study.json": "Australian adults aged 45 and over (NSW)",
    "oceania/qimr-berghofer-qimr-biobank.json": "Australian research volunteers (QIMR Berghofer)",
}


def main() -> int:
    for dirpath, _, filenames in os.walk(BIOBANKS):
        for fn in filenames:
            if not fn.endswith(".json"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, BIOBANKS).replace(os.sep, "/")
            if rel not in PARTICIPANTS_BY_REL:
                raise SystemExit(f"Missing PARTICIPANTS mapping for {rel}")

    for rel, text in PARTICIPANTS_BY_REL.items():
        path = os.path.join(BIOBANKS, *rel.split("/"))
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        data["PARTICIPANTS"] = text
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")

    print(f"Set PARTICIPANTS description on {len(PARTICIPANTS_BY_REL)} biobank JSON file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
