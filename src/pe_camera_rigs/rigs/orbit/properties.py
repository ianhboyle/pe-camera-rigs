import bpy

# Define presets with initial values (should match ORBIT_PRESETS in operators.py)
ORBIT_PRESET_ITEMS = [
    ('PRODUCT', "Product Photography", "A standard product shot setup"),
    ('DETAIL', "Detail Close-Up", "For small objects like jewelry"),
    ('CHARACTER', "Character Showcase", "For character turnarounds"),
    ('HERO', "Hero Shot", "Dramatic reveals, low angle"),
    ('ARCHITECTURAL', "Architectural Walkaround", "For buildings and large structures"),
    ('ENVIRONMENT', "Environment Tour", "For large scenes and environments"),
]

class PE_OrbitCameraAddProps(bpy.types.PropertyGroup):
    """Temporary properties used by the UI panel when adding a new rig."""
    preset: bpy.props.EnumProperty(
        name="Preset",
        items=ORBIT_PRESET_ITEMS,
        default='PRODUCT',
        description="Select the initial preset for the new orbit camera rig"
    )
