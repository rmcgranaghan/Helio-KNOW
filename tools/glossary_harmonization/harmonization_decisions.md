# Glossary Harmonization — Session Notes

Living record of the phenomena-glossary harmonization effort: process, decisions, current status, and how to resume. Working notebook: `glossary_generation_experiment_v1.ipynb` (all narrative/decision history lives there, cell by cell, in chronological order). This file is the condensed entry point.

## Process (established via the CME worked example)

For each term:
1. Gather all available source definitions (glossaries: HELIO Ontology, SPASE Dictionary, NASA Heliophysics Vocabulary, NASA CCMC, Space Weather Glossary/ESA variant, GCMD, SWEET, AGU Index Terms, plus non-glossary literature when a term has no glossary coverage).
2. Strip to semantic elements: core concept (shared) / variations-additions / degenerate cases.
3. Categorize:
   - **Category 1 — Non-Problematic**: one definition, or definitions identical/stylistically different only.
   - **Category 2 — Coalescible**: definitions differ slightly, aligned core — draft a merged definition.
   - **Category 3 — Conflicting**: different conceptual boundaries/superclass/scope — flag for structured analysis, but still draft a definition.
   - **Category 4 — Community Resolution Needed**: polysemy/conflation — draft anyway, add comments on what's unresolved instead of refusing to draft. Rare in practice; several automated Category-4 flags turned out to be false positives (see "corrections" below).
4. Identify semantic tensions explicitly (as many as needed).
5. Draft one harmonized core definition — keep it minimal; push descriptive/quantitative/associative detail into relationships instead of the definition sentence.
6. Add structured semantic extensions: Subclasses / Relationships / New Resulting Entities.
7. Map each source to the harmonized definition (which source contributed what; note gaps like SWEET-label-only).
8. Every `relates_to` / `associated_with` target in a term's Relationships becomes a **candidate** for a future round (not automatically included — see inclusion rule below).

**Term-splitting rule** (from the aurora/particle-precipitation/auroral-activity precedent): split one glossary term into siblings when the structured-extensions step keeps producing multiple *distinct, independently-usable* entities (a measurable quantity, a process, an observable manifestation) rather than staying subclasses/relationships of one thing. Example this session: `ion outflow` vs. `polar wind` were split rather than merged.

**Inclusion rule for new terms**: only pull a candidate term into a round if it (a) appears in an already-harmonized term's semantic neighborhood/relationships, or (b) is reached by walking the HelioKNOW hierarchy one step Broader/Narrower from an already-harmonized term. This is what keeps out neighborhood noise from unrelated domains (e.g., oceanographic/meteorological senses of "convection" that a naive embedding-similarity search would otherwise pull in).

## Where everything is stored

- **Notebook** `tools/glossary_harmonization/glossary_generation_experiment_v1.ipynb` — full narrative history, one markdown cell per exchange, in order. This is the "why" record; read it top to bottom to reconstruct reasoning, tensions raised, and corrections made.
- **Spreadsheet** `tools/glossary_harmonization/data/harmonization_worksheet_worked_examples_updating.xlsx`:
  - Sheet **"Terms"**: master term list. Columns: `Term`, `Definitions` (raw source text), `Round Included`. Update this every round — it had gotten out of sync earlier this session (new rows were appended past ~1000 blank formatted rows and were invisible without scrolling); fixed by moving Round 2 entries up to rows 14–29, directly after the Round 1 rows (2–13).
  - Sheet **"Worked Examples"**: the actual harmonization output. Columns: `Term`, `Definitions`, `Semantic Elements: Core concept`, `Variations/Additions`, `Degenerate Case(s)`, `Category for Harmonization`, `Semantic Tensions`, `Draft Definition`, `Structured Semantic Extensions: Subclasses`, `Relationships`, `New Resulting Entities`, `Map to Source Definitions`, `Comments`, `Round`.
