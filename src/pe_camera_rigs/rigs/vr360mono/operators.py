import bpy
import math
import os
import logging
from pathlib import Path
from bpy.types import Operator
from bpy.props import EnumProperty, BoolProperty

logger = logging.getLogger(__name__)

from .rig import create_vr360_camera
from ...utils.scene_setup import (
    create_lighting_preset,
    create_cyclorama,
    add_reference_sphere
)
from ...utils.blender import detect_and_enable_gpu
from .properties import PE_VR360MonoSceneSettings
from ...constants import VR360_CAM_NAME, VR360_COMPOSITOR_SCENE_NAME

class VR360_OT_CreateScene(Operator):
    """Create VR360 Scene - Sets up a 360 Mono rig and scene elements"""
    bl_idname = "vr360mono.create_scene"
    bl_label = "1. Create VR360 Scene"
    bl_description = "Creates a complete VR360 Mono scene with a camera, lighting, cyclorama, and reference objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = context.scene.pe_vr360_mono_settings

        try:
            # 1. Create the VR360 camera
            camera = create_vr360_camera(context, height=1.6)

            # 2. Set resolution based on preset
            if settings.resolution_preset == '5K':
                context.scene.render.resolution_x = 5120
                context.scene.render.resolution_y = 2560
            elif settings.resolution_preset == '8K':
                context.scene.render.resolution_x = 7680
                context.scene.render.resolution_y = 3840
            
            context.scene.render.image_settings.file_format = 'PNG' # Default for stills

            # 3. Create lighting
            if settings.lighting_preset != 'NONE':
                create_lighting_preset(context=context, preset=settings.lighting_preset)

            # 4. Create Cyclorama and Reference
            if settings.include_cyclorama:
                create_cyclorama(context, settings.cyclorama_size, settings.cyclorama_color)
            if settings.include_reference:
                add_reference_sphere(context)

            # 5. Auto-configure scene
            context.scene.render.engine = 'CYCLES'

            # Try to enable GPU rendering for better performance
            gpu_name = detect_and_enable_gpu()
            if gpu_name:
                self.report({'INFO'}, f"GPU rendering enabled: {gpu_name}")
            else:
                self.report({'INFO'}, "Using CPU rendering (no GPU detected)")

            # Set camera as active
            context.scene.camera = camera
            bpy.ops.object.select_all(action='DESELECT')
            camera.select_set(True)
            context.view_layer.objects.active = camera


            self.report({'INFO'}, "VR360 Mono Scene Created!")
            return {'FINISHED'}

        except (KeyError, AttributeError) as e:
            self.report({'ERROR'}, f"Data error creating scene: {str(e)}")
            return {'CANCELLED'}
        except RuntimeError as e:
            self.report({'ERROR'}, f"Blender API error: {str(e)}")
            return {'CANCELLED'}
        except Exception as e:
            # Catch unexpected errors but log them
            logger.exception("Unexpected error creating VR360 scene")
            self.report({'ERROR'}, f"Unexpected error creating VR360 scene: {str(e)}")
            return {'CANCELLED'}

