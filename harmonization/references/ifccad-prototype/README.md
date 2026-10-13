# IFCCAD Prototype

IFCCAD is an open package concept for CAD-only and BIM-aware drawings. A package combines semantic project and drawing structure with compact drawing resources and optional preservation data:

```text
IFCCAD package = IFCX + one or more IFCDR resources + optional IFCPR resources
```

| Part | Responsibility |
| --- | --- |
| **IFCX** | Project context, drawing sets, layouts, reusable named definitions, resource references, and optional links to IFC products. |
| **IFCDR** | High-volume drawing payloads encoded as typed columnar streams: geometry, text, dimensions, block content, hatches, viewports, bindings, and occurrence overrides. |
| **IFCPR** | Optional source records, dependencies, fingerprints, and opaque payloads for information that IFCX and IFCDR do not represent. |

## Prototype Status

This repository is the experimental, model-first Python reference implementation and format laboratory for IFCCAD. It demonstrates the package architecture, validates the physical contracts, and supports semantic DXF roundtrips for a useful 2D CAD subset.

The prototype is an interoperability baseline. It is not yet a production converter, a complete DWG/DXF replacement, or a guarantee of lossless roundtrips for arbitrary source files. Unsupported source-record capture and re-emission are specified and tested with synthetic payloads. The primary Rust format implementation lives in [ifccad](https://github.com/OpenAEC-Foundation/ifccad); production DWG/DXF preservation and `CadDocument` conversion belong at the boundary of the future `ifccad-cad-document` companion crate.

## Architecture

```text
DXF <-> IfcCadDocument + PreservationStore <-> package codec
                                               <-> IFCX + IFCDR[] + IFCPR[]

IfcCadDocument
  definitions: IfcDefinitionCatalog
  drawings[]: IfcCadDrawing
    layouts and workspace state
    drawing: DrawingDocument
      modelspace, paperspaces, blocks, viewports
      typed CAD entities with persistent EntityId values
      explicit per-scope draw order
  preservation: optional PreservationStore
```

The runtime model is object-based. Streams are an on-disk representation, not the editing model. Feature development follows this direction:

```text
CAD concept -> package/drawing object model -> storage mapping -> adapter
```

Named reusable definitions live in IFCX. IFCDR contains resource-local bindings, occurrences, geometry, placement, and sparse occurrence overrides. IFCPR remains a synchronized preservation layer beside editable CAD meaning.

## Supported Scope

The current prototype covers:

- lines, polylines, circles, arcs, points, and ellipses;
- text, structured multiline text, text styles, and block attributes;
- block definitions, nested inserts, and cycle validation;
- hatch boundaries, solid fills, and line-based hatch patterns;
- linear and aligned dimensions with styles and sparse overrides;
- layers, reusable appearances, opacity, and ByLayer/ByBlock/explicit intent;
- multiple drawing resources, modelspace, paperspaces, layouts, and viewports;
- plot settings, workspace state, stored views, grid, snap, and UCS state;
- persistent resource-local entity identity and explicit draw order;
- IFCX/IFCDR/IFCPR JSON codecs, validation, checksums, and conformance fixtures.

Important gaps include splines, leaders, raster images, external references, tables, most dimension types, proxy objects, 3D geometry, complete MTEXT layout fidelity, and production source-record preservation. The detailed and authoritative matrix is in [File Format Support](docs/file-format-support.md).

## Run the Prototype

Requirements:

- Python 3.11 or newer;
- `ezdxf` 1.3 or newer;
- `jsonschema` 4.23 or newer.

Create an environment and install the package in editable mode:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

Run the complete Python test suite:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

Run the self-contained cross-language conformance suite:

```powershell
$env:PYTHONPATH = "src"
python -m ifccad.conformance conformance
```

The committed [`conformance`](conformance) corpus is the interoperability handoff for independent implementations such as [ifccad](https://github.com/OpenAEC-Foundation/ifccad). It does not depend on the repository's DXF/DWG samples.

## Documentation

Start with the [documentation index](docs/README.md). The main living documents are:

- [IFCCAD Vision](docs/vision/ifccad_vision.md)
- [File Format Support](docs/file-format-support.md)
- [Object Model](docs/object-model.md)
- [Prototype Evaluation and Acadifc Guidance](docs/prototype-evaluation-and-acadifc-guidance.md)

Historical phase specifications and implementation plans under `docs/superpowers/` record how the prototype evolved; they are not the current normative overview.

## Repository Layout

```text
src/ifccad/       Python domain model, codecs, validation, and DXF adapter
schemas/          Language-neutral IFCDR and IFCPR schemas
conformance/      Cross-language packages, vectors, scenarios, and manifest
tests/            Unit, semantic roundtrip, and conformance tests
docs/             Vision, format, object-model, evaluation, and design history
DXF DWG samples/  Source CAD samples; generated conversions remain ignored
```

Python is used for rapid, readable format experiments. The standalone [ifccad](https://github.com/OpenAEC-Foundation/ifccad) crate owns the production Rust format implementation and links back to this prototype through its provenance record. Performance-sensitive CAD conversion is expected to use the future `ifccad-cad-document` companion crate, while this repository remains a reference implementation and conformance test bed.

## License

IFCCAD is available under the [MIT License](LICENSE).
