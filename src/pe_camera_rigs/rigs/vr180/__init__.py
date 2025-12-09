import bpy

from . import rig
from .operators import (
    VR180_OT_CreateScene,
    VR180_OT_RenderSequences,
    VR180_OT_SetupCompositor,
    VR180_OT_RenderYouTube,
)
from .panels import VR180_PT_Workflow
from .properties import PE_VR180SceneSettings, PE_VR180RigSettings

classes = (
    VR180_OT_CreateScene,
    VR180_OT_RenderSequences,
    VR180_OT_SetupCompositor,
    VR180_OT_RenderYouTube,
    VR180_PT_Workflow,
    PE_VR180SceneSettings,
    PE_VR180RigSettings,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.pe_vr180_settings = bpy.props.PointerProperty(type=PE_VR180SceneSettings)
    bpy.types.Object.pe_vr180_rig_settings = bpy.props.PointerProperty(type=PE_VR180RigSettings)


def unregister():
    del bpy.types.Scene.pe_vr180_settings
    del bpy.types.Object.pe_vr180_rig_settings
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
