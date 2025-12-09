import bpy
import math
from ...constants import VR360_CAM_NAME

def create_vr360_camera(context, height=1.6):
    """
    Creates a single, level, equirectangular camera for VR360 Mono.

    Returns:
        (bpy.types.Object): The created camera object.
    """
    bpy.ops.object.camera_add(location=(0, 0, height))
    camera = context.active_object
    camera.name = VR360_CAM_NAME
    
    cam_data = camera.data
    cam_data.type = 'PANO'
    cam_data.cycles.panorama_type = 'EQUIRECTANGULAR'
    
    # Level the camera
    camera.rotation_euler[0] = math.radians(90)
    camera.rotation_euler[1] = 0
    camera.rotation_euler[2] = 0

    return camera