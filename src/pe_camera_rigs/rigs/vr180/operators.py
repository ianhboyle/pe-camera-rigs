import bpy
import math
import os
import logging
from pathlib import Path
from bpy.types import Operator
from bpy.props import EnumProperty, FloatProperty, BoolProperty

logger = logging.getLogger(__name__)

from .rig import create_vr180_rig
from ...utils.scene_setup import (
    create_lighting_preset,
    create_cyclorama,
    add_reference_sphere,
)
from ...constants import (
    VR180_RIG_NAME,
    VR180_LEFT_CAM_NAME,
    VR180_RIGHT_CAM_NAME,
    VR180_COMPOSITOR_SCENE_NAME,
    REFERENCE_CAPSULE_NAME,
)

class VR180_OT_CreateScene(Operator):
    """Create VR180 Scene - Sets up a VR180 rig and scene elements"""
    bl_idname = "vr180.create_scene"
    bl_label = "1. Create VR180 Scene"
    bl_description = "Creates a complete VR180 scene with a camera rig, lighting, and other elements"
    bl_options = {'REGISTER', 'UNDO'}

    # Operator properties to receive settings from the UI panel
    lighting_preset: EnumProperty(
        name="Lighting",
        items=[
            ('NONE', "None", "No lights added"),
            ('3POINT_STUDIO', "3-Point (Studio)", "Professional 3-point studio lighting"),
        ],
        default='3POINT_STUDIO',
    )
    include_cyclorama: BoolProperty(name="Cyclorama Stage", default=True)
    cyclorama_size: EnumProperty(name="Size", items=[('SMALL', 'Small (10m)', ''), ('MEDIUM', "20m × 20m", ""), ('LARGE', 'Large (30m)', '')], default='MEDIUM')
    cyclorama_color: EnumProperty(name="Color", items=[('WHITE', "White", ""), ('GRAY', "Neutral Gray", ""), ('BLACK', "Black", "")], default='GRAY')
    include_reference: BoolProperty(name="Person-Scale Reference", default=True)

    def execute(self, context):
        settings = context.scene.pe_vr180_settings

        # 1. Create the parented VR180 camera rig
        rig, left_cam, right_cam = create_vr180_rig(context)
        
        # 2. Assign rig-specific settings from the UI to the rig's custom properties
        if hasattr(rig, "pe_vr180_rig_settings"):
            rig.pe_vr180_rig_settings.ipd = settings.ipd 
        else:
            self.report({'WARNING'}, "pe_vr180_rig_settings not found on rig. IPD not set.")

        # 3. Create lighting, cyclorama, and reference objects
        if self.lighting_preset != 'NONE':
            create_lighting_preset(context, preset=self.lighting_preset)
        if self.include_cyclorama:
            create_cyclorama(context, size=self.cyclorama_size, color=self.cyclorama_color)
        if self.include_reference:
            # For VR180, a capsule is better than a sphere for human scale
            bpy.ops.mesh.primitive_capsule_add(radius=0.25, depth=1.3, location=(0,0,0.9))
            context.active_object.name = REFERENCE_CAPSULE_NAME
            
        # 4. Auto-configure scene settings
        context.scene.render.engine = 'CYCLES'
        if settings.resolution_preset == 'YOUTUBE_5_7K':
            context.scene.render.resolution_x = 5760
            context.scene.render.resolution_y = 2880
        
        # 5. Set active camera and select the main rig controller
        context.scene.camera = left_cam # Default to left eye for viewport
        bpy.ops.object.select_all(action='DESELECT')
        rig.select_set(True)
        context.view_layer.objects.active = rig

        self.report({'INFO'}, "VR180 Scene created! Adjust rig IPD in the 'Object Properties' tab.")
        return {'FINISHED'}

