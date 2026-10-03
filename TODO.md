# Master TODO — AltiumPcbLibTools

## Project Goal

Build a practical, reusable toolset for working with Altium Designer
`.PcbLib` footprints through a semantic JSON representation.

The project uses real Altium PcbLib files as the source of truth.

The JSON representation is **semantic**, not a byte-for-byte representation of
the original PcbLib binary data.

Low-level PcbLib mechanics are provided by the separate `altium_monkey`
project. AltiumPcbLibTools focuses on extraction, semantic representation,
transformation, and practical workflow.

---

# Product 1 — Extract PcbLib to JSON

## Working

* [x] Accept PcbLib library path
* [x] Accept footprint name
* [x] Locate requested footprint
* [x] Read real PcbLib using `altium_monkey`
* [x] Preserve native primitive order
* [x] Extract primitive data
* [x] Export semantic JSON
* [x] Save JSON to a selected file
* [x] Report extraction summary
* [x] Test with real `Test_Copy.PcbLib`
* [x] Test `CAP_BOSHKE_SMD`
* [x] Confirm 33 primitives
* [x] Confirm 2 Pads
* [x] Confirm 28 Tracks
* [x] Confirm 2 Arcs
* [x] Confirm 1 ComponentBody
* [x] Resolve legacy layer IDs through `PcbLayer`
* [x] Preserve raw layer information
* [x] Add layer information to semantic JSON

## Future improvements

* [ ] Automated extraction tests
* [ ] Formal JSON Schema
* [ ] Formal documentation of every extracted field
* [ ] Better handling/reporting of unsupported primitive types

---

# Product 2 — JSON to PcbLib: Pads Only

## Working

* [x] Load semantic JSON
* [x] Create PcbLib container
* [x] Create footprint
* [x] Create pad masters
* [x] Create pads
* [x] Preserve pad position
* [x] Preserve pad dimensions
* [x] Preserve pad shape
* [x] Preserve pad rotation
* [x] Preserve pad hole information
* [x] Preserve plated/unplated state
* [x] Preserve top pad properties
* [x] Reuse pad masters
* [x] Generate valid PcbLib
* [x] Verify generated PcbLib in Altium Designer 15.1
* [x] Demonstrate pad duplication
* [x] Demonstrate pad rotation

## Future improvements

* [ ] Improve handling of additional pad options
* [ ] Add more SMD and through-hole test cases
* [ ] Improve validation and error messages

---

# Product 3 — JSON to PcbLib: Full Supported Footprint

Current supported primitives:

* Pads
* Tracks
* Arcs

## Working

* [x] Load semantic JSON
* [x] Create PcbLib container
* [x] Create footprint
* [x] Create pads
* [x] Create tracks
* [x] Create arcs
* [x] Preserve Track start/end points
* [x] Preserve Track width
* [x] Preserve Track layer
* [x] Preserve Arc center
* [x] Preserve Arc radius
* [x] Preserve Arc start/end angles
* [x] Preserve Arc width
* [x] Preserve Arc layer
* [x] Generate valid PcbLib
* [x] Test real footprint `29-04`
* [x] Open generated PcbLib in Altium Designer 15.1
* [x] Verify Pads + Tracks + Arcs are accepted by Altium

## Future primitive support

* [ ] ComponentBody
* [ ] Text
* [ ] Region
* [ ] Fill
* [ ] Via
* [ ] Other graphical primitives
* [ ] 3D model data

These are future extensions, not prerequisites for the current Products 2
and 3.

---

# Semantic JSON

* [x] Establish semantic footprint model
* [x] Define current JSON representation
* [x] Represent footprint parameters
* [x] Represent pad masters
* [x] Represent pads
* [x] Represent tracks
* [x] Represent arcs
* [ ] Formalize JSON Schema
* [ ] Define schema versioning strategy
* [ ] Define required vs optional fields
* [ ] Define unknown-field policy
* [ ] Add JSON validation

