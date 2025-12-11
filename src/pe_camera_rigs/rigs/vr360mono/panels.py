import bpy
from bpy.types import Panel
from pathlib import Path
from ...constants import VR360_CAM_NAME, VR360_COMPOSITOR_SCENE_NAME

class VR360_PT_Workflow(Panel):
    """VR360 Mono Professional 4-Step Workflow Panel"""
    bl_label = "VR360 Mono Professional Workflow"
    bl_idname = "VR360MONO_PT_workflow"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = 'PE_PT_main_panel'
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

        # Show status if scene created
        if VR360_CAM_NAME in bpy.data.objects:
            col.separator()
            col.label(text="Scene Created!", icon='CHECKMARK')
            col.label(text="Next: Add content, then Step 2", icon='FORWARD')

        layout.separator()

        # STEP 2: Render EXR Sequence
        box = layout.box()
        box.label(text="STEP 2: Render EXR Sequence", icon='RENDER_ANIMATION')
        col = box.column(align=True)
        col.scale_y = 1.3

        # Check if Step 1 is complete
        step1_complete = VR360_CAM_NAME in bpy.data.objects
        if not step1_complete:
            col.enabled = False
            col.label(text="Complete Step 1 first", icon='INFO')

        col.operator("vr360mono.render_sequence", icon='RENDER_STILL')

        # Show status if sequence rendered
        if step1_complete:
            try:
                output_base_path = bpy.path.abspath(settings.output_path)
                sequence_folder = Path(output_base_path) / "vr360" / "sequence"
                if sequence_folder.exists():
                    col.separator()
                    col.label(text="Sequence Rendered!", icon='CHECKMARK')
                    col.label(text="Next: Step 3", icon='FORWARD')
            except:
                pass

        layout.separator()

        # STEP 3: Setup Compositor
        box = layout.box()
        box.label(text="STEP 3: Setup Compositor", icon='NODE_COMPOSITING')
        col = box.column(align=True)
        col.scale_y = 1.3

        # Check if Step 2 is complete
        step2_complete = False
        try:
            output_base_path = bpy.path.abspath(settings.output_path)
            sequence_folder = Path(output_base_path) / "vr360" / "sequence"
            step2_complete = sequence_folder.exists()
        except:
            pass

        if not step2_complete:
            col.enabled = False
            col.label(text="Complete Step 2 first", icon='INFO')

        col.operator("vr360mono.setup_compositor", icon='NODETREE')

        # Show status if compositor setup
        if VR360_COMPOSITOR_SCENE_NAME in bpy.data.scenes:
            col.separator()
            col.label(text="Compositor Ready!", icon='CHECKMARK')
            col.label(text="Next: Step 4", icon='FORWARD')

        layout.separator()

        # STEP 4: Render YouTube Video
        box = layout.box()
        box.label(text="STEP 4: Render YouTube Video", icon='FILE_MOVIE')
        col = box.column(align=True)
        col.scale_y = 1.3

        # Check if Step 3 is complete
        step3_complete = VR360_COMPOSITOR_SCENE_NAME in bpy.data.scenes
        if not step3_complete:
            col.enabled = False
            col.label(text="Complete Step 3 first", icon='INFO')

        col.operator("vr360mono.render_youtube", icon='RENDER_OUTPUT')

        # Show status if final video rendered
        if step3_complete:
            try:
                output_base_path = bpy.path.abspath(settings.output_path)
                final_output_path = Path(output_base_path) / "vr360" / "youtube_vr360"
                if final_output_path.exists():
                    col.separator()
                    col.label(text="Video Complete!", icon='CHECKMARK')
            except:
                pass
