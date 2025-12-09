import bpy

class PE_PT_main_panel(bpy.types.Panel):
    """Creates the main parent panel in the 3D Viewport Sidebar"""
    bl_label = "PE Camera Rigs"
    bl_idname = "PE_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'PE Cams'

    def draw(self, context):
        layout = self.layout
        layout.label(text="Select a rig to add:")
        # This panel will serve as the parent for all camera rig sub-panels.
