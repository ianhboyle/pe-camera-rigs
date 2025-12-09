# rigs/isometric/__init__.py

import bpy
from . import operators
from . import panels
from . import properties

classes = (
    panels.ISOMETRIC_PT_add_panel,
    panels.ISOMETRIC_PT_controller_settings,
    operators.ISOMETRIC_OT_add_controller,
)

def register():
    # Register properties first (must come before classes that use them)
    properties.register()
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    # Unregister properties last
    properties.unregister()
