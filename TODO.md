# Master TODO — AltiumPcbLibTools

## Project Goal

Build a reusable toolset for reading, understanding, validating, modifying, creating, and verifying Altium Designer `.PcbLib` footprints.

The project uses real Altium PcbLib files as the source of truth.

The JSON representation is **semantic**, not a byte-for-byte representation of the original PcbLib binary data.

---

# Phase 1 — Read / Extract

## Product 1 — Extract Footprint to JSON

* [x] Accept PcbLib library path from the user
* [x] Accept footprint name from the user
* [x] Locate the requested footprint
* [x] Read the real PcbLib using `altium_monkey`
* [x] Preserve native primitive order
* [x] Extract primitive data
* [x] Export JSON
* [x] Save JSON to a user-selected file
* [x] Report extraction summary
* [x] Test with real `Test_Copy.PcbLib`
* [x] Test `CAP_BOSHKE_SMD`
* [x] Confirm 33 primitives
* [x] Confirm 2 Pads
* [x] Confirm 28 Tracks
* [x] Confirm 2 Arcs
* [x] Confirm 1 ComponentBody
* [x] Resolve legacy layer IDs through `PcbLayer`
* [x] Preserve raw `layer` ID
* [x] Add `layer_info`
* [ ] Test layer resolution for every layer used by the footprint
* [ ] Define the semantic JSON schema
* [ ] Add JSON schema validation
* [ ] Add automated extraction tests

---

# Phase 2 — Understand Primitive Types

## Pads

* [ ] Fully document Pad fields
* [ ] Extract pad designator
* [ ] Extract pad position
* [ ] Extract pad dimensions
* [ ] Extract pad shape
* [ ] Extract pad rotation
* [ ] Extract hole size
* [ ] Extract plated/unplated state
* [ ] Extract top/mid/bottom pad properties
* [ ] Extract solder-mask expansion
* [ ] Extract paste-mask expansion
* [ ] Understand all Pad flags
* [ ] Test SMD pads
* [ ] Test through-hole pads

## Tracks

* [ ] Fully document Track fields
* [ ] Extract start point
* [ ] Extract end point
* [ ] Extract width
* [ ] Extract layer
* [ ] Extract routing information
* [ ] Understand net information
* [ ] Understand polygon information
* [ ] Understand V7 layer information

## Arcs

* [ ] Fully document Arc fields
* [ ] Extract center
* [ ] Extract radius
* [ ] Extract start angle
* [ ] Extract end angle
* [ ] Extract width
* [ ] Extract layer
* [ ] Understand V7 layer information

## Component Bodies

* [ ] Fully document ComponentBody fields
* [ ] Extract body layer
* [ ] Extract outline geometry
* [ ] Extract holes
* [ ] Extract body height
* [ ] Extract standoff height
* [ ] Extract 3D body information
* [ ] Understand embedded STEP data
* [ ] Determine how 3D models should be represented in semantic JSON

## Other Primitive Types

* [ ] Fills
* [ ] Vias
* [ ] Regions
* [ ] Text
* [ ] Strings
* [ ] Dimensions
* [ ] Other graphical primitives
* [ ] Identify unsupported/unknown primitive types

---

# Phase 3 — Layers

* [x] Identify `PcbLayer`
* [x] Use official Altium Monkey layer enum
* [x] Resolve legacy layer ID
* [x] Resolve display name
* [x] Resolve JSON name
* [ ] Understand `v7_layer_id`
* [ ] Map legacy layer IDs to V7 layer identities
* [ ] Understand extended mechanical layers
* [ ] Understand extended signal layers
* [ ] Handle unknown layer IDs safely
* [ ] Create reusable layer resolver
* [ ] Add layer validation

---

# Phase 4 — Semantic JSON Model

* [ ] Define JSON format
* [ ] Define format versioning strategy
* [ ] Define library metadata
* [ ] Define footprint metadata
* [ ] Define primitive schema
* [ ] Define coordinate representation
* [ ] Define unit representation
* [ ] Define layer representation
* [ ] Define pad representation
* [ ] Define track representation
* [ ] Define arc representation
* [ ] Define component-body representation
* [ ] Define 3D model representation
* [ ] Define optional fields
* [ ] Define required fields
* [ ] Define unknown-field policy
* [ ] Write JSON Schema
* [ ] Validate generated JSON against schema

---

# Phase 5 — Validation

