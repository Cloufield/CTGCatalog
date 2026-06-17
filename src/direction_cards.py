"""
Direction cards showing research trends within each CTGCatalog section/topic.
Cards appear on hub pages and category listing pages.

Data structure:
  _SECTION_DIRECTION: section_name -> markdown card content (tab-level)
  _TOPIC_DIRECTION: (section, topic) -> markdown card content (category-level)
  _SUBTOPIC_DIRECTION: (section, topic, subtopic) -> markdown card content (subcategory-level)
"""

# ── Tab-level direction cards ──────────────────────────────────────────────

_SECTION_DIRECTION: dict[str, str] = {
    "AI": """\
**AI in Genomics & Biomedical Research**

The AI tab tracks the intersection of artificial intelligence with human genomics and biomedical discovery. Key trajectories:

- **Genomic foundation models** (DNA/RNA): From BPE-based tokenisers (DNABERT, Ji *et al.* PMID 33542176, *Bioinformatics* 2021) to reverse-complement equivariant architectures (HyenaDNA, Nguyen *et al.* *NeurIPS* 2023; Caduceus, Schiff *et al.* *NeurIPS* 2024) to whole-genome autoregressive models (Evo 2, Brixi *et al.* PMID 39664581, *Science* 2025; Genos, Arora *et al.* *bioRxiv* 2025). Scaling trend: kilo-base → mega-base context windows, single-species → cross-species generalization.

- **Pathology foundation models**: 2024 explosion — self-supervised whole-slide image models (UNI, Chen *et al.* *Nat Med* 2024; Virchow, Vorontsov *et al.* *Nat Med* 2024; Prov-GigaPath, Xu *et al.* PMID 38931993, *Nature* 2024) → vision-language alignment for multimodal interpretation (CONCH, Lu *et al.* *Nat Med* 2024; TITAN, Ding *et al.* *Nat Med* 2025) → knowledge-enhanced architectures (KEEP, Li *et al.* PMID 39972922, *Nat Med* 2026).

- **AI for GWAS**: Image-based phenotyping via CNN/U-Net (Haas *et al.* PMID 34957434, *Cell Genom* 2021; Khurshid *et al.* PMID 36944631, *Nat Commun* 2023) → self-supervised contrastive learning from raw images (iGWAS, Kirchler *et al.* *Nat Genet* 2024) → Transformer-based association methods (InsightGWAS, Song *et al.* *bioRxiv* 2025) → AI-enhanced post-GWAS interpretation (PoPS, Weeks *et al.* PMID 37106029, *Nat Genet* 2023).

- **Autonomous AI agents**: From assistive diagnostic tools (AI-MARRVEL, Mao *et al.* PMID 39631886, *NEJM AI* 2024) to fully autonomous scientific discovery — hypothesis generation, experimental design, and execution (AI Scientist, Lu *et al.* *ICML* 2025; Robin, Qiu *et al.* *Nat Biotechnol* 2026; Co-Scientist, Gottweis *et al.* *Nature* 2026).

- **Regulatory genomics models**: From short-range sequence-to-function prediction (DeepSEA, Zhou & Troyanskaya PMID 26301841, *Nat Methods* 2015) to cell-type-specific, long-range expression models integrating epigenomic context (Enformer, Avsec *et al.* PMID 34316034, *Nat Methods* 2021; Borzoi, Linder *et al.* PMID 39704929, *Nat Genet* 2025).
""",
}

# ── Topic-level direction cards (within a section) ─────────────────────────

