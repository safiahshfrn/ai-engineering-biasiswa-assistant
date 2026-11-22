# BiasiswaBot · Topic 4 data quality report (v2 corpus)

Run: `python src/pipeline_v2.py` · run date pinned to 2026-11-22 · outputs in `data/processed/v2/` · [pipeline figure](week4_pipeline_v2.png) · [coverage figure](week4_coverage.png)

## 1. Data card

| Item | Value |
|---|---|
| Purpose | Knowledge Source for answering school leavers' questions about undergraduate funding, with citations and "who can apply" (FR1, FR2, FR8) |
| Intended users | SPM, STPM/matriculation/foundation and diploma leavers |
| Sources | PTPTN (S01–S04), MARA (S05–S06), BNM (S07–S08), JPA via BERNAMA (S09–S10), MyGOV registry (S11), UTM list (S12, quarantined) |
| Format | Curated English paraphrase notes with a metadata header; providers publish Malay (9 sections) or English (2) HTML |
| Rights / access | Public pages; reuse rights **N.V.** (not verified). Repository stores original paraphrases and metadata, not page copies |
| Personal data | None collected. Privacy rule R8 found 0 IC-number or contact-detail hits |
| Known gaps | No state foundations (Yayasan), no private-sector scholarships, JPA programme conditions not on a primary page, only 2 schemes for STPM/matriculation leavers |

## 2. Quality scorecard

| Dimension | Rule(s) | Result |
|---|---|---|
| Completeness | R1 required metadata, R4 usable content | 12/12 complete metadata; 1 source (S12) has names only → quarantined |
| Consistency | R2 controlled vocabulary, R7 numeric consistency | 0 vocabulary errors; 1 numeric anomaly (S03, MBBS 50% tier) → manual review |
| Accuracy | Manual check of each note against the provider page on 2026-11-22 | 9 primary sections checked; 2 secondary sections (S09, S10) marked N.V. |
| Timeliness | R5 content date | 4 sections dated 13 May 2024 (923 days) → warning; 5 sections undated → manual review |
| Uniqueness | R9 exact and near duplicates | 0 exact, 0 near duplicates (Jaccard ≥ 0.5) |

## 3. Validation and defect findings

| Rule | Severity | Source | Finding | Action / residual risk |
|---|---|---|---|---|
| R3 scope fit, R4 usable content | Hard fail | S12 | UTM list names 8 aid items (incl. staff and postgraduate) with no criteria, levels or dates | Quarantined; replace with a UTM page that states undergraduate criteria |
| R7 numeric consistency | Manual review | S03 | MBBS/dentistry/veterinary row reads 50,000 / 37,500 / 30,000; the 50% tier should be 25,000 by the stated rule. Re-checked on the live page: the page shows 30,000 | Kept as published; answer must cite the page and add a verify notice. Not "fixed" by us |
| R5 timeliness | Warning | S01–S04 | PTPTN page metadata 13 May 2024 | Kept; re-check each intake. Amounts may have changed |
| R5 timeliness | Manual review | S05–S08 | MARA and BNM pages show no content date; BNM heading says "Scholarships 2025" while criteria refer to 2026 | Show retrieval date; treat cycle-specific facts as time-bound |
| R6 provenance | Warning | S09, S10 | JPA portal not retrievable; facts come from BERNAMA reports of JPA statements | Status `secondary_NV`; answer carries "verify on the JPA portal" |
| Manual inspection | Note | S05, S10 | Sources silent on application period, offer requirement (TESP) and per-programme conditions (JPA) | Recorded as `U_NOT_STATED`; FR3/FR8 say "the source does not state" |

## 4. Chunking decision

| Strategy | Chunks | Mean / max chars | Tiny (<80) | Heading kept | Sentences intact |
|---|---|---|---|---|---|
| Fixed 400 chars, 50 overlap | 35 | 319 / 400 | 3 | 0% | 81/90 (90.0%) |
| **Structure-aware, ≤700 chars (selected)** | **27** | **346 / 657** | **0** | **100%** | **90/90 (100%)** |

Observation → strategy → justification: fixed-size chunks split 9 sentences, including the DB40 per-capita income limit (RM5,249), the PTPTN diploma loan-amount row and the GPA ≥ 2.0 condition for continued PTPTN payments. Structure-aware chunks keep each rule whole and carry the section heading for citation. Trade-off: variable length (111–657 chars); a long policy section would need sentence-level splitting, which the code already supports.

## 5. Representation, coverage and bias

- **Coverage by pathway** (figure): SPM leavers are covered by 5 schemes, diploma graduates by 4, STPM and matriculation leavers by only 2 (PTPTN, BNM Kijang Undergraduate). The matrix is an upper bound: pathways and levels are stored as independent lists, so a pair such as "diploma graduate → foundation" is counted even if no source states it. v3 should store explicit (pathway, level) pairs.
- **Representation bias (source selection):** all providers are federal bodies; no state foundations or private-sector scholarships. Students in states with strong Yayasan schemes would be under-served.
- **Group conditions:** 2 of 7 schemes are Bumiputera-only and 1 is B40-only. These are stated eligibility rules, not pipeline bias, but the assistant must state them as written and never infer a user's group (RAI4).
- **Merit vs need:** BNM and JPA PBUA programmes are merit-based (8 As; CGPA ≥ 3.50), DB40 and PTPTN tiers are need-based. A test set drawn only from merit schemes would hide errors on need-based questions, so the seed set covers both.
- **Language:** 9 of 11 accepted sections are Malay-language sources, paraphrased in English. RAI3 parity must be tested in both directions (`evaluation/seed_test_set_v0.jsonl`: 8 EN/BM pairs).
- **Pipeline-introduced bias check:** the only removal was S12 (no criteria). No rule removes short policy text: the smallest kept chunk is 111 chars and R10 flags rather than drops.

## 6. Privacy, rights and governance

| Question | Answer |
|---|---|
| Personal data present? | No. Sources are public policy pages; R8 scan found 0 hits |
| Will data leave the system? | Only public chunk text is sent to the model service. User questions are screened by Scope / Safety Control; IC numbers are refused (seed item T11) |
| Rights | Publicly accessible ≠ public domain → recorded as N.V.; only paraphrased notes are stored |
| Version and change control | `retrieved_on`, `page_last_updated`, `version_label` per source; SHA-256 per input and output in `manifest.json`; refresh trigger = each SPM/STPM results and intake period |
| Owner | Project owner (Wan Safiah); provider pages are owned by each agency |

## 7. Quality gate

**GO WITH CONDITIONS.** The corpus is controlled enough for prototype retrieval and evaluation. Conditions: (1) every answer from S01–S10 shows source, retrieval date and a verify notice; (2) S09–S10 answers say the source is a news report of a JPA statement; (3) the S03 anomaly is never "corrected" by the assistant; (4) before the evaluation run, add at least one state foundation, one private scholarship and one more STPM-relevant scheme, and confirm JPA conditions on a primary page.

## 8. Impact on Topic 2 requirements and evaluation

| Requirement | Data evidence now | Effect on evaluation |
|---|---|---|
| FR2 / RAI2 | Every chunk carries URL, section, retrieval date; 6 chunks `secondary_NV` | Citation-presence check can be automated against chunk metadata |
| FR3 / FR8 | `U_NOT_STATED` recorded for TESP offer rule and JPA conditions | Seed items T07/T08 test "source is silent" and abstention |
| RAI1 | S03 numeric anomaly | Critical-fact set includes PTPTN amounts; expected answer = value as published + verify notice |
| RAI3 | Malay-majority sources | Paired EN/BM items in the seed set; gap threshold ≤ 10 pp unchanged |
