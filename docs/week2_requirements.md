# Requirements Specification — BiasiswaBot

Version: 1.1 (Week 2, revised after lecturer feedback)

## Section 0 — Project Framing & Application Scope Checkpoint

| Element | Content |
|---|---|
| **Problem Evidence** | Funding for postgraduate study in Malaysia comes from several bodies, and **who can apply differs by scheme**, which a degree holder cannot tell from the scheme name. (1) PTPTN financing requires an admission offer and enrolment on a programme approved by the Ministry and accredited by MQA (University of Reading Malaysia, n.d.; Asia Pacific University of Technology & Innovation, n.d.). (2) Universiti Malaya's postgraduate fee-reduction scheme is open only to Malaysian citizens registered as UM Master's or doctoral students with no other scholarship (Universiti Malaya, 2024). (3) The University of Aberdeen's David Stewart Scholarship (2024 intake) requires an offer of a place at Aberdeen and is held only there (University of Aberdeen, n.d.). (4) MyGOV lists assistance from several providers with different conditions (MyGOV Malaysia, n.d.). A degree holder who has not yet been admitted has to read each scheme's conditions just to find out whether it is open to them. |
| **Existing Approaches** | (1) **BarkPlug v.2** (Neupane et al., 2024): RAG chatbot whose corpus includes scholarships and financial aid, evaluated at one university. (2) **hoBIT / proFILL** (Kim et al., 2026): profile-aware RAG for academic advising, because identical questions need different answers depending on department, cohort and degree. (3) **Carolina Guide** (Torkian & Zhou, 2026): RAG system with institutional guardrails (explicit citation, metadata-aware filtering, refusal of personalised planning, student data protection). (4) **Marcel** (Trienes et al., 2025): open-source admissions agent that shows sources and abstains when its documents lack the answer. (5) Agency and university funding pages, which are authoritative but each covers only its own schemes. |
| **Project / Engineering Gap** | The chatbots above work on one institution's own documents. Funding information for degree holders is spread across agencies and universities, and each scheme's availability differs: open to eligible applicants generally, open only with an admission offer or enrolment, or open only to students registered at one university. hoBIT shows that a profile-blind answer can be inapplicable, but it solves this by collecting profile attributes. The gap addressed here is practical: **state, with a citation, who each scheme is open to, across several public sources, without storing a user profile and without deciding eligibility.** This is an engineering gap, not a claim of scientific novelty. |
| **Objective O1** | To design a document-grounded AI assistant that answers questions about postgraduate funding for Malaysian degree holders using approved public sources, and states who each scheme is open to. |
| **Objective O2** | To develop the assistant with source retrieval, source citation with date, availability metadata, and scope and evidence controls (decline out-of-scope requests, state when evidence is insufficient). |
| **Objective O3** | To evaluate the assistant on answer correctness, citation support, availability accuracy, refusal behaviour, English/BM parity, latency and cost using a curated test set. |
| **Intended Users** | Malaysian **degree holders** (bachelor's graduates), including those not yet admitted to a university, who are looking for funding for postgraduate (Master's or PhD) study in Malaysia. |
| **Supported Tasks** | Answer questions about a scheme's provider, eligibility criteria, benefits, application steps, required documents and deadlines; **state who the scheme is open to and the condition (open to eligible applicants generally / requires an admission offer or enrolment / only for students registered at a named university)**; compare schemes on stated criteria; show the source and date for each answer; answer in English or Bahasa Melayu. |
| **Information / Knowledge Domain** | Postgraduate funding and financial aid for Malaysian degree holders, taken only from approved public documents: PTPTN official pages, the Ministry of Higher Education scholarship portal, MyGOV, and university postgraduate funding pages (exact documents to be recorded in Week 3). |
| **Operating Context** | A web chat interface used on a laptop or phone, mainly around postgraduate application and funding periods. V1 is a course prototype, not a deployed service. |
| **Important Constraints** | Public documents only; links and metadata are stored in the repository, not copyrighted files; information changes over time (deadlines, eligibility, availability); one-semester timeline; low budget (free or low-cost tiers); must run locally or in Google Colab; no personal data collected. |
| **Explicit Out-of-Scope Tasks** | Deciding whether a person is eligible; recommending the scheme a specific person should choose; financial, legal or tax advice; submitting or filling in applications; collecting or storing IC numbers, income or other personal data; schemes for international students; undergraduate (diploma and first-degree) funding; schemes outside Malaysia or not in the indexed sources. |
| **Evaluation Focus** | Can the assistant give correct, source-cited answers about postgraduate funding in English and Bahasa Melayu, state correctly who each scheme is open to, decline out-of-scope requests, and stay within latency and cost limits, so that a degree holder can trust and verify the information? |

### Section 0a — Availability check: is each scheme open to all, or only to registered students?

Checked on three schemes. The categories are: **A** = open to eligible applicants without an admission offer or registration; **B** = requires an admission offer or enrolment at a recognised institution; **C** = only for students registered at one named university.

