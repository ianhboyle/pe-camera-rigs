import bpy

class PE_AddonPreferences(bpy.types.AddonPreferences):
    """Defines the preferences for the PE Camera Rigs addon."""
    bl_idname = __package__

    default_output_path: bpy.props.StringProperty(
        name="Default Render Output Path",
        description="Default directory for all render outputs from this addon. Can be overridden in each camera's settings",
        subtype='DIR_PATH',
        default="//pe_renders/"
    )

    spatial_media_tool_path: bpy.props.StringProperty(
        name="Spatial Media Tool Path",
        description="Path to the 'spatialmedia' executable for VR metadata injection. Leave blank to use the bundled version",
        subtype='FILE_PATH'
    )

    def draw(self, context):
        """Draws the addon preferences UI."""
        layout = self.layout
        
        box = layout.box()
        box.label(text="Default Paths")
        box.prop(self, "default_output_path")
        box.prop(self, "spatial_media_tool_path")

        # Add the help button
        box = layout.box()
        box.label(text="Help & Documentation")
        op = box.operator("wm.open_documentation", icon='URL')
        op.bl_label = "Open Online Documentation"
