# Week 1 Project Scope

## Project Name
**BiasiswaBot — Scholarship & Financial Aid Information Assistant**

## Domain
Higher Education / Student Financial Aid (Malaysia). Scope is limited to **information retrieval with citations**, not eligibility decisions or financial advice.

## Problem Statement
Malaysian undergraduates must find scholarship and financial-aid information (providers, eligibility, deadlines, application steps) spread across many separate agency and university pages, each with its own conditions. Finding the right scheme means reading and cross-checking several documents, and information may be outdated or hard to interpret. A document-grounded AI assistant can answer questions in natural language (English and Bahasa Melayu) and cite the official source, which a keyword search or static FAQ cannot do across multiple documents.

## Evidence of the Problem
- **Evidence 1:** The Malaysian government portal lists financial assistance from several separate providers (e.g. JPA aid, PTPK TVET financing) each with different conditions such as parental income limits and "no other sponsorship". Students must compare these by hand.
  **Source:** MyGOV Malaysia, "Scholarships and Financial Assistance", https://www.malaysia.gov.my/en/categories/school--education/scholarships-and-financial-assistance
- **Evidence 2:** Institutions restate PTPTN loan rules in their own pages with institution-specific details (e.g. application windows, GPA conditions, no full-scholarship holders), so a student may need to check both PTPTN and their institution.
  **Sources:** Heriot-Watt University Malaysia, "National Higher Education Fund (PTPTN)", https://www.hw.ac.uk/malaysia/study/fees-and-funding/scholarships/national-higher-education-fund-ptptn ; Asia Pacific University, "PTPTN", https://new.apu.edu.my/national-higher-education-fund-perbadanan-tabung-pendidikan-tinggi-nasional-ptptn

> ⚠ Before Week 2, add 1–2 stronger sources (e.g. a survey or news report on students' difficulty finding aid information).

## Initial Related Work (at least 3)
1. **RAG admission chatbot**
   - **Source:** Chen, Z., Zou, D., Xie, H., & Lou, H. (2024). Facilitating university admission using a chatbot based on large language models with retrieval-augmented generation. *Educational Technology & Society*. https://doaj.org/article/1def23f23c554d11a962e11b2399a49e
   - **Key limitation:** Applied to admission data of three universities (US, Kenya, Hong Kong), not Malaysian scholarship/financial-aid sources; evaluation relied on feedback from 53 high-school students.
2. **Marcel — open-source university student-support agent**
   - **Source:** Trienes et al. (2025). Marcel: A Lightweight and Open-Source Conversational Agent for University Student Support. arXiv:2507.13937. https://arxiv.org/html/2507.13937v2
   - **Key limitation:** Demo focused on enrolment questions for one M.Sc. programme at one university; single-institution knowledge base.
3. **Unipa-GPT — university information chatbot**
   - **Source:** Siragusa et al. (2024). Conditioning ChatGPT for information retrieval: the Unipa-GPT case study. arXiv:2407.14246. https://arxiv.org/pdf/2407.14246v1
   - **Key limitation:** Built from one university's website in Italian; does not combine multiple external funding agencies or handle bilingual queries.

## Engineering Gap / Limitation
In this initial scan, existing university RAG chatbots target a single institution's admission or enrolment information. Scholarship and financial-aid rules in Malaysia sit across multiple agencies and institutions, change over time (deadlines, eligibility) and are written in both English and Bahasa Melayu. The unresolved gap is a **multi-source, citation-grounded assistant that handles time-sensitive information and declines to make eligibility decisions**.

## Initial Project Objectives
- **O1:** To design a document-grounded AI assistant that answers scholarship and financial-aid questions from official public Malaysian sources.
- **O2:** To develop the assistant with retrieval, source citation and guardrails (scope check, "verify with official source" for deadlines and eligibility).
- **O3:** To evaluate the assistant in terms of answer accuracy, groundedness, latency and safety using a test question set.

## Target Users
Malaysian undergraduate students (especially first- and second-year students at public universities) and prospective students looking for scholarships and financial aid.

## Data Sources (at least 2)
- **Source 1:** MyGOV Malaysia — Scholarships and Financial Assistance — URL: https://www.malaysia.gov.my/en/categories/school--education/scholarships-and-financial-assistance
- **Source 2:** PTPTN (National Higher Education Fund Corporation) official portal — URL: https://www.ptptn.gov.my
- **Source 3:** Public Service Department (JPA) scholarship pages — URL: https://www.jpa.gov.my

> ⚠ Before Week 2, open each site and record the exact page/document URLs (e.g. the specific PTPTN guideline PDF). Store links and metadata only; do not commit copyrighted documents.

## Similar to EduAdvisor
Same document-grounded RAG pattern: official public documents → load, clean, chunk, embed → vector store → LLM with retrieved context → guardrails → chat interface → feedback and monitoring. Same evaluation themes (accuracy, groundedness, latency, safety) and same focus on helping students find fragmented information.

## Different from EduAdvisor
- Sources come from **multiple external agencies** (government, PTPTN, JPA), not one university's catalogue.
- Information is **time-sensitive** (deadlines, intakes), so source dates and freshness matter.
- Queries may be in **English and Bahasa Melayu**.
- The assistant gives **information only**, never eligibility decisions or financial advice.

## Responsible AI Risks (at least 2)
- **Risk 1 — Hallucination / wrong eligibility or deadline:** Model states an incorrect rule or date → student misses an application or applies when ineligible.
- **Risk 2 — Outdated information:** Documents change after indexing → student follows an old process.
- **Risk 3 — Fairness / language:** Bahasa Melayu or rural-focused schemes under-represented → unequal answer quality across students.
- **Risk 4 — Privacy:** Students type income or IC details → sensitive data exposure; the assistant will warn users and not store personal data.
