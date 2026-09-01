#!/usr/bin/env python3
import argparse
import csv
import re
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

ENVO_PATH = DATA_DIR / "envo.owl"
PHENOMENA_PATH = DATA_DIR / "phenomena_unified.csv"
HARMONIZATION_PATH = DATA_DIR / "harmonization_top100_initial_focus_v1_cleaned.csv"

OUT_CSV = DATA_DIR / "envo_heliophysics_subset_quick.csv"
OUT_SUMMARY = DATA_DIR / "envo_heliophysics_subset_quick_summary.txt"
OUT_GAPS = DATA_DIR / "envo_heliophysics_subset_quick_missing_reference_terms.csv"

RDF_NS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
OWL_NS = "http://www.w3.org/2002/07/owl#"
RDFS_NS = "http://www.w3.org/2000/01/rdf-schema#"
OBO_NS = "http://purl.obolibrary.org/obo/"
OBOINOWL_NS = "http://www.geneontology.org/formats/oboInOwl#"

SYNONYM_LOCAL_NAMES = {
    "hasExactSynonym",
    "hasRelatedSynonym",
    "hasBroadSynonym",
    "hasNarrowSynonym",
    "IAO_0000118",
}

STRICT_ANCHOR_TOKENS = {
    "solar", "sun", "heliosphere", "corona", "coronal", "magnetosphere", "magnetopause",
    "magnetotail", "ionosphere", "geomagnetic", "aurora", "auroral", "plasma",
    "interplanetary", "flare", "cme", "proton", "electron", "shock",
    "chromosphere", "photosphere", "thermosphere", "xray", "ultraviolet",
    "imf", "cosmic", "electromagnetic", "heliophysics",
    "heliospheric", "magnetic", "sunspot", "sunspots", "x", "ray", "kp", "dst",
    "ap", "ae", "tec", "reconnection",
}

BROAD_ANCHOR_TOKENS = STRICT_ANCHOR_TOKENS | {
    "radiation", "particle", "wind", "space", "spectrum", "stellar", "infrared", "microwave",
    "gamma", "radio", "wave", "photic", "insolation",
}

STOPWORDS = {
    "the", "and", "for", "with", "from", "into", "onto", "over", "under", "about",
    "this", "that", "these", "those", "term", "terms", "index", "indices", "region",
    "process", "processes", "field", "fields", "energy", "data", "model", "models",
}


@dataclass
class MatchResult:
    score: int
    reasons: list
    matched_terms: list


def normalize(text: str) -> str:
    text = (text or "").strip().lower()
    text = text.replace("'", "")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def singularize(word: str) -> str:
    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"
    if len(word) > 4 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def tokenize(text: str) -> set:
    toks = [singularize(t) for t in normalize(text).split() if t]
    return set(toks)


def parse_similar_terms(cell: str) -> list:
    if not cell:
        return []
    parts = [p.strip() for p in cell.split("|")]
    out = []
    for p in parts:
        p = re.sub(r"\s*\([^)]*\)\s*$", "", p).strip()
        if p:
            out.append(p)
    return out


def read_reference_terms(mode: str) -> set:
    terms = set()

    with PHENOMENA_PATH.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            in_hk = (row.get("in_helioknow") or "").strip().lower()
            if mode == "quick" and in_hk not in {"true", "1", "yes"}:
                continue
            for col in ("canonical_term",):
                val = (row.get(col) or "").strip()
                if val:
                    terms.add(val)

    with HARMONIZATION_PATH.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            selected = (row.get("selected_for_ranking") or "").strip().lower() in {"true", "1", "yes"}
            excl_far = (row.get("exclude_farfield") or "").strip().lower() in {"true", "1", "yes"}
            excl_low = (row.get("exclude_low_relevance") or "").strip().lower() in {"true", "1", "yes"}
            try:
                rel = float((row.get("relevance_score") or "0").strip())
            except ValueError:
                rel = 0.0

            if mode == "quick":
                if not selected or excl_far or excl_low or rel < 0.65:
                    continue
            else:
                if not selected or excl_far:
                    continue

            if mode == "broad" and rel < 0.45:
                continue

            for col in ("term", "canonical_term"):
                val = (row.get(col) or "").strip()
                if val:
                    terms.add(val)
            for sim in parse_similar_terms(row.get("semantically_similar_terms", "")):
                terms.add(sim)

    cleaned = {t for t in terms if t and len(normalize(t)) >= 3}
    return cleaned


def build_seed_indices(seed_terms: set, anchor_tokens: set):
    seed_norm = set()
    seed_tokens = {}
    token_to_seeds = defaultdict(set)

    for t in seed_terms:
        n = normalize(t)
        if not n:
            continue
        toks = tokenize(n)
        # Keep only seed terms that have explicit heliophysics signal.
        if not (toks & anchor_tokens):
            continue
        seed_norm.add(n)
        seed_tokens[n] = toks
        for tok in toks:
            if len(tok) >= 3:
                token_to_seeds[tok].add(n)

    return seed_norm, seed_tokens, token_to_seeds


