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

        # Header with icon
        row = layout.row()
        row.label(text="Professional Camera Rigs", icon='CAMERA_DATA')

        # Quick info box
        box = layout.box()
        box.label(text="Available Rigs", icon='ADD')
        col = box.column(align=True)
        col.scale_y = 0.8
        col.label(text="Orbit & Isometric: One-click setup")
        col.label(text="VR Workflows: Multi-step production")

        layout.separator()

        # This panel serves as the parent for all camera rig sub-panels
