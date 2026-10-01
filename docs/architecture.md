# Project Architecture

## Overview

AltiumPcbLibTools is being developed as a set of tools for programmatic analysis and manipulation of Altium Designer PcbLib footprints.

The project is intentionally being developed in stages.

The first priority is to understand the structure of real PcbLib data and establish a clear semantic representation before implementing footprint generation and modification features.

## Development Flow

The intended processing flow is:

```text
Altium PcbLib
      |
      v
  Read / Decode
      |
      v
Footprint Structure
      |
      v
 Semantic JSON
      |
      v
   Validate
      |
      v
 Modify / Create
      |
      v
Altium PcbLib
      |
      v
 Verification in Altium Designer
```

This represents the intended direction of the project. Not all stages are currently implemented.

## PcbLib as the Source

The source of the initial research is real Altium Designer PcbLib files.

Rather than designing a hypothetical data model first, the project uses real footprints to discover the structures and properties that need to be represented.

This approach helps ensure that the JSON model is based on actual Altium data.

## Footprint Representation

A footprint is treated as a collection of semantic objects, or primitives.

Examples include:

* Pads
* Tracks
* Arcs
* Component bodies
* Other footprint-level properties

Each primitive may contain geometric, electrical, layer, display, or other properties depending on its type.

The JSON representation should preserve the information necessary to understand these objects without requiring the reader to interpret the original binary PcbLib structure.

## Semantic JSON

The JSON representation is not intended to be a byte-for-byte representation of a PcbLib file.

Its purpose is to provide a readable description of the footprint.

For example, a track should be represented through meaningful properties such as its layer, endpoints, width, and other applicable attributes rather than as an encoded binary record.

The exact schema will be developed from real PcbLib examples and refined as additional footprint types are analyzed.

## Validation

Validation is an important part of the architecture.

A valid semantic representation should contain the properties required by each primitive type and should reject invalid or incomplete data.

Examples of validation may include:

* Required properties are present.
* Coordinates are valid.
* Geometric relationships are valid.
* Layer names or identifiers are recognized.
* Primitive-specific properties are present.
* Values have appropriate types and ranges.

The validation rules will be developed incrementally as the underlying PcbLib structures become better understood.

## PcbLib Generation

A later stage of the project will use the semantic representation to create or modify PcbLib footprints.

Generated files must ultimately be tested against real Altium Designer software.

Successful generation therefore means more than producing a syntactically valid file; the resulting footprint must be correctly interpreted by Altium Designer.

## Verification

Verification will be performed at multiple levels.

### Data Level

Compare extracted information with the original PcbLib data.

### Structural Level

Verify that the expected primitives and properties are present.

### File Level

Verify that generated or modified PcbLib files can be opened and processed correctly.

### Application Level

Open generated PcbLib files in Altium Designer and verify the resulting footprints.

Altium Designer 15.1 is being used as one of the reference environments for testing.

## Third-Party Software

The project may use third-party software and libraries to assist with reading and writing Altium files.

In particular, `altium_monkey` has been used during the initial PcbLib research and testing.

Third-party code remains subject to its own licensing terms and is kept conceptually separate from original AltiumPcbLibTools code.

See the project README for additional information.

## Repository Structure

The repository is organized around the following areas:

```text
AltiumPcbLibTools/
├── README.md
├── docs/
├── src/
└── tests/
```

### `docs/`

Project documentation, technical notes, architecture information, and findings from reverse engineering.

### `src/`

Source code belonging to AltiumPcbLibTools.

### `tests/`

Tests used to verify individual components and complete processing workflows.

## Development Principle

The project follows a simple principle:

> Understand the real data first, then build the abstraction.

This means that observations from real PcbLib files should guide the design of the semantic model rather than forcing real files into a prematurely defined structure.
