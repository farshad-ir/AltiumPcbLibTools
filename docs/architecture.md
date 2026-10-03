# Project Architecture

## Overview

**AltiumPcbLibTools** is a semantic toolkit for extracting,
transforming, and generating Altium Designer PcbLib footprints.

The project is built around a clear separation of responsibilities:

* Real Altium PcbLib files are the source of truth.
* `altium_monkey` handles low-level PcbLib file mechanics.
* AltiumPcbLibTools operates at the semantic level.
* JSON provides a readable and programmatically usable representation.
* Generated PcbLib files are verified in real Altium Designer.

The project has been developed incrementally through three working products.

---

## Architecture

The current architecture is:

```text
                 Real Altium PcbLib
                         |
                         v
                   altium_monkey
                 Read / Write layer
                         |
                         v
              AltiumPcbLibTools
                     Extractor
                         |
                         v
               Semantic Footprint
                         |
                         v
                   Semantic JSON
                         |
              +----------+----------+
              |                     |
              v                     v
       Analysis /              Transformation
       Modification                  |
              |                     |
              +----------+----------+
                         |
                         v
                   altium_monkey
                         |
                         v
                Generated PcbLib
                         |
                         v
                 Altium Designer
```

The important architectural decision is that AltiumPcbLibTools does not
attempt to reimplement the PcbLib binary format.

The low-level file mechanics are delegated to `altium_monkey`.

AltiumPcbLibTools works above that layer with meaningful footprint concepts.

---

# Three Current Products

The project currently has three working products.

## Product 1 — PcbLib to JSON

The first product extracts a real Altium footprint and converts it into
semantic JSON.

```text
PcbLib
   |
   v
altium_monkey
   |
   v
Extractor
   |
   v
Semantic Footprint
   |
   v
JSON
```

The extraction process can:

1. Open a real PcbLib.
2. Locate a footprint.
3. Extract supported primitives.
4. Extract footprint parameters.
5. Build the semantic representation.
6. Export the result as JSON.

The JSON representation currently includes:

* Footprint parameters
* Pad Masters
* Pads
* Tracks
* Arcs

A real `CAP_BOSHKE_SMD` footprint has been used during development and
testing.

---

## Product 2 — JSON to PcbLib: Pads

The second product takes semantic JSON and generates a new PcbLib
containing pads.

```text
JSON
 |
 v
Pad Masters
 |
 v
Pad Instances
 |
 v
altium_monkey
 |
 v
PcbLib
```

The writer can:

* Create the PcbLib container.
* Create the footprint.
* Recreate Pad Masters.
* Create pad instances.
* Reuse Pad Masters.
* Preserve pad geometry.
* Preserve pad position.
* Preserve pad rotation.
* Preserve supported hole and plating information.

This product also demonstrated programmatic pad duplication and rotation.

A single Pad Master can be reused by multiple pad instances:

```text
              Pad Master
                   |
        +----------+----------+
        |          |          |
      Pad 1      Pad 2      Pad 3
        |          |          |
     position   position   position
     rotation   rotation   rotation
```

The important capability is therefore not simply rotating a pad, but
programmatically creating multiple instances from a common semantic
definition.

The generated PcbLib has been verified in Altium Designer 15.1.

---

## Product 3 — JSON to PcbLib: Pads + Tracks + Arcs

The third product extends the writer to the currently supported full
graphical footprint representation.

```text
JSON
 |
 +---- Pads
 |
 +---- Tracks
 |
 +---- Arcs
 |
 v
altium_monkey
 |
 v
PcbLib
```

The current supported primitives are:

* Pads
* Tracks
* Arcs

Supported Track information includes:

* Start point
* End point
* Width
* Layer

Supported Arc information includes:

* Center
* Radius
* Start angle
* End angle
* Width
* Layer

A real `29-04` footprint of a `Q2n2222` containing Pads, Tracks, and an Arc has been
extracted, transformed, generated again, and successfully opened in
Altium Designer 15.1.

This is the current definition of the project's **Full supported
footprint**.

It does not mean that every possible Altium primitive is currently
supported.

---

# Semantic Footprint Model

The semantic model is the central abstraction of the project.

A footprint is represented through meaningful objects rather than through
the binary structures of a PcbLib file.

The current model contains:

```text
Footprint
 |
 +-- Parameters
 |
 +-- Pad Masters
 |      |
 |      +-- Pad
 |      +-- Pad
 |      +-- Pad
 |
 +-- Tracks
 |
 +-- Arcs
```

The model can therefore be manipulated without requiring the user to work
directly with PcbLib binary data.

---

# Semantic JSON

The JSON representation is a **semantic intermediate representation**.

It is not intended to be a byte-for-byte copy of the original PcbLib.

For example, a Track is represented by meaningful properties such as:

```text
layer
start
end
width
options
```

An Arc is represented by:

```text
layer
geometry
options
```

where the geometry contains information such as:

```text
center
radius
start angle
end angle
```

Pads use the Pad Master / Pad Instance relationship.

This design makes the JSON:

* readable
* editable
* programmatically transformable
* suitable for testing
* independent of the original binary encoding

---

# Pad Master and Pad Instance

A Pad Master represents the common definition of a pad.

It can contain properties such as:

