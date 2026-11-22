# Requirements Specification — BiasiswaBot

Version: 1.2 (revised 22 Nov 2026: target users changed from postgraduate degree holders to SPM, STPM/matriculation and diploma leavers; evidence and Section 0a rebuilt from the v2 corpus)

## Section 0 — Project Framing & Application Scope Checkpoint

| Element | Content |
|---|---|
| **Problem Evidence** | Funding for pre-university, diploma and first-degree study comes from several providers, and **when and whether a school leaver can apply differs by scheme**. (1) PTPTN loans require an admission offer from an IPTA, IPTS or polytechnic and a PTPTN-registered course, and the amount depends on household income tier (PTPTN, 2024). (2) JPA's Dermasiswa B40 2026 was opened to SPM 2025 candidates on their results, for B40 households with per-capita income of RM5,249 or less, for only two weeks (3–16 Aug 2026) (BERNAMA, 2026b). (3) MARA's TESP loan is limited to Bumiputera applicants and its page gives no application period (MARA, n.d.). (4) BNM's Kijang Undergraduate Scholarship needs an offer from a BNM-approved university and an STPM, diploma or matriculation CGPA of at least 3.50 (Bank Negara Malaysia, n.d.). (5) The MyGOV portal lists aid but sends users to each provider for the conditions (MyGOV Malaysia, 2026). (6) News reporting notes that students from B40, rural and disabled backgrounds leave their studies because of financial barriers or a lack of information about available aid (Busst, 2026). A school leaver therefore has to read each provider's page to learn whether they can apply now, on results, or only after an offer. |
| **Existing Approaches** | (1) **BarkPlug v.2** (Neupane et al., 2024): RAG chatbot whose corpus includes scholarships and financial aid, evaluated at one university. (2) **hoBIT / proFILL** (Kim et al., 2026): profile-aware RAG for academic advising, because identical questions need different answers depending on department, cohort and degree. (3) **Carolina Guide** (Torkian & Zhou, 2026): RAG system with institutional guardrails (explicit citation, metadata-aware filtering, refusal of personalised planning, student data protection). (4) **Marcel** (Trienes et al., 2025): open-source admissions agent that shows sources and abstains when its documents lack the answer. (5) Agency and university funding pages, which are authoritative but each covers only its own schemes. |
| **Project / Engineering Gap** | The chatbots above work on one institution's own documents. Funding information for school leavers is spread across agencies (PTPTN, JPA, MARA, BNM) and each scheme's availability differs: open on school-leaving results, open only with an admission offer or enrolment, open only to graduates of one institution, or restricted to a stated group. hoBIT shows that a profile-blind answer can be inapplicable, but it solves this by collecting profile attributes. The gap addressed here is practical: **state, with a citation, who each scheme is open to, across several public sources, without storing a user profile and without deciding eligibility.** This is an engineering gap, not a claim of scientific novelty. |
| **Objective O1** | To design a document-grounded AI assistant that answers questions about undergraduate funding (pre-university, diploma and first degree) for Malaysian SPM, STPM/matriculation and diploma leavers using approved public sources, and states who each scheme is open to. |
| **Objective O2** | To develop the assistant with source retrieval, source citation with date, availability metadata, and scope and evidence controls (decline out-of-scope requests, state when evidence is insufficient). |
| **Objective O3** | To evaluate the assistant on answer correctness, citation support, availability accuracy, refusal behaviour, English/BM parity, latency and cost using a curated test set. |
| **Intended Users** | Malaysian **school leavers** looking for funding for pre-university, diploma or first-degree study in Malaysia: SPM leavers, STPM and matriculation/foundation leavers, and diploma graduates moving on to a degree, including those who have results but no admission offer yet. |
| **Supported Tasks** | Answer questions about a scheme's provider, eligibility criteria, benefits, application steps, required documents and deadlines; **state who the scheme is open to: A = apply on school-leaving results, B = admission offer or enrolment required, C = only for students or graduates of a named institution, U = the source does not say, plus any group condition (e.g. B40, Bumiputera) as written**; compare schemes on stated criteria; show the source and date for each answer; answer in English or Bahasa Melayu. |
| **Information / Knowledge Domain** | Undergraduate funding and financial aid for Malaysian school leavers, taken only from approved public documents: PTPTN, JPA, MARA and BNM pages, with MyGOV used as a registry for finding schemes. University pages are admitted only if they state criteria (see `docs/week4_data_quality_report.md`). |
| **Operating Context** | A web chat interface used on a laptop or phone, mainly around SPM/STPM results and intake periods, when application windows are short. V1 is a course prototype, not a deployed service. |
| **Important Constraints** | Public documents only; links and metadata are stored in the repository, not copyrighted files; information changes over time (deadlines, eligibility, availability); one-semester timeline; low budget (free or low-cost tiers); must run locally or in Google Colab; no personal data collected. |
| **Explicit Out-of-Scope Tasks** | Deciding whether a person is eligible; recommending the scheme a specific person should choose; financial, legal or tax advice; submitting or filling in applications; collecting or storing IC numbers, income or other personal data; schemes for international students; **postgraduate (Master's and PhD) funding**; schemes not in the indexed sources. |
| **Evaluation Focus** | Can the assistant give correct, source-cited answers about undergraduate funding in English and Bahasa Melayu, state correctly who each scheme is open to, decline out-of-scope requests, and stay within latency and cost limits, so that a school leaver can trust and verify the information? |

### Section 0a — Availability check: who can apply, and when?

Rebuilt from the v2 corpus (`data/processed/v2/scheme_registry.csv`). Categories: **A** = apply on school-leaving results (no admission offer stated as required); **B** = requires an admission offer or enrolment; **C** = only for students or graduates of a named institution; **U** = the source does not say. Group conditions are recorded separately.

| Scheme | Who it is open to (from the source) | Type | Group condition | Source |
|---|---|---|---|---|
| PTPTN education loan | Citizens aged 45 or below with an offer from an IPTA, IPTS or polytechnic and a PTPTN-registered course; parents' gross income ≤ RM50,000 after RM250 per dependant | B | none | PTPTN (2024) |
| JPA Dermasiswa B40 2026 | SPM 2025 first-time candidates under 19 (20 for transition class), going to diploma study | A | B40 (per capita ≤ RM5,249) | BERNAMA (2026b) — secondary, primary portal not retrievable |
| MARA TESP | SPM, certificate and diploma leavers going to diploma (age < 30) or degree (age < 40) | U (offer not mentioned) | Bumiputera | MARA (n.d.) |
| MARA Program Pelajar Cemerlang | Outstanding IPMa graduates, CGPA ≥ 3.90 | C | Bumiputera | MARA (n.d.) |
| BNM Kijang Pre-University | SPM leavers with ≥ 8 As, age ≤ 19 on 1 July 2026 | A | none | Bank Negara Malaysia (n.d.) |
| BNM Kijang Undergraduate | STPM/diploma/matriculation/foundation CGPA ≥ 3.50 with an offer from a BNM-approved university, age ≤ 22 | B | none | Bank Negara Malaysia (n.d.) |

**Finding:** two of the six schemes can be applied for on results alone, two require an offer, one is institution-specific, and for MARA TESP the source is silent. This is why FR8 requires the assistant to state the availability condition from the source and to say when the source is silent rather than assume.

## Section 1 — Functional Requirements

| # | Requirement — The system SHALL | Scope Boundary — SHALL NOT (where relevant) |
|---|---|---|
| **FR1** | Answer questions about a scheme's provider, eligibility criteria, benefits, application steps, required documents and deadlines, using the approved source documents. | Invent schemes, criteria, amounts or dates that are not in the source documents. |
| **FR2** | Provide a source reference (document title, URL, and section or page where available) and the date the source was retrieved for every document-based answer. | Present unsupported information as if it came from an approved source. |
| **FR3** | State clearly when the approved sources do not contain enough information to answer, and direct the user to the official agency page. | Guess an answer to fill the gap. |
| **FR4** | Accept questions in English or Bahasa Melayu and reply in the language of the question. | — |
| **FR5** | Compare two or more schemes on stated criteria (eligibility, availability, benefit, deadline) in a structured format when asked. | Rank schemes or say which one a specific user should choose. |
| **FR6** | Decline out-of-scope requests (eligibility decisions, financial or legal advice, submitting applications, schemes outside the sources) and redirect the user to the relevant agency or university financial-aid office. | Decide whether a person is eligible for a scheme. |
| **FR7** | Present answers in clear, plain language for school leavers, with the key fact (deadline, eligibility condition or availability) stated first. | — |
| **FR8** | State, for each scheme it describes, who the scheme is open to (open to eligible applicants generally, requires an admission offer or enrolment, or only for students registered at a named university) and the condition as written in the source. | Assume or infer availability that the source does not state; if the source is silent, say so. |

## Section 2 — Non-Functional Requirements

| # | Quality Attribute | Requirement | Measurement Method | Metric | Threshold |
|---|---|---|---|---|---|
| **NFR1** | Performance | The system shall keep interactive responses within the agreed latency target. | Measure end-to-end latency over a defined workload of 30 test questions. | p90 latency | < 5,000 ms |
| **NFR2** | Correctness | Answers shall be factually consistent with the approved source documents. | Score a curated test set of at least 30 questions against a rubric, with answers verified from the sources. | Correct response rate (%) | ≥ 80% |
| **NFR3** | Reliability | The system shall give consistent answers when the same question is asked repeatedly. | Ask each of 20 questions 3 times and compare the key facts in the answers. | Key-fact agreement across runs (%) | ≥ 90% |
| **NFR4** | Cost | Inference cost shall stay within the project budget. | Record model/API usage over the 30-question evaluation workload. | Cost per 100 queries | < US$0.50 per 100 queries (illustrative; to be refined) |
| **NFR5** | Maintainability | Updated source documents shall be incorporated without rebuilding unrelated components. | Run a controlled document-update test: replace one document and check that answers change. | Update time | < 15 min |

## Section 3 — Responsible AI Requirements

| # | Responsible AI Risk | Requirement | Measurement Method | Metric | Threshold |
|---|---|---|---|---|---|
| **RAI1** | Hallucination / wrong eligibility, availability, amount or deadline | The system shall state eligibility, availability, amount and deadline facts correctly or abstain. | Run a "critical-fact" subset of at least 15 questions (including who each scheme is open to) whose answers are verified in the sources. | Critical-fact accuracy; number of invented schemes | ≥ 95%; 0 invented schemes |
| **RAI2** | Outdated information | Every answer that includes a deadline, eligibility rule or availability condition shall show the source date and a notice to verify with the official source. | Inspect answers to a time-sensitive question subset. | Share of answers with source date and verify notice | 100% |
| **RAI3** | Fairness / language | Answer quality shall not differ beyond the agreed tolerance between English and Bahasa Melayu questions. | Ask the same questions in both languages and compare correctness rates. | Absolute correctness-rate gap (EN vs BM) | ≤ 10 percentage points |
| **RAI4** | Privacy | The system shall not request, store or send personal data (IC number, income, contact details) to external model APIs. | Run at least 10 privacy test prompts containing fake personal data and inspect the outgoing API payloads and logs. | Number of personal-data transmissions or stored records | 0 |
| **RAI5** | Misuse / out-of-scope decisions | The system shall refuse out-of-scope requests, including eligibility decisions, and redirect the user. | Run a safety/scope test set of at least 20 out-of-scope queries. | Refusal-and-redirect success rate | ≥ 95% |

## Reflection — Which Responsible AI requirement will be the most difficult to measure or enforce technically?

RAI3 (English/Bahasa Melayu fairness) will be the hardest. To measure it I need a paired test set with the same questions in both languages and verified answers (a 16-item paired seed set is in `evaluation/seed_test_set_v0.jsonl`). The v2 corpus reversed my Week 2 assumption: 9 of the 11 accepted source sections are in Malay and only the BNM pages are in English, while the curated notes are English paraphrases. So retrieval must work across languages in both directions, and English questions about MARA or JPA could retrieve weaker evidence. A small test set also makes the gap noisy: with 30 questions, one question changes the correctness rate by about 3 percentage points.

## References

Bank Negara Malaysia. (n.d.). *Scholarships*. Retrieved November 22, 2026, from https://www.bnm.gov.my/careers/scholarships

BERNAMA. (2026a, June 19). *JPA tawar 640 slot penajaan lepasan SPM 2026, perkukuh pembangunan bakat negara*. https://www.bernama.com/bm/news.php?id=2570294

BERNAMA. (2026b, August 5). *JPA buka permohonan Program Dermasiswa B40 (DB40) tahun 2026*. https://bernama.com/bm/news.php?id=2590472

Busst, N. (2026, January 6). Govt scholarships open doors for students in need. *Free Malaysia Today*. https://www.freemalaysiatoday.com/category/nation/2026/01/06/govt-scholarships-open-doors-for-students-in-need

Kim, Y., Lee, S., Kim, J., & Kang, S. (2026). *hoBIT: A profile-aware retrieval-augmented chatbot for university academic advising* (arXiv:2608.26604). arXiv. https://arxiv.org/pdf/2608.26604

Majlis Amanah Rakyat. (n.d.). *Pembiayaan pelajaran: Peringkat diploma & ijazah*. Retrieved November 22, 2026, from https://www.mara.gov.my/bm/pendidikan/pembiayaan-pelajaran/peringkat-diploma-ijazah/

MyGOV Malaysia. (2026). *Bantuan kewangan pengajian tinggi*. Retrieved November 22, 2026, from https://www.malaysia.gov.my/my/categories/sekolah--pendidikan/penajaan-dan-bantuan-kewangan/bantuan-kewangan-pengajian-tinggi

Neupane, S., Hossain, E., Keith, J., Tripathi, H., Ghiasi, F., Golilarz, N. A., Amirlatifi, A., Mittal, S., & Rahimi, S. (2024). *From questions to insightful answers: Building an informed chatbot for university resources* (arXiv:2405.08120). arXiv. https://arxiv.org/abs/2405.08120

Perbadanan Tabung Pendidikan Tinggi Nasional. (2024). *Pinjaman pendidikan*. Retrieved November 22, 2026, from https://www.ptptn.gov.my/pinjaman-pendidikan/

Torkian, B., & Zhou, J. (2026). *Carolina Guide: A multi-agent RAG system with institutional guardrails for academic policy assistance* (arXiv:2606.28360). arXiv. https://arxiv.org/pdf/2606.28360

Trienes, J., Derzhanskaia, A., Schwarzkopf, R., Mühling, M., Schlötterer, J., & Seifert, C. (2025). *Marcel: A lightweight and open-source conversational agent for university student support* (arXiv:2507.13937). arXiv. https://arxiv.org/abs/2507.13937
