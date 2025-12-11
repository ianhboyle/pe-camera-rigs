import bpy
from .properties import ORBIT_PRESET_ITEMS
from ...constants import ORBIT_CONTROLLER_NAME

class ORBIT_PT_add_panel(bpy.types.Panel):
    """Creates a sub-panel in the main addon panel for adding the Orbit rig."""
    bl_label = "Orbit Camera"
    bl_idname = "ORBIT_PT_add_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = 'PE_PT_main_panel' # Parent to the main addon panel
    bl_order = 1 # Order after Isometric

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.label(text="Add Controller:")

        # Use a temporary property group on the scene to hold the selected preset
        col.prop(context.scene.pe_orbit_cam_add_props, "preset", text="")

        col.separator()
        col.scale_y = 1.3
        # The operator button will use the value from the dropdown
        op = col.operator("cgt.add_orbit_controller", text="Add Orbit Rig", icon='CAMERA_DATA')
        op.preset = context.scene.pe_orbit_cam_add_props.preset
