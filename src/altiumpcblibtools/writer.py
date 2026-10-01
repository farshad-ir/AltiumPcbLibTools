import json
import sys
import types
from pathlib import Path
from typing import Any


IGNORED_FIELDS = {
    "type",
    "layer_info",
    "record_type",
}


def _load_altium_pcb_lib():
    monkey_path = (
        Path(__file__).resolve().parents[2]
        / "altium_monkey"
        / "src"
        / "py"
    )

    if not monkey_path.exists():
        raise RuntimeError(
            f"altium_monkey source not found: {monkey_path}"
        )

    package = types.ModuleType("altium_monkey")
    package.__path__ = [
        str(monkey_path / "altium_monkey")
    ]
    sys.modules["altium_monkey"] = package

    from altium_monkey.altium_pcblib import AltiumPcbLib

    return AltiumPcbLib


def load_json(path: str | Path) -> dict[str, Any]:
    path = Path(path)

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object")

    return data


def _editable_fields(data: dict[str, Any]) -> list[str]:
    fields = []

    for name, value in data.items():

        if name in IGNORED_FIELDS:
            continue

        if name.endswith("_mils"):
            continue

        if name.startswith("_"):
            continue

        if isinstance(
            value,
            (str, int, float, bool),
        ) or value is None:

            fields.append(name)

    return fields


def apply_json(
    pcb_path: str | Path,
    footprint_name: str,
    json_path: str | Path,
    output_path: str | Path,
) -> Path:

    pcb_path = Path(pcb_path)
    output_path = Path(output_path)

    if not pcb_path.is_file():
        raise FileNotFoundError(
            f"PcbLib file not found: {pcb_path}"
        )

    data = load_json(json_path)

    source = data.get("source", {})
    json_footprint = source.get("footprint")

    if json_footprint and json_footprint != footprint_name:
        raise ValueError(
            f"JSON footprint is {json_footprint!r}, "
            f"but requested footprint is {footprint_name!r}"
        )

    json_primitives = data.get("primitives")

    if not isinstance(json_primitives, list):
        raise ValueError(
            "JSON must contain a 'primitives' list"
        )

    AltiumPcbLib = _load_altium_pcb_lib()

    lib = AltiumPcbLib.from_file(
        str(pcb_path)
    )

    footprint = lib.find_footprint(
        footprint_name
    )

    if footprint is None:
        raise ValueError(
            f"Footprint not found: {footprint_name}"
        )

    primitives = tuple(
        footprint.primitives
    )

    if len(json_primitives) != len(primitives):
        raise ValueError(
            f"Primitive count mismatch: "
            f"JSON has {len(json_primitives)}, "
            f"template has {len(primitives)}"
        )

    changes = []

    for index, json_primitive in enumerate(
        json_primitives
    ):

        if not isinstance(json_primitive, dict):
            raise ValueError(
                f"Primitive {index}: "
                f"expected an object"
            )

        primitive = primitives[index]

        json_type = json_primitive.get("type")
        actual_type = type(primitive).__name__

        if (
            json_type
            and json_type != actual_type
        ):
            raise ValueError(
                f"Primitive {index}: "
                f"JSON type {json_type!r} "
                f"does not match template type "
                f"{actual_type!r}"
            )

        for field in _editable_fields(
            json_primitive
        ):

            new_value = json_primitive[field]

            try:
                old_value = getattr(
                    primitive,
                    field,
                )

            except AttributeError:
                raise ValueError(
                    f"Primitive {index} "
                    f"({actual_type}): "
                    f"unknown field {field!r}"
                ) from None

            if old_value == new_value:
                continue

            try:
                setattr(
                    primitive,
                    field,
                    new_value,
                )

            except Exception as exc:
                raise ValueError(
                    f"Primitive {index} "
                    f"({actual_type}): "
                    f"cannot set {field!r} "
                    f"from {old_value!r} "
                    f"to {new_value!r}: {exc}"
                ) from exc

            changes.append(
                (
                    index,
                    field,
                    old_value,
                    new_value,
                )
            )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    lib.save(output_path)

    print(
        f"Applied {len(changes)} "
        f"semantic change(s)."
    )

    for (
        index,
        field,
        old_value,
        new_value,
    ) in changes:

        print(
            f"  [{index:03d}] "
            f"{field}: "
            f"{old_value!r} -> "
            f"{new_value!r}"
        )

    print(
        f"Saved: {output_path}"
    )

    return output_path