- **Source data** (read-only inputs, not edited): `data/harmonization_terms_with_categories.csv` (per-term source defs + automated category + semantic-neighbor lists for ~10,600 candidate terms), `data/harmonization_prioritized_phenomena_v1_cleaned.csv` (95-term curated subset with fuller definitions — used as the fallback for gap-filling), `data/phenomena_helioknow_coverage.csv` (HelioKNOW's own term list with a shallow `broader` hierarchy + `is_principal` flag + `n_glossary_defs`).

## Current status (end of this session)

**Round 1 (11 terms, all in Worked Examples rows 2–12):** coronal mass ejection, aurora, geomagnetic activity (= geomagnetic storm), magnetic reconnection (merged with duplicate "reconnection"), Poynting flux, interplanetary magnetic field, solar flare, solar wind, substorm, convection (renamed "magnetospheric convection"), ion outflow.

**Round 2 (15 terms + 1 stub, Worked Examples rows 13–27):**
- Broader/parent terms: `plasma`, `sunspot`, `coronal hole`, `interplanetary shock`, `solar energetic particle` (all harmonized) + `burst` (still gapped — only 1 source definition exists anywhere).
- Narrower/HelioKNOW-hierarchy terms: `dayside reconnection`, `near-Earth magnetotail reconnection`, `distant-tail reconnection`, `diffuse aurora`, `broadband aurora`, `monoenergetic aurora`, `proton aurora`, `pulsating aurora`, `throat aurora` — all harmonized from user-supplied literature (NASA mission pages, Newell et al., Chen/Han/Zhang et al.).
- `magnetotail reconnection` — added as a structural umbrella parent (not independently sourced; inferred from its two children) to fix a hierarchy problem: "near-Earth" and "distant-tail" are locational qualifiers of magnetotail reconnection, not coordinate siblings of dayside (magnetopause) reconnection.

**Known open gaps:**
- `burst` — only one usable definition (Space Weather Glossary), needs another source before harmonizing.
- `magnetotail reconnection` — needs an independent source definition (currently purely inferred).
- Several `New Resulting Entities` flagged across rows are unharmonized candidate terms, not yet promoted to their own rows: `near-Earth neutral line (NENL)`, `distant neutral line`, `dispersive/kinetic Alfvén wave`, `field-aligned electric field/acceleration potential`, `magnetopause indentation`, `solar radiation storm`, `impulsive/gradual SEP event`.
- Semantic-neighborhood watchlist (parked, not yet queued — per the "hierarchy first" ordering decision): `auroral oval`, `high-speed stream` (now reinforced twice — via solar wind and via coronal hole), `Parker spiral`, `plasma sheet`, `polar wind`, `magnetic field` (already in Terms sheet row 8 but not yet in Worked Examples), `Dungey cycle`, `E×B drift`.

**Corrections made to the automated categorization** in `harmonization_terms_with_categories.csv` (recorded per-row in Comments, worth remembering for future rounds — the automated Category 3/4 flags are noisy):
- `solar wind`'s Category 4 flag was driven by an off-topic duplicate GCMD row ("solar winds", atmospheric-escape sense) — downgraded to Coalescible.
- `solar flare` / `substorm` / `interplanetary magnetic field` were flagged Conflicting mainly due to one source adding operational/quantitative detail, not a real boundary conflict — downgraded to Coalescible.
- `convection`'s Category 4 is real at the full-corpus level (cross-domain collision with meteorology/oceanography) but only one definition is heliophysics-relevant, so the HelioKNOW-scoped entry is effectively Category 1. Renamed to "magnetospheric convection" to disambiguate.
- `proton aurora` is a genuine Category 3: Earth (pitch-angle-scattered magnetospheric protons) and Mars (solar-wind charge-exchange ENAs) share a label but not a mechanism — kept split into two subclasses rather than merged, flagged as a cross-planetary harmonization case.

## Next steps

1. **Decide Round 3 term list.** Two ready sourcing strategies, not yet reconciled into one list:
   - HelioKNOW-hierarchy walk (one more step Broader/Narrower from Round 2 nodes): `Solar Wind Shock` cluster (+`Magnetopause Current`, `Region 1 Current`), `Ionization` cluster (+`Primary Ionization`, `Secondary Ionization`), `Termination Shock`, `Recombination`, `Fountain`, remaining `Ionization Feature` tail (~12 terms: Morning-side Arc, PBI, PMAF, Polar Cap Arc, Polar Cap Patch, Quiet Arc, SAID, SAPS, SED, STEVE, Streamer, Tongue Of Ionization). Full detail and rationale is in the notebook cell that walked `phenomena_helioknow_coverage.csv` as a graph.
   - Semantic-neighborhood watchlist (see above) — parked behind the hierarchy walk per the user's stated ordering preference, but `high-speed stream` now has two independent pointers to it (solar wind, coronal hole) and is a reasonable candidate to pull forward.
2. **Source the two remaining gaps**: `burst` (second definition) and `magnetotail reconnection` (independent definition) — likely need AGU Index Terms or a magnetospheric-physics textbook, not the existing glossary CSVs (already checked, zero/one rows).
3. **Promote flagged "New Resulting Entities"** (NENL, distant neutral line, Alfvén wave, etc.) to their own Worked Examples rows once/if they're prioritized.
4. **Cross-check against HelioKNOW ontology** (`data-models/hk_phenomenon.ttl`, `data/phenomena_helioknow_coverage.csv`) once a critical mass of terms is harmonized, to (a) list HelioKNOW terms with no definition from this process, and (b) feed back the hierarchy gaps discovered this session (HelioKNOW currently routes aurora/reconnection subtypes through generic buckets like "Ionization Feature"/"Solar Wind Shock" rather than through "Aurora"/"Reconnection" directly — worth reporting upstream).
5. Keep both spreadsheet sheets ("Terms" and "Worked Examples") in sync every round — this was missed for one cycle and had to be repaired.

## To resume this thread in a new session, read (in this order)

1. This file.
2. `tools/glossary_harmonization/glossary_generation_experiment_v1.ipynb` — full cell-by-cell history (start to finish; it's short enough to read in full and is the actual decision log).
3. `tools/glossary_harmonization/data/harmonization_worksheet_worked_examples_updating.xlsx` — sheets "Terms" and "Worked Examples", to see the actual current harmonized state.
4. `tools/glossary_harmonization/data/harmonization_terms_with_categories.csv` and `harmonization_prioritized_phenomena_v1_cleaned.csv` — source definitions for any term before assuming it needs non-glossary sourcing (check both; the second is a curated 95-term subset with fuller text and is the better first stop for "broader" candidate terms).
5. `tools/glossary_harmonization/data/phenomena_helioknow_coverage.csv` — HelioKNOW's own term list/hierarchy, for hierarchy-driven Round 3+ candidates.
