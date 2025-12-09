import bpy
import math

PROJECTION_TYPES = [
    ('GAME_2_1', "Game (2:1 Ratio)", "26.565° tilt for 2:1 pixel art"),
    ('GAME_4_3', "Game (4:3 Ratio)", "30° tilt for 4:3 pixel art"),
    ('TRUE_ISOMETRIC', "True Isometric", "35.264° tilt, mathematically correct"),
    ('DIMETRIC', "Dimetric (30°)", "30° tilt, a common artistic variation"),
    ('MILITARY', "Military (Top-Down)", "90° tilt for a top-down view"),
    ('CAVALIER', "Cavalier", "0° tilt, 45° roll for a front-facing view with depth"),
    ('CUSTOM', "Custom", "Use custom rotation and tilt values from the modifier"),
]

# Map projection type identifiers to integer indices (used by geometry nodes)
PROJECTION_TYPE_TO_INDEX = {
    'GAME_2_1': 0,
    'GAME_4_3': 1,
    'TRUE_ISOMETRIC': 2,
    'DIMETRIC': 3,
    'MILITARY': 4,
    'CAVALIER': 5,
    'CUSTOM': 6,
}


# === Update Callbacks ===

def update_projection_type(self, context):
    """Update modifier when projection type changes"""
    # Only update if this is a controller object (Empty with modifier)
    if self.id_data.type != 'EMPTY':
        return

    modifier = self.id_data.modifiers.get('Isometric Camera')
    if modifier and modifier.node_group:
        # Convert projection type string to index
        projection_index = PROJECTION_TYPE_TO_INDEX.get(self.projection_type, 2)
        modifier["Socket_1"] = projection_index

        # Force viewport update
        context.view_layer.update()


def update_ortho_scale(self, context):
    """Update modifier when ortho scale changes"""
    if self.id_data.type != 'EMPTY':
        return

    modifier = self.id_data.modifiers.get('Isometric Camera')
    if modifier and modifier.node_group:
        modifier["Socket_2"] = self.ortho_scale
        context.view_layer.update()


def update_custom_rotation_z(self, context):
    """Update modifier when custom rotation Z changes"""
    if self.id_data.type != 'EMPTY':
        return

    modifier = self.id_data.modifiers.get('Isometric Camera')
    if modifier and modifier.node_group:
        # Convert degrees to radians for modifier
        modifier["Socket_3"] = math.radians(self.custom_rotation_z)
        context.view_layer.update()


def update_custom_tilt_x(self, context):
    """Update modifier when custom tilt X changes"""
    if self.id_data.type != 'EMPTY':
        return

    modifier = self.id_data.modifiers.get('Isometric Camera')
    if modifier and modifier.node_group:
        # Convert degrees to radians for modifier
        modifier["Socket_4"] = math.radians(self.custom_tilt_x)
        context.view_layer.update()


def update_custom_roll_y(self, context):
    """Update modifier when custom roll Y changes"""
    if self.id_data.type != 'EMPTY':
        return

    modifier = self.id_data.modifiers.get('Isometric Camera')
    if modifier and modifier.node_group:
        # Convert degrees to radians for modifier
        modifier["Socket_5"] = math.radians(self.custom_roll_y)
        context.view_layer.update()


# === Property Groups ===

class PE_IsometricCameraAddProps(bpy.types.PropertyGroup):
    """Properties for the Isometric camera add panel."""
    initial_preset: bpy.props.EnumProperty(
        name="Initial Preset",
        items=PROJECTION_TYPES,
        default='TRUE_ISOMETRIC',
        description="Choose a projection type preset for the isometric camera"
    )


class PE_IsometricCameraSettings(bpy.types.PropertyGroup):
    """Settings for an Isometric camera controller object."""

    projection_type: bpy.props.EnumProperty(
        name="Projection Type",
        items=PROJECTION_TYPES,
        default='TRUE_ISOMETRIC',
        description="Isometric projection type",
        update=update_projection_type
    )

    ortho_scale: bpy.props.FloatProperty(
        name="Orthographic Scale",
        description="Camera orthographic scale (zoom level)",
        default=10.0,
        min=0.1,
        max=1000.0,
        subtype='DISTANCE',
        update=update_ortho_scale
    )

    custom_rotation_z: bpy.props.FloatProperty(
        name="Rotation (Z)",
        description="Custom Z-axis rotation in degrees",
        default=45.0,
        min=-180.0,
        max=180.0,
        subtype='ANGLE',
        unit='ROTATION',
        update=update_custom_rotation_z
    )

    custom_tilt_x: bpy.props.FloatProperty(
        name="Tilt (X)",
        description="Custom X-axis tilt in degrees",
        default=35.264,
        min=-90.0,
        max=90.0,
        subtype='ANGLE',
        unit='ROTATION',
        update=update_custom_tilt_x
    )

    custom_roll_y: bpy.props.FloatProperty(
        name="Roll (Y)",
        description="Custom Y-axis roll in degrees",
        default=0.0,
        min=-180.0,
        max=180.0,
        subtype='ANGLE',
        unit='ROTATION',
        update=update_custom_roll_y
    )


def register():
    bpy.utils.register_class(PE_IsometricCameraAddProps)
    bpy.utils.register_class(PE_IsometricCameraSettings)

    # Scene property for add panel
    bpy.types.Scene.pe_iso_cam_add_props = bpy.props.PointerProperty(
        type=PE_IsometricCameraAddProps
    )

    # Object property for controller settings
    bpy.types.Object.pe_iso_cam = bpy.props.PointerProperty(
        type=PE_IsometricCameraSettings
    )


def unregister():
    # Remove properties first
    del bpy.types.Object.pe_iso_cam
    del bpy.types.Scene.pe_iso_cam_add_props

    # Unregister classes
    bpy.utils.unregister_class(PE_IsometricCameraSettings)
    bpy.utils.unregister_class(PE_IsometricCameraAddProps)
