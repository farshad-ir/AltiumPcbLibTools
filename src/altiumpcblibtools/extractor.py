import json
import sys
import types
from pathlib import Path
from typing import Any


def _load_altium_pcb_lib():
    """
    Load altium_monkey's PcbLib module without importing its package
    __init__, because the full package currently requires optional
    dependencies that are not needed for PcbLib extraction.
    """
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
    from altium_monkey.altium_record_types import PcbLayer

    return AltiumPcbLib, PcbLayer


def _public_attributes(obj: object) -> dict[str, Any]:
    """
    Extract public simple attributes from a primitive.

    Nested objects, callables and private/internal fields are skipped.
    """
    result: dict[str, Any] = {}

    for name in dir(obj):

        if name.startswith("_"):
            continue

        try:
            value = getattr(obj, name)
        except Exception:
            continue

        if isinstance(
            value,
            (str, int, float, bool)
        ) or value is None:

            result[name] = value

        elif isinstance(value, (list, tuple)):

            simple = True

            for item in value:

                if not isinstance(
                    item,
                    (
                        str,
                        int,
                        float,
                        bool,
                        type(None),
                    ),
                ):
                    simple = False
                    break

            if simple:
                result[name] = list(value)

    return result


def primitive_to_dict(
    primitive: object,
    PcbLayer,
) -> dict[str, Any]:
    """
    Convert one Altium Monkey primitive into JSON-compatible data.
    """
    data = _public_attributes(primitive)

    data["type"] = type(primitive).__name__

    if "layer" in data:

        layer_id = data["layer"]

        try:
            layer = PcbLayer(int(layer_id))

            data["layer_info"] = {
                "name": layer.name,
                "display_name": layer.to_display_name(),
                "json_name": layer.to_json_name(),
            }

        except (ValueError, TypeError):
            data["layer_info"] = {
                "name": None,
                "display_name": f"Unknown ({layer_id})",
                "json_name": f"UNKNOWN_{layer_id}",
            }

    return data


def extract_footprint(
    pcb_path: str | Path,
    footprint_name: str,
) -> dict[str, Any]:

    pcb_path = Path(pcb_path)

    if not pcb_path.is_file():
        raise FileNotFoundError(
            f"PcbLib file not found: {pcb_path}"
        )

    AltiumPcbLib, PcbLayer = _load_altium_pcb_lib()

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

    primitives = footprint.primitives

    result: dict[str, Any] = {
        "format": "AltiumPcbLibTools",
        "format_version": 1,

        "source": {
            "library": str(
                pcb_path.resolve()
            ),
            "footprint": footprint.name,
        },

        "summary": {
            "total_primitives": len(primitives),
            "pads": len(footprint.pads),
            "tracks": len(footprint.tracks),
            "arcs": len(footprint.arcs),
            "fills": len(footprint.fills),
            "vias": len(footprint.vias),
            "regions": len(footprint.regions),
            "component_bodies": len(
                footprint.component_bodies
            ),
        },

        "primitives": [
            primitive_to_dict(
                primitive,
                PcbLayer,
            )
            for primitive in primitives
        ],
    }

    return result


def save_json(
    data: dict[str, Any],
    output_path: str | Path,
) -> Path:

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with output_path.open(
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )

        f.write("\n")

    return output_path

