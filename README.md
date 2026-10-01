# AltiumPcbLibTools

Tools for reading, analyzing, validating, editing, and creating Altium Designer PcbLib footprints.

## Project Purpose

This project is intended to study and work with real Altium Designer `.PcbLib` files programmatically.

The main objective is to read an existing footprint from an Altium PcbLib library and convert its meaningful structure into a human-readable JSON representation.

The JSON representation is intended to describe the **semantic structure of a footprint**, rather than being a raw dump of the binary PcbLib data.

The resulting JSON can then be used as a reference or intermediate representation for understanding, validating, modifying, and eventually producing other Altium footprints.

The project is therefore focused on questions such as:

* What primitives make up a real Altium footprint?
* What properties does each primitive contain?
* How are pads, tracks, arcs, component bodies, layers, and other objects represented?
* Which fields are required for a valid footprint?
* How can a footprint be represented in a clear and portable JSON structure?
* How can that JSON representation be validated?
* How can a validated representation eventually be converted back into a usable PcbLib footprint?

## Initial Real-World Test

Development began by examining a real footprint from a local Altium Designer library.

The initial test used a footprint for a **surface-mount cylindrical electrolytic capacitor**. The footprint was taken from a locally available PcbLib library and was used as a real-world reference for understanding the internal structure of Altium footprints.

The footprint contained:

* 2 Pads
* 28 Tracks
* 2 Arcs
* 1 ComponentBody

This real footprint is being used as a reference case for understanding how different primitive types and their properties are represented inside an Altium PcbLib.

The goal is not to reproduce this particular footprint, but to use real library data to discover and document the general structure needed to work with other footprints.

## Project Direction

The project is being developed in stages.

### 1. Read

Read existing Altium PcbLib files and identify their footprints and primitives.

### 2. Extract

Extract the meaningful properties of a footprint into a structured JSON representation.

### 3. Validate

Validate the JSON structure and detect missing, invalid, or inconsistent properties.

### 4. Modify

Allow footprint properties and geometry to be modified through the structured representation.

### 5. Create

Use the validated representation to create or reconstruct usable Altium PcbLib footprints.

### 6. Verify

Open the resulting PcbLib files in Altium Designer and compare the result with the intended footprint structure.

## Use of altium_monkey

This project would not have reached its current stage without the work provided by **altium_monkey**.

We would like to thank the author and contributors of `altium_monkey` for providing a Python toolkit capable of reading, writing, analyzing, and working with Altium file formats, including PcbLib files.

Repository:

https://github.com/wavenumber-eng/altium_monkey

`altium_monkey` is licensed under the **GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later)**.

This project uses `altium_monkey` as a third-party dependency/tool where applicable. The `altium_monkey` source code and its license remain the property and responsibility of their respective authors and are not claimed as original code of this project.

## Ownership and Licensing

The code written specifically for **AltiumPcbLibTools** is separate from third-party software used by the project.

Unless explicitly stated otherwise, original source code, documentation, and other original materials created for this repository belong to the author of AltiumPcbLibTools.

Third-party components remain subject to their own licenses.

In particular:

* `altium_monkey` is a separate third-party project.
* Its source code is not claimed as original AltiumPcbLibTools code.
* Its AGPL-3.0-or-later license applies to the `altium_monkey` project and any use of it that is subject to that license.
* Third-party notices and license information will be documented separately as the project develops.

Nothing in this repository should be interpreted as claiming ownership of Altium Designer, the Altium file formats, or third-party libraries used to process those formats.

## Relationship to Altium Designer

AltiumPcbLibTools is an independent project for programmatic analysis and manipulation of Altium Designer library files.

It is not affiliated with or endorsed by Altium.

Testing of generated or modified PcbLib files may be performed using Altium Designer 15.1.

## Current Status

The project is in an early research and development stage.

The current focus is understanding the structure of real PcbLib footprints and establishing a reliable semantic representation before building higher-level generation and editing tools.

Future functionality will be added incrementally as the underlying file structures become better understood.

## Repository

GitHub:

https://github.com/farshad-ir/AltiumPcbLibTools
