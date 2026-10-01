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
    package.__path__ = [str(monkey_path / "altium_monkey")]
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


def _public_fields(data: dict[str, Any]) -> dict[str, Any]:
    result = {}

    for name, value in data.items():
        if name in IGNORED_FIELDS:
            continue

        if name.endswith("_mils"):
            continue

        if name.startswith("_"):
            continue

        if isinstance(value, (str, int, float, bool)) or value is None:
            result[name] = value

    return result


def _primitive_type(data: dict[str, Any]) -> str:
    value = data.get("type")

    if not isinstance(value, str):
        raise ValueError("Primitive JSON object has no valid 'type'")

    return value


def _mils(data: dict[str, Any], name: str) -> float | None:
    value = data.get(name)

    if value is None:
        return None

    return float(value)


def _required(
    data: dict[str, Any],
    name: str,
    primitive_type: str,
) -> Any:
    if name not in data or data[name] is None:
        raise HumanAssistanceRequired(
            primitive_type,
            name,
            (
                f"Required semantic field {name!r} is missing. "
                f"It cannot be safely inferred."
            ),
        )

    return data[name]


class HumanAssistanceRequired(ValueError):
    def __init__(
        self,
        primitive_type: str,
        field: str,
        message: str,
    ):
        self.primitive_type = primitive_type
        self.field = field
        super().__init__(message)


class ChangeTracker:
    def __init__(self):
        self.items: list[str] = []

    def automatic(
        self,
        primitive_type: str,
        field: str,
        value: Any,
        reason: str,
    ):
        self.items.append(
            "\n".join(
                [
                    "[HUMAN-ASSISTED]",
                    f"Primitive : {primitive_type}",
                    f"Field     : {field}",
                    f"Value     : {value!r}",
                    f"Source    : automatic/default",
                    f"Reason    : {reason}",
                ]
            )
        )

    def print(self):
        if not self.items:
            return

        print()
        print("=" * 72)
        print("HUMAN-ASSISTED RESOLUTION LOG")
        print("=" * 72)

        for item in self.items:
            print(item)
            print("-" * 72)


def _layer(data: dict[str, Any]) -> Any:
    if "layer" in data:
        return data["layer"]

    layer_info = data.get("layer_info")

    if isinstance(layer_info, dict):
        if "id" in layer_info:
            return layer_info["id"]

    return None