_TOPIC_DIRECTION: dict[tuple[str, str], str] = {
    ("Tools", "GxE_interactions"): """\
**Gene–Environment Interaction Methods**

Methods for detecting and characterizing gene–environment interactions (G×E) in genome-wide studies:

- **Early foundations** (2010–2019): Environment-wide interaction scans (G×Escan, Gauderman *et al.* PMID 23873611, *PLoS ONE* 2013; StructLMM, Moore *et al.* PMID 30478441, *Nat Genet* 2019) and adaptive G×E tests (Chen *et al.* PMID 30793815, *Genet Epidemiol* 2019).

- **Whole-genome regression** (2020–2024): LEMMA (Kerin *et al.* PMID 32888427, *Nat Commun* 2020) and GPLEMMA (Kerin *et al.* PMID 33367483, *Nat Commun* 2021) for genome-wide G×E with multiple environmental variables. IMRP-GxE (Zhu *et al.* PMID 38649715, *Nat Commun* 2024) integrates Mendelian randomization principles.

- **Scalable biobank methods** (2025–2026): SPAGxECCT (Ma *et al.* PMID 40157913, *Nat Commun* 2025) for diverse trait types with saddlepoint calibration. SAGELD (Xu *et al.* PMID 42304093, *Nat Comput Sci* 2026) extends to longitudinal data, using matrix projection and SPA GRM to achieve 10–10,000× speedups while discovering 74 genetic×age and 5 genetic×adiposity loci in UK Biobank.

- **Reviews**: Comprehensive overviews of G×E in human health (Herrera-Luis *et al.* PMID 38806721, *Nat Rev Genet* 2024; Thomas *et al.* PMID 20212493, *Nat Rev Genet* 2010).

Trend: from single-environment cross-sectional scans → multi-environment, multi-ancestry, and longitudinal frameworks integrated with biobank-scale analysis.
""",
    ("AI", "GWAS"): """\
**AI-enhanced GWAS**

The GWAS topic within AI covers methods that use machine learning to boost genome-wide association studies. Main trajectories:

- **Imaging GWAS**: Early work applied supervised CNNs (U-Net, ResNet) to medical images for trait quantification and GWAS (Haas PMID 34957434, *Cell Genomics* 2021; Khurshid PMID 36944631, *Nat Commun* 2023). Recent work uses self-supervised contrastive learning to bypass manual annotation, running GWAS directly on image embeddings (iGWAS, Kirchler *et al.* PMID 39020183, *Nature Genetics* 2024).

- **AI Phenotyping**: Ensemble ML and multimodal topic models (EHR + genetics) for phenotype extraction and GWAS on imputed phenotypes (MILTON, Garg *et al.* PMID 39471869, *Nat Genet* 2024; MixEHR-SAGE, Cui *et al.* PMID 39843619, *Nat Med* 2026).

- **AI Association Methods**: Neural network-based association tests (GWANN, Holzinger *et al.* PMID 38918402, *Nat Genet* 2024) and Transformer-based models for discovering novel loci (InsightGWAS, Song *et al.* *bioRxiv* 2025).

- **Post-GWAS AI**: Gene prioritization using polygenic features (PoPS, Weeks *et al.* PMID 37106029, *Nat Genet* 2023).

- **Methodology reviews**: Causal ML for single-cell genomics (Tejada-Lapuerta *et al.* PMID 40336376, *Nat Genet* 2025).
""",
    ("AI", "Imaging"): """\
**Pathology & Medical Imaging Foundation Models**

Rapidly growing since 2024. Models for computational pathology that learn from millions of whole-slide images:

- **Self-supervised pretraining** on slide patches without manual labels (UNI, Chen *et al.* *Nat Med* 2024; Virchow, Vorontsov *et al.* *Nat Med* 2024; Prov-GigaPath, Xu *et al.* PMID 38931993, *Nature* 2024).
- **Vision-language alignment** connecting histology images with text descriptions for zero-shot tasks (CONCH, Lu *et al.* *Nat Med* 2024; TITAN, Ding *et al.* *Nat Med* 2025; mSTAR, Guo *et al.* *Nat Med* 2025).
- **Knowledge-enhanced architectures** incorporating biomedical ontologies and multimodal clinical data (KEEP, Li *et al.* PMID 39972922, *Nat Med* 2026; PathOrchestra, Xiong *et al.* *Nat Med* 2025).

Trend: from single-modal patch-level models → multimodal whole-slide understanding with clinical context.
""",
    ("AI", "Genomic_language_model"): """\
**DNA/RNA Foundation Models**

Genomic language models that learn representations of DNA sequence for variant effect prediction and genome annotation:

- **1st generation** (2021-2023): BPE tokenization + BERT-style pretraining on reference genomes (DNABERT, Ji *et al.* PMID 33542176, *Bioinformatics* 2021; DNABERT-2, Zhou *et al.* *arXiv* 2024).
- **2nd generation** (2023-2024): Biologically motivated architectures — reverse-complement equivariance and long-range operators (HyenaDNA, Nguyen *et al.* *NeurIPS* 2023; Caduceus, Schiff *et al.* *NeurIPS* 2024).
- **3rd generation** (2025-2026): Species-aware embeddings with Manifold Instance Mixup (DNABERT-S, Zhou *et al.* *Nat Mach Intell* 2025), whole-genome autoregressive training (Evo 2, Brixi *et al.* PMID 39664581, *Science* 2025; Genos, Arora *et al.* *bioRxiv* 2025), and multimodal reasoning (BioReason, Wei *et al.* *NeurIPS* 2025).

Scaling trajectory: context from 512bp → 1M+ bp, training from single genomes → whole-genome alignments → cross-species.
""",
    ("AI", "Agent"): """\
**Biomedical AI Agents**

LLM-powered agents designed for biomedical knowledge tasks, from diagnosis to experiment automation:

- **Diagnostic agents**: Knowledge-driven systems combining LLMs with curated databases and APIs for rare disease diagnosis (AI-MARRVEL, Mao *et al.* PMID 39631886, *NEJM AI* 2024; MARRVEL-MCP, Mao *et al.* *AJHG* 2026).
- **Multi-agent frameworks**: Self-evolving systems that learn to use diverse biomedical tools (BioMedAgent, Wang *et al.* *Nat Mach Intell* 2026). Specialized agents for gene editing (CRISPR-GPT, Huang *et al.* *Nat Commun* 2026) and rare disease (DeepRare, Chen *et al.* *Nat Med* 2026).
- **Domain-general platforms**: Open-source, local-first frameworks (OpenClaw, Hermes Agent) vs. cloud-based commercial solutions.

Trend: from single-purpose chatbots → modular multi-agent systems with tool-use → self-evolving scientific agents.
""",
    ("AI", "Auto_research"): """\
**Autonomous Scientific Discovery**

AI systems that autonomously conduct research — generating hypotheses, designing experiments, and validating results:

- **Foundation** (2025): Specialized multi-agent systems for structured scientific reasoning (Co-Scientist, Gottweis *et al.* *Nature* 2026; Virtual Lab, Swanson *et al.* PMID 39719521, *Nature* 2025).
- **Full autonomy** (2025-2026): End-to-end systems that generate complete research papers from idea to manuscript (AI Scientist, Lu *et al.* *ICML* 2025; Robin, Qiu *et al.* *Nat Biotechnol* 2026).
- **Open-source pipelines**: Reproducible multi-stage workflows (AutoResearchClaw, CodeScientist from Ai2).

Trend: from assistive → autonomous, from specialized domains → general-purpose scientific discovery.
""",
    ("AI", "Regulatory_model"): """\
**Gene Regulation Prediction Models**

Deep learning models predicting molecular phenotypes from DNA sequence:

- **Early work** (2015-2018): Chromatin effect prediction from short DNA windows (DeepSEA, Zhou & Troyanskaya PMID 26301841, *Nat Methods* 2015) and tissue-specific expression prediction (ExPecto, Zhou *et al.* PMID 30013180, *Nat Genet* 2018).
- **Long-range integration** (2021-2022): Models incorporating up to 200kb context via transformer/enhancer architectures (Enformer, Avsec *et al.* PMID 34316034, *Nat Methods* 2021; Sei, Chen *et al.* PMID 35404663, *Nat Genet* 2022).
- **Cell-type resolution** (2025): Tissue- and cell-type-specific expression prediction with improved positional encoding (Borzoi, Linder *et al.* PMID 39704929, *Nat Genet* 2025; Flashzoi, Linder *et al.* *Nat Genet* 2025).

Trend: 1kb → 200kb context, tissue-average → cell-type-specific, static → condition-aware.
""",
}

# ── Subtopic-level direction cards ─────────────────────────────────────────

_SUBTOPIC_DIRECTION: dict[tuple[str, str, str], str] = {
    ("AI", "GWAS", "Imaging_GWAS"): """\
**Image-based Phenotyping for GWAS**

Methods using computer vision to extract quantitative traits from medical images for genetic association:

- **Supervised CNNs** (2021-2023): U-Net-based segmentation of organs (Liu PMID 34128465, *eLife* 2021), ResNet transferred from ImageNet for trait regression (Haas PMID 34957434, *Cell Genomics* 2021; Pirruccello PMID 35637384, *Nat Genet* 2022; Khurshid PMID 36944631, *Nat Commun* 2023).
- **Self-supervised** (2024): Contrastive learning (SimCLR-style CNN encoder) enabling GWAS directly from image embeddings without manual trait definition (iGWAS, Kirchler *et al.* PMID 39020183, *Nat Genet* 2024).

Trend: supervised organ-specific CNNs → self-supervised whole-image representation learning.
""",
    ("AI", "GWAS", "Methods"): """\
**AI-enhanced GWAS Methods**

Machine learning approaches that improve statistical power or discover novel genetic architecture:

- **Non-linear covariate adjustment** using deep neural networks (DeepNull, Hormozdiari *et al.* PMID 36195755, *Nat Commun* 2022).
- **Neural network-based association tests** with built-in epistasis detection (GWANN, Holzinger *et al.* PMID 38918402, *Nat Genet* 2024).
- **Transformer models** for discovering trait-relevant genetic variants by learning from summary statistics (InsightGWAS, Song *et al.* *bioRxiv* 2025).
- **Power-boosting methods** that combine multiple association statistics (Quickdraws, Shi *et al.* *Nat Genet* 2025).
""",
    ("AI", "GWAS", "Phenotyping"): """\
**AI-driven Phenotype Extraction**

ML methods that create or enhance phenotypes from clinical data for GWAS:

- **Ensemble ML** using biomarkers and multimodal features for case ascertainment (MILTON, Garg *et al.* PMID 39471869, *Nat Genet* 2024).
- **Synthetic surrogates** enabling GWAS on imputed phenotypes (SynSurr, McCaw *et al.* PMID 39468299, *Nat Genet* 2024).
- **Multimodal topic models** integrating diagnosis codes, medications, and genetics (MixEHR-SAGE, Cui *et al.* PMID 39843619, *Nat Med* 2026).
""",
    ("AI", "GWAS", "Post_GWAS"): """\
**AI for Post-GWAS Interpretation**

ML tools that translate GWAS loci into biological mechanism:

- **Gene prioritization**: Learning trait-relevant gene features from GWAS summary statistics and functional genomics data (PoPS, Weeks *et al.* PMID 37106029, *Nat Genet* 2023). Uses polygenic enrichment to rank genes at GWAS loci.

Current frontier: integrating single-cell and spatial data with GWAS signals for cell-type-specific interpretation.
""",
}


def get_section_direction(section: str) -> str | None:
    """Return the tab-level direction card for a section, or None."""
    return _SECTION_DIRECTION.get(section)


def get_topic_direction(section: str, topic: str) -> str | None:
    """Return the topic-level direction card, or None."""
    return _TOPIC_DIRECTION.get((section, topic))


def get_subtopic_direction(section: str, topic: str, subtopic: str) -> str | None:
    """Return the subtopic-level direction card, or None."""
    return _SUBTOPIC_DIRECTION.get((section, topic, subtopic))


def render_direction_card(content: str) -> str:
    """Wrap direction content in a card div with proper class."""
    return (
        '<div class="catalog-direction-card" markdown="block">\n\n'
        + content.strip()
        + "\n\n</div>\n\n"
    )
