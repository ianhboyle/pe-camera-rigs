import bpy
from bpy.types import Panel
from ...constants import VR180_RIG_NAME

class VR180_PT_Workflow(Panel):
    """VR180 Professional 4-Step Workflow Panel"""
    bl_label = "VR180 Professional Workflow"
    bl_idname = "VR180_PT_workflow"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'PE Cams'
    bl_order = 3
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        settings = context.scene.pe_vr180_settings

        # Quick Start Guide
        box = layout.box()
        box.label(text="Quick Start Guide", icon='INFO')
        col = box.column(align=True)
        col.label(text="1. Click 'Create Scene'")
        col.label(text="2. Add your assets to the scene")
        col.label(text="3. Click 'Render EXR Sequences'")
        col.label(text="4. Click 'Setup Compositor'")
        col.label(text="5. Click 'Render YouTube Video'")
        
        layout.separator()

        box = layout.box()
        box.label(text="Global Settings", icon='PREFERENCES')
        col = box.column(align=True)
        col.prop(settings, "resolution_preset")
        col.prop(settings, "render_quality")
        col.prop(settings, "output_path")

        layout.separator()

        # STEP 1: Create Scene
        box = layout.box()
        box.label(text="STEP 1: Create Scene", icon='SCENE_DATA')

        col = box.column(align=True)
        op = col.operator("vr180.create_scene", icon='ADD')
        
        # Pass properties from the panel to the operator
        op.lighting_preset = settings.lighting_preset
        op.include_cyclorama = settings.include_cyclorama
        op.cyclorama_size = settings.cyclorama_size
        op.cyclorama_color = settings.cyclorama_color
        op.include_reference = settings.include_reference


        # Show status if scene created
        if VR180_RIG_NAME in bpy.data.objects:
            col.separator()
            col.label(text="Scene Created!", icon='CHECKMARK')
            col.label(text="Next: Add content, then Step 2", icon='FORWARD')
            col.label(text=f"Adjust rig in '{VR180_RIG_NAME}' Object Properties", icon='OBJECT_DATA')

        layout.separator()

        # STEP 2: Render EXR Sequences
        box = layout.box()
        box.label(text="STEP 2: Render EXR Sequences", icon='RENDER_ANIMATION')
        col = box.column(align=True)
        col.scale_y = 1.3
        col.operator("vr180.render_sequences", icon='RENDER_STILL')

        layout.separator()

        # STEP 3: Setup Compositor
        box = layout.box()
        box.label(text="STEP 3: Setup Compositor", icon='NODE_COMPOSITING')
        col = box.column(align=True)
        col.scale_y = 1.3
        col.operator("vr180.setup_compositor", icon='NODETREE')

        layout.separator()

        # STEP 4: Render YouTube Video
        box = layout.box()
        box.label(text="STEP 4: Render YouTube Video", icon='FILE_MOVIE')
        col = box.column(align=True)
        col.scale_y = 1.3
        col.operator("vr180.render_youtube", icon='RENDER_OUTPUT')