import bpy
import math
from ...utils.nodes import create_isometric_camera_node_group
from ...utils.blender import set_modifier_input
from .properties import PROJECTION_TYPES
from ...constants import ISO_TEMPLATE_CAM_NAME, ISO_CONTROLLER_NAME

class ISOMETRIC_OT_add_controller(bpy.types.Operator):
    """Adds an Isometric Camera Controller to the scene"""
    bl_idname = "cgt.add_isometric_controller"
    bl_label = "Add Isometric Controller"
    bl_description = "Creates an interactive, Geometry Nodes-based isometric camera rig"
    bl_options = {'REGISTER', 'UNDO'}

    # Property to set the initial preset from the UI in the sidebar
    initial_preset: bpy.props.EnumProperty(
        name="Preset",
        items=PROJECTION_TYPES,
        default='TRUE_ISOMETRIC'
    )

    def execute(self, context):
        # Validate preset exists
        preset_names = [name for name, _, _ in PROJECTION_TYPES]
        if self.initial_preset not in preset_names:
            self.report({'ERROR'}, f"Invalid preset: {self.initial_preset}")
            return {'CANCELLED'}

        template_cam_obj = None
        controller = None

        try:
            # 1. Create a template camera to be instanced by the node group
            template_cam_data = bpy.data.cameras.new(name="Isometric_Template_CamData")
            template_cam_data.type = 'ORTHO'
            template_cam_obj = bpy.data.objects.new(name=ISO_TEMPLATE_CAM_NAME, object_data=template_cam_data)
            template_cam_obj.hide_set(True)
            template_cam_obj.hide_render = True
            context.collection.objects.link(template_cam_obj)

            # 2. Create the Geometry Node group
            node_group = create_isometric_camera_node_group()

            if not node_group:
                self.report({'ERROR'}, "Failed to create isometric camera node group")
                return {'CANCELLED'}

            # 3. Create the controller empty
            controller = bpy.data.objects.new(name=ISO_CONTROLLER_NAME, object_data=None)
            controller.empty_display_type = 'CUBE'
            controller.empty_display_size = 0.5
            context.collection.objects.link(controller)

            # 4. Add the Geometry Nodes modifier
            mod = controller.modifiers.new(name="Isometric Camera", type='NODES')
            mod.node_group = node_group

            # Validate node group has required inputs
            if len(node_group.inputs) < 6:
                self.report({'ERROR'}, "Node group missing required inputs")
                return {'CANCELLED'}

            # 5. Set initial values on the modifier using name-based access (more robust than index-based)
            if not set_modifier_input(mod, "Camera Template", template_cam_obj):
                self.report({'ERROR'}, "Failed to set camera template")
                return {'CANCELLED'}

            # Map the string enum to an integer for the node group
            preset_map = {name: i for i, (name, _, _) in enumerate(PROJECTION_TYPES)}
            set_modifier_input(mod, "Projection Type", preset_map.get(self.initial_preset, 2))
            set_modifier_input(mod, "Ortho Scale", 10.0)
            set_modifier_input(mod, "Custom Rotation Z", math.radians(45.0))
            set_modifier_input(mod, "Custom Tilt X", math.radians(35.264))
            set_modifier_input(mod, "Custom Roll Y", 0.0)

            # 6. Initialize property group on controller
            controller.pe_iso_cam.projection_type = self.initial_preset
            controller.pe_iso_cam.ortho_scale = 10.0
            controller.pe_iso_cam.custom_rotation_z = math.radians(45.0)
            controller.pe_iso_cam.custom_tilt_x = math.radians(35.264)
            controller.pe_iso_cam.custom_roll_y = 0.0

            # 7. Make the new rig active and set the scene camera
            bpy.ops.object.select_all(action='DESELECT')
            context.view_layer.objects.active = controller
            controller.select_set(True)

            context.view_layer.update()
            depsgraph = context.evaluated_depsgraph_get()

            generated_cam_obj = None
            for obj_instance in depsgraph.object_instances:
                if obj_instance.parent and obj_instance.parent.original == controller and obj_instance.is_instance:
                    if obj_instance.object.original.type == 'CAMERA':
                        generated_cam_obj = obj_instance.object.original
                        break

            if generated_cam_obj:
                context.scene.camera = generated_cam_obj
            else:
                self.report({'WARNING'}, "Could not find generated camera. Please set scene camera manually.")

            self.report({'INFO'}, f"Isometric Controller created with '{self.initial_preset}' preset.")
            return {'FINISHED'}

        except AttributeError as e:
            self.report({'ERROR'}, f"Depsgraph or node error: {str(e)}")
            # Clean up partial objects
            if template_cam_obj and template_cam_obj.name in bpy.data.objects:
                bpy.data.objects.remove(template_cam_obj, do_unlink=True)
            if controller and controller.name in bpy.data.objects:
                bpy.data.objects.remove(controller, do_unlink=True)
            return {'CANCELLED'}

        except RuntimeError as e:
            self.report({'ERROR'}, f"Blender API error: {str(e)}")
            # Clean up partial objects
            if template_cam_obj and template_cam_obj.name in bpy.data.objects:
                bpy.data.objects.remove(template_cam_obj, do_unlink=True)
            if controller and controller.name in bpy.data.objects:
                bpy.data.objects.remove(controller, do_unlink=True)
            return {'CANCELLED'}