class VR180_OT_RenderSequences(Operator):
    """Render EXR Sequences - Crash-safe left/right eye sequences"""
    bl_idname = "vr180.render_sequences"
    bl_label = "2. Render EXR Sequences"
    bl_description = "Renders left and right eye sequences to crash-safe OpenEXR files"
    bl_options = {'REGISTER'}

    def _validate_preconditions(self, context):
        """Validate all prerequisites before starting render."""
        settings = context.scene.pe_vr180_settings

        # Check frame range is valid
        if context.scene.frame_end <= context.scene.frame_start:
            self.report({'ERROR'}, "Invalid frame range: End frame must be greater than start frame")
            return False

        # Check VR180 rig exists
        if VR180_RIG_NAME not in bpy.data.objects:
            self.report({'ERROR'}, f"{VR180_RIG_NAME} not found. Please run Step 1 (Create VR180 Scene) first.")
            return False

        # Verify cameras exist
        if VR180_LEFT_CAM_NAME not in bpy.data.objects:
            self.report({'ERROR'}, "Left camera not found. Please run Step 1 first.")
            return False

        if VR180_RIGHT_CAM_NAME not in bpy.data.objects:
            self.report({'ERROR'}, "Right camera not found. Please run Step 1 first.")
            return False

        # Validate output path is writable
        try:
            output_base_path = bpy.path.abspath(settings.output_path)
            output_path = Path(output_base_path)

            # Check parent directory exists
            if not output_path.parent.exists():
                self.report({'ERROR'}, f"Output directory does not exist: {output_path.parent}")
                return False

            # Check directory is writable
            if not os.access(output_path.parent, os.W_OK):
                self.report({'ERROR'}, f"Output directory not writable: {output_path.parent}")
                return False

        except (OSError, PermissionError) as e:
            self.report({'ERROR'}, f"Cannot access output path: {str(e)}")
            return False

        return True

    def execute(self, context):
        settings = context.scene.pe_vr180_settings

        # Validate preconditions before starting render
        if not self._validate_preconditions(context):
            return {'CANCELLED'}

        # Store original render settings
        render = context.scene.render
        original_settings = {
            'engine': render.engine,
            'filepath': render.filepath,
            'resolution_x': render.resolution_x,
            'resolution_y': render.resolution_y,
            'resolution_percentage': render.resolution_percentage,
            'camera': context.scene.camera,
            'image_settings': {
                'file_format': render.image_settings.file_format,
                'color_mode': render.image_settings.color_mode,
                'color_depth': render.image_settings.color_depth,
                'exr_codec': render.image_settings.exr_codec,
            }
        }

        try:
            # 1. Detect the VR180 rig and its cameras
            rig = bpy.data.objects.get(VR180_RIG_NAME)
            if not rig:
                self.report({'ERROR'}, f"No {VR180_RIG_NAME} found! Please run Step 1 first.")
                return {'CANCELLED'}

            left_cam_obj = bpy.data.objects.get(VR180_LEFT_CAM_NAME)
            right_cam_obj = bpy.data.objects.get(VR180_RIGHT_CAM_NAME)

            if not left_cam_obj or not right_cam_obj or left_cam_obj.parent != rig or right_cam_obj.parent != rig:
                self.report({'ERROR'}, "Could not find left/right cameras. Please run Step 1 first.")
                return {'CANCELLED'}

            # 2. Create output folders
            output_base_path = bpy.path.abspath(settings.output_path)
            left_folder = Path(output_base_path) / "vr180" / "left"
            right_folder = Path(output_base_path) / "vr180" / "right"
            left_folder.mkdir(parents=True, exist_ok=True)
            right_folder.mkdir(parents=True, exist_ok=True)

            # 3. Configure render settings for OpenEXR
            context.scene.render.engine = 'CYCLES'
            context.scene.render.image_settings.file_format = 'OPEN_EXR'
            context.scene.render.image_settings.color_depth = '32'
            context.scene.render.image_settings.exr_codec = 'DWAA'
            
            # Per-eye resolution
            context.scene.render.resolution_x = int(settings.resolution_x / 2)
            context.scene.render.resolution_y = settings.resolution_y

            # 4. Render Left Eye Sequence
            context.scene.camera = left_cam_obj
            context.scene.render.filepath = str(left_folder / "left_")
            bpy.ops.render.render(animation=True)
            self.report({'INFO'}, f"Rendered Left Eye sequence to {left_folder}")

            # 5. Render Right Eye Sequence
            context.scene.camera = right_cam_obj
            context.scene.render.filepath = str(right_folder / "right_")
            bpy.ops.render.render(animation=True)
            self.report({'INFO'}, f"Rendered Right Eye sequence to {right_folder}")

        except (IOError, OSError, PermissionError) as e:
            self.report({'ERROR'}, f"File system error: {str(e)}")
            return {'CANCELLED'}
        except RuntimeError as e:
            self.report({'ERROR'}, f"Render error: {str(e)}")
            return {'CANCELLED'}
        except Exception as e:
            # Catch unexpected errors but log them
            logger.exception("Unexpected error during render")
            self.report({'ERROR'}, f"Unexpected error during render: {str(e)}")
            return {'CANCELLED'}
        finally:
            # 6. Restore original render settings
            render = context.scene.render
            render.engine = original_settings['engine']
            render.filepath = original_settings['filepath']
            render.resolution_x = original_settings['resolution_x']
            render.resolution_y = original_settings['resolution_y']
            render.resolution_percentage = original_settings['resolution_percentage']
            render.image_settings.file_format = original_settings['image_settings']['file_format']
            render.image_settings.color_mode = original_settings['image_settings']['color_mode']
            render.image_settings.color_depth = original_settings['image_settings']['color_depth']
            render.image_settings.exr_codec = original_settings['image_settings']['exr_codec']
            context.scene.camera = original_settings['camera']
        
        self.report({'INFO'}, "VR180 Sequences Rendered!")
        return {'FINISHED'}


