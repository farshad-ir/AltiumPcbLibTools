from model.footprint import Footprint
from model.pad import Pad
from model.track import Track
from model.arc import Arc
from builder.master_builder import PadMasterBuilder


class Extractor:

    def extract(self, source, footprint_name):
        source_footprint = source.find_footprint(footprint_name)

        footprint = Footprint(source_footprint.name)
        footprint.parameters = dict(source_footprint.parameters)

        for primitive in source_footprint.primitives:

            primitive_type = type(primitive).__name__

            if primitive_type == "AltiumPcbPad":
                footprint.pads.append(
                    self.extract_pad(primitive)
                )

            elif primitive_type == "AltiumPcbTrack":
                footprint.tracks.append(
                    self.extract_track(primitive)
                )

            elif primitive_type == "AltiumPcbArc":
                footprint.arcs.append(
                    self.extract_arc(primitive)
                )




        footprint.pad_masters = PadMasterBuilder().build(
            footprint.pads
        )


        return footprint

    def extract_pad(self, source_pad):
        pad = Pad()

        pad.designator = source_pad.designator

        pad.position = {
            "x": source_pad.x,
            "y": source_pad.y,
        }

        pad.shape = self.shape_name(
            source_pad.semantic_top_shape
        )

        pad.size = {
            "width": source_pad.top_width,
            "height": source_pad.top_height,
        }

        pad.layer = self.layer_display_name(
            source_pad
        )

        pad.rotation = source_pad.rotation

        pad.options = {
            "pad_mode": source_pad.pad_mode,
            "is_plated": source_pad.is_plated,
            "hole_size": source_pad.hole_size,
            "hole_shape": source_pad.hole_shape,

            "top_shape": self.shape_name(
                source_pad.semantic_top_shape
            ),

            "mid_shape": self.shape_name(
                source_pad.mid_shape
            ),

            "bot_shape": self.shape_name(
                source_pad.bot_shape
            ),

            "top_width": source_pad.top_width,
            "top_height": source_pad.top_height,

            "mid_width": source_pad.mid_width,
            "mid_height": source_pad.mid_height,

            "bot_width": source_pad.bot_width,
            "bot_height": source_pad.bot_height,

            "soldermask_expansion_mode":
                source_pad.soldermask_expansion_mode,

            "soldermask_expansion_manual":
                source_pad.soldermask_expansion_manual,

            "pastemask_expansion_mode":
                source_pad.pastemask_expansion_mode,

            "pastemask_expansion_manual":
                source_pad.pastemask_expansion_manual,

            "legacy_layer_id":
                source_pad.layer,

            "v7_layer_id":
                getattr(source_pad, "v7_layer_id", None),

            "layer_family":
                self.layer_family(source_pad),

            "layer_number":
                self.layer_number(source_pad),
        }

        return pad

    def extract_track(self, source_track):
        track = Track()

        track.layer = self.layer_display_name(
            source_track
        )

        track.start = {
            "x": source_track.start_x,
            "y": source_track.start_y,
        }

        track.end = {
            "x": source_track.end_x,
            "y": source_track.end_y,
        }

        track.width = source_track.width

        track.options = {
            "solder_mask_expansion":
                source_track.solder_mask_expansion,

            "paste_mask_expansion":
                source_track.paste_mask_expansion,

            "v7_layer_id":
                source_track.v7_layer_id,

            "keepout_restrictions":
                source_track.keepout_restrictions,

            "polygon_index":
                source_track.polygon_index,

            "subpoly_index":
                source_track.subpoly_index,

            "union_index":
                source_track.union_index,

            "user_routed":
                source_track.user_routed,

            "is_locked":
                source_track.is_locked,

            "is_keepout":
                source_track.is_keepout,

            "is_polygon_outline":
                source_track.is_polygon_outline,

            "component_index":
                source_track.component_index,

            "net_index":
                source_track.net_index,

            "legacy_layer_id":
                source_track.layer,

            "layer_family":
                self.layer_family(source_track),

            "layer_number":
                self.layer_number(source_track),
        }

        return track

    def extract_arc(self, source_arc):
        arc = Arc()

        arc.layer = self.layer_display_name(
            source_arc
        )

        arc.geometry = {
            "center_x": source_arc.center_x,
            "center_y": source_arc.center_y,
            "radius": source_arc.radius,
            "start_angle": source_arc.start_angle,
            "end_angle": source_arc.end_angle,
        }

        arc.options = {
            "width": source_arc.width,

            "solder_mask_expansion":
                source_arc.solder_mask_expansion,

            "paste_mask_expansion":
                source_arc.paste_mask_expansion,

            "v7_layer_id":
                source_arc.v7_layer_id,

            "keepout_restrictions":
                source_arc.keepout_restrictions,

            "polygon_index":
                source_arc.polygon_index,

            "subpoly_index":
                source_arc.subpoly_index,

            "union_index":
                source_arc.union_index,

            "user_routed":
                source_arc.user_routed,

            "is_locked":
                source_arc.is_locked,

            "is_keepout":
                source_arc.is_keepout,

            "is_polygon_outline":
                source_arc.is_polygon_outline,

            "component_index":
                source_arc.component_index,

            "net_index":
                source_arc.net_index,

            "legacy_layer_id":
                source_arc.layer,

            "layer_family":
                self.layer_family(source_arc),

            "layer_number":
                self.layer_number(source_arc),
        }

        return arc

    def layer_display_name(self, primitive):
        layer_ref = primitive.layer_ref()

        return layer_ref.legacy_layer.to_display_name()

    def layer_family(self, primitive):
        layer_ref = primitive.layer_ref()

        return layer_ref.family.value

    def layer_number(self, primitive):
        layer_ref = primitive.layer_ref()

        return layer_ref.number

    def shape_name(self, shape):
        mapping = {
            1: "circle",
            2: "rectangle",
            3: "octagonal",
            4: "rounded_rectangle",
            10: "custom",
        }

        return mapping.get(
            shape,
            f"unknown_{shape}"
        )