def domain_token_set(seed_tokens: dict, anchor_tokens: set) -> set:
    counts = defaultdict(int)
    for toks in seed_tokens.values():
        for t in toks:
            if len(t) >= 4 and t not in STOPWORDS:
                counts[t] += 1

    frequent = {t for t, c in counts.items() if c >= 2}
    return frequent | anchor_tokens


def score_term(
    label: str,
    synonyms: list,
    seed_norm: set,
    seed_tokens: dict,
    token_to_seeds: dict,
    domain_tokens: set,
    anchor_tokens: set,
) -> MatchResult:
    label_n = normalize(label)
    syn_n = [normalize(s) for s in synonyms if normalize(s)]
    term_text = " | ".join([label_n] + syn_n)
    term_tokens = tokenize(term_text)
    has_anchor = bool(term_tokens & anchor_tokens)

    reasons = []
    matched = []
    score = 0

    if label_n in seed_norm:
        score = max(score, 100)
        reasons.append("exact_label_match")
        matched.append(label_n)

    # Candidate seed terms restricted by token overlap for speed.
    candidates = set()
    for tok in term_tokens:
        candidates.update(token_to_seeds.get(tok, set()))

    # Phrase containment checks on a reduced candidate set.
    contains_hits = []
    for s in candidates:
        if len(s) >= 5 and s in term_text:
            contains_hits.append(s)
    if contains_hits:
        score = max(score, 90)
        reasons.append("phrase_match")
        matched.extend(sorted(contains_hits)[:10])

    # Fuzzy and token-overlap checks only on reduced candidates.
    best_ratio = 0.0
    best_seed = ""
    best_overlap = 0.0
    best_overlap_seed = ""

    label_toks = tokenize(label_n)
    for s in candidates:
        stoks = seed_tokens.get(s, set())
        if not stoks:
            continue

        overlap = len(label_toks & stoks) / max(1, len(stoks))
        if overlap > best_overlap:
            best_overlap = overlap
            best_overlap_seed = s

        if abs(len(label_n) - len(s)) <= 18:
            ratio = SequenceMatcher(None, label_n, s).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_seed = s

    if best_ratio >= 0.92:
        score = max(score, 85)
        reasons.append("fuzzy_label_match>=0.92")
        matched.append(best_seed)
    elif best_ratio >= 0.86:
        score = max(score, 75)
        reasons.append("fuzzy_label_match>=0.86")
        matched.append(best_seed)

    if best_overlap >= 0.60 and len(label_toks & seed_tokens.get(best_overlap_seed, set())) >= 2:
        score = max(score, 70)
        reasons.append("token_overlap>=0.60")
        matched.append(best_overlap_seed)

    d_hits = sorted(term_tokens & domain_tokens)
    if len(d_hits) >= 3:
        score = max(score, 45)
        reasons.append("domain_token_hits>=3")

    if has_anchor:
        score = max(score, 50)
        reasons.append("contains_heliophysics_anchor")

    matched = [m for m in matched if m]
    return MatchResult(score=score, reasons=sorted(set(reasons)), matched_terms=sorted(set(matched))[:12])


def local_name(tag: str) -> str:
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def parse_envo_and_filter(
    seed_norm: set,
    seed_tokens: dict,
    token_to_seeds: dict,
    domain_tokens: set,
    anchor_tokens: set,
    threshold: int,
):
    records = []
    total_classes = 0
    envo_lexicon = set()
    envo_labels = []

    rdf_about = "{" + RDF_NS + "}about"
    class_tag = "{" + OWL_NS + "}Class"
    label_tag = "{" + RDFS_NS + "}label"
    def_tag = "{" + OBO_NS + "}IAO_0000115"

    for event, elem in ET.iterparse(ENVO_PATH, events=("end",)):
        if elem.tag != class_tag:
            continue

        total_classes += 1
        uri = (elem.attrib.get(rdf_about) or "").strip()
        if not uri:
            elem.clear()
            continue
        if "/ENVO_" not in uri:
            elem.clear()
            continue

        label = ""
        definitions = []
        synonyms = []

        for child in elem:
            if child.tag == label_tag and (child.text or "").strip() and not label:
                label = child.text.strip()
            elif child.tag == def_tag and (child.text or "").strip():
                definitions.append(child.text.strip())
            elif local_name(child.tag) in SYNONYM_LOCAL_NAMES and (child.text or "").strip():
                synonyms.append(child.text.strip())

        if label:
            label_n = normalize(label)
            if label_n:
                envo_lexicon.add(label_n)
                envo_labels.append(label_n)
            for s in synonyms:
                sn = normalize(s)
                if sn:
                    envo_lexicon.add(sn)

            result = score_term(
                label=label,
                synonyms=synonyms,
                seed_norm=seed_norm,
                seed_tokens=seed_tokens,
                token_to_seeds=token_to_seeds,
                domain_tokens=domain_tokens,
                anchor_tokens=anchor_tokens,
            )

            # Keep reasonably strict threshold to stay heliophysics-focused.
            term_tokens = tokenize(" ".join([label] + synonyms))
            if result.score >= threshold and (term_tokens & anchor_tokens):
                envo_id = uri.rsplit("/", 1)[-1].replace("_", ":")
                records.append(
                    {
                        "envo_id": envo_id,
                        "envo_uri": uri,
                        "label": label,
                        "definition": " || ".join(definitions),
                        "synonyms": " | ".join(sorted(set(synonyms))),
                        "match_score": result.score,
                        "match_reason": " | ".join(result.reasons),
                        "matched_reference_terms": " | ".join(result.matched_terms),
                    }
                )

        elem.clear()

    return total_classes, records, sorted(envo_lexicon), sorted(set(envo_labels))