def _create_pad(
    footprint,
    data: dict[str, Any],
    log: ChangeTracker,
):
    primitive_type = "AltiumPcbPad"

    designator = _required(
        data,
        "designator",
        primitive_type,
    )

    x = _mils(data, "x_mils")
    y = _mils(data, "y_mils")
    width = _mils(data, "width_mils")
    height = _mils(data, "height_mils")

    if x is None:
        raise HumanAssistanceRequired(
            primitive_type,
            "x_mils",
            "Pad X coordinate is missing.",
        )

    if y is None:
        raise HumanAssistanceRequired(
            primitive_type,
            "y_mils",
            "Pad Y coordinate is missing.",
        )

    if width is None:
        raise HumanAssistanceRequired(
            primitive_type,
            "width_mils",
            "Pad width is missing.",
        )

    if height is None:
        raise HumanAssistanceRequired(
            primitive_type,
            "height_mils",
            "Pad height is missing.",
        )

    layer = _layer(data)

    if layer is None:
        raise HumanAssistanceRequired(
            primitive_type,
            "layer",
            "Pad layer cannot be safely determined.",
        )

    shape = data.get("shape", 3)
    if "shape" not in data:
        log.automatic(
            primitive_type,
            "shape",
            shape,
            "Prof. Monkey add_pad() defines RECTANGLE as its default.",
        )

    rotation = data.get("rotation", data.get("rotation_degrees", 0.0))
    if "rotation" not in data and "rotation_degrees" not in data:
        log.automatic(
            primitive_type,
            "rotation_degrees",
            rotation,
            "No rotation was supplied; using add_pad() default.",
        )

    hole_size = data.get("hole_size_mils", 0.0)
    if "hole_size_mils" not in data:
        log.automatic(
            primitive_type,
            "hole_size_mils",
            hole_size,
            "No drill size was supplied; using SMT/default value 0.",
        )

    return footprint.add_pad(
        designator=str(designator),
        position_mils=(x, y),
        width_mils=width,
        height_mils=height,
        layer=layer,
        shape=shape,
        rotation_degrees=rotation,
        hole_size_mils=hole_size,
        plated=data.get("plated"),
        corner_radius_percent=data.get("corner_radius_percent"),
        top_shape=data.get("top_shape"),
        top_width_mils=data.get("top_width_mils"),
        top_height_mils=data.get("top_height_mils"),
        mid_shape=data.get("mid_shape"),
        mid_width_mils=data.get("mid_width_mils"),
        mid_height_mils=data.get("mid_height_mils"),
        bottom_shape=data.get("bottom_shape"),
        bottom_width_mils=data.get("bottom_width_mils"),
        bottom_height_mils=data.get("bottom_height_mils"),
        pad_mode=data.get("pad_mode"),
        slot_length_mils=data.get("slot_length_mils", 0.0),
        slot_rotation_degrees=data.get(
            "slot_rotation_degrees",
            0.0,
        ),
        hole_shape=data.get("hole_shape", "round"),
        solder_mask_expansion_mode=data.get(
            "solder_mask_expansion_mode"
        ),
        solder_mask_expansion_mils=data.get(
            "solder_mask_expansion_mils"
        ),
        paste_mask_expansion_mode=data.get(
            "paste_mask_expansion_mode"
        ),
        paste_mask_expansion_mils=data.get(
            "paste_mask_expansion_mils"
        ),
        hole_positive_tolerance_mils=data.get(
            "hole_positive_tolerance_mils"
        ),
        hole_negative_tolerance_mils=data.get(
            "hole_negative_tolerance_mils"
        ),
        is_test_fab_top=data.get(
            "is_test_fab_top",
            False,
        ),
        is_test_fab_bottom=data.get(
            "is_test_fab_bottom",
            False,
        ),
        is_assy_testpoint_top=data.get(
            "is_assy_testpoint_top",
            False,
        ),
        is_assy_testpoint_bottom=data.get(
            "is_assy_testpoint_bottom",
            False,
        ),
    )


def _create_track(
    footprint,
    data: dict[str, Any],
    log: ChangeTracker,
):
    primitive_type = "AltiumPcbTrack"

    sx = _required(
        data,
        "start_x_mils",
        primitive_type,
    )
    sy = _required(
        data,
        "start_y_mils",
        primitive_type,
    )
    ex = _required(
        data,
        "end_x_mils",
        primitive_type,
    )
    ey = _required(
        data,
        "end_y_mils",
        primitive_type,
    )
    width = _required(
        data,
        "width_mils",
        primitive_type,
    )

    layer = _layer(data)

    if layer is None:
        raise HumanAssistanceRequired(
            primitive_type,
            "layer",
            "Track layer cannot be safely determined.",
        )

    return footprint.add_track(
        (float(sx), float(sy)),
        (float(ex), float(ey)),
        width_mils=float(width),
        layer=layer,
        v7_layer_id=data.get("v7_layer_id"),
        solder_mask_expansion_mils=data.get(
            "solder_mask_expansion_mils"
        ),
        paste_mask_expansion_mils=data.get(
            "paste_mask_expansion_mils"
        ),
    )


