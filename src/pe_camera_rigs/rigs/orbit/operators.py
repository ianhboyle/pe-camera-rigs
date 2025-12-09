import bpy
import math
from ...utils.nodes import create_orbit_camera_node_group
from ...utils.blender import set_modifier_input
from ...constants import ORBIT_TEMPLATE_CAM_NAME, ORBIT_CONTROLLER_NAME

# Define presets with initial values for the modifier inputs
# These correspond to the order of inputs in create_orbit_camera_node_group()
ORBIT_PRESETS = {
    'PRODUCT':      {'radius': 3.0, 'height': 1.5, 'focal_length': 35.0, 'duration': 240, 'speed_multiplier': 1.0, 'reverse': False, 'easing': 'LINEAR'},
    'DETAIL':       {'radius': 1.5, 'height': 0.0, 'focal_length': 85.0, 'duration': 240, 'speed_multiplier': 1.0, 'reverse': False, 'easing': 'LINEAR'},
    'CHARACTER':    {'radius': 4.0, 'height': 1.6, 'focal_length': 50.0, 'duration': 360, 'speed_multiplier': 1.0, 'reverse': False, 'easing': 'LINEAR'},
    'HERO':         {'radius': 2.5, 'height': 0.5, 'focal_length': 24.0, 'duration': 120, 'speed_multiplier': 1.0, 'reverse': False, 'easing': 'EASE_IN_OUT'},
    'ARCHITECTURAL':{'radius': 15.0,'height': 2.0, 'focal_length': 35.0, 'duration': 480, 'speed_multiplier': 1.0, 'reverse': False, 'easing': 'LINEAR'},
    'ENVIRONMENT':  {'radius': 20.0,'height': 3.0, 'focal_length': 28.0, 'duration': 600, 'speed_multiplier': 1.0, 'reverse': False, 'easing': 'LINEAR'},
}

class ORBIT_OT_add_controller(bpy.types.Operator):
    """Adds a procedural Orbit Camera Controller to the scene"""
    bl_idname = "cgt.add_orbit_controller"
    bl_label = "Add Orbit Controller"
    bl_description = "Creates an interactive, procedural orbit camera rig"
    bl_options = {'REGISTER', 'UNDO'}

    preset: bpy.props.EnumProperty(
        name="Preset",
        items=[
            ('PRODUCT', "Product Photography", "A standard product shot setup"),
            ('DETAIL', "Detail Close-Up", "For small objects like jewelry"),
            ('CHARACTER', "Character Showcase", "For character turnarounds"),
            ('HERO', "Hero Shot", "Dramatic reveals, low angle"),
            ('ARCHITECTURAL', "Architectural Walkaround", "For buildings and large structures"),
            ('ENVIRONMENT', "Environment Tour", "For large scenes and environments"),
        ],
        default='PRODUCT'
    )

    def execute(self, context):
        # Validate preset exists
        if self.preset not in ORBIT_PRESETS:
            self.report({'ERROR'}, f"Invalid preset: {self.preset}")
            return {'CANCELLED'}

        template_cam_obj = None
        controller = None

        try:
            # 1. Create a template camera data-block (hidden, used by GeoNodes)
            #    This is critical because GN can instance objects but not create new Camera data.
            template_cam_data = bpy.data.cameras.new(name="Orbit_Template_CamData")
            template_cam_obj = bpy.data.objects.new(name=ORBIT_TEMPLATE_CAM_NAME, object_data=template_cam_data)

            # Hide the template object from view and render
            template_cam_obj.hide_set(True)
            template_cam_obj.hide_render = True
            context.collection.objects.link(template_cam_obj) # Link it so it saves

            # 2. Create the Geometry Node group for the orbit logic
            node_group = create_orbit_camera_node_group()

            if not node_group:
                self.report({'ERROR'}, "Failed to create orbit camera node group")
                return {'CANCELLED'}

            # 3. Create the controller object (an empty)
            controller = bpy.data.objects.new(name=ORBIT_CONTROLLER_NAME, object_data=None)
            controller.empty_display_type = 'SPHERE'
            controller.empty_display_size = 0.5
            context.collection.objects.link(controller)

            # 4. Add the Geometry Nodes modifier
            mod = controller.modifiers.new(name="Orbit Camera", type='NODES')
            mod.node_group = node_group

            # 5. Set initial values on the modifier from our presets
            initial_values = ORBIT_PRESETS[self.preset]

            # Validate node group has required inputs
            if len(node_group.inputs) < 8:
                self.report({'ERROR'}, "Node group missing required inputs")
                return {'CANCELLED'}

            # Set inputs using name-based access (more robust than index-based)
            if not set_modifier_input(mod, "Camera Template Object", template_cam_obj):
                self.report({'ERROR'}, "Failed to set camera template")
                return {'CANCELLED'}

            set_modifier_input(mod, "Orbit Radius", initial_values['radius'])
            set_modifier_input(mod, "Camera Height", initial_values['height'])
            set_modifier_input(mod, "Focal Length", initial_values['focal_length'])
            set_modifier_input(mod, "Duration (Frames)", initial_values['duration'])
            set_modifier_input(mod, "Speed Multiplier", initial_values['speed_multiplier'])
            set_modifier_input(mod, "Reverse Direction", initial_values['reverse'])

            # Easing is a bit special, needs to be mapped from string to int
            easing_map = {"LINEAR": 0, "EASE_IN_OUT": 1, "EASE_IN": 2, "EASE_OUT": 3}
            set_modifier_input(mod, "Easing", easing_map.get(initial_values['easing'], 0))

            # 6. Make the new rig active
            bpy.ops.object.select_all(action='DESELECT')
            context.view_layer.objects.active = controller
            controller.select_set(True)

            # 7. Set the scene camera to the one generated by Geometry Nodes.
            # This requires a dependency graph update to find the instanced object.
            context.view_layer.update()
            depsgraph = context.evaluated_depsgraph_get()

            generated_cam_obj = None
            for obj_instance in depsgraph.object_instances:
                # Check if the object instance is from our controller's modifier and is a camera
                if obj_instance.parent and obj_instance.parent.original == controller and obj_instance.is_instance:
                    if obj_instance.object.original.type == 'CAMERA':
                        # This is the instanced camera object.
                        generated_cam_obj = obj_instance.object.original
                        break

            if generated_cam_obj:
                context.scene.camera = generated_cam_obj
            else:
                # Fallback for headless environments or if depsgraph method fails
                self.report({'WARNING'}, "Could not find generated camera. Please set scene camera manually.")

            self.report({'INFO'}, f"Orbit Controller created with '{self.preset}' preset.")
            return {'FINISHED'}

        except AttributeError as e:
            self.report({'ERROR'}, f"Node group error: {str(e)}")
            # Clean up partial objects
            if template_cam_obj and template_cam_obj.name in bpy.data.objects:
                bpy.data.objects.remove(template_cam_obj, do_unlink=True)
            if controller and controller.name in bpy.data.objects:
                bpy.data.objects.remove(controller, do_unlink=True)
            return {'CANCELLED'}

        except KeyError as e:
            self.report({'ERROR'}, f"Missing preset value: {str(e)}")
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
