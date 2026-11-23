# Glossary Harmonization — Session Notes

Living record of the phenomena-glossary harmonization effort: process, decisions, current status, and how to resume. The [working notebook](glossary_generation_experiment_v1.ipynb) contains the original harmonization narrative and decision history. This file is the condensed entry point and records subsequent cross-check findings as well.

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
- **Comparison workbook**, created in the November 2026 cross-check: [glossary_hk_phenomena_comparison.xlsx](data/glossary_hk_phenomena_comparison.xlsx). Its **Comparison** sheet contains the 26 worked-example rows, the separately tracked `burst` gap, and 21 proposed Round 3 candidates. It records draft definitions, match/scope status, HK identifiers and asserted hierarchy, definitions, regions, instruments and models, plus review notes. Its **Read me** sheet documents methods, sources, and interpretation. This is a review snapshot, not an automatically refreshed or approved ontology mapping; update it when its source workbook or HK models change.
- **Source data** (read-only inputs, not edited): `data/harmonization_terms_with_categories.csv` (per-term source defs + automated category + semantic-neighbor lists for ~10,600 candidate terms), `data/harmonization_prioritized_phenomena_v1_cleaned.csv` (95-term curated subset with fuller definitions — used as the fallback for gap-filling), `data/phenomena_helioknow_coverage.csv` (HelioKNOW's own term list with a shallow `broader` hierarchy + `is_principal` flag + `n_glossary_defs`).

## Current status (November 2026 cross-check)

**26 worked-example rows:** 25 harmonized drafts and one inferred structural stub. The source worksheet has 11 Round 1 rows (2–12) and 15 Round 2 rows (13–27). `burst` is separately recorded in the Terms sheet, not in Worked Examples. This corrects the earlier Round 2 count in these notes and the notebook's inconsistent arithmetic; it does not mean all 26 rows are independently sourced harmonizations.

**Round 1 (11 terms, all in Worked Examples rows 2–12):** coronal mass ejection, aurora, geomagnetic activity, magnetic reconnection (merged with duplicate "reconnection"), Poynting flux, interplanetary magnetic field, solar flare, solar wind, substorm, convection (renamed "magnetospheric convection"), ion outflow. The worked definition treats geomagnetic activity as a broad concept; the HK `Geomagnetic Storm` is a related, more specific event, not an established equivalent.

**Round 2 (14 harmonized drafts + 1 structural stub, Worked Examples rows 13–27):**
- Broader/parent terms: `plasma`, `sunspot`, `coronal hole`, `interplanetary shock`, `solar energetic particle` (all harmonized) + `burst` (separately tracked as a gap — one usable source definition found in the checked material).
- Narrower/HelioKNOW-hierarchy terms: `dayside reconnection`, `near-Earth magnetotail reconnection`, `distant-tail reconnection`, `diffuse aurora`, `broadband aurora`, `monoenergetic aurora`, `proton aurora`, `pulsating aurora`, `throat aurora` — all harmonized from user-supplied literature (NASA mission pages, Newell et al., Chen/Han/Zhang et al.).
- `magnetotail reconnection` — added as a structural umbrella parent (not independently sourced; inferred from its two children) to fix a hierarchy problem: "near-Earth" and "distant-tail" are locational qualifiers of magnetotail reconnection, not coordinate siblings of dayside (magnetopause) reconnection.

**Known open gaps:**
- `burst` — only one usable definition (Space Weather Glossary), needs another source before harmonizing.
- `magnetotail reconnection` — needs an independent source definition (currently purely inferred).
- Several `New Resulting Entities` flagged across rows are unharmonized candidate terms, not yet promoted to their own rows: `near-Earth neutral line (NENL)`, `distant neutral line`, `dispersive/kinetic Alfvén wave`, `field-aligned electric field/acceleration potential`, `magnetopause indentation`, `solar radiation storm`, `impulsive/gradual SEP event`.
- Semantic-neighborhood watchlist (parked, not yet queued — per the "hierarchy first" ordering decision): `auroral oval`, `high-speed stream` (now reinforced twice — via solar wind and via coronal hole), `Parker spiral`, `plasma sheet`, `polar wind`, `magnetic field` (already in Terms sheet row 8 but not yet in Worked Examples), `Dungey cycle`, `E×B drift`.

**Corrections to the automated categorization** from `harmonization_terms_with_categories.csv` (recorded in worked-example rows, not edits to the source CSV; automated Category 3/4 flags are noisy):
- `solar wind`'s Category 4 flag was driven by an off-topic duplicate GCMD row ("solar winds", atmospheric-escape sense) — downgraded to Coalescible.
- `solar flare` / `substorm` / `interplanetary magnetic field` were flagged Conflicting mainly due to one source adding operational/quantitative detail, not a real boundary conflict — downgraded to Coalescible.
- `convection`'s Category 4 is real at the full-corpus level (cross-domain collision with meteorology/oceanography) but only one definition is heliophysics-relevant, so the HelioKNOW-scoped entry is effectively Category 1. Renamed to "magnetospheric convection" to disambiguate.
- `proton aurora` is a genuine Category 3: Earth (pitch-angle-scattered magnetospheric protons) and Mars (solar-wind charge-exchange ENAs) share a label but not a mechanism — kept split into two subclasses rather than merged, flagged as a cross-planetary harmonization case.

## Cross-check findings and decisions

- **Separation of responsibilities:** the glossary retains source definitions, draft harmonizations, tensions, and provenance; the HK models represent concepts and relationships. A shared label or related concept is a candidate for review, not an approved equivalence, definition, or ontology assertion. Preserve existing concept URIs when considering changes.
- **Meaningful existing overlap:** the phenomenon model includes CME, flare, geomagnetic storm, IMF, Poynting flux, solar wind, ion outflow, substorm, and several aurora and reconnection subtypes. It also links some phenomena to instrument types, models, and regions. The core supplies shared classes/properties; the other modules supply resource and spatial context.
- **Missing or incomplete alignment:** no direct HK phenomenon concept was identified for general aurora or magnetic reconnection, magnetospheric convection, sunspot, coronal hole, or solar energetic particle. The HK graph references external SWEET `Plasma` as a parent of `SolarWindPlasma`; that is not a general HK phenomenon concept. Existing related concepts are not automatically missing-label equivalents.
- **Hierarchy and scope require review:** HK places aurora subtypes under `Ionization Feature`, and near-Earth/tail reconnection under `Solar Wind Shock`; the glossary proposes a general aurora concept and a magnetotail-reconnection umbrella. HK `Tail Reconnection` is less specific by label than the glossary's distant-tail draft. `Solar Wind Shock` has `Bow shock` as an alternate label, so do not equate it with interplanetary shock without reviewing scope. The one available `burst` source describes solar radio emission, whereas HK places CME and flare beneath `Burst`; its scope also needs review.
- **Other review issues:** examine Poynting flux as a physical quantity versus its HK phenomenon typing, the draft's wave/per-steradian wording, the planetary scope of proton aurora, and whether HK `Streamer` refers to an auroral or solar sense. These are review questions, not adopted ontology changes.
- **Comparison limits:** the workbook uses assertions in the five local HK TTL files, without resolving external imports. A blank relationship means no local assertion was found, not that no scientific connection exists. The coverage CSV's glossary-definition count is not an HK definition count. No HK TTL files or source harmonization worksheets were changed in this cross-check.
- **Round selection remains provisional:** retain the user's hierarchy-first ordering; semantic-neighborhood candidates stay parked unless deliberately selected. The notebook's 21 named Round 3 candidates have not been approved, and its 12-term `Ionization Feature` tail may be deferred to Round 4.

## Targeted next work (recommended priorities)

1. **Resolve the two sourcing gaps.** Find an additional usable definition for `burst` and an independent source for `magnetotail reconnection`; review the `burst` scope against HK before harmonizing. Do not count the structural stub as complete until sourced and reviewed.
2. **Confirm the Round 3 scope before drafting.** The proposed 21 terms are: `Solar Wind Shock`, `Magnetopause Current`, `Region 1 Current`; `Ionization`, `Primary Ionization`, `Secondary Ionization`; `Termination Shock`, `Recombination`, `Fountain`; and the optional 12-term tail `Morning-side Arc`, `Poleward Boundary Intensification (PBI)`, `Poleward Moving Auroral Form (PMAF)`, `Polar Cap Arc`, `Polar Cap Patch`, `Quiet Arc`, `Subauroral Ion Drift (SAID)`, `Subauroral Polarization Stream (SAPS)`, `Storm-Enhanced Density (SED)`, `Strong Thermal Emission Velocity Enhancement (STEVE)`, `Streamer`, and `Tongue Of Ionization`. Decide whether to defer the tail. `high-speed stream` remains a watchlist candidate, not an automatically included term.
3. **Review and propose HK changes with provenance.** Start with aurora/reconnection parents and subtype hierarchies, the geomagnetic activity/storm distinction, and the shock/burst scope questions above. Review candidate definitions and identifiers before feeding changes upstream; do not convert the comparison workbook into ontology assertions without review.
4. **After priorities are chosen**, promote relevant flagged new entities (NENL, distant neutral line, Alfvén wave, etc.) to worked examples, source their definitions, and assess missing HK concepts. Produce a broader HK coverage inventory if needed; the comparison covers the existing worked examples and proposed candidates, not every HK phenomenon.
5. **Keep artifacts synchronized:** update both Terms and Worked Examples each round, record decisions and provenance here and in the notebook as appropriate, and refresh the comparison workbook after glossary or HK changes.

## To resume this thread in a new session, read (in this order)

1. This file.
2. `tools/glossary_harmonization/glossary_generation_experiment_v1.ipynb` — original cell-by-cell harmonization history and detailed scientific rationale.
3. `tools/glossary_harmonization/data/harmonization_worksheet_worked_examples_updating.xlsx` — sheets "Terms" and "Worked Examples", to see the actual current harmonized state.
4. [glossary_hk_phenomena_comparison.xlsx](data/glossary_hk_phenomena_comparison.xlsx) — cross-check snapshot, Round 3 candidate list, and methodology in its Read me sheet.
5. `tools/glossary_harmonization/data/harmonization_terms_with_categories.csv` and `harmonization_prioritized_phenomena_v1_cleaned.csv` — source definitions for any term before assuming it needs non-glossary sourcing (check both; the second is a curated 95-term subset with fuller text and is the better first stop for "broader" candidate terms).
6. `tools/glossary_harmonization/data/phenomena_helioknow_coverage.csv` — HelioKNOW's own term list/hierarchy, for hierarchy-driven Round 3+ candidates.
