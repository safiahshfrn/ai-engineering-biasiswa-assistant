# BiasiswaBot · Topic 3 data inventory

The [Topic 2 architecture](week2_architecture_v1.png) uses a Knowledge Source for postgraduate funding. This batch covers two sections of one official scheme page. The published source is unstructured Malay HTML. The pipeline ingests original, manually curated English TXT notes. JSONL stores the resulting document text and citation metadata.

| Topic 2 requirement | Data need | Selected evidence |
| --- | --- | --- |
| FR1 | Official funding evidence | PTPTN’s postgraduate coverage and application conditions |
| FR2 | Source and date | Publisher, URL, exact section heading, review date and a null publication date |
| FR8 | Who can apply | The coverage table lists postgraduate modes at public institutions. Application conditions include an admission offer and an approved, PTPTN-registered course. |

See the [requirements](week2_requirements.md), [evaluation criteria](week2_evaluation_criteria.md) and [architecture decisions](week2_architecture_decisions.md).

| Source ID and input | Publisher section and purpose | Version and access | Ingestion evidence |
| --- | --- | --- | --- |
| S01 · [Postgraduate coverage](../data/raw/week3/ptptn_postgraduate_coverage.txt) | “Pinjaman Pendidikan Yang Ditawarkan” gives institution coverage by level | PTPTN · English section notes v1 · reviewed 2026-11-16 · public reference · publication date unverified | 356 UTF-8 bytes, two paragraphs. The first links master's and doctoral studies at public institutions with full-time, part-time and distance learning. The second qualifies the geographic scope. |
| S02 · [Application conditions](../data/raw/week3/ptptn_application_conditions.txt) | “Syarat-Syarat Permohonan” gives application prerequisites | PTPTN · English section notes v1 · reviewed 2026-11-16 · public reference · publication date unverified | 356 UTF-8 bytes, two paragraphs. The first groups an admission offer with course approval and registration. The second covers remaining study and the Simpan SSPN condition. |

Both sections are publicly readable on the [official PTPTN education-loan page](https://www.ptptn.gov.my/pinjaman-pendidikan/). The repository holds original paraphrases of selected facts. Checksums identify the tracked TXT inputs. The upstream HTML version and publication date were unverified.

The sample covers one scheme, selected rules and no application window. The notes omit page layout, table structure and original Malay wording. Use the provider page to check exact conditions and current availability. Coverage and language parity require additional schemes and Malay evidence.