class VR180_OT_SetupCompositor(Operator):
    """Setup Compositor - Auto-loads sequences and creates nodes"""
    bl_idname = "vr180.setup_compositor"
    bl_label = "3. Setup Compositor"
    bl_description = "Creates compositor scene with all nodes linked correctly"
    bl_options = {'REGISTER', 'UNDO'}

    def _validate_preconditions(self, context):
        """Validate that rendered sequences exist before setting up compositor."""
        settings = context.scene.pe_vr180_settings

        # Check that sequences were rendered
        try:
            output_base_path = bpy.path.abspath(settings.output_path)
            left_folder = Path(output_base_path) / "vr180" / "left"
            right_folder = Path(output_base_path) / "vr180" / "right"

            # Check folders exist
            if not left_folder.exists():
                self.report({'ERROR'}, f"Left eye sequence folder not found: {left_folder}. Run Step 2 (Render Sequences) first.")
                return False

            if not right_folder.exists():
                self.report({'ERROR'}, f"Right eye sequence folder not found: {right_folder}. Run Step 2 first.")
                return False

            # Check for rendered files
            left_files = list(left_folder.glob("left_*.exr"))
            right_files = list(right_folder.glob("right_*.exr"))

            if not left_files:
                self.report({'ERROR'}, "No left eye EXR files found. Run Step 2 (Render Sequences) first.")
                return False

            if not right_files:
                self.report({'ERROR'}, "No right eye EXR files found. Run Step 2 first.")
                return False

            # Verify file counts match frame range
            expected_frames = context.scene.frame_end - context.scene.frame_start + 1
            if len(left_files) < expected_frames or len(right_files) < expected_frames:
                self.report({'WARNING'}, f"Incomplete sequences detected. Expected {expected_frames} frames, found {len(left_files)} left and {len(right_files)} right.")

        except (OSError, PermissionError) as e:
            self.report({'ERROR'}, f"Cannot access sequence folders: {str(e)}")
            return False

        return True

    def execute(self, context):
        settings = context.scene.pe_vr180_settings

        # Validate preconditions
        if not self._validate_preconditions(context):
            return {'CANCELLED'}

        # Store original state
        original_scene = context.window.scene
        original_active = context.view_layer.objects.active
        original_selected = list(context.selected_objects)

        try:
            # Create or get compositor scene
            if VR180_COMPOSITOR_SCENE_NAME in bpy.data.scenes:
                comp_scene = bpy.data.scenes[VR180_COMPOSITOR_SCENE_NAME]
            else:
                comp_scene = bpy.data.scenes.new(VR180_COMPOSITOR_SCENE_NAME)

            # Switch to compositor scene for setup
            context.window.scene = comp_scene

            # Enable compositor
            comp_scene.use_nodes = True
            comp_scene.render.use_compositing = True

            # Clear existing nodes
            comp_scene.node_tree.nodes.clear()

            # Auto-detect sequence paths
            output_base_path = bpy.path.abspath(settings.output_path)
            left_path = str(Path(output_base_path) / "vr180" / "left" / "left_")
            right_path = str(Path(output_base_path) / "vr180" / "right" / "right_")

            # Create nodes
            nodes = comp_scene.node_tree.nodes
            links = comp_scene.node_tree.links

            # Left eye chain
            left_img = nodes.new('CompositorNodeImage')
            left_img.location = (-800, 200)
            left_img.label = "Left Eye"
            left_img.file_format = 'OPEN_EXR'
            left_img.filepath = left_path
            
            # Need to find the frame count from the rendered sequences
            # For now, use a placeholder frame_end
            left_img.frame_duration = bpy.context.scene.frame_end - bpy.context.scene.frame_start + 1

            left_denoise = nodes.new('CompositorNodeDenoise')
            left_denoise.location = (-500, 200)
            # Denoise settings will come from render_quality setting

            left_translate = nodes.new('CompositorNodeTranslate')
            left_translate.location = (-200, 200)
            left_translate.inputs['X'].default_value = 0
            left_translate.inputs['Y'].default_value = 0

            # Right eye chain
            right_img = nodes.new('CompositorNodeImage')
            right_img.location = (-800, -200)
            right_img.label = "Right Eye"
            right_img.file_format = 'OPEN_EXR'
            right_img.filepath = right_path
            right_img.frame_duration = bpy.context.scene.frame_end - bpy.context.scene.frame_start + 1


            right_denoise = nodes.new('CompositorNodeDenoise')
            right_denoise.location = (-500, -200)

            right_translate = nodes.new('CompositorNodeTranslate')
            right_translate.location = (-200, -200)
            right_translate.inputs['X'].default_value = settings.resolution_x / 2 # Offset to right half
            right_translate.inputs['Y'].default_value = 0

            # Combine node
            alpha_over = nodes.new('CompositorNodeAlphaOver')
            alpha_over.location = (100, 0)

            # Output nodes
            composite = nodes.new('CompositorNodeComposite')
            composite.location = (400, 100)

            viewer = nodes.new('CompositorNodeViewer')
            viewer.location = (400, -100)

            # Link nodes
            links.new(left_img.outputs['Image'], left_denoise.inputs['Image'])
            links.new(left_denoise.outputs['Image'], left_translate.inputs['Image'])
            links.new(left_translate.outputs['Image'], alpha_over.inputs[1])

            links.new(right_img.outputs['Image'], right_denoise.inputs['Image'])
            links.new(right_denoise.outputs['Image'], right_translate.inputs['Image'])
            links.new(right_translate.outputs['Image'], alpha_over.inputs[2])

            links.new(alpha_over.outputs['Image'], composite.inputs['Image'])
            links.new(alpha_over.outputs['Image'], viewer.inputs['Image'])

            # Configure scene settings for compositor output
            comp_scene.render.resolution_x = settings.resolution_x
            comp_scene.render.resolution_y = settings.resolution_y
            comp_scene.frame_start = context.scene.frame_start
            comp_scene.frame_end = context.scene.frame_end

            # Switch to Compositing workspace
            # This requires finding the workspace by name, which might not always exist or be named consistently.
            # For robust production, it's safer to ensure a workspace exists or provide an option.
            # For spec, assume it exists.
            if "Compositing" in bpy.data.workspaces:
                context.window.workspace = bpy.data.workspaces["Compositing"]

            self.report({'INFO'}, "Compositor Ready! Make manual tweaks, then click Step 4")
            return {'FINISHED'}

        except (IOError, OSError) as e:
            self.report({'ERROR'}, f"File system error accessing sequences: {str(e)}")
            return {'CANCELLED'}
        except (KeyError, AttributeError) as e:
            self.report({'ERROR'}, f"Scene data error: {str(e)}")
            return {'CANCELLED'}
        except RuntimeError as e:
            self.report({'ERROR'}, f"Blender compositor error: {str(e)}")
            return {'CANCELLED'}
        except Exception as e:
            # Catch unexpected errors but log them
            logger.exception("Unexpected error setting up compositor")
            self.report({'ERROR'}, f"Unexpected error setting up compositor: {str(e)}")
            return {'CANCELLED'}
        finally:
            # Restore original scene context
            context.window.scene = original_scene

            # Restore original selection and active object
            if original_active and original_active.name in bpy.data.objects:
                context.view_layer.objects.active = original_active

            bpy.ops.object.select_all(action='DESELECT')
            for obj in original_selected:
                if obj and obj.name in bpy.data.objects:
                    obj.select_set(True)