def write_gap_report(seed_norm: set, envo_lexicon: list, envo_labels: list, out_gaps: Path):
    envo_lex = set(envo_lexicon)
    missing = sorted([s for s in seed_norm if s not in envo_lex])

    with out_gaps.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "reference_term",
                "status",
                "nearest_envo_label_1",
                "nearest_envo_label_2",
                "nearest_envo_label_3",
            ],
        )
        writer.writeheader()

        for term in missing:
            best = []
            for lbl in envo_labels:
                # Fast prefilter: compare only somewhat similar lengths.
                if abs(len(lbl) - len(term)) > 18:
                    continue
                r = SequenceMatcher(None, term, lbl).ratio()
                if r >= 0.50:
                    best.append((r, lbl))
            best.sort(reverse=True)
            top = [b[1] for b in best[:3]]
            top += [""] * (3 - len(top))

            writer.writerow(
                {
                    "reference_term": term,
                    "status": "missing_in_envo",
                    "nearest_envo_label_1": top[0],
                    "nearest_envo_label_2": top[1],
                    "nearest_envo_label_3": top[2],
                }
            )

    return len(missing)


def write_outputs(
    total_classes: int,
    seed_count: int,
    records: list,
    out_csv: Path,
    out_summary: Path,
    out_gaps: Path,
    missing_count: int,
):
    records.sort(key=lambda r: (-int(r["match_score"]), r["label"].lower()))

    with out_csv.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "envo_id",
            "envo_uri",
            "label",
            "definition",
            "synonyms",
            "match_score",
            "match_reason",
            "matched_reference_terms",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    top_preview = "\n".join(f"- {r['label']} ({r['envo_id']}) [score={r['match_score']}]" for r in records[:25])
    summary = (
        "Quick ENVO Heliophysics Subset Summary\n"
        "====================================\n"
        f"ENVO source file: {ENVO_PATH}\n"
        f"Reference terms collected: {seed_count}\n"
        f"ENVO classes scanned: {total_classes}\n"
        f"Subset rows kept: {len(records)}\n"
        f"Output CSV: {out_csv}\n\n"
        f"Reference terms missing in ENVO: {missing_count}\n"
        f"Missing-term report: {out_gaps}\n\n"
        "Top matches:\n"
        f"{top_preview}\n"
    )

    out_summary.write_text(summary, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Quick/broad ENVO heliophysics subsetting")
    parser.add_argument("--mode", choices=["quick", "broad"], default="quick")
    args = parser.parse_args()

    mode = args.mode
    if mode == "broad":
        anchor_tokens = BROAD_ANCHOR_TOKENS
        threshold = 55
        out_csv = DATA_DIR / "envo_heliophysics_subset_broad.csv"
        out_summary = DATA_DIR / "envo_heliophysics_subset_broad_summary.txt"
        out_gaps = DATA_DIR / "envo_heliophysics_subset_broad_missing_reference_terms.csv"
    else:
        anchor_tokens = STRICT_ANCHOR_TOKENS
        threshold = 65
        out_csv = OUT_CSV
        out_summary = OUT_SUMMARY
        out_gaps = OUT_GAPS

    seed_terms = read_reference_terms(mode=mode)
    seed_norm, seed_tokens, token_to_seeds = build_seed_indices(seed_terms, anchor_tokens=anchor_tokens)
    domain_tokens = domain_token_set(seed_tokens, anchor_tokens=anchor_tokens)

    total_classes, records, envo_lexicon, envo_labels = parse_envo_and_filter(
        seed_norm=seed_norm,
        seed_tokens=seed_tokens,
        token_to_seeds=token_to_seeds,
        domain_tokens=domain_tokens,
        anchor_tokens=anchor_tokens,
        threshold=threshold,
    )

    missing_count = write_gap_report(
        seed_norm=seed_norm,
        envo_lexicon=envo_lexicon,
        envo_labels=envo_labels,
        out_gaps=out_gaps,
    )

    write_outputs(
        total_classes=total_classes,
        seed_count=len(seed_norm),
        records=records,
        out_csv=out_csv,
        out_summary=out_summary,
        out_gaps=out_gaps,
        missing_count=missing_count,
    )

    print(f"Mode: {mode}")
    print(f"Done. Scanned {total_classes} ENVO classes, kept {len(records)} rows.")
    print(f"Subset: {out_csv}")
    print(f"Summary: {out_summary}")
    print(f"Missing reference terms report: {out_gaps} ({missing_count} terms)")


if __name__ == "__main__":
    main()