def _create_arc(
    footprint,
    data: dict[str, Any],
    log: ChangeTracker,
):
    primitive_type = "AltiumPcbArc"

    cx = _required(
        data,
        "center_x_mils",
        primitive_type,
    )
    cy = _required(
        data,
        "center_y_mils",
        primitive_type,
    )
    radius = _required(
        data,
        "radius_mils",
        primitive_type,
    )
    width = _required(
        data,
        "width_mils",
        primitive_type,
    )

    layer = _layer(data)

    if layer is None:
        raise HumanAssistanceRequired(
            primitive_type,
            "layer",
            "Arc layer cannot be safely determined.",
        )

    start_angle = data.get("start_angle", 0.0)
    end_angle = data.get("end_angle", 360.0)

    if "start_angle" not in data:
        log.automatic(
            primitive_type,
            "start_angle",
            start_angle,
            "No start angle supplied; using API default.",
        )

    if "end_angle" not in data:
        log.automatic(
            primitive_type,
            "end_angle",
            end_angle,
            "No end angle supplied; using API default.",
        )

    return footprint.add_arc(
        center_mils=(float(cx), float(cy)),
        radius_mils=float(radius),
        start_angle_degrees=float(start_angle),
        end_angle_degrees=float(end_angle),
        width_mils=float(width),
        layer=layer,
        v7_layer_id=data.get("v7_layer_id"),
        solder_mask_expansion_mils=data.get(
            "solder_mask_expansion_mils"
        ),
        paste_mask_expansion_mils=data.get(
            "paste_mask_expansion_mils"
        ),
    )


def _create_primitive(
    footprint,
    data: dict[str, Any],
    log: ChangeTracker,
):
    primitive_type = _primitive_type(data)

    if primitive_type == "AltiumPcbPad":
        return _create_pad(footprint, data, log)

    if primitive_type == "AltiumPcbTrack":
        return _create_track(footprint, data, log)

    if primitive_type == "AltiumPcbArc":
        return _create_arc(footprint, data, log)

    raise HumanAssistanceRequired(
        primitive_type,
        "type",
        (
            f"Automatic creation of {primitive_type} is not yet "
            "implemented in Product 2. The JSON is valid, but this "
            "primitive requires another Prof. Monkey authoring API."
        ),
    )


def _set_existing_fields(
    primitive,
    data: dict[str, Any],
    index: int,
):
    changes = []

    for field, new_value in _public_fields(data).items():
        try:
            old_value = getattr(primitive, field)
        except AttributeError:
            continue

        if old_value == new_value:
            continue

        try:
            setattr(primitive, field, new_value)
        except Exception as exc:
            raise ValueError(
                f"Primitive {index} "
                f"({type(primitive).__name__}): "
                f"cannot set {field!r} "
                f"from {old_value!r} "
                f"to {new_value!r}: {exc}"
            ) from exc

        changes.append(
            (
                index,
                type(primitive).__name__,
                field,
                old_value,
                new_value,
            )
        )

    return changes


def _typed_list(footprint, primitive):
    mapping = {
        "AltiumPcbPad": "pads",
        "AltiumPcbTrack": "tracks",
        "AltiumPcbArc": "arcs",
        "AltiumPcbFill": "fills",
        "AltiumPcbText": "texts",
        "AltiumPcbVia": "vias",
        "AltiumPcbRegion": "regions",
        "AltiumPcbShapeBasedRegion": "regions",
        "AltiumPcbComponentBody": "component_bodies",
    }

    name = mapping.get(type(primitive).__name__)

    if name is None:
        raise ValueError(
            f"Unsupported primitive collection: "
            f"{type(primitive).__name__}"
        )

    return getattr(footprint, name)


def _remove_primitive(footprint, primitive):
    collection = _typed_list(footprint, primitive)

    if primitive in collection:
        collection.remove(primitive)

    if primitive in footprint._record_order:
        footprint._record_order.remove(primitive)


def _snapshot(footprint):
    result = []

    for index, primitive in enumerate(footprint.primitives):
        fields = {}

        for name in dir(primitive):
            if name.startswith("_"):
                continue

            try:
                value = getattr(primitive, name)
            except Exception:
                continue

            if isinstance(
                value,
                (str, int, float, bool),
            ) or value is None:
                fields[name] = value

        result.append(
            {
                "index": index,
                "type": type(primitive).__name__,
                "fields": fields,
            }
        )

    return result