class VR360_OT_RenderSequence(Operator):
    """Render EXR Sequence - Renders a crash-safe mono 360 sequence"""
    bl_idname = "vr360mono.render_sequence"
    bl_label = "2. Render EXR Sequence"
    bl_description = "Renders a crash-safe OpenEXR sequence for the 360 mono camera"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        """Only enable if VR360 scene has been created."""
        return VR360_CAM_NAME in bpy.data.objects

    def _validate_preconditions(self, context):
        """Validate all prerequisites before starting render."""
        settings = context.scene.pe_vr360_mono_settings

        # Check frame range is valid
        if context.scene.frame_end <= context.scene.frame_start:
            self.report({'ERROR'}, "Invalid frame range: End frame must be greater than start frame")
            return False

        # Check VR360 camera exists
        if VR360_CAM_NAME not in bpy.data.objects:
            self.report({'ERROR'}, f"{VR360_CAM_NAME} not found. Please run Step 1 (Create VR360 Scene) first.")
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
        settings = context.scene.pe_vr360_mono_settings

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
            # 1. Detect the VR360 camera
            camera = bpy.data.objects.get(VR360_CAM_NAME)
            if not camera:
                self.report({'ERROR'}, f"No {VR360_CAM_NAME} found! Please create scene first.")
                return {'CANCELLED'}

            # 2. Create output folder
            output_base_path = bpy.path.abspath(settings.output_path)
            sequence_folder = Path(output_base_path) / "vr360" / "sequence"
            sequence_folder.mkdir(parents=True, exist_ok=True)

            # 3. Configure render settings for OpenEXR
            context.scene.render.image_settings.file_format = 'OPEN_EXR'
            context.scene.render.image_settings.color_depth = '32'
            context.scene.render.image_settings.exr_codec = 'DWAA'
            
            # 4. Render Sequence
            context.scene.camera = camera
            context.scene.render.filepath = str(sequence_folder / "vr360_")
            bpy.ops.render.render(animation=True)
            self.report({'INFO'}, f"Rendered 360 Mono sequence to {sequence_folder}")

        except (IOError, OSError, PermissionError) as e:
            self.report({'ERROR'}, f"File system error: {str(e)}")
            return {'CANCELLED'}
        except RuntimeError as e:
            self.report({'ERROR'}, f"Render error: {str(e)}")
            return {'CANCELLED'}
        except Exception as e:
            # Catch unexpected errors but log them
            logger.exception("Unexpected error rendering sequence")
            self.report({'ERROR'}, f"Unexpected error rendering sequence: {str(e)}")
            return {'CANCELLED'}
        finally:
            # 5. Restore original render settings
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

        self.report({'INFO'}, "VR360 Mono Sequence Rendered!")
        return {'FINISHED'}

class VR360_OT_SetupCompositor(Operator):
    """Setup Compositor - Auto-loads sequence and creates nodes"""
    bl_idname = "vr360mono.setup_compositor"
    bl_label = "3. Setup Compositor"
    bl_description = "Creates a compositor scene with all nodes linked for 360 mono"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        """Only enable if VR360 sequence has been rendered."""
        settings = context.scene.pe_vr360_mono_settings
        try:
            output_base_path = bpy.path.abspath(settings.output_path)
            sequence_folder = Path(output_base_path) / "vr360" / "sequence"
            return sequence_folder.exists()
        except:
            return False

    def _validate_preconditions(self, context):
        """Validate that rendered sequence exists before setting up compositor."""
        settings = context.scene.pe_vr360_mono_settings

        # Check that sequence was rendered
        try:
            output_base_path = bpy.path.abspath(settings.output_path)
            sequence_folder = Path(output_base_path) / "vr360" / "sequence"

            # Check folder exists
            if not sequence_folder.exists():
                self.report({'ERROR'}, f"Sequence folder not found: {sequence_folder}. Run Step 2 (Render Sequence) first.")
                return False

            # Check for rendered files
            sequence_files = list(sequence_folder.glob("vr360_*.exr"))

            if not sequence_files:
                self.report({'ERROR'}, "No VR360 EXR files found. Run Step 2 (Render Sequence) first.")
                return False

            # Verify file count matches frame range
            expected_frames = context.scene.frame_end - context.scene.frame_start + 1
            if len(sequence_files) < expected_frames:
                self.report({'WARNING'}, f"Incomplete sequence detected. Expected {expected_frames} frames, found {len(sequence_files)}.")

        except (OSError, PermissionError) as e:
            self.report({'ERROR'}, f"Cannot access sequence folder: {str(e)}")
            return False

        return True

    def execute(self, context):
        settings = context.scene.pe_vr360_mono_settings

        # Validate preconditions
        if not self._validate_preconditions(context):
            return {'CANCELLED'}

        # Store original state
        original_scene = context.window.scene
        original_active = context.view_layer.objects.active
        original_selected = list(context.selected_objects)

        try:
            # 1. Create or get compositor scene
            if VR360_COMPOSITOR_SCENE_NAME in bpy.data.scenes:
                comp_scene = bpy.data.scenes[VR360_COMPOSITOR_SCENE_NAME]
            else:
                comp_scene = bpy.data.scenes.new(VR360_COMPOSITOR_SCENE_NAME)

            context.window.scene = comp_scene
            comp_scene.use_nodes = True
            comp_scene.node_tree.nodes.clear()

            # 2. Auto-detect sequence path
            output_base_path = bpy.path.abspath(settings.output_path)
            sequence_path = str(Path(output_base_path) / "vr360" / "sequence" / "vr360_")

            # 3. Create nodes
            nodes = comp_scene.node_tree.nodes
            links = comp_scene.node_tree.links

            image_node = nodes.new('CompositorNodeImage')
            image_node.location = (-400, 0)
            image_node.filepath = sequence_path
            image_node.frame_duration = original_scene.frame_end - original_scene.frame_start + 1

            denoise_node = nodes.new('CompositorNodeDenoise')
            denoise_node.location = (-150, 0)

            composite_node = nodes.new('CompositorNodeComposite')
            composite_node.location = (100, 0)

            viewer_node = nodes.new('CompositorNodeViewer')
            viewer_node.location = (100, -150)

            # 4. Link nodes
            links.new(image_node.outputs['Image'], denoise_node.inputs['Image'])
            links.new(denoise_node.outputs['Image'], composite_node.inputs['Image'])
            links.new(denoise_node.outputs['Image'], viewer_node.inputs['Image'])
            
            # 5. Configure scene settings for compositor output
            if settings.resolution_preset == '5K':
                comp_scene.render.resolution_x = 5120
                comp_scene.render.resolution_y = 2560
            elif settings.resolution_preset == '8K':
                comp_scene.render.resolution_x = 7680
                comp_scene.render.resolution_y = 3840

            comp_scene.frame_start = original_scene.frame_start
            comp_scene.frame_end = original_scene.frame_end

            self.report({'INFO'}, "360 Mono Compositor Ready!")
            return {'FINISHED'}

        except (IOError, OSError) as e:
            self.report({'ERROR'}, f"File system error accessing sequence: {str(e)}")
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