| Scheme | Who it is open to (from the source) | Type | Source |
|---|---|---|---|
| PTPTN education financing (including postgraduate) | Applicants with an admission offer who are enrolled on a full-time programme approved by the Ministry and accredited by MQA. An older PTPTN terms document also states an age limit of 45. | B | University of Reading Malaysia (n.d.); Asia Pacific University of Technology & Innovation (n.d.); Universiti Pendidikan Sultan Idris (n.d., older document) |
| Universiti Malaya postgraduate fee-reduction scheme (disabled and senior-citizen candidates) | Malaysian citizens registered as UM Master's or PhD students, with no other scholarship or sponsorship. | C | Universiti Malaya (2024) |
| David Stewart Scholarship, University of Aberdeen (2024 intake) | Malaysian nationals with an offer of a place at Aberdeen and a recognised Malaysian degree, who are self-funded and not receiving Malaysian Government assistance. | B and C (one specific overseas university) | University of Aberdeen (n.d.) |

**Finding:** in these three, none is open to someone who has not yet been admitted or registered. No type-A scheme for Malaysian degree holders has been verified yet. This is why FR8 requires the assistant to state the availability condition from the source and never assume it.

**Still to verify:** (1) read the official PTPTN pages directly, since this check used institutional pages and an older terms document; secondary guides also report that PTPTN postgraduate financing applies to public universities only, which must be confirmed on the official site before it is used as a fact; (2) find at least one type-A scheme and several more type-B and type-C schemes before building the test set.

## Section 1 — Functional Requirements

| # | Requirement — The system SHALL | Scope Boundary — SHALL NOT (where relevant) |
|---|---|---|
| **FR1** | Answer questions about a scheme's provider, eligibility criteria, benefits, application steps, required documents and deadlines, using the approved source documents. | Invent schemes, criteria, amounts or dates that are not in the source documents. |
| **FR2** | Provide a source reference (document title, URL, and section or page where available) and the date the source was retrieved for every document-based answer. | Present unsupported information as if it came from an approved source. |
| **FR3** | State clearly when the approved sources do not contain enough information to answer, and direct the user to the official agency page. | Guess an answer to fill the gap. |
| **FR4** | Accept questions in English or Bahasa Melayu and reply in the language of the question. | — |
| **FR5** | Compare two or more schemes on stated criteria (eligibility, availability, benefit, deadline) in a structured format when asked. | Rank schemes or say which one a specific user should choose. |
| **FR6** | Decline out-of-scope requests (eligibility decisions, financial or legal advice, submitting applications, schemes outside the sources) and redirect the user to the relevant agency or university financial-aid office. | Decide whether a person is eligible for a scheme. |
| **FR7** | Present answers in clear, plain language for degree holders, with the key fact (deadline, eligibility condition or availability) stated first. | — |
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

RAI3 (English/Bahasa Melayu fairness) will be the hardest. To measure it I need a paired test set with the same questions in both languages and verified answers, but most official sources are in English, so Bahasa Melayu questions may retrieve weaker evidence for reasons that are not about the model itself. A small test set also makes the gap noisy: with 30 questions, one question changes the correctness rate by about 3 percentage points. Enforcing it is harder still, because fixing the gap may need Bahasa Melayu source documents or retrieval that works across languages, which I may not have in one semester.

## References

Asia Pacific University of Technology & Innovation. (n.d.). *National Higher Education Fund / Perbadanan Tabung Pendidikan Tinggi Nasional (PTPTN)*. Retrieved [date], from https://training.apiit.edu.my/ptptninfo

Kim, Y., Lee, S., Kim, J., & Kang, S. (2026). *hoBIT: A profile-aware retrieval-augmented chatbot for university academic advising* (arXiv:2608.26604). arXiv. https://arxiv.org/pdf/2608.26604

MyGOV Malaysia. (n.d.). *Scholarships and financial assistance*. Retrieved [date], from https://www.malaysia.gov.my/en/categories/school--education/scholarships-and-financial-assistance

Neupane, S., Hossain, E., Keith, J., Tripathi, H., Ghiasi, F., Golilarz, N. A., Amirlatifi, A., Mittal, S., & Rahimi, S. (2024). *From questions to insightful answers: Building an informed chatbot for university resources* (arXiv:2405.08120). arXiv. https://arxiv.org/abs/2405.08120

Torkian, B., & Zhou, J. (2026). *Carolina Guide: A multi-agent RAG system with institutional guardrails for academic policy assistance* (arXiv:2606.28360). arXiv. https://arxiv.org/pdf/2606.28360

Trienes, J., Derzhanskaia, A., Schwarzkopf, R., Mühling, M., Schlötterer, J., & Seifert, C. (2025). *Marcel: A lightweight and open-source conversational agent for university student support* (arXiv:2507.13937). arXiv. https://arxiv.org/abs/2507.13937

Universiti Malaya. (2024). *Skim pengurangan yuran orang kurang upaya dan warga emas calon pascasiswazah* [Fee reduction scheme for disabled and senior-citizen postgraduate candidates]. https://masd.um.edu.my/skim-pengurangan-yuran-orang-kurang-upaya-dan-warga-emas-calon-pascasiswazah

Universiti Pendidikan Sultan Idris. (n.d.). *Maklumat PTPTN baru: Terma dan syarat permohonan pembiayaan pendidikan PTPTN* [Older document; verify current terms]. https://www.upsi.edu.my/kemasukan/maklumat_am/ismfeb1415/pdf/MAKLUMAT_PTPTN_BARU.pdf

University of Aberdeen. (n.d.). *David Stewart Scholarship* [2024 intake]. https://www.abdn.ac.uk/funding/124

University of Reading Malaysia. (n.d.). *National Higher Education Fund: Perbadanan Tabung Pendidikan Tinggi Nasional (PTPTN)*. Retrieved [date], from https://www.reading.edu.my/admissions/funding-2/ptptn
