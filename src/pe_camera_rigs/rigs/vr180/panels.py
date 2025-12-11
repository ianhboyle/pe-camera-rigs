import bpy
from bpy.types import Panel
from pathlib import Path
from ...constants import VR180_RIG_NAME, VR180_COMPOSITOR_SCENE_NAME

class VR180_PT_Workflow(Panel):
    """VR180 Professional 4-Step Workflow Panel"""
    bl_label = "VR180 Professional Workflow"
    bl_idname = "VR180_PT_workflow"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = 'PE_PT_main_panel'
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

        # Check if Step 1 is complete
        step1_complete = VR180_RIG_NAME in bpy.data.objects
        if not step1_complete:
            col.enabled = False
            col.label(text="Complete Step 1 first", icon='INFO')

        col.operator("vr180.render_sequences", icon='RENDER_STILL')

        # Show status if sequences rendered
        if step1_complete:
            try:
                output_base_path = bpy.path.abspath(settings.output_path)
                left_folder = Path(output_base_path) / "vr180" / "left"
                right_folder = Path(output_base_path) / "vr180" / "right"
                if left_folder.exists() and right_folder.exists():
                    col.separator()
                    col.label(text="Sequences Rendered!", icon='CHECKMARK')
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
            left_folder = Path(output_base_path) / "vr180" / "left"
            right_folder = Path(output_base_path) / "vr180" / "right"
            step2_complete = left_folder.exists() and right_folder.exists()
        except:
            pass

        if not step2_complete:
            col.enabled = False
            col.label(text="Complete Step 2 first", icon='INFO')

        col.operator("vr180.setup_compositor", icon='NODETREE')

        # Show status if compositor setup
        if VR180_COMPOSITOR_SCENE_NAME in bpy.data.scenes:
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
        step3_complete = VR180_COMPOSITOR_SCENE_NAME in bpy.data.scenes
        if not step3_complete:
            col.enabled = False
            col.label(text="Complete Step 3 first", icon='INFO')

        col.operator("vr180.render_youtube", icon='RENDER_OUTPUT')

        # Show status if final video rendered
        if step3_complete:
            try:
                output_base_path = bpy.path.abspath(settings.output_path)
                final_output_path = Path(output_base_path) / "vr180" / "youtube_vr180"
                if final_output_path.exists():
                    col.separator()
                    col.label(text="Video Complete!", icon='CHECKMARK')
            except:
                pass