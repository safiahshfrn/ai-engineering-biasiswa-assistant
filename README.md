# BiasiswaBot — Scholarship & Financial Aid Information Assistant

> A document-grounded AI assistant that answers Malaysian degree holders' postgraduate scholarship and financial-aid questions with citations from official public sources.

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
Malaysian degree holders seeking funding for postgraduate study.

## Data Sources
- MyGOV — Scholarships and Financial Assistance: https://www.malaysia.gov.my/en/categories/school--education/scholarships-and-financial-assistance
- PTPTN official portal: https://www.ptptn.gov.my
- JPA scholarship pages: https://www.jpa.gov.my

## Repository Structure
```
docs/          week1_observation_sheet.md, week1_system_map.png, week1_project_scope.md
data/  src/  notebooks/  evaluation/  prompts/
```

## Weekly Progress
| Week | Focus | Deliverable | Status |
|------|-------|-------------|--------|
| W1 | System map + project scope | README + docs | ✅ |
| W2 | Requirements, evaluation criteria, V1 architecture | `docs/week2_requirements.md`, `week2_evaluation_criteria.md`, `week2_architecture_v1.png`, `week2_architecture_decisions.md` | ✅ |
| W3 | Data ingestion, preparation, validation and repeatable V1 batch pipeline | [Notebook](notebooks/week3_pipeline.ipynb) and [workflow](docs/week3_pipeline_diagram.png) | ✅ |

## Topic 3 · Data pipeline

BiasiswaBot uses the document pathway with two original TXT notes based on PTPTN’s official education-loan page. Paragraph chunking produced four validated records. Notebook Cell 9 matched source and output fingerprints, sizes, counts and lineage on a second run.

- [Source inventory](docs/week3_data_inventory.md) and [pipeline decisions](docs/week3_pipeline_decisions.md)
- [Executed notebook](notebooks/week3_pipeline.ipynb) and [pipeline diagram](docs/week3_pipeline_diagram.png)
- [Part B prepared data](data/processed/prepared_text.jsonl) and [common lineage manifest](data/week3_manifest.json)
- [Part C prepared data](data/pipeline_v1/documents/prepared_text.jsonl) and [pipeline manifest](data/pipeline_v1/documents/pipeline_manifest.json)

Open the notebook from GitHub in Colab or run it in Jupyter from the repository. It uses Python’s standard library and the tracked TXT notes.