def _diagnose(original, modified):
    print()
    print("=" * 72)
    print("SEMANTIC DIFFERENCE REPORT")
    print("=" * 72)

    old_by_type = {}
    new_by_type = {}

    for item in original:
        old_by_type.setdefault(item["type"], []).append(item)

    for item in modified:
        new_by_type.setdefault(item["type"], []).append(item)

    all_types = sorted(
        set(old_by_type) | set(new_by_type)
    )

    for primitive_type in all_types:
        old_items = old_by_type.get(
            primitive_type,
            [],
        )
        new_items = new_by_type.get(
            primitive_type,
            [],
        )

        common = min(
            len(old_items),
            len(new_items),
        )

        for i in range(common):
            old_fields = old_items[i]["fields"]
            new_fields = new_items[i]["fields"]

            fields = sorted(
                set(old_fields) | set(new_fields)
            )

            for field in fields:
                old = old_fields.get(field)
                new = new_fields.get(field)

                if old != new:
                    print(
                        f"[CHANGED] "
                        f"{primitive_type}[{i}] "
                        f"{field}:"
                    )
                    print(f"    OLD: {old!r}")
                    print(f"    NEW: {new!r}")

        if len(new_items) > common:
            for item in new_items[common:]:
                print(
                    f"[ADDED] "
                    f"{primitive_type} "
                    f"JSON index={item['index']}"
                )

        if len(old_items) > common:
            for item in old_items[common:]:
                print(
                    f"[REMOVED] "
                    f"{primitive_type} "
                    f"original index={item['index']}"
                )

    print("=" * 72)


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

    if (
        json_footprint
        and json_footprint != footprint_name
    ):
        raise ValueError(
            f"JSON footprint is {json_footprint!r}, "
            f"but requested footprint is "
            f"{footprint_name!r}"
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

    original_snapshot = _snapshot(footprint)

    original_primitives = list(
        footprint.primitives
    )

    # Group original primitives by type.
    pools = {}

    for primitive in original_primitives:
        pools.setdefault(
            type(primitive).__name__,
            [],
        ).append(primitive)

    used = {
        primitive_type: 0
        for primitive_type in pools
    }

    log = ChangeTracker()

    changes = []

    # JSON is the source of truth.
    for json_index, json_primitive in enumerate(
        json_primitives
    ):

        if not isinstance(json_primitive, dict):
            raise ValueError(
                f"Primitive {json_index}: "
                "expected an object"
            )

        primitive_type = _primitive_type(
            json_primitive
        )

        pool = pools.setdefault(
            primitive_type,
            [],
        )

        position = used.get(
            primitive_type,
            0,
        )

        if position < len(pool):
            primitive = pool[position]
            used[primitive_type] = position + 1

            changes.extend(
                _set_existing_fields(
                    primitive,
                    json_primitive,
                    json_index,
                )
            )

        else:
            primitive = _create_primitive(
                footprint,
                json_primitive,
                log,
            )

            changes.append(
                (
                    json_index,
                    primitive_type,
                    "<created>",
                    None,
                    "NEW PRIMITIVE",
                )
            )

    # Anything left unused is removed.
    for primitive_type, pool in pools.items():
        position = used.get(
            primitive_type,
            0,
        )

        for primitive in pool[position:]:
            _remove_primitive(
                footprint,
                primitive,
            )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    try:
        lib.save(output_path)

    except Exception as exc:
        print()
        print("=" * 72)
        print("PROF. MONKEY SAVE ERROR")
        print("=" * 72)
        print(type(exc).__name__)
        print(str(exc))
        print("=" * 72)

        modified_snapshot = _snapshot(
            footprint
        )

        _diagnose(
            original_snapshot,
            modified_snapshot,
        )

        log.print()

        raise

    # Success: only show assisted decisions.
    log.print()

    return output_path
