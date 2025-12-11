import bpy

class ISOMETRIC_PT_add_panel(bpy.types.Panel):
    """Creates a sub-panel in the main addon panel for adding the Isometric rig."""
    bl_label = "Isometric Camera"
    bl_idname = "ISOMETRIC_PT_add_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = 'PE_PT_main_panel' # Parent to the main addon panel
    bl_order = 0

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.label(text="Add Controller:")

        # Use an EnumProperty to show presets in a dropdown menu
        col.prop(context.scene.pe_iso_cam_add_props, "initial_preset", text="")

        col.separator()
        col.scale_y = 1.3
        # The operator button will use the value from the dropdown
        op = col.operator("cgt.add_isometric_controller", text="Add Isometric Rig", icon='CAMERA_DATA')
        op.initial_preset = context.scene.pe_iso_cam_add_props.initial_preset


class ISOMETRIC_PT_controller_settings(bpy.types.Panel):
    """Draws the UI in the Object Properties panel for the controller."""
    bl_label = "Isometric Camera Controller"
    bl_idname = "ISOMETRIC_PT_controller_settings"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        # Only show this panel if the active object has our custom property group.
        obj = context.object
        return (obj is not None and hasattr(obj, "pe_iso_cam"))

    def draw(self, context):
        layout = self.layout
        # Get the property group from the active object
        iso_cam_settings = context.object.pe_iso_cam

        box = layout.box()
        box.label(text="Projection Settings", icon='CAMERA_DATA')
        box.prop(iso_cam_settings, "projection_type", text="Type")
        box.prop(iso_cam_settings, "ortho_scale")

        # Only show custom angle controls if the type is set to 'CUSTOM'
        if iso_cam_settings.projection_type == 'CUSTOM':
            box = layout.box()
            box.label(text="Custom Angles", icon='DRIVER_ROTATIONAL')
            col = box.column(align=True)
            col.prop(iso_cam_settings, "custom_rotation_z")
            col.prop(iso_cam_settings, "custom_tilt_x")
            col.prop(iso_cam_settings, "custom_roll_y")
