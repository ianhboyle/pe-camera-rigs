import bpy
import math
from ...constants import VR180_RIG_NAME, VR180_LEFT_CAM_NAME, VR180_RIGHT_CAM_NAME

def create_vr180_rig(context):
    """
    Creates a parented VR180 stereo camera rig.

    Returns:
        (tuple): The main rig empty, the left camera object, and the right camera object.
    """
    # 1. Create the main parent object (an empty)
    rig = bpy.data.objects.new(name=VR180_RIG_NAME, object_data=None)
    rig.empty_display_type = 'CIRCLE'
    rig.location = (0, 0, 1.6) # Default eye level
    context.collection.objects.link(rig)

    # 2. Create the left camera
    left_cam_data = bpy.data.cameras.new("VR180_Camera_Left_Data")
    left_cam_obj = bpy.data.objects.new(VR180_LEFT_CAM_NAME, left_cam_data)

    # 3. Create the right camera
    right_cam_data = bpy.data.cameras.new("VR180_Camera_Right_Data")
    right_cam_obj = bpy.data.objects.new(VR180_RIGHT_CAM_NAME, right_cam_data)

    # 4. Configure both cameras
    for cam_obj in [left_cam_obj, right_cam_obj]:
        cam_obj.parent = rig
        cam_data = cam_obj.data
        cam_data.type = 'PANO'
        cam_data.cycles.panorama_type = 'FISHEYE_EQUISOLID'
        cam_data.cycles.fisheye_fov = math.radians(190)
        cam_data.lens = 5.2
        context.collection.objects.link(cam_obj)

    # 5. Add custom properties to the rig controller
    # This assumes a 'PE_VR180RigSettings' PropertyGroup is defined in properties.py
    # and registered to bpy.types.Object
    
    # 6. Use drivers to link the IPD property to the camera positions
    ipd_path = 'pe_vr180_rig_settings.ipd'

    # Left camera X location driver
    d_left = left_cam_obj.driver_add('location', 0).driver
    v_left = d_left.variables.new()
    v_left.name = 'ipd'
    v_left.targets[0].id = rig
    v_left.targets[0].data_path = ipd_path
    d_left.expression = '-ipd / 2000.0' # Convert mm to meters and divide by 2

    # Right camera X location driver
    d_right = right_cam_obj.driver_add('location', 0).driver
    v_right = d_right.variables.new()
    v_right.name = 'ipd'
    v_right.targets[0].id = rig
    v_right.targets[0].data_path = ipd_path
    d_right.expression = 'ipd / 2000.0' # Convert mm to meters and divide by 2

    return rig, left_cam_obj, right_cam_obj
