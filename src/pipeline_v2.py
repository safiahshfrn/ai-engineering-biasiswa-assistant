"""BiasiswaBot data pipeline v2 (undergraduate funding corpus).

Stages: ingest -> inspect -> clean -> chunk (compare two strategies) -> validate
(quality rules) -> coverage and bias check -> store (JSONL, registry, manifest,
quality report) -> quality gate.

Run from the repository root:  python src/pipeline_v2.py
Only the Python standard library is used.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data/raw/v2"
OUT_DIR = ROOT / "data/processed/v2"
EVAL_DIR = ROOT / "evaluation"
RUN_DATE = date(2026, 11, 22)  # pinned so reruns give identical output

REQUIRED_FIELDS = [
    "source_id", "scheme_id", "provider", "provider_type", "source_url",
    "source_section", "source_kind", "source_language", "retrieved_on",
    "availability_type", "form_of_aid", "verification_status",
]
AVAILABILITY_TYPES = {"A_RESULTS", "B_OFFER", "C_INSTITUTION", "U_NOT_STATED"}
AID_FORMS = {"loan", "bursary", "scholarship_with_bond", "convertible_loan",
             "mixed", "not_stated"}
IN_SCOPE_LEVELS = {"certificate", "foundation", "pre-university", "diploma", "degree"}
STALE_DAYS = 365
FIXED = {"size": 400, "overlap": 50}
STRUCTURED = {"max_chars": 700}


# ---------------------------------------------------------------- ingest
def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_value(raw: str):
    raw = raw.strip()
    if raw == "null":
        return None
    if raw.startswith("[") and raw.endswith("]"):
        return [v.strip() for v in raw[1:-1].split(",") if v.strip()]
    return raw


def load_note(path: Path) -> dict:
    data = path.read_bytes()
    text = data.decode("utf-8")  # fails loudly on bad encoding
    if not text.startswith("---"):
        raise ValueError(f"{path.name}: missing metadata header")
    _, header, body = text.split("---", 2)
    meta = {}
    for line in header.strip().splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = parse_value(value)
    return {"meta": meta, "body": body, "file": path.relative_to(ROOT).as_posix(),
            "sha256": sha256_bytes(data), "bytes": len(data)}


# ---------------------------------------------------------------- clean
def clean(body: str) -> str:
    text = unicodedata.normalize("NFC", body)
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in text.splitlines()]
    text = "\n".join(lines)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def sentences(text: str) -> list[str]:
    flat = re.sub(r"^## .*$", "", text, flags=re.M)
    parts = re.split(r"(?<=[.;])\s+", re.sub(r"\s+", " ", flat))
    return [p.strip() for p in parts if len(p.strip()) > 20]


# ---------------------------------------------------------------- chunk
def chunk_fixed(text: str, size: int, overlap: int) -> list[dict]:
    flat = re.sub(r"\s+", " ", text)
    chunks, start = [], 0
    while start < len(flat):
        chunks.append({"heading": None, "text": flat[start:start + size]})
        start += size - overlap
    return chunks


def chunk_structured(text: str, max_chars: int) -> list[dict]:
    """Split on '## ' headings; keep each section whole up to max_chars,
    otherwise split at paragraph, then sentence, boundaries."""
    chunks, heading = [], None
    sections = re.split(r"^## (.*)$", text, flags=re.M)
    if sections[0].strip():
        sections = ["", None, sections[0]] + sections[1:]  # headless preamble
    for i in range(1, len(sections), 2):
        heading, body = sections[i], sections[i + 1].strip()
        if not body:
            continue
        pieces, buf = [], ""
        for para in body.split("\n\n"):
            para = re.sub(r"\s+", " ", para).strip()
            if len(buf) + len(para) + 1 <= max_chars:
                buf = f"{buf} {para}".strip()
                continue
            if buf:
                pieces.append(buf)
            if len(para) <= max_chars:
                buf = para
            else:  # rare: split an over-long paragraph at sentence ends
                buf = ""
                for sent in re.split(r"(?<=[.;])\s+", para):
                    if len(buf) + len(sent) + 1 > max_chars and buf:
                        pieces.append(buf)
                        buf = ""
                    buf = f"{buf} {sent}".strip()
        if buf:
            pieces.append(buf)
        chunks += [{"heading": heading, "text": p} for p in pieces]
    return chunks


def compare_strategies(docs: list[dict]) -> dict:
    result = {}
    for name, fn in (("fixed_400_overlap_50", lambda t: chunk_fixed(t, **FIXED)),
                     ("structure_aware_700", lambda t: chunk_structured(t, **STRUCTURED))):
        lengths, intact, total_sent, with_heading, tiny, n = [], 0, 0, 0, 0, 0
        for d in docs:
            chunks = fn(d["clean"])
            n += len(chunks)
            lengths += [len(c["text"]) for c in chunks]
            with_heading += sum(1 for c in chunks if c["heading"])
            tiny += sum(1 for c in chunks if len(c["text"]) < 80)
            flat_chunks = [re.sub(r"\s+", " ", c["text"]) for c in chunks]
            for s in sentences(d["clean"]):
                total_sent += 1
                intact += any(s in fc for fc in flat_chunks)
        result[name] = {
            "chunks": n,
            "mean_chars": round(sum(lengths) / len(lengths)),
            "max_chars": max(lengths),
            "tiny_chunks_lt_80": tiny,
            "chunks_with_heading_pct": round(100 * with_heading / n, 1),
            "sentences_intact": f"{intact}/{total_sent}",
            "sentence_integrity_pct": round(100 * intact / total_sent, 1),
        }
    return result


# ---------------------------------------------------------------- validate
IC_RE = re.compile(r"\b\d{6}-\d{2}-\d{4}\b")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
PHONE_RE = re.compile(r"\b0\d{1,2}-?\d{7,8}\b")
TIER_RE = re.compile(r"([\d,]+) / ([\d,]+) / ([\d,]+)\.")


def to_int(s: str) -> int:
    return int(s.replace(",", ""))


def issue(rule, severity, source_id, detail, action, chunk_id=None):
    return {"rule": rule, "severity": severity, "source_id": source_id,
            "chunk_id": chunk_id, "detail": detail, "action": action}


def validate_source(doc: dict) -> list[dict]:
    m, sid, out = doc["meta"], doc["meta"].get("source_id", doc["file"]), []
    missing = [f for f in REQUIRED_FIELDS if not m.get(f)]
    if missing:
        out.append(issue("R1 required metadata", "HARD_FAIL", sid,
                         f"missing {missing}", "quarantine source"))
    if m.get("availability_type") not in AVAILABILITY_TYPES or \
            m.get("form_of_aid") not in AID_FORMS:
        out.append(issue("R2 controlled vocabulary", "HARD_FAIL", sid,
                         "availability_type or form_of_aid outside allowed values",
                         "quarantine source"))
    if not set(m.get("study_levels") or []) & IN_SCOPE_LEVELS or not m.get("entry_pathways"):
        out.append(issue("R3 scope fit", "HARD_FAIL", sid,
                         "no in-scope study level or entry pathway recorded",
                         "quarantine source"))
    usable = [s for s in sentences(doc["clean"]) if len(s.split()) >= 8]
    if len(usable) < 2:
        out.append(issue("R4 usable content", "HARD_FAIL", sid,
                         f"{len(doc['clean'])} chars, {len(usable)} sentences of 8+ words; "
                         "scheme names only, no criteria", "quarantine source"))
    dated = m.get("page_last_updated") or m.get("publication_date")
    if not dated:
        out.append(issue("R5 timeliness", "MANUAL_REVIEW", sid,
                         f"no content date ({m.get('version_label')})",
                         "keep; show retrieval date and verify notice"))
    elif (RUN_DATE - date.fromisoformat(dated)).days > STALE_DAYS:
        out.append(issue("R5 timeliness", "WARNING", sid,
                         f"content date {dated} is {(RUN_DATE - date.fromisoformat(dated)).days} days old",
                         "keep; re-check provider page each intake"))
    if m.get("source_kind") == "secondary":
        out.append(issue("R6 provenance tier", "WARNING", sid,
                         "secondary report of an official statement; primary page not retrievable",
                         "keep with status secondary_NV; answer must carry verify notice"))
    for line in doc["clean"].splitlines():
        hit = TIER_RE.search(line)
        if hit:
            mx, p75, p50 = map(to_int, hit.groups())
            if abs(p75 - 0.75 * mx) > 10 or abs(p50 - 0.5 * mx) > 10:
                out.append(issue("R7 numeric consistency", "MANUAL_REVIEW", sid,
                                 f"tier values {mx}/{p75}/{p50} do not match 75%/50% rule: "
                                 f"{line[:70]}", "keep as published; flag for provider check"))
    return out


def validate_chunks(chunks: list[dict]) -> tuple[list[dict], set]:
    out, drop, seen = [], set(), {}
    for c in chunks:
        t = c["text"]
        if IC_RE.search(t):
            out.append(issue("R8 privacy", "HARD_FAIL", c["source_id"],
                             "IC-number pattern found", "remove chunk", c["chunk_id"]))
            drop.add(c["chunk_id"])
        if EMAIL_RE.search(t) or PHONE_RE.search(t):
            out.append(issue("R8 privacy", "WARNING", c["source_id"],
                             "contact detail found", "review", c["chunk_id"]))
        h = sha256_bytes(t.encode())
        if h in seen:
            out.append(issue("R9 uniqueness", "WARNING", c["source_id"],
                             f"exact duplicate of {seen[h]}", "remove duplicate", c["chunk_id"]))
            drop.add(c["chunk_id"])
        seen[h] = c["chunk_id"]
        if len(t) < 80:
            out.append(issue("R10 chunk size", "WARNING", c["source_id"],
                             f"{len(t)} chars", "inspect", c["chunk_id"]))
    # near-duplicates across different sources (5-word shingles, Jaccard)
    def shingles(t):
        w = re.findall(r"\w+", t.lower())
        return {tuple(w[i:i + 5]) for i in range(max(1, len(w) - 4))}
    sh = {c["chunk_id"]: shingles(c["text"]) for c in chunks}
    for i, a in enumerate(chunks):
        for b in chunks[i + 1:]:
            if a["source_id"] == b["source_id"]:
                continue
            j = len(sh[a["chunk_id"]] & sh[b["chunk_id"]]) / len(sh[a["chunk_id"]] | sh[b["chunk_id"]])
            if j >= 0.5:
                out.append(issue("R9 uniqueness", "WARNING", a["source_id"],
                                 f"near-duplicate of {b['chunk_id']} (Jaccard {j:.2f})",
                                 "keep both; retrieval dedup", a["chunk_id"]))
    return out, drop


# ---------------------------------------------------------------- coverage
def coverage(docs: list[dict]) -> dict:
    schemes = {}
    for d in docs:
        m = d["meta"]
        if m["scheme_id"] in schemes or m["scheme_id"] == "MYGOV-INDEX":
            continue
        schemes[m["scheme_id"]] = m
    matrix = defaultdict(lambda: defaultdict(list))
    for sid, m in schemes.items():
        for p in m["entry_pathways"]:
            for lvl in m["study_levels"]:
                matrix[p][lvl].append(sid)
    return {
        "schemes": len(schemes),
        "pathway_by_level": {p: dict(v) for p, v in matrix.items()},
        "schemes_per_pathway": {p: len({s for v in lv.values() for s in v}) for p, lv in matrix.items()},
        "provider_type": dict(Counter(m["provider_type"] for m in schemes.values())),
        "availability_type": dict(Counter(m["availability_type"] for m in schemes.values())),
        "group_condition": dict(Counter(m["group_condition"] for m in schemes.values())),
        "source_language": dict(Counter(d["meta"]["source_language"] for d in docs)),
        "source_kind": dict(Counter(d["meta"]["source_kind"] for d in docs)),
    }


# ---------------------------------------------------------------- run
def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    paths = sorted(RAW_DIR.glob("S*.md"))
    if not paths:
        raise FileNotFoundError("No raw notes in data/raw/v2")

    # 1 ingest + inspect
    docs = [load_note(p) for p in paths]
    for d in docs:
        d["clean"] = clean(d["body"])
    print(f"[ingest] {len(docs)} files, {sum(d['bytes'] for d in docs)} bytes")
    for d in docs:
        print(f"  {d['meta']['source_id']} {d['meta']['scheme_id']:<20} "
              f"{len(d['clean']):>5} chars  {d['meta']['source_kind']}")

    # 2 validate sources -> quarantine hard fails
    issues, quarantined = [], []
    for d in docs:
        found = validate_source(d)
        issues += found
        if any(i["severity"] == "HARD_FAIL" for i in found):
            quarantined.append(d)
    accepted = [d for d in docs if d not in quarantined]
    print(f"[validate] accepted {len(accepted)}, quarantined {len(quarantined)}")

    # 3 chunk: compare, then apply selected strategy
    comparison = compare_strategies(accepted)
    chunks = []
    for d in accepted:
        m = d["meta"]
        for n, c in enumerate(chunk_structured(d["clean"], **STRUCTURED), 1):
            chunks.append({
                "chunk_id": f"{m['source_id']}-C{n:02d}",
                "source_id": m["source_id"], "scheme_id": m["scheme_id"],
                "text": c["text"], "heading": c["heading"],
                "provider": m["provider"], "source_url": m["source_url"],
                "source_section": m["source_section"], "source_language": m["source_language"],
                "page_last_updated": m["page_last_updated"], "publication_date": m["publication_date"],
                "retrieved_on": m["retrieved_on"], "study_levels": m["study_levels"],
                "entry_pathways": m["entry_pathways"], "availability_type": m["availability_type"],
                "group_condition": m["group_condition"], "form_of_aid": m["form_of_aid"],
                "status": "secondary_NV" if m["source_kind"] == "secondary" else "ready",
                "processing": f"NFC; whitespace collapsed; structure_aware max_chars={STRUCTURED['max_chars']}",
            })

    # 4 chunk-level rules
    chunk_issues, drop = validate_chunks(chunks)
    issues += chunk_issues
    chunks = [c for c in chunks if c["chunk_id"] not in drop]

    # 5 store
    def write_jsonl(path, rows):
        with path.open("w", encoding="utf-8", newline="\n") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    chunk_path = OUT_DIR / "chunks.jsonl"
    write_jsonl(chunk_path, chunks)
    write_jsonl(OUT_DIR / "quarantine.jsonl",
                [{"source_id": d["meta"]["source_id"], "file": d["file"],
                  "reasons": [i["rule"] for i in issues
                              if i["source_id"] == d["meta"]["source_id"] and i["severity"] == "HARD_FAIL"]}
                 for d in quarantined])

    # scheme registry (one row per scheme; the who-can-apply metadata for FR8)
    reg_fields = ["scheme_id", "provider", "provider_type", "study_levels", "entry_pathways",
                  "availability_type", "group_condition", "form_of_aid", "source_kind",
                  "verification_status", "source_ids"]
    reg = {}
    for d in accepted:
        m = d["meta"]
        row = reg.setdefault(m["scheme_id"], {k: m.get(k) for k in reg_fields} | {"source_ids": []})
        row["source_ids"].append(m["source_id"])
    with (OUT_DIR / "scheme_registry.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=reg_fields)
        w.writeheader()
        for row in reg.values():
            w.writerow({k: ";".join(v) if isinstance(v, list) else v for k, v in row.items()})

    # 6 read back and verify before writing the manifest
    back = [json.loads(l) for l in chunk_path.read_text(encoding="utf-8").splitlines()]
    assert len(back) == len(chunks), "read-back count mismatch"
    assert len({c["chunk_id"] for c in back}) == len(back), "duplicate chunk_id"
    assert all(c["source_url"] and c["retrieved_on"] for c in back), "chunk lost provenance"

    cov = coverage(accepted)
    sev = Counter(i["severity"] for i in issues)
    gate = "HOLD" if any(i["severity"] == "HARD_FAIL" and i["source_id"] not in
                         {q["meta"]["source_id"] for q in quarantined} for i in issues) \
        else ("GO_WITH_CONDITIONS" if sev["WARNING"] or sev["MANUAL_REVIEW"] else "GO")
    report = {
        "run_date": RUN_DATE.isoformat(),
        "sources_ingested": len(docs), "sources_accepted": len(accepted),
        "sources_quarantined": [d["meta"]["source_id"] for d in quarantined],
        "chunks": len(chunks), "chunking_comparison": comparison,
        "issue_counts": dict(sev), "issues": issues, "coverage": cov, "quality_gate": gate,
    }
    (OUT_DIR / "quality_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")

    manifest = {
        "schema_version": 2, "run_date": RUN_DATE.isoformat(),
        "processing": {"clean": "NFC; collapse whitespace", "selected_strategy": "structure_aware",
                       **STRUCTURED, "compared_with": f"fixed size={FIXED['size']} overlap={FIXED['overlap']}"},
        "outputs": {p.name: sha256_bytes(p.read_bytes()) for p in sorted(OUT_DIR.glob("*"))
                    if p.name != "manifest.json"},
        "lineage": [{"source_id": d["meta"]["source_id"], "file": d["file"], "sha256": d["sha256"],
                     "bytes": d["bytes"], "source_url": d["meta"]["source_url"],
                     "retrieved_on": d["meta"]["retrieved_on"],
                     "status": "quarantined" if d in quarantined else "accepted",
                     "chunk_ids": [c["chunk_id"] for c in chunks if c["source_id"] == d["meta"]["source_id"]]}
                    for d in docs],
    }
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")

    print(f"[chunk] {json.dumps(comparison, indent=1)}")
    print(f"[store] {len(chunks)} chunks -> {chunk_path.relative_to(ROOT)}")
    print(f"[quality] {dict(sev)} -> gate {gate}")


if __name__ == "__main__":
    main()
