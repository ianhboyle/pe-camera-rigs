import bpy

from . import properties
from .operators import (
    VR360_OT_CreateScene,
    VR360_OT_RenderSequence,
    VR360_OT_SetupCompositor,
    VR360_OT_RenderYouTube,
)
from .panels import VR360_PT_Workflow

classes = (
    VR360_OT_CreateScene,
    VR360_OT_RenderSequence,
    VR360_OT_SetupCompositor,
    VR360_OT_RenderYouTube,
    VR360_PT_Workflow,
)

def register():
    properties.register()
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    properties.unregister()
