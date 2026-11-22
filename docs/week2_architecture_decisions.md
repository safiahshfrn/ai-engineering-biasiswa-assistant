# Architecture Decisions & Traceability — BiasiswaBot

Version: 1.2 (revised 22 Nov 2026: target users changed to SPM, STPM/matriculation and diploma leavers). Diagram: `docs/proposal_architecture_v2.png` (V2, replaces the Week 2 V1 diagram, whose user box still reads "Degree Holder")

## Architecture Needs from Requirements

| Requirement ID | What does the requirement need? | Architecture Response |
|---|---|---|
| FR1 / NFR2 | Answers must come from approved funding documents, not from general model knowledge. | Knowledge Source and Knowledge Access |
| FR2 / RAI2 | Every answer needs a source and a date. | Source metadata kept with the Knowledge Source; Citation & Evidence Control |
| FR3 / RAI1 | The system must say when evidence is insufficient and must not guess critical facts. | Citation & Evidence Control (abstain) |
| FR8 / RAI1 | Each scheme must state who it is open to: A = apply on school-leaving results (no offer stated as required), B = admission offer or enrolment required, C = only for students or graduates of a named institution, U = the source does not say; plus any group condition (e.g. B40, Bumiputera) as written. | "Who can apply" metadata stored with each document in the Knowledge Source; Citation & Evidence Control checks the statement against the source |
| FR6 / RAI5 / RAI4 | Out-of-scope requests must be refused and personal data must not be collected. | Scope / Safety Control |
| FR4 / RAI3 | Questions in English and Bahasa Melayu must be handled with similar quality. | Language Model Service that answers in the user's language; matched test set |
| NFR5 / RAI2 | Changed documents must be refreshed without rebuilding everything. | Source Update Process |
| NFR1 / NFR4 / all evaluated requirements | Latency, cost and quality must be measurable. | Evaluation Point (test set and logs) |

## Architecture Decision Records

| # | Decision | Requirement / Constraint | Alternatives Considered | Selected Option | Trade-off Accepted |
|---|---|---|---|---|---|
| ADR1 | Include knowledge access over approved sources | FR1, FR2, NFR2; rules change and are scattered across agencies and universities | Base model only; static FAQ or keyword search; dynamic knowledge access | Generic knowledge-access component over approved documents | More system complexity and an index to maintain, in return for grounded and traceable answers. |
| ADR2 | Include an explicit scope/safety control before the answer is generated, and keep the assistant stateless (no user profile) | FR6, RAI4, RAI5 | Instruction in the prompt only; explicit control; personalised eligibility checker using income | Explicit scope control, no personal profile | Possible false refusals, extra processing time, and no personalised "you qualify" answers, in return for fewer wrong decisions and no personal data handling. |
| ADR3 | Include a citation and evidence check after generation that can abstain | FR2, FR3, RAI1, RAI2 | Trust the model to cite correctly; check after generation | Post-generation evidence control with abstention | Extra latency (affects NFR1) and some answerable questions will be withheld, in return for fewer wrong deadlines or eligibility facts. |
| ADR4 | Separate the source update process from the rest of the system | NFR5, RAI2; deadlines change | One-time static index; full rebuild on each change; incremental refresh with retrieval date | Incremental refresh that stores the retrieval date | Ongoing maintenance effort, in return for fresher answers and a visible date. |
| ADR5 | Store "who can apply" metadata with each document and state the condition, instead of collecting a user profile | FR8, RAI1, RAI4; availability differs by scheme (Section 0a of the requirements) | Ignore availability; profile-aware retrieval that asks for department, cohort or degree as in hoBIT (Kim et al., 2026); availability metadata plus stated condition | Availability metadata and a stated condition | The assistant cannot automatically narrow results to "schemes you can apply for", and the user must read the condition. In return, no personal profile is collected or stored, which protects privacy (RAI4). A status typed in the current question may be used in that session only and is never stored. |

## Initial Requirements Traceability Matrix

| Objective | Requirement | Evaluation Criterion | Architecture Element | Later Evidence |
|---|---|---|---|---|
| O1 | FR1, FR2, NFR2 | Answer correctness; citation support | Knowledge Source, Knowledge Access | Week 3–4 retrieval test; `evaluation/` correctness results on the 30-question set |
| O2 | FR3, RAI1, RAI2 | Critical-fact accuracy and abstention | Citation & Evidence Control | `evaluation/` critical-fact results; sample answers showing dates and verify notices |
| O2 | FR8, RAI1 | Availability accuracy (who can apply) | Knowledge Source (who-can-apply metadata), Citation & Evidence Control | `evaluation/` availability test (at least 10 questions); metadata table of verified schemes |
| O2 | FR6, RAI4, RAI5 | Out-of-scope refusal | Scope / Safety Control | `evaluation/` refusal test (at least 20 queries); privacy payload check |
| O3 | RAI3, FR4 | English/BM answer parity | Language Model Service, Knowledge Source | `evaluation/` paired EN/BM results |
| O3 | NFR1, NFR4 | Latency; cost | Evaluation Point (logs) | `evaluation/` latency and cost log over the workload |

## Final Review Checklist

- **Does each major component support a requirement or evaluation need?** Yes. Each component in the diagram carries the FR / NFR / RAI tags it supports.
- **Is any important data source, safety control or evaluation point missing?** The approved document list is still incomplete: the official PTPTN pages have not been read directly, and no scheme open without an admission offer or registration has been verified yet (Section 0a of the requirements). A Bahasa Melayu source set is not yet defined (see RAI3).
- **Have I added any technology or component that is not yet justified?** No. All components are named by function and tied to a requirement, and no model, retrieval method or tool is chosen yet.
- **Is there a simpler architecture that could still satisfy the requirements?** A model-only chatbot is simpler but cannot meet FR1, FR2, FR8 or RAI1, because it has no approved sources, dates, availability metadata or evidence check.

## Reflection — Which architecture decision involved the most important trade-off?

ADR3, the citation and evidence control that can abstain. It is driven by RAI1 (critical-fact accuracy ≥ 95%) and FR3 (say when evidence is insufficient). The trade-off I accept is extra latency, which counts against NFR1, and some questions the model could answer will be withheld because the evidence is weak. For funding information I prefer "I could not confirm this, check the official page" over a fluent but wrong deadline or availability condition. ADR5 is a close second, because choosing not to collect a profile means the user has to read the availability condition themselves.

## References

Kim, Y., Lee, S., Kim, J., & Kang, S. (2026). *hoBIT: A profile-aware retrieval-augmented chatbot for university academic advising* (arXiv:2608.26604). arXiv. https://arxiv.org/pdf/2608.26604

## Topic 3 evidence

The [data inventory](week3_data_inventory.md) maps FR1, FR2 and FR8 to two sections of PTPTN’s official education-loan page. The [pipeline decisions](week3_pipeline_decisions.md) and [executed workflow](week3_pipeline_diagram.png) show the Knowledge Source preparation step for ADR1 and the pinned-source approach for ADR4.

## Topic 4 evidence (proposal, v2 corpus)

After the scope change, the Knowledge Source is rebuilt from undergraduate funding sources by `src/pipeline_v2.py`: 12 notes ingested, 11 accepted, 1 quarantined, 27 chunks, quality gate GO WITH CONDITIONS. The "who can apply" field required by ADR5 is now stored per scheme in [`data/processed/v2/scheme_registry.csv`](../data/processed/v2/scheme_registry.csv). See the [Topic 4 data quality report](week4_data_quality_report.md).
