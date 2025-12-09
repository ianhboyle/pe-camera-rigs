# ui/__init__.py

import bpy
from bpy.utils import register_class, unregister_class

from . import main_panel

classes = (
    main_panel.PE_PT_main_panel,
)

def register():
    for cls in classes:
        register_class(cls)

def unregister():
    for cls in reversed(classes):
        unregister_class(cls)