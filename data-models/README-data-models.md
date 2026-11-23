# Helio-KNOW Data Models

This directory contains the semantic models and controlled vocabularies used by **Helio-KNOW (Heliophysics KNOWledge Network)** and related heliophysics data-discovery activities.

The artifacts provide shared concepts and relationships for describing heliophysics phenomena, instruments, models, and regions. They are intended to support consistent annotation and discovery across datasets, services, scientific software, and knowledge-based applications.

The models are complementary modules, not interchangeable files. The core model provides shared classes and properties; the domain modules provide more specific concepts and mappings.

## What is here

| Artifact | Scope | How to use it |
|---|---|---|
| `hk_core.ttl` | Shared Helio-KNOW core vocabulary and foundational classes, properties, and concepts. It imports BFO and SKOS. | Start here for shared terms and the common semantic foundation used by the other `hk_*` models. |
| `hk_phenomenon.ttl` | Phenomenon concepts and semantic links between phenomena, instruments, models, and regions. | Use for phenomenon-centered discovery and for connecting scientific phenomena to relevant resources. This module imports the core, instrument, model, and region modules. |
| `hk_instruments.ttl` | Instrument and instrument-type concepts, including mappings to external instrument vocabularies and metadata systems such as SPASE and Madrigal/CEDAR. | Use to describe instrument types and connect external instrument descriptions to Helio-KNOW concepts. |
| `hk_model.ttl` | Model concepts and model metadata, including identifiers, labels, versions, status, and landing pages for CCMC models. | Use to describe models and connect them to the phenomena they represent. |
| `hk_region.ttl` | SKOS-oriented heliophysics region taxonomy. | Use for region concepts and their broader/narrower organization. Check its version metadata before relying on it in a release. |
| `hk_region-v3.0.ttl`, `hk_region-v3.1.ttl` | Earlier versioned region-taxonomy snapshots. | Retained for historical comparison and migration context; do not assume these are the current region model. |
| `heliodata_region_taxonomy-v2.0.ttl` | Earlier region taxonomy associated with the HelioData/helio.data use case. | Retained for compatibility and historical context. It is not interchangeable with the newer `hk_region` taxonomy. |

## How the modules fit together

- **Core (`hk_core.ttl`)** defines shared semantic foundations used across the network.
- **Phenomena (`hk_phenomenon.ttl`)** organizes scientific phenomena and connects them to related resources and semantic contexts.
- **Instruments (`hk_instruments.ttl`)** describes instruments and instrument types, including mappings to external descriptions.
- **Models (`hk_model.ttl`)** describes models and their metadata.
- **Regions (`hk_region.ttl`)** provides a controlled vocabulary and hierarchy for heliophysics regions.

The modules use separate namespaces under `https://www.helioknowledge.network/`:

- `https://www.helioknowledge.network/core/`
- `https://www.helioknowledge.network/phenomenon/`
- `https://www.helioknowledge.network/instruments/`
- `https://www.helioknowledge.network/model/`
- `https://www.helioknowledge.network/region/`

The Turtle files declare ontology base URIs without the trailing slash (for example, `https://www.helioknowledge.network/core`) and use namespace IRIs with a trailing slash for terms. Preserve existing identifiers when editing or extending the models. Do not mint replacement identifiers solely to reorganize files.

The current phenomenon module imports the core, instruments, model, and region modules. The instrument, model, and region modules import the core model. Consult the imports declared in each TTL file as the authoritative record of dependencies.

## Relationship to glossary harmonization

The phenomenon model and the phenomenon glossary serve related but distinct purposes.

- The **glossary harmonization work** records source definitions, compares usage across communities and resources, develops harmonized natural-language definitions, and documents semantic tensions and editorial decisions.
- The **phenomenon model** represents concepts and their formal relationships, including broader/narrower structure and links to instruments, models, and regions.

The two should be linked using stable phenomenon concept URIs. Where a glossary term corresponds to a concept in `hk_phenomenon.ttl`, its harmonized definition can be represented as a definition annotation on that concept, with source attribution and provenance retained. The glossary can also expose selected ontology relationships as an expanded dictionary entry.

Do not treat every draft definition, candidate relationship, or unresolved harmonization issue as an approved ontology assertion. Preserve review status and provenance in the source glossary/harmonization record.

## Intended use

These models are intended to support:

1. **Phenomenon-centered resource discovery** — connecting scientific phenomena to datasets, instruments, and models.
2. **Metadata annotation and interoperability** — providing shared labels, identifiers, and mappings that data providers and services can use.
3. **Semantic integration** — relating concepts across heliophysics resources and external vocabularies.
4. **Knowledge-based applications** — providing explicit semantic context for search, APIs, literature and dataset annotation, and agentic information retrieval.

The Level 1 use case is primarily discovery and semantic linking: for example, identifying datasets, instruments, or models associated with a phenomenon. It should not be confused with observation-level retrieval, such as identifying the exact time intervals in a dataset when a particular signature occurred. That requires additional observation, feature-of-interest, time, and result representations beyond the phenomenon-centered model.

## Working with the Turtle files

The models are provided in RDF Turtle (`.ttl`). A typical workflow is:

1. Load the relevant Turtle files into an RDF tool or triple store.
2. Load the dependencies required by the modules you intend to use.
3. Query the relevant concept scheme and relationships using SPARQL.
4. Follow external identifiers and mappings where a concept is linked to SPASE, Madrigal/CEDAR, CCMC, SWEET, or another vocabulary.
5. Record proposed changes with their rationale, source, and impact on dependent modules.

A consumer that needs only one domain may still need to load the shared core and any imported modules required to resolve the graph. Check each file's `owl:imports` declarations rather than assuming that a file is standalone.

## Versioning and status

The directory contains artifacts at different stages and with different histories. A filename alone does not guarantee that an artifact is a formally released version.

Before treating a file as a stable release, check:

- Its ontology IRI and namespace.
- `owl:versionInfo` and other version metadata.
- Its declared imports.
- Whether it is the current artifact or a retained historical snapshot.
- Whether its concepts and mappings have been reviewed for the intended use.

The region taxonomy has explicit historical snapshots in this directory. Keep the README synchronized with the version metadata in the current `hk_region.ttl` file.

**Status note:** This README describes the observed organization and intended roles of the files. It does not certify every file as production-ready or establish a formal release process. Release status, maintainers, and version policy should be recorded explicitly as the project adopts them.

## Contributing

When proposing a change:

1. Identify the affected concept(s), file(s), and namespace(s).
2. Preserve existing concept URIs unless a reviewed migration plan explicitly requires otherwise.
3. Provide a source or scientific rationale for new definitions, labels, mappings, or relationships.
4. Distinguish asserted relationships from candidate, provisional, or unresolved ones.
5. Check imports and downstream dependencies.
6. Update this README when module scope, dependencies, or status changes.
7. Submit changes through a pull request that explains the scientific or interoperability need and any compatibility implications.

For changes to phenomenon definitions, coordinate with the glossary-harmonization process so that the formal ontology and community-reviewed terminology remain aligned without collapsing their distinct responsibilities.

## Important distinctions

- A **concept vocabulary / ontology** defines terms and semantic relationships; it is not itself a catalog of all observations or a replacement for numerical data services.
- A **phenomenon** is not the same thing as an **observable property**, an **observation**, or an **event**. These may be linked in more advanced semantic models, but should not be conflated.
- A **model associated with a phenomenon** is not necessarily an observation of that phenomenon.
- A **region taxonomy** organizes spatial concepts; it does not, by itself, specify the time-dependent location or spatial footprint of a particular observation.

## Related project resources

- Helio-KNOW repository: https://github.com/rmcgranaghan/Helio-KNOW
- Data models directory: https://github.com/rmcgranaghan/Helio-KNOW/tree/main/data-models
- Glossary-harmonization materials: https://github.com/rmcgranaghan/Helio-KNOW/tree/main/tools/glossary_harmonization

## Maintenance items for the next repository pass

- Confirm that `hk_core.ttl` is the core ontology and `hk_phenomenon.ttl` is the phenomenon module. Their namespaces and contents indicate these are distinct roles.
- Add explicit version, status, and maintainer metadata to each module where it is absent or incomplete.
- Identify which region files are current, historical, or compatibility artifacts.
- Document the release process and supported dependency/import strategy.
- Add small validated examples, such as a SPARQL query that finds instruments or models associated with a phenomenon.