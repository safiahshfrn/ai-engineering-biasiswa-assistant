# BiasiswaBot — Scholarship & Financial Aid Information Assistant

> A document-grounded AI assistant that answers Malaysian SPM, STPM/matriculation and diploma leavers' scholarship and financial-aid questions for pre-university, diploma and first-degree study, with citations from official public sources.

## Problem Statement
Scholarship and financial-aid information (providers, eligibility, deadlines, steps) is spread across many agency and university pages, each with different conditions. Students must cross-check several documents. A retrieval-grounded AI assistant can answer in English and Bahasa Melayu and cite the official source.

## Evidence of the Problem
- MyGOV Malaysia lists financial assistance from separate providers (e.g. JPA, PTPK) with different conditions — https://www.malaysia.gov.my/en/categories/school--education/scholarships-and-financial-assistance
- Institutions restate PTPTN rules with institution-specific details (windows, GPA conditions) — https://www.hw.ac.uk/malaysia/study/fees-and-funding/scholarships/national-higher-education-fund-ptptn

## Initial Related Work / Existing Approaches
- Chen et al. (2024), RAG admission chatbot — limitation: non-Malaysian admission data, small user study (53 students).
- Trienes et al. (2025), Marcel — limitation: one programme at one university.
- Siragusa et al. (2024), Unipa-GPT — limitation: single university website, Italian only.

## Engineering Gap / Limitation
Existing university RAG chatbots focus on a single institution's admissions. There is no multi-source, citation-grounded assistant for time-sensitive Malaysian scholarship information that also refuses to make eligibility decisions.

## Project Objectives
- O1: To design a document-grounded AI assistant based on official public scholarship and financial-aid sources.
- O2: To develop it with retrieval, citations and guardrails.
- O3: To evaluate answer accuracy, groundedness, latency and safety.

## Target Users
Malaysian school leavers seeking funding for pre-university, diploma or first-degree study: SPM leavers, STPM and matriculation/foundation leavers, and diploma graduates moving on to a degree. Postgraduate funding is out of scope.

## Data Sources (v2 corpus, retrieved 22 Nov 2026)
- PTPTN — Pinjaman Pendidikan: https://www.ptptn.gov.my/pinjaman-pendidikan/
- MARA — Pembiayaan pelajaran peringkat diploma & ijazah: https://www.mara.gov.my/bm/pendidikan/pembiayaan-pelajaran/peringkat-diploma-ijazah/
- Bank Negara Malaysia — Kijang scholarships: https://www.bnm.gov.my/careers/scholarships
- JPA statements on Dermasiswa B40 2026 and Penajaan Lepasan SPM 2026 (via BERNAMA; JPA portal not retrievable, marked *not verified*)
- MyGOV — Bantuan kewangan pengajian tinggi (registry only)

The repository stores original paraphrased notes with source metadata, not copies of the provider pages.

## Repository Structure
```
docs/        week1–week4 design and data documents, diagrams
data/raw/v2/ curated source notes with metadata (S01–S12)
data/processed/v2/  chunks.jsonl, scheme_registry.csv, quality_report.json, manifest.json, quarantine.jsonl
src/         pipeline_v2.py (ingest → clean → chunk → validate → store)
evaluation/  seed_test_set_v0.jsonl (20 items, EN/BM pairs)
notebooks/   week3_pipeline.ipynb (Topic 3 lab record)
```

## Weekly Progress
| Week | Focus | Deliverable | Status |
|------|-------|-------------|--------|
| W1 | System map + project scope | README + docs | ✅ |
| W2 | Requirements, evaluation criteria, V1 architecture | `docs/week2_requirements.md`, `week2_evaluation_criteria.md`, `week2_architecture_v1.png`, `week2_architecture_decisions.md` | ✅ |
| W3 | Data ingestion, preparation, validation and repeatable V1 batch pipeline | [Notebook](notebooks/week3_pipeline.ipynb) and [workflow](docs/week3_pipeline_diagram.png) | ✅ |
| W4 | Scope change to school leavers; v2 corpus, data quality rules, coverage and bias review, quality gate | [`src/pipeline_v2.py`](src/pipeline_v2.py), [data quality report](docs/week4_data_quality_report.md) | ✅ |

## Topic 4 · Data quality (v2 corpus)

Run `python src/pipeline_v2.py` from the repository root (standard library only). It ingests 12 source notes, quarantines 1 that fails the scope and usable-content rules, and writes 27 chunks with full lineage. Quality gate: **GO WITH CONDITIONS**. Details in [docs/week4_data_quality_report.md](docs/week4_data_quality_report.md).

## Topic 3 · Data pipeline (lab record, superseded by v2)

BiasiswaBot uses the document pathway with two original TXT notes based on PTPTN’s official education-loan page. Paragraph chunking produced four validated records. Notebook Cell 9 matched source and output fingerprints, sizes, counts and lineage on a second run.

- [Source inventory](docs/week3_data_inventory.md) and [pipeline decisions](docs/week3_pipeline_decisions.md)
- [Executed notebook](notebooks/week3_pipeline.ipynb) and [pipeline diagram](docs/week3_pipeline_diagram.png)
- [Part B prepared data](data/processed/prepared_text.jsonl) and [common lineage manifest](data/week3_manifest.json)
- [Part C prepared data](data/pipeline_v1/documents/prepared_text.jsonl) and [pipeline manifest](data/pipeline_v1/documents/pipeline_manifest.json)

Open the notebook from GitHub in Colab or run it in Jupyter from the repository. It uses Python’s standard library and the tracked TXT notes.