---

# Practical CLI / Usability

Goal: make the project useful on another computer without needing to know
the internal Python classes.

* [ ] Define a simple user-facing CLI
* [ ] Add one-command PcbLib → JSON extraction
* [ ] Add one-command JSON → Pads PcbLib transformation
* [ ] Add one-command JSON → Full PcbLib transformation
* [ ] Add clear command help
* [ ] Add friendly file/path errors
* [ ] Add friendly footprint errors
* [ ] Add friendly JSON errors
* [ ] Add useful operation summaries
* [ ] Document the quick-start workflow

---

# Installation / Portability

Goal: clone/download the project on another machine and start using it easily.

* [ ] Document supported Python version
* [ ] Document virtual-environment setup
* [ ] Document dependencies
* [ ] Document `altium_monkey` setup
* [ ] Document Linux setup
* [ ] Document Windows setup where practical
* [ ] Provide a simple installation/setup procedure
* [ ] Test setup on a clean machine

---

# Documentation

* [x] README
* [x] Architecture documentation
* [x] Explain semantic JSON concept
* [x] Document pad duplication/rotation milestone
* [ ] Add Quick Start
* [ ] Document Product 1
* [ ] Document Product 2
* [ ] Document Product 3
* [ ] Document current JSON format
* [ ] Document dependencies
* [ ] Document `altium_monkey` attribution/licensing
* [ ] Add practical examples
* [ ] Add troubleshooting guide
* [ ] Add development guide

---

# Testing

## Completed

* [x] Real PcbLib extraction
* [x] Real footprint extraction
* [x] Pad round trip
* [x] Pad duplication and rotation
* [x] Track transformation
* [x] Arc transformation
* [x] Full Pads + Tracks + Arcs transformation
* [x] Verify generated full footprint in Altium Designer 15.1

## Future

* [ ] Automated test runner
* [ ] More real-footprint tests
* [ ] SMD footprint tests
* [ ] Through-hole footprint tests
* [ ] Mixed-layer tests
* [ ] Invalid JSON tests
* [ ] Missing footprint tests
* [ ] Unsupported primitive tests
* [ ] Automated read → JSON → PcbLib verification

---

# Repository / Engineering

* [x] Initialize Git repository
* [x] Establish project architecture
* [x] Add extractor
* [x] Add semantic model
* [x] Add JSON export
* [x] Add Pad transformation
* [x] Add Full transformation
* [x] Add tests for Products 2 and 3
* [x] Keep third-party `altium_monkey` source separate
* [ ] Document third-party dependencies
* [ ] Document `altium_monkey` licensing
* [ ] Add project configuration
* [ ] Add formatting/linting if useful
* [ ] Add type checking if useful
* [ ] Add CI
* [ ] Define release/version strategy

---

# Future Primitive Research

Do not investigate these until they are actually needed for a real use case.

* [ ] ComponentBody
* [ ] 3D models
* [ ] Text
* [ ] Regions
* [ ] Fills
* [ ] Vias
* [ ] Dimensions
* [ ] Other unsupported primitives
* [ ] Extended layer handling
* [ ] Advanced V7 layer handling

---

# Suggested Continue

- Add README quick start examples.
- Compare original and generated pad names.
- Determine meaning of lost pad suffixes
  such as:
  s250h120zc250 -> s250h120


---

# Current Status

**Product 1 — PcbLib → JSON: WORKING**

**Product 2 — JSON → Pads → PcbLib: WORKING**

**Product 3 — JSON → Pads + Tracks + Arcs → PcbLib: WORKING**

Latest real-world full transformation:

```text
Test_Copy.PcbLib
        ↓
footprint: 29-04 implementation of Q2n2222
        ↓
F2904.json
        ↓
FullRoundTripWriter
        ↓
FULL_2904.PcbLib
        ↓
verified in Altium Designer 15.1
