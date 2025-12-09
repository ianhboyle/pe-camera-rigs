import bpy
from bpy.types import Panel

class VR360_PT_Workflow(Panel):
    """VR360 Mono Professional 4-Step Workflow Panel"""
    bl_label = "VR360 Mono Professional Workflow"
    bl_idname = "VR360MONO_PT_workflow"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'PE Cams'
    bl_order = 4
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        settings = context.scene.pe_vr360_mono_settings

        # Quick Start Guide
        box = layout.box()
        box.label(text="Quick Start Guide", icon='INFO')
        col = box.column(align=True)
        col.label(text="1. Click 'Create Scene'")
        col.label(text="2. Add your assets")
        col.label(text="3. Click 'Render EXR Sequence'")
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
        col.prop(settings, "lighting_preset")
        col.prop(settings, "include_cyclorama")
        if settings.include_cyclorama:
            sub = col.column(align=True)
            sub.prop(settings, "cyclorama_size")
            sub.prop(settings, "cyclorama_color")
        col.prop(settings, "include_reference")
        
        col.separator()
        col.scale_y = 1.3
        col.operator("vr360mono.create_scene", icon='ADD')

        layout.separator()

        # STEP 2: Render EXR Sequence
        box = layout.box()
        box.label(text="STEP 2: Render EXR Sequence", icon='RENDER_ANIMATION')
        col = box.column(align=True)
        col.scale_y = 1.3
        col.operator("vr360mono.render_sequence", icon='RENDER_STILL')

        layout.separator()

        # STEP 3: Setup Compositor
        box = layout.box()
        box.label(text="STEP 3: Setup Compositor", icon='NODE_COMPOSITING')
        col = box.column(align=True)
        col.scale_y = 1.3
        col.operator("vr360mono.setup_compositor", icon='NODETREE')

        layout.separator()

        # STEP 4: Render YouTube Video
        box = layout.box()
        box.label(text="STEP 4: Render YouTube Video", icon='FILE_MOVIE')
        col = box.column(align=True)
        col.scale_y = 1.3
        col.operator("vr360mono.render_youtube", icon='RENDER_OUTPUT')
