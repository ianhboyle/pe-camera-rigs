# rigs/orbit/__init__.py

import bpy
from . import operators
from . import panels
from . import properties

classes = (
    properties.PE_OrbitCameraAddProps,
    panels.ORBIT_PT_add_panel,
    operators.ORBIT_OT_add_controller,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # Add the property group to Blender's Scene type
    bpy.types.Scene.pe_orbit_cam_add_props = bpy.props.PointerProperty(type=properties.PE_OrbitCameraAddProps)


def unregister():
    # Delete the custom property from Blender's Scene type
    del bpy.types.Scene.pe_orbit_cam_add_props

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
