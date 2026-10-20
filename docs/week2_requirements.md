# Requirements Specification — BiasiswaBot

Version: 1.0 (Week 2)

## Section 0 — Project Framing & Application Scope Checkpoint

| Element | Content |
|---|---|
| **Problem Evidence** | Scholarship and financial-aid information for Malaysian undergraduates is spread across separate providers with different conditions. (1) MyGOV Malaysia lists assistance from several providers (e.g. JPA, PTPK), each with its own conditions such as income limits and "no other sponsorship": https://www.malaysia.gov.my/en/categories/school--education/scholarships-and-financial-assistance (2) Universities restate PTPTN rules with institution-specific details such as application windows and GPA conditions: https://www.hw.ac.uk/malaysia/study/fees-and-funding/scholarships/national-higher-education-fund-ptptn and https://new.apu.edu.my/national-higher-education-fund-perbadanan-tabung-pendidikan-tinggi-nasional-ptptn. A student must read and cross-check several pages to find the right scheme. |
| **Existing Approaches** | (1) Chen et al. (2024) — RAG admission chatbot: gives grounded answers about admissions at three universities. (2) Trienes et al. (2025) — Marcel: open-source student-support agent for enrolment questions about one programme. (3) Siragusa et al. (2024) — Unipa-GPT: chatbot answering questions from one university's website in Italian. (4) Agency portals and FAQ pages (MyGOV, PTPTN, JPA): authoritative, but each covers its own scheme and the student must compare them manually. |
| **Project / Engineering Gap** | The approaches above serve one institution or one agency. None of them (in this initial scan) combines scholarship and financial-aid rules from several Malaysian agencies, shows the source and date for every answer, handles English and Bahasa Melayu questions, and declines to make eligibility decisions. This is a practical engineering gap in grounding, traceability and scope control, not a claim of scientific novelty. |
| **Objective O1** | To design a document-grounded AI assistant that answers scholarship and financial-aid questions using approved public Malaysian sources. |
| **Objective O2** | To develop the assistant with source retrieval, source citation with date, and scope and evidence controls (decline out-of-scope requests, state when evidence is insufficient). |
| **Objective O3** | To evaluate the assistant on answer correctness, citation support, refusal behaviour, English/BM parity, latency and cost using a curated test set. |
| **Intended Users** | Malaysian undergraduate students (especially first- and second-year students at public universities) and prospective students looking for scholarships and financial aid. |
| **Supported Tasks** | Answer questions about a scheme's provider, eligibility criteria, benefits, application steps, required documents and deadlines; compare two or more schemes on stated criteria; show the source and date for each answer; answer in English or Bahasa Melayu. |
| **Information / Knowledge Domain** | Scholarship and financial-aid schemes for Malaysian undergraduates, taken only from approved public documents (MyGOV, PTPTN, JPA and similar official pages). |
| **Operating Context** | A web chat interface used by a student on a laptop or phone, mainly around scholarship and loan application periods. V1 is a course prototype, not a deployed service. |
| **Important Constraints** | Public documents only; links and metadata are stored in the repository, not copyrighted files; information changes over time (deadlines, eligibility); one-semester timeline; low budget (free or low-cost tiers); work must run locally or in Google Colab; no personal data collected. |
| **Explicit Out-of-Scope Tasks** | Deciding whether a person is eligible; recommending the scheme a specific person should choose; financial, legal or tax advice; submitting or filling in applications; collecting or storing IC numbers, income or other personal data; schemes outside Malaysia or not in the indexed sources. |
| **Evaluation Focus** | Can the assistant give correct, source-cited answers about scholarships and financial aid in English and Bahasa Melayu, decline out-of-scope requests, and stay within latency and cost limits, so that a student can trust and verify the information? |

## Section 1 — Functional Requirements

| # | Requirement — The system SHALL | Scope Boundary — SHALL NOT (where relevant) |
|---|---|---|
| **FR1** | Answer questions about a scheme's provider, eligibility criteria, benefits, application steps, required documents and deadlines, using the approved source documents. | Invent schemes, criteria, amounts or dates that are not in the source documents. |
| **FR2** | Provide a source reference (document title, URL, and section or page where available) and the date the source was retrieved for every document-based answer. | Present unsupported information as if it came from an approved source. |
| **FR3** | State clearly when the approved sources do not contain enough information to answer, and direct the user to the official agency page. | Guess an answer to fill the gap. |
| **FR4** | Accept questions in English or Bahasa Melayu and reply in the language of the question. | — |
| **FR5** | Compare two or more schemes on stated criteria (eligibility, benefit, deadline) in a structured format when asked. | Rank schemes or say which one a specific user should choose. |
| **FR6** | Decline out-of-scope requests (eligibility decisions, financial or legal advice, submitting applications, schemes outside the sources) and redirect the user to the relevant agency or university financial-aid office. | Decide whether a person is eligible for a scheme. |
| **FR7** | Present answers in clear, plain language for undergraduate students, with the key fact (deadline or eligibility condition) stated first. | — |

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
| **RAI1** | Hallucination / wrong eligibility, amount or deadline | The system shall state eligibility, amount and deadline facts correctly or abstain. | Run a "critical-fact" subset of at least 15 questions whose answers are verified in the sources. | Critical-fact accuracy; number of invented schemes | ≥ 95%; 0 invented schemes |
| **RAI2** | Outdated information | Every answer that includes a deadline or eligibility rule shall show the source date and a notice to verify with the official source. | Inspect answers to a time-sensitive question subset. | Share of answers with source date and verify notice | 100% |
| **RAI3** | Fairness / language | Answer quality shall not differ beyond the agreed tolerance between English and Bahasa Melayu questions. | Ask the same questions in both languages and compare correctness rates. | Absolute correctness-rate gap (EN vs BM) | ≤ 10 percentage points |
| **RAI4** | Privacy | The system shall not request, store or send personal data (IC number, income, contact details) to external model APIs. | Run at least 10 privacy test prompts containing fake personal data and inspect the outgoing API payloads and logs. | Number of personal-data transmissions or stored records | 0 |
| **RAI5** | Misuse / out-of-scope decisions | The system shall refuse out-of-scope requests, including eligibility decisions, and redirect the user. | Run a safety/scope test set of at least 20 out-of-scope queries. | Refusal-and-redirect success rate | ≥ 95% |

## Reflection — Which Responsible AI requirement will be the most difficult to measure or enforce technically?

RAI3 (English/Bahasa Melayu fairness) will be the hardest. To measure it I need a paired test set with the same questions in both languages and verified answers, but most official sources are in English, so Bahasa Melayu questions may retrieve weaker evidence for reasons that are not about the model itself. A small test set also makes the gap noisy: with 30 questions, one question changes the correctness rate by about 3 percentage points. Enforcing it is harder still, because fixing the gap may need Bahasa Melayu source documents or retrieval that works across languages, which I may not have in one semester.
