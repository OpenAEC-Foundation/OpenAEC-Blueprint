# IFCCAD Documentation

This directory contains the living description of the IFCCAD package and the engineering record behind the Python reference prototype.

## Start Here

- [IFCCAD Vision](vision/ifccad_vision.md) explains the long-term purpose and the IFCX/IFCDR package split. A [formatted concept page](vision/ifccad_vision.html) presents the same vision visually.
- [File Format Support](file-format-support.md) is the authoritative matrix of implemented formats, entities, streams, validation rules, and known gaps.
- [Object Model](object-model.md) describes the model-first Python domain objects and their mapping to storage.
- [Prototype Evaluation and Acadifc Guidance](prototype-evaluation-and-acadifc-guidance.md) evaluates the complete IFCX/IFCDR/IFCPR P24 baseline and records the rules to carry into the Rust implementation.

## Interoperability Contracts

The machine-readable contracts live at repository root:

- [`schemas/ifcdr`](../schemas/ifcdr) defines the IFCDR `0.5.0` stream registry.
- [`schemas/ifcpr`](../schemas/ifcpr) defines the IFCPR `0.1.0` preservation resource.
- [`conformance`](../conformance) contains versioned package fixtures, canonicalization vectors, lifecycle scenarios, export-planning scenarios, and the suite manifest.

These contracts are intended for independent implementations. The Python runner is available through `python -m ifccad.conformance conformance` from the repository root.

## Development Record

- [`superpowers/specs`](superpowers/specs) contains approved design specifications for prototype phases.
- [`superpowers/plans`](superpowers/plans) contains the corresponding implementation plans.
- [`reports`](reports) contains historical sample-coverage reports.

The phase documents explain design history but are not normative. For the current state, use the four living documents listed under **Start Here** together with the machine-readable schemas and conformance corpus.
