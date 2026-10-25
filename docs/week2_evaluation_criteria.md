# Evaluation Criteria — BiasiswaBot

Version: 1.1 (Week 2, revised after lecturer feedback)

| Objective / Requirement ID | Evaluation Criterion | Capability Bucket | Measurement Method | Metric | Threshold | User / Business Outcome |
|---|---|---|---|---|---|---|
| O3 / FR1 / NFR2 | Answer correctness | Domain-specific capability | Score a curated set of at least 30 supported scholarship questions against a rubric verified from the sources. | Correct response rate | ≥ 80% | Degree holders get sufficiently reliable answers about schemes, eligibility and steps. |
| O2 / FR3 / RAI1 | Critical-fact accuracy and abstention | Domain-specific capability | Run a subset of at least 15 questions on eligibility, amounts and deadlines; check each answer is correct or abstains. | Critical-fact accuracy; invented schemes | ≥ 95%; 0 invented | Degree holders do not miss a deadline or apply for the wrong scheme because of a wrong answer. |
| O2 / FR2 / RAI2 | Source citation and support | Instruction-following capability | Inspect document-based answers for a source reference and date, then check that the cited source supports the answer. | Citation presence rate; citation-source match rate | 100% presence; ≥ 90% match | Degree holders can verify every answer against the official page. |
| O2 / FR8 / RAI1 | Availability accuracy (who can apply) | Domain-specific capability | Run at least 10 questions asking who a scheme is open to (including a user who says they have a degree but no admission offer yet); check the stated availability type and condition against the source. | Availability accuracy | ≥ 95% | Degree holders do not spend time on schemes they cannot apply for. |
| O2 / FR6 / RAI5 | Out-of-scope refusal | Instruction-following capability | Run at least 20 out-of-scope queries (eligibility decisions, financial advice, submitting applications). | Refusal-and-redirect success rate | ≥ 95% | Degree holders are not given eligibility decisions or advice the system is not able to give. |
| O3 / RAI3 | English/BM answer parity | Domain-specific capability | Ask matched questions in English and Bahasa Melayu and compare correctness. | Absolute correctness-rate gap | ≤ 10 percentage points | Degree holders get similar quality whichever language they use. |
| O1 / FR7 | Response clarity | Generation capability | Two reviewers rate 20 answers on a simple 1–5 clarity rubric (key fact first, plain language). | Mean clarity score | ≥ 4.0 / 5 | Degree holders can understand the answer without reading the whole source document. |
| O3 / NFR1 | Response latency | Cost and latency | Measure end-to-end response time over the 30-question workload. | p90 latency | < 5 s | Degree holders get a responsive interaction. |
| O3 / NFR4 | Inference cost | Cost and latency | Record model/API usage over the evaluation workload. | Cost per 100 queries | < US$0.50 (illustrative) | The prototype stays within a student project budget. |

## Reflection — Which evaluation criterion is most important for determining whether the application will be useful?

Critical-fact accuracy (O2 / FR3 / RAI1). A degree holder uses the assistant to decide whether and when to apply, so a wrong deadline, amount, eligibility rule or availability condition has a real cost, such as a missed or wasted application. A fluent answer that is wrong is worse than "I could not find this, check the official page". This is why the threshold is higher (≥ 95%) than for general correctness (≥ 80%), and why it allows abstaining as an acceptable outcome.
