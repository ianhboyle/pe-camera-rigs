import bpy
from bpy.props import (
    StringProperty,
    EnumProperty,
    BoolProperty,
    PointerProperty,
)
from bpy.types import PropertyGroup

class PE_VR360MonoSceneSettings(PropertyGroup):
    resolution_preset: EnumProperty(
        name="Resolution Preset",
        items=[
            ('5K', "5K (5120x2560)", "YouTube 5K"),
            ('8K', "8K (7680x3840)", "YouTube 8K"),
        ],
        default='5K',
        description="Resolution preset for the final render"
    )

    render_quality: EnumProperty(
        name="Render Quality",
        items=[
            ('PREVIEW', "Preview (256 samples)", "Fast preview render"),
            ('PRODUCTION', "Production (512 samples)", "Balanced quality for production"),
            ('FINAL', "Final (1024 samples)", "High quality for final render"),
        ],
        default='PRODUCTION',
        description="Render quality preset"
    )

    output_path: StringProperty(
        name="Output Path",
        subtype='DIR_PATH',
        default='//output/',
        description="Directory to save rendered files"
    )

    lighting_preset: EnumProperty(
        name="Lighting",
        items=[
            ('NONE', "None", "No lights added"),
            ('3POINT_STUDIO', "3-Point (Studio)", "Professional 3-point studio lighting"),
            ('3POINT_OUTDOOR', "3-Point (Outdoor)", "Outdoor 3-point with sun"),
        ],
        default='3POINT_STUDIO',
    )
    include_cyclorama: BoolProperty(name="Cyclorama Stage", default=True)
    cyclorama_size: EnumProperty(
        name="Size",
        items=[('SMALL', "10m × 10m", ""), ('MEDIUM', "20m × 20m", ""), ('LARGE', "30m × 30m", "")],
        default='MEDIUM',
    )
    cyclorama_color: EnumProperty(
        name="Color",
        items=[('WHITE', "White", ""), ('GRAY', "Neutral Gray", ""), ('BLACK', "Black", "")],
        default='GRAY',
    )
    include_reference: BoolProperty(name="Person-Scale Reference", default=True)


classes = (
    PE_VR360MonoSceneSettings,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.pe_vr360_mono_settings = PointerProperty(type=PE_VR360MonoSceneSettings)

def unregister():
    del bpy.types.Scene.pe_vr360_mono_settings
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