class VR360_OT_RenderYouTube(Operator):
    """Render YouTube Video - Renders the final 360 mono video"""
    bl_idname = "vr360mono.render_youtube"
    bl_label = "4. Render YouTube Video"
    bl_description = "Renders the final 360 mono video from the compositor scene"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        """Only enable if compositor scene exists."""
        return VR360_COMPOSITOR_SCENE_NAME in bpy.data.scenes

    def _validate_preconditions(self, context):
        """Validate that compositor scene exists with valid node setup."""
        # Check compositor scene exists
        comp_scene = bpy.data.scenes.get(VR360_COMPOSITOR_SCENE_NAME)
        if not comp_scene:
            self.report({'ERROR'}, f"Compositor scene '{VR360_COMPOSITOR_SCENE_NAME}' not found. Please run Step 3 (Setup Compositor) first.")
            return False

        # Verify compositor is enabled and has nodes
        if not comp_scene.use_nodes:
            self.report({'ERROR'}, "Compositor not enabled in VR360_Compositor scene. Run Step 3 again.")
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
        settings = context.scene.pe_vr360_mono_settings
        original_scene = context.window.scene

        # Validate preconditions
        if not self._validate_preconditions(context):
            return {'CANCELLED'}

        try:
            # 1. Find the compositor scene
            comp_scene = bpy.data.scenes.get(VR360_COMPOSITOR_SCENE_NAME)

            # 2. Set active scene to compositor
            context.window.scene = comp_scene

            # 3. Configure render settings for YouTube video
            output_base_path = bpy.path.abspath(settings.output_path)
            final_output_path = Path(output_base_path) / "vr360" / "youtube_vr360"
            final_output_path.mkdir(parents=True, exist_ok=True)
            
            comp_scene.render.filepath = str(final_output_path / "vr360_mono_")
            
            comp_scene.render.image_settings.file_format = 'FFMPEG'
            comp_scene.render.ffmpeg.format = 'MPEG4'
            comp_scene.render.ffmpeg.codec = 'H264'
            comp_scene.render.ffmpeg.constant_rate_factor = 'PERC_LOSSLESS'
            comp_scene.render.ffmpeg.ffmpeg_preset = 'SLOW'
            comp_scene.render.ffmpeg.audio_codec = 'NONE'

            # 4. Trigger the render
            bpy.ops.render.render(animation=True)

            self.report({'INFO'}, f"Final 360 mono video rendered to: {comp_scene.render.filepath}")
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