* Shape
* Dimensions
* Layer
* Hole information
* Plating
* Other pad-specific properties

A pad instance contains information specific to its placement:

* Designator
* Position
* Rotation
* Optional overrides

Conceptually:

```text
                Pad Master
                    |
        +-----------+-----------+
        |           |           |
      Pad 1       Pad 2       Pad 3
        |           |           |
     position    position    position
     rotation    rotation    rotation
```

This separation allows multiple pads to reuse the same definition while
having independent positions and rotations.

It is one of the important semantic concepts established by the project.

---

# Division of Responsibility

## `altium_monkey`

`altium_monkey` is responsible for the low-level mechanics required to
read and write Altium PcbLib files.

This includes the difficult binary/file-format work.

AltiumPcbLibTools deliberately does not duplicate that functionality.

## AltiumPcbLibTools

AltiumPcbLibTools operates at a higher level.

Its responsibilities include:

* Extracting semantic information.
* Building the semantic footprint model.
* Serializing the model to JSON.
* Transforming footprint data.
* Generating supported footprint primitives.
* Providing practical tools and workflows.
* Testing the resulting PcbLib files.

This separation keeps the project focused on **what the footprint means**
rather than on reimplementing the complete PcbLib binary format.

Third-party code remains subject to its own licensing terms.

---

# Current Supported Primitives

The current Products 1–3 support:

```text
Pads
Tracks
Arcs
```

The following primitives are future extensions:

```text
ComponentBody
Text
Region
Fill
Via
Other graphical primitives
3D model data
```

These are intentionally not current prerequisites.

They should only be investigated and implemented when a real use case
requires them.

---

# Verification Strategy

Verification takes place at several levels.

## Extraction Verification

Check that information extracted from a real PcbLib corresponds to the
actual footprint.

## Semantic Verification

Check that the semantic model contains the expected objects and properties.

## Transformation Verification

Check that programmatic changes produce the intended semantic result.

For example, the pad duplication milestone demonstrated that multiple pad
instances can reuse one Pad Master while having independent positions and
rotations.

## PcbLib Verification

Check that the generated PcbLib can be opened and processed correctly.

## Altium Verification

Open the generated PcbLib in Altium Designer 15.1 and verify the resulting
footprint.

Application-level verification is important because producing a file is not
by itself sufficient.

---

# Repository Structure

The current repository structure is:

```text
AltiumPcbLibTools/
├── .git/
├── .gitignore
├── .venv/
│
├── README.md
├── TODO.md
│
├── 29_04.json
├── CAP_BOSHKE_ROUNDTRIP.PcbLib
├── P2904.PcbLib
├── PSMD4.PcbLib
│
├── altium_monkey/
│
├── builder/
├── classifier/
├── exporter/
├── extractor/
├── model/
├── tools/
├── writer/
│
├── docs/
│
├── examples/
│
├── tests/
│
└── main.py
```

The `.venv/` directory is a local development environment and is not part
of the conceptual application architecture.

The sample PcbLib and JSON files at the repository root are development and
testing artifacts.

### `altium_monkey/`

Third-party low-level PcbLib implementation used for reading and writing
Altium files.

### `extractor/`

Code responsible for reading PcbLib data through `altium_monkey` and
converting it into the project's semantic representation.

### `model/`

Semantic footprint data structures.

### `writer/`

PcbLib generation and transformation logic.

This includes the current Pad-only and Full writers.

### `exporter/`

Export-related functionality, including semantic JSON export.

### `tools/`

Practical command-line and utility tools.

### `builder/`

Footprint-building functionality and supporting development code.

### `classifier/`

Classification and analysis-related functionality.

### `examples/`

Examples and practical usage material.

### `tests/`

Tests and real-footprint transformation examples.

### `docs/`

Architecture documentation, milestones, technical notes, and development
findings.

### `main.py`

Project-level entry point used by the current development workflow.

---

# Development Principles

The project follows several principles.

### 1. Understand the real data first

Real Altium PcbLib files guide the design of the semantic model.

### 2. Work at the semantic level

The user should work with concepts such as Pads, Tracks, Arcs, and Pad
Masters rather than binary records.

### 3. Do not reinvent low-level PcbLib mechanics

`altium_monkey` provides the underlying file-format implementation.

### 4. Verify with real Altium software

A generated file is not considered successful merely because it was written
without an exception.

It must be accepted and usable by Altium Designer.

### 5. Implement only what is currently needed

Unsupported primitives remain future work until a practical use case
requires them.

---

# Current Status

The current project status is:

```text
Product 1
PcbLib -> JSON
        WORKING

Product 2
JSON -> Pads -> PcbLib
        WORKING

Product 3
JSON -> Pads + Tracks + Arcs -> PcbLib
        WORKING
```

The current architecture therefore provides a complete working round-trip
for the supported footprint primitives:

```text
                PcbLib
                   |
                   v
              Extraction
                   |
                   v
             Semantic JSON
                   |
                   v
          Programmatic changes
                   |
                   v
          Pads + Tracks + Arcs
                   |
                   v
             New PcbLib
                   |
                   v
          Altium Designer 15.1
```

The next development phase is focused on usability: simple commands,
installation, documentation, examples, and making the three products easy
to use on another computer.