class VR180_OT_RenderYouTube(Operator):
    """Render YouTube Video - Renders the final SBS video from compositor"""
    bl_idname = "vr180.render_youtube"
    bl_label = "4. Render YouTube Video"
    bl_description = "Renders the final Side-by-Side (SBS) video from the compositor scene, ready for YouTube"
    bl_options = {'REGISTER'}

    def _validate_preconditions(self, context):
        """Validate that compositor scene exists with valid node setup."""
        # Check compositor scene exists
        comp_scene = bpy.data.scenes.get(VR180_COMPOSITOR_SCENE_NAME)
        if not comp_scene:
            self.report({'ERROR'}, f"Compositor scene '{VR180_COMPOSITOR_SCENE_NAME}' not found. Please run Step 3 (Setup Compositor) first.")
            return False

        # Verify compositor is enabled and has nodes
        if not comp_scene.use_nodes:
            self.report({'ERROR'}, "Compositor not enabled in VR180_Compositor scene. Run Step 3 again.")
            return False

        if not comp_scene.node_tree or not comp_scene.node_tree.nodes:
            self.report({'ERROR'}, "Compositor has no nodes. Run Step 3 (Setup Compositor) first.")
            return False

        # Check for essential compositor nodes
        has_composite = False
        for node in comp_scene.node_tree.nodes:
            if node.type == 'COMPOSITE':
                has_composite = True
                break

        if not has_composite:
            self.report({'ERROR'}, "Compositor missing Composite output node. Run Step 3 again.")
            return False

        return True

    def execute(self, context):
        settings = context.scene.pe_vr180_settings
        original_scene = context.window.scene

        # Validate preconditions
        if not self._validate_preconditions(context):
            return {'CANCELLED'}

        try:
            # 1. Find the compositor scene
            comp_scene = bpy.data.scenes.get(VR180_COMPOSITOR_SCENE_NAME)

            # 2. Set active scene to compositor
            context.window.scene = comp_scene

            # 3. Configure render settings for YouTube video
            output_base_path = bpy.path.abspath(settings.output_path)
            final_output_path = Path(output_base_path) / "vr180" / "youtube_vr180"
            final_output_path.mkdir(parents=True, exist_ok=True)
            
            comp_scene.render.filepath = str(final_output_path / "vr180_sbs_")
            
            comp_scene.render.image_settings.file_format = 'FFMPEG'
            
            # Container
            comp_scene.render.ffmpeg.format = 'MPEG4'

            # Codec
            comp_scene.render.ffmpeg.codec = 'H264' # Using H264 for broader compatibility, though H265 is also good
            
            # Quality / Bitrate
            comp_scene.render.ffmpeg.constant_rate_factor = 'PERC_LOSSLESS' # Visually lossless
            
            # Encoding speed
            comp_scene.render.ffmpeg.ffmpeg_preset = 'SLOW' # Slower encoding for better quality/compression
            
            # Audio (optional, for now no audio)
            comp_scene.render.ffmpeg.audio_codec = 'NONE'

            # 4. Trigger the render
            bpy.ops.render.render(animation=True)

            self.report({'INFO'}, f"Final video rendered to: {comp_scene.render.filepath}")
            return {'FINISHED'}

        except (IOError, OSError, PermissionError) as e:
            self.report({'ERROR'}, f"File system error: {str(e)}")
            return {'CANCELLED'}
        except RuntimeError as e:
            self.report({'ERROR'}, f"Render error: {str(e)}")
            return {'CANCELLED'}
        except (KeyError, AttributeError) as e:
            self.report({'ERROR'}, f"Scene/node data error: {str(e)}")
            return {'CANCELLED'}
        except Exception as e:
            # Catch unexpected errors but log them
            logger.exception("Unexpected error rendering video")
            self.report({'ERROR'}, f"Unexpected error rendering video: {str(e)}")
            return {'CANCELLED'}
        finally:
            # 5. Restore original scene
            context.window.scene = original_scene