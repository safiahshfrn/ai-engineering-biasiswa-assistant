# BiasiswaBot · Topic 3 pipeline decisions

> **Scope change (22 Nov 2026):** BiasiswaBot now serves SPM, STPM/matriculation and diploma leavers seeking undergraduate funding. This Week 3 batch (PTPTN postgraduate sections) is kept as the Topic 3 lab record only and is superseded by the v2 corpus in `data/raw/v2/` and `src/pipeline_v2.py`. See [week4_data_quality_report.md](week4_data_quality_report.md).

The [executed notebook](../notebooks/week3_pipeline.ipynb) prepares four citable chunks for the Knowledge Source in the [Topic 2 architecture](week2_architecture_v1.png). The [inventory](week3_data_inventory.md) maps the two TXT inputs to FR1, FR2 and FR8.

## Preparation comparison

Both configurations began with the same four normalized paragraphs. The baseline joins the paragraphs within each source and wraps at word boundaries. The selected configuration retains paragraph boundaries. An intact paragraph appears in full within one chunk.

| Configuration | S01 chunks / longest / intact | S02 chunks / longest / intact | Intact paragraphs |
| --- | --- | --- | --- |
| Fixed 150-character wrap | 3 / 147 chars / 0 | 3 / 149 chars / 0 | 0 of 4 |
| One chunk per paragraph | 2 / 180 chars / 2 | 2 / 185 chars / 2 | 4 of 4 |

I selected paragraph chunks so each coverage statement keeps its institution category and each application statement retains its qualifiers. Variable chunk length is the trade-off. The longest observed chunk is 185 characters. Longer documents may require subdivision by policy item. Retrieval and answer performance remain to be evaluated against the [Topic 2 criteria](week2_evaluation_criteria.md).

## V1 workflow and stage contracts

| Stage | Contract and evidence | Failure response |
| --- | --- | --- |
| Ingest | Open the two explicitly named UTF-8 files and compute SHA-256 fingerprints. | Stop for a missing file or unreadable encoding. Restore the tracked file and rerun. |
| Inspect | Show each provider section, paragraph count and sample text. | Stop when no readable paragraph remains. Check the curated note against the provider page. |
| Prepare | Normalize whitespace and emit one record per paragraph with a chunk ID and provenance fields. | Stop for an invalid strategy. Restore the selected settings. |
| Validate and store | Read staged JSONL back. Check uniqueness, count, exact normalized text and source metadata. Publish validated output. | Reject a failed candidate before it replaces the prior export. Review the reported data contract. |
| Record lineage | Map source paths and fingerprints to chunk IDs, output path and fingerprint. Verify against disk. | Stop before saving a successful manifest if hashes or mappings disagree. Restore the intended inputs and rerun. |

V1 uses batch ETL. The corpus is small and pinned, and upstream changes are manually reviewed. The update path is to review the official page, revise the affected note and its review metadata, and rerun. Retrieval indexing and automatic refresh are future steps under ADR1 and ADR4.

## Execution evidence and reflection

- Part B produced [prepared text](../data/processed/prepared_text.jsonl) and the [common manifest](../data/week3_manifest.json). Chunk S02:p1 contains the offer and course conditions with its source heading.
- Cell 8A produced four records from two sources, and the [Part C output](../data/pipeline_v1/documents/prepared_text.jsonl) matched Part B byte for byte. The [pipeline manifest](../data/pipeline_v1/documents/pipeline_manifest.json) captures the successful rerun.
- Cell 9 independently reread the inputs and rebuilt the export. Source and output hashes, sizes, counts and mappings matched. The timestamp records when the pipeline ran and changes with each execution.

An admission offer can satisfy one condition while the postgraduate institution category or course approval still needs checking. Both sections are needed for a later evidence-aware answer. The sample omits other conditions, and the source review date marks when the page was checked. The official publication date remains unknown.