* [ ] Validate JSON structure
* [ ] Validate required fields
* [ ] Validate primitive types
* [ ] Validate coordinates
* [ ] Validate dimensions
* [ ] Validate angles
* [ ] Validate layer IDs
* [ ] Validate layer names
* [ ] Validate pad geometry
* [ ] Validate track geometry
* [ ] Validate arc geometry
* [ ] Validate component-body geometry
* [ ] Detect invalid references
* [ ] Detect unsupported primitive types
* [ ] Produce useful validation errors

---

# Phase 6 — Modify

## Product 2 — Modify Footprint

* [ ] Load semantic JSON
* [ ] Validate JSON before modification
* [ ] Select footprint
* [ ] Modify pad properties
* [ ] Modify track properties
* [ ] Modify arc properties
* [ ] Modify component-body properties
* [ ] Add primitives
* [ ] Remove primitives
* [ ] Move primitives
* [ ] Change layers
* [ ] Change dimensions
* [ ] Preserve unsupported data where possible
* [ ] Generate modified PcbLib
* [ ] Verify generated PcbLib

---

# Phase 7 — Create

## Product 3 — Create Footprint / PcbLib

* [ ] Define footprint creation API
* [ ] Create empty footprint
* [ ] Create pads
* [ ] Create tracks
* [ ] Create arcs
* [ ] Create component body
* [ ] Assign layers
* [ ] Define footprint metadata
* [ ] Create PcbLib container
* [ ] Write valid PcbLib binary
* [ ] Open generated PcbLib in Altium Designer
* [ ] Verify visual result
* [ ] Compare generated structure against expected JSON

---

# Phase 8 — Verification

* [ ] Open generated PcbLib in Altium Designer 15.1
* [ ] Verify footprint appears in library
* [ ] Verify footprint name
* [ ] Verify pad geometry
* [ ] Verify track geometry
* [ ] Verify arc geometry
* [ ] Verify layers
* [ ] Verify component body
* [ ] Verify 3D model where applicable
* [ ] Re-extract generated PcbLib
* [ ] Compare extracted JSON with source JSON
* [ ] Define acceptable differences
* [ ] Build automated round-trip tests

---

# Phase 9 — Testing

* [ ] Unit tests for layer resolver
* [ ] Unit tests for primitive serialization
* [ ] Unit tests for JSON schema
* [ ] Test real PcbLib extraction
* [ ] Test multiple footprints
* [ ] Test SMD footprints
* [ ] Test through-hole footprints
* [ ] Test mixed-layer footprints
* [ ] Test footprints containing 3D bodies
* [ ] Test unknown/unsupported primitives
* [ ] Test malformed PcbLib files
* [ ] Test missing footprint
* [ ] Test invalid JSON
* [ ] Test modify → save → read
* [ ] Test create → save → read
* [ ] Test read → JSON → create → read

---

# Phase 10 — Documentation

* [x] README
* [x] Architecture documentation
* [x] Explain semantic JSON concept
* [ ] Document installation
* [ ] Document dependencies
* [ ] Document Product 1 CLI
* [ ] Document JSON format
* [ ] Document primitive types
* [ ] Document layers
* [ ] Document validation
* [ ] Document modification
* [ ] Document creation
* [ ] Document verification
* [ ] Add examples
* [ ] Add troubleshooting guide
* [ ] Add development guide

---

# Phase 11 — Repository / Engineering

* [x] Initialize Git repository
* [x] Create project architecture
* [x] Add initial extractor
* [x] Add extraction test
* [ ] Add `TODO.md`
* [ ] Add automated test runner
* [ ] Add project configuration
* [ ] Add linting
* [ ] Add formatting
* [ ] Add type checking
* [ ] Add CI
* [ ] Define release/version strategy
* [ ] Document third-party dependencies
* [ ] Document `altium_monkey` licensing
* [ ] Keep third-party source separate from project code

---

# Current Status

**Product 1 — PcbLib → JSON: WORKING**

Current real-world test:

```text
Library:
Test_Copy.PcbLib

Footprint:
CAP_BOSHKE_SMD

Primitives:
33

Pads:
2

Tracks:
28

Arcs:
2

Component Bodies:
1
```

Layer resolution is working through the official `PcbLayer` enum:

```text
69
→ MECHANICAL_13
→ Mechanical 13
→ MECHANICAL13
```

---

# Immediate Next Tasks

1. [ ] Verify all layers used by `CAP_BOSHKE_SMD`
2. [ ] Understand `v7_layer_id`
3. [ ] Define the semantic JSON schema
4. [ ] Improve primitive-specific serialization
5. [ ] Add automated tests
6. [ ] Commit and push the completed Product 1 changes
