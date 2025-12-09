# PE Camera Rigs Addon (Perpetual Exploration)
# Copyright (C) 2025 Ian Boyle
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

bl_info = {
    "name": "PE Camera Rigs",
    "author": "Ian Worthington",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > PE Cams",
    "description": "Advanced camera rig creation for Isometric, Orbit, VR180, and VR360 workflows. Part of Perpetual Exploration.",
    "warning": "",
    "doc_url": "https://github.com/ianworthington/blender-camera-rigs-addon",
    "category": "Camera",
}

import bpy
from . import preferences
from . import ui
from . import rigs

# Classes that need to be registered at the top level
top_level_classes = (
    preferences.PE_AddonPreferences,
)

def register():
    """Registers all addon classes and submodules."""
    for cls in top_level_classes:
        bpy.utils.register_class(cls)
    
    # Register submodules
    ui.register()
    rigs.register()

def unregister():
    """Unregisters all addon classes and submodules."""
    # Unregister submodules in reverse order
    rigs.unregister()
    ui.unregister()

    for cls in reversed(top_level_classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
