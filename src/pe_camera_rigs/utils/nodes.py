import bpy
import math

def create_orbit_camera_node_group():
    """
    Creates the Geometry Node group that procedurally generates and
    animates the orbit camera.
    """
    node_group_name = "GN_Orbit_Camera_Rig"
    if node_group_name in bpy.data.node_groups:
        return bpy.data.node_groups[node_group_name]

    node_group = bpy.data.node_groups.new(name=node_group_name, type='GeometryNodeTree')
    nodes = node_group.nodes
    links = node_group.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # === Group Inputs (Node Socket definition) ===
    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-1200, 0)

    # 0: Camera Template Object (an object that has Camera Data)
    input_node.outputs.new('NodeSocketObject', "Camera Template Object")
    
    # 1: Orbit Radius
    input_node.outputs.new('NodeSocketFloat', "Orbit Radius")
    node_group.inputs[1].default_value = 3.0
    node_group.inputs[1].min_value = 0.1
    node_group.inputs[1].max_value = 100.0

    # 2: Camera Height
    input_node.outputs.new('NodeSocketFloat', "Camera Height")
    node_group.inputs[2].default_value = 1.5
    node_group.inputs[2].min_value = -10.0
    node_group.inputs[2].max_value = 50.0

    # 3: Focal Length
    input_node.outputs.new('NodeSocketFloat', "Focal Length")
    node_group.inputs[3].default_value = 35.0
    node_group.inputs[3].min_value = 10.0
    node_group.inputs[3].max_value = 200.0

    # 4: Duration (Frames)
    input_node.outputs.new('NodeSocketInt', "Duration (Frames)")
    node_group.inputs[4].default_value = 240
    node_group.inputs[4].min_value = 1

    # 5: Speed Multiplier
    input_node.outputs.new('NodeSocketFloat', "Speed Multiplier")
    node_group.inputs[5].default_value = 1.0
    node_group.inputs[5].min_value = 0.01
    node_group.inputs[5].max_value = 10.0

    # 6: Reverse Direction
    input_node.outputs.new('NodeSocketBool', "Reverse Direction")
    node_group.inputs[6].default_value = False

    # 7: Easing (Mapped to integer, will be translated to curve in Python)
    input_node.outputs.new('NodeSocketInt', "Easing")
    node_group.inputs[7].default_value = 0 # LINEAR
    node_group.inputs[7].min_value = 0
    node_group.inputs[7].max_value = 3 # Max index of easing enum

    # 8: Start Angle Offset
    input_node.outputs.new('NodeSocketFloat', "Start Angle Offset")
    node_group.inputs[8].default_value = 0.0
    node_group.inputs[8].min_value = -360.0
    node_group.inputs[8].max_value = 360.0
    
    # 9: Target Object (for 'Look At')
    input_node.outputs.new('NodeSocketObject', "Target Object")
    
    # === Group Outputs ===
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (1000, 0)
    output_node.inputs.new('NodeSocketGeometry', "Camera Geometry")
    # Outputting the actual camera object for external use is complex in GN.
    # We will rely on Python to find the generated camera from the controller's instances.

    # === Node Tree Logic ===

    # 1. Get Scene Time
    scene_time = nodes.new('GeometryNodeInputSceneTime')
    scene_time.location = (-1000, 400)

    # 2. Calculate Animation Progress (0 to 1 over Duration)
    # Current Frame * Speed Multiplier
    mult_speed = nodes.new('ShaderNodeMath')
    mult_speed.operation = 'MULTIPLY'
    links.new(scene_time.outputs['Frame'], mult_speed.inputs[0])
    links.new(input_node.outputs['Speed Multiplier'], mult_speed.inputs[1])
    mult_speed.location = (-800, 400)

    # Modulo Duration (loops animation)
    modulo_duration = nodes.new('ShaderNodeMath')
    modulo_duration.operation = 'MODULO'
    links.new(mult_speed.outputs['Value'], modulo_duration.inputs[0])
    links.new(input_node.outputs['Duration (Frames)'], modulo_duration.inputs[1])
    modulo_duration.location = (-600, 400)
    
    # Divide by Duration (normalize to 0-1)
    normalize_progress = nodes.new('ShaderNodeMath')
    normalize_progress.operation = 'DIVIDE'
    links.new(modulo_duration.outputs['Value'], normalize_progress.inputs[0])
    links.new(input_node.outputs['Duration (Frames)'], normalize_progress.inputs[1])
    normalize_progress.location = (-400, 400)

    # Reverse Direction (if checked)
    # Need a separate switch for the reverse
    progress_not_reversed = normalize_progress.outputs['Value']
    progress_reversed = nodes.new('ShaderNodeMath')
    progress_reversed.operation = 'SUBTRACT'
    progress_reversed.inputs[0].default_value = 1.0 # 1 - progress
    links.new(normalize_progress.outputs['Value'], progress_reversed.inputs[1])
    
    switch_reverse = nodes.new('GeometryNodeSwitch')
    switch_reverse.input_type = 'FLOAT'
    links.new(input_node.outputs['Reverse Direction'], switch_reverse.inputs['Switch'])
    links.new(progress_not_reversed, switch_reverse.inputs['False'])
    links.new(progress_reversed.outputs['Value'], switch_reverse.inputs['True'])
    switch_reverse.location = (-200, 400)

    # 3. Easing Function
    # The 'Easing' input is an integer: 0=Linear, 1=Ease-In-Out, 2=Ease-In, 3=Ease-Out
    
    progress_value = switch_reverse.outputs['Output']

    # Ease-In-Out (Smooth) - Implemented with a Float Curve node
    ease_in_out_curve = nodes.new('ShaderNodeFloatCurve')
    ease_in_out_curve.location = (-200, 200)
    # Set curve points for a smooth S-curve
    curve = ease_in_out_curve.mapping.curves[0]
    curve.points.new(0.5, 0.5)
    curve.points[0].location = (0, 0)
    curve.points[1].location = (1, 1)
    curve.points[0].handle_type = 'AUTO'
    curve.points[1].handle_type = 'AUTO'
    ease_in_out_curve.mapping.update()
    links.new(progress_value, ease_in_out_curve.inputs['Fac'])
    ease_in_out_result = ease_in_out_curve.outputs['Value']
    
    # Ease-In (Quadratic) - Power of 2
    ease_in_power = nodes.new('ShaderNodeMath')
    ease_in_power.operation = 'POWER'
    ease_in_power.inputs[1].default_value = 2.0
    links.new(progress_value, ease_in_power.inputs[0])
    ease_in_result = ease_in_power.outputs['Value']

    # Ease-Out (Quadratic) - 1 - (1 - x)^2
    one_minus_x = nodes.new('ShaderNodeMath')
    one_minus_x.operation = 'SUBTRACT'
    one_minus_x.inputs[0].default_value = 1.0
    links.new(progress_value, one_minus_x.inputs[1])
    
    power_of_2 = nodes.new('ShaderNodeMath')
    power_of_2.operation = 'POWER'
    power_of_2.inputs[1].default_value = 2.0
    links.new(one_minus_x.outputs['Value'], power_of_2.inputs[0])

    ease_out_result_node = nodes.new('ShaderNodeMath')
    ease_out_result_node.operation = 'SUBTRACT'
    ease_out_result_node.inputs[0].default_value = 1.0
    links.new(power_of_2.outputs['Value'], ease_out_result_node.inputs[1])
    ease_out_result = ease_out_result_node.outputs['Value']

    # Chain switches to select the easing type
    # Switch between Ease-In and Ease-Out
    switch_ease_in_out = nodes.new('GeometryNodeSwitch')
    switch_ease_in_out.input_type = 'FLOAT'
    is_ease_out = nodes.new('ShaderNodeCompare')
    is_ease_out.operation = 'EQUAL'
    is_ease_out.inputs[0].default_value = 3
    links.new(input_node.outputs['Easing'], is_ease_out.inputs[1])
    links.new(is_ease_out.outputs['Result'], switch_ease_in_out.inputs['Switch'])
    links.new(ease_in_result, switch_ease_in_out.inputs['False'])
    links.new(ease_out_result, switch_ease_in_out.inputs['True'])
    
    # Switch between (Ease-In/Ease-Out result) and Ease-In-Out
    switch_smooth = nodes.new('GeometryNodeSwitch')
    switch_smooth.input_type = 'FLOAT'
    is_ease_in = nodes.new('ShaderNodeCompare')
    is_ease_in.operation = 'EQUAL'
    is_ease_in.inputs[0].default_value = 2
    links.new(input_node.outputs['Easing'], is_ease_in.inputs[1])
    is_gte_2 = nodes.new('ShaderNodeCompare')
    is_gte_2.operation = 'GREATER_THAN_OR_EQUAL'
    is_gte_2.inputs[0].default_value = 2
    links.new(input_node.outputs['Easing'], is_gte_2.inputs[1])
    links.new(is_gte_2.outputs['Result'], switch_smooth.inputs['Switch'])
    links.new(ease_in_out_result, switch_smooth.inputs['False']) # Use if Easing is 1
    links.new(switch_ease_in_out.outputs['Output'], switch_smooth.inputs['True']) # Use if Easing is 2 or 3

    # Switch between (all other results) and Linear
    final_ease_switch = nodes.new('GeometryNodeSwitch')
    final_ease_switch.input_type = 'FLOAT'
    is_linear = nodes.new('ShaderNodeCompare')
    is_linear.operation = 'EQUAL'
    is_linear.inputs[0].default_value = 0
    links.new(input_node.outputs['Easing'], is_linear.inputs[1])
    links.new(is_linear.outputs['Result'], final_ease_switch.inputs['Switch'])
    links.new(switch_smooth.outputs['Output'], final_ease_switch.inputs['False']) # Use if Easing is not 0
    links.new(progress_value, final_ease_switch.inputs['True']) # Use if Easing is 0 (Linear)

    eased_progress = final_ease_switch.outputs['Output']
    final_ease_switch.location = (0, 400)


    # 4. Calculate Angle (radians)
    # Progress * 2 * PI + Start Angle Offset
    mult_two_pi = nodes.new('ShaderNodeMath')
    mult_two_pi.operation = 'MULTIPLY'
    links.new(eased_progress, mult_two_pi.inputs[0])
    mult_two_pi.inputs[1].default_value = math.pi * 2 # 2 * PI
    
    add_offset = nodes.new('ShaderNodeMath')
    add_offset.operation = 'ADD'
    links.new(mult_two_pi.outputs['Value'], add_offset.inputs[0])
    links.new(input_node.outputs['Start Angle Offset'], add_offset.inputs[1])
    add_offset.location = (200, 400)

    # 5. Calculate Camera X, Y Position (polar to Cartesian)
    # X = R * cos(angle), Y = R * sin(angle)
    
    cos_angle = nodes.new('ShaderNodeMath')
    cos_angle.operation = 'COSINE'
    links.new(add_offset.outputs['Value'], cos_angle.inputs[0])
    
    sin_angle = nodes.new('ShaderNodeMath')
    sin_angle.operation = 'SINE'
    links.new(add_offset.outputs['Value'], sin_angle.inputs[0])
    
    mult_radius_x = nodes.new('ShaderNodeMath')
    mult_radius_x.operation = 'MULTIPLY'
    links.new(cos_angle.outputs['Value'], mult_radius_x.inputs[0])
    links.new(input_node.outputs['Orbit Radius'], mult_radius_x.inputs[1])
    
    mult_radius_y = nodes.new('ShaderNodeMath')
    mult_radius_y.operation = 'MULTIPLY'
    links.new(sin_angle.outputs['Value'], mult_radius_y.inputs[0])
    links.new(input_node.outputs['Orbit Radius'], mult_radius_y.inputs[1])
    
    # 6. Combine X, Y, Z (Camera Height) into a Vector
    combine_xyz_pos = nodes.new('ShaderNodeCombineXYZ')
    links.new(mult_radius_x.outputs['Value'], combine_xyz_pos.inputs[0]) # X
    links.new(mult_radius_y.outputs['Value'], combine_xyz_pos.inputs[1]) # Y
    links.new(input_node.outputs['Camera Height'], combine_xyz_pos.inputs[2]) # Z
    combine_xyz_pos.location = (400, 200)

    # 7. Get Target Object's Position (default to (0,0,0) if no target)
    get_target_pos = nodes.new('GeometryNodeObjectInfo')
    get_target_pos.inputs['As Instance'].default_value = False
    links.new(input_node.outputs['Target Object'], get_target_pos.inputs['Object'])
    
    # If no object is linked to "Target Object", its location is (0,0,0).
    # We'll use a switch to provide (0,0,0) explicitly for cleaner logic or if target is None.
    # For now, let's assume valid target or (0,0,0).
    target_location = get_target_pos.outputs['Location']
    get_target_pos.location = (0, -200)

    # 8. Instantiate the Camera Template Object
    instance_cam = nodes.new('GeometryNodeInstanceOnPoints')
    # Create a dummy point at the origin for instancing
    mesh_to_points = nodes.new('GeometryNodeMeshToPoints')
    mesh_line = nodes.new('GeometryNodeMeshLine') # A single point
    mesh_line.inputs['Count'].default_value = 1
    links.new(mesh_line.outputs['Points'], mesh_to_points.inputs['Mesh'])
    links.new(mesh_to_points.outputs['Points'], instance_cam.inputs['Points']) # Points socket
    
    # Get the Camera Template Object to instance
    get_template_obj = nodes.new('GeometryNodeObjectInfo')
    links.new(input_node.outputs['Camera Template Object'], get_template_obj.inputs['Object'])
    links.new(get_template_obj.outputs['Geometry'], instance_cam.inputs['Instance']) # Geometry to instance
    
    instance_cam.location = (600, 0)
    
    # 9. Set Camera Position (relative to target if target is not (0,0,0))
    # Relative position calculation for the camera
    add_target_offset = nodes.new('ShaderNodeVectorMath')
    add_target_offset.operation = 'ADD'
    links.new(combine_xyz_pos.outputs['Vector'], add_target_offset.inputs[0])
    links.new(target_location, add_target_offset.inputs[1])
    add_target_offset.location = (500, 0)
    
    set_position = nodes.new('GeometryNodeSetPosition')
    links.new(instance_cam.outputs['Instances'], set_position.inputs['Geometry'])
    links.new(add_target_offset.outputs['Vector'], set_position.inputs['Position'])
    set_position.location = (700, 0)

    # 10. Set Camera Rotation (Look At Target)
    # Vector from Camera Pos to Target Pos
    vector_math_sub = nodes.new('ShaderNodeVectorMath')
    vector_math_sub.operation = 'SUBTRACT'
    links.new(target_location, vector_math_sub.inputs[0])
    links.new(add_target_offset.outputs['Vector'], vector_math_sub.inputs[1])
    vector_math_sub.location = (500, -100)
    
    # Align Euler to Vector
    align_euler = nodes.new('GeometryNodeAlignEulerToVector')
    links.new(vector_math_sub.outputs['Vector'], align_euler.inputs['Vector'])
    align_euler.inputs['Axis'].default_value = 'Z' # Camera's forward axis is +Z in object space, so it should look along -Vector
    align_euler.inputs['Factor'].default_value = 1.0
    align_euler.location = (700, -100)
    
    set_rotation = nodes.new('GeometryNodeSetRotation')
    links.new(set_position.outputs['Geometry'], set_rotation.inputs['Geometry'])
    links.new(align_euler.outputs['Rotation'], set_rotation.inputs['Rotation'])
    set_rotation.location = (800, 0)

    # 11. Set Camera Focal Length (only works if the instanced object *is* a camera)
    set_focal_length = nodes.new('GeometryNodeSetCamera')
    links.new(set_rotation.outputs['Geometry'], set_focal_length.inputs['Geometry'])
    links.new(input_node.outputs['Focal Length'], set_focal_length.inputs['Focal Length'])
    set_focal_length.location = (900, 0)
    
    # Output Camera Geometry
    links.new(set_focal_length.outputs['Geometry'], output_node.inputs['Camera Geometry'])

    return node_group

def create_isometric_camera_node_group():
    """
    Creates the Geometry Node group that procedurally generates and
    positions the isometric camera.

    Supports multiple projection presets: Game 2:1, Game 4:3, True Isometric,
    Dimetric, Military, Cavalier, and Custom angles.
    """
    node_group_name = "GN_Isometric_Camera_Rig"
    if node_group_name in bpy.data.node_groups:
        return bpy.data.node_groups[node_group_name]

    node_group = bpy.data.node_groups.new(name=node_group_name, type='GeometryNodeTree')
    nodes = node_group.nodes
    links = node_group.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # === Group Inputs ===
    input_node = nodes.new('NodeGroupInput')
    input_node.location = (-1400, 0)

    # 0: Camera Template Object
    input_node.outputs.new('NodeSocketObject', "Camera Template")

    # 1: Projection Type (as int: 0=GAME_2_1, 1=GAME_4_3, 2=TRUE_ISOMETRIC, 3=DIMETRIC, 4=MILITARY, 5=CAVALIER, 6=CUSTOM)
    input_node.outputs.new('NodeSocketInt', "Projection Type")
    node_group.inputs[1].default_value = 2  # TRUE_ISOMETRIC
    node_group.inputs[1].min_value = 0
    node_group.inputs[1].max_value = 6

    # 2: Ortho Scale
    input_node.outputs.new('NodeSocketFloat', "Ortho Scale")
    node_group.inputs[2].default_value = 10.0
    node_group.inputs[2].min_value = 0.1
    node_group.inputs[2].max_value = 1000.0

    # 3: Custom Rotation Z
    input_node.outputs.new('NodeSocketFloat', "Custom Rotation Z")
    node_group.inputs[3].default_value = math.radians(45.0)

    # 4: Custom Tilt X
    input_node.outputs.new('NodeSocketFloat', "Custom Tilt X")
    node_group.inputs[4].default_value = math.radians(35.264)

    # 5: Custom Roll Y
    input_node.outputs.new('NodeSocketFloat', "Custom Roll Y")
    node_group.inputs[5].default_value = 0.0

    # === Group Outputs ===
    output_node = nodes.new('NodeGroupOutput')
    output_node.location = (1200, 0)
    output_node.inputs.new('NodeSocketGeometry', "Camera")

    # === CAMERA INSTANCING ===
    # 1. Create a point to instance the camera on
    instance_point = nodes.new('GeometryNodePrimitivePoint')
    instance_point.location = (-1000, 0)

    # 2. Get template camera geometry
    get_template_obj = nodes.new('GeometryNodeObjectInfo')
    get_template_obj.location = (-1000, -200)
    links.new(input_node.outputs['Camera Template'], get_template_obj.inputs['Object'])

    # 3. Instance camera on point
    instance_cam = nodes.new('GeometryNodeInstanceOnPoints')
    instance_cam.location = (-800, 0)
    links.new(instance_point.outputs['Geometry'], instance_cam.inputs['Points'])
    links.new(get_template_obj.outputs['Geometry'], instance_cam.inputs['Instance'])

    # === PRESET ANGLE DEFINITIONS ===
    # Define rotation vectors for each projection type (Rotation Z, Tilt X, Roll Y)

    # GAME_2_1: 26.565° tilt, 45° rotation
    game_2_1_vec = nodes.new('ShaderNodeCombineXYZ')
    game_2_1_vec.location = (-600, 600)
    game_2_1_vec.inputs[0].default_value = math.radians(26.565)  # Tilt X
    game_2_1_vec.inputs[1].default_value = 0.0  # Roll Y
    game_2_1_vec.inputs[2].default_value = math.radians(45.0)  # Rotation Z

    # GAME_4_3: 30° tilt, 45° rotation
    game_4_3_vec = nodes.new('ShaderNodeCombineXYZ')
    game_4_3_vec.location = (-600, 450)
    game_4_3_vec.inputs[0].default_value = math.radians(30.0)
    game_4_3_vec.inputs[1].default_value = 0.0
    game_4_3_vec.inputs[2].default_value = math.radians(45.0)

    # TRUE_ISOMETRIC: arctan(sin(45°)) = 35.264° tilt, 45° rotation
    true_iso_vec = nodes.new('ShaderNodeCombineXYZ')
    true_iso_vec.location = (-600, 300)
    true_iso_vec.inputs[0].default_value = math.radians(35.264)
    true_iso_vec.inputs[1].default_value = 0.0
    true_iso_vec.inputs[2].default_value = math.radians(45.0)

    # DIMETRIC: 30° tilt, 45° rotation
    dimetric_vec = nodes.new('ShaderNodeCombineXYZ')
    dimetric_vec.location = (-600, 150)
    dimetric_vec.inputs[0].default_value = math.radians(30.0)
    dimetric_vec.inputs[1].default_value = 0.0
    dimetric_vec.inputs[2].default_value = math.radians(45.0)

    # MILITARY: 90° tilt (top-down), 0° rotation
    military_vec = nodes.new('ShaderNodeCombineXYZ')
    military_vec.location = (-600, 0)
    military_vec.inputs[0].default_value = math.radians(90.0)
    military_vec.inputs[1].default_value = 0.0
    military_vec.inputs[2].default_value = 0.0

    # CAVALIER: 0° tilt, 45° rotation
    cavalier_vec = nodes.new('ShaderNodeCombineXYZ')
    cavalier_vec.location = (-600, -150)
    cavalier_vec.inputs[0].default_value = 0.0
    cavalier_vec.inputs[1].default_value = 0.0
    cavalier_vec.inputs[2].default_value = math.radians(45.0)

    # CUSTOM: Use custom angle inputs
    custom_vec = nodes.new('ShaderNodeCombineXYZ')
    custom_vec.location = (-600, -300)
    links.new(input_node.outputs['Custom Tilt X'], custom_vec.inputs[0])
    links.new(input_node.outputs['Custom Roll Y'], custom_vec.inputs[1])
    links.new(input_node.outputs['Custom Rotation Z'], custom_vec.inputs[2])

    # === PROJECTION TYPE SELECTION (Switch Chain) ===
    # Build a chain of switches to select the correct angle vector based on Projection Type

    # Switch 6: CUSTOM vs CAVALIER
    switch_6_5 = nodes.new('GeometryNodeSwitch')
    switch_6_5.input_type = 'VECTOR'
    switch_6_5.location = (-400, -200)
    compare_6 = nodes.new('FunctionNodeCompare')
    compare_6.data_type = 'INT'
    compare_6.operation = 'EQUAL'
    compare_6.inputs[2].default_value = 6  # CUSTOM
    links.new(input_node.outputs['Projection Type'], compare_6.inputs[3])
    links.new(compare_6.outputs['Result'], switch_6_5.inputs['Switch'])
    links.new(cavalier_vec.outputs['Vector'], switch_6_5.inputs['False'])
    links.new(custom_vec.outputs['Vector'], switch_6_5.inputs['True'])

    # Switch 5: Result vs MILITARY
    switch_5_4 = nodes.new('GeometryNodeSwitch')
    switch_5_4.input_type = 'VECTOR'
    switch_5_4.location = (-200, -100)
    compare_5 = nodes.new('FunctionNodeCompare')
    compare_5.data_type = 'INT'
    compare_5.operation = 'EQUAL'
    compare_5.inputs[2].default_value = 4  # MILITARY
    links.new(input_node.outputs['Projection Type'], compare_5.inputs[3])
    links.new(compare_5.outputs['Result'], switch_5_4.inputs['Switch'])
    links.new(switch_6_5.outputs['Output'], switch_5_4.inputs['False'])
    links.new(military_vec.outputs['Vector'], switch_5_4.inputs['True'])

    # Switch 4: Result vs DIMETRIC
    switch_4_3 = nodes.new('GeometryNodeSwitch')
    switch_4_3.input_type = 'VECTOR'
    switch_4_3.location = (0, 0)
    compare_4 = nodes.new('FunctionNodeCompare')
    compare_4.data_type = 'INT'
    compare_4.operation = 'EQUAL'
    compare_4.inputs[2].default_value = 3  # DIMETRIC
    links.new(input_node.outputs['Projection Type'], compare_4.inputs[3])
    links.new(compare_4.outputs['Result'], switch_4_3.inputs['Switch'])
    links.new(switch_5_4.outputs['Output'], switch_4_3.inputs['False'])
    links.new(dimetric_vec.outputs['Vector'], switch_4_3.inputs['True'])

    # Switch 3: Result vs TRUE_ISOMETRIC
    switch_3_2 = nodes.new('GeometryNodeSwitch')
    switch_3_2.input_type = 'VECTOR'
    switch_3_2.location = (200, 100)
    compare_3 = nodes.new('FunctionNodeCompare')
    compare_3.data_type = 'INT'
    compare_3.operation = 'EQUAL'
    compare_3.inputs[2].default_value = 2  # TRUE_ISOMETRIC
    links.new(input_node.outputs['Projection Type'], compare_3.inputs[3])
    links.new(compare_3.outputs['Result'], switch_3_2.inputs['Switch'])
    links.new(switch_4_3.outputs['Output'], switch_3_2.inputs['False'])
    links.new(true_iso_vec.outputs['Vector'], switch_3_2.inputs['True'])

    # Switch 2: Result vs GAME_4_3
    switch_2_1 = nodes.new('GeometryNodeSwitch')
    switch_2_1.input_type = 'VECTOR'
    switch_2_1.location = (400, 200)
    compare_2 = nodes.new('FunctionNodeCompare')
    compare_2.data_type = 'INT'
    compare_2.operation = 'EQUAL'
    compare_2.inputs[2].default_value = 1  # GAME_4_3
    links.new(input_node.outputs['Projection Type'], compare_2.inputs[3])
    links.new(compare_2.outputs['Result'], switch_2_1.inputs['Switch'])
    links.new(switch_3_2.outputs['Output'], switch_2_1.inputs['False'])
    links.new(game_4_3_vec.outputs['Vector'], switch_2_1.inputs['True'])

    # Switch 1: Result vs GAME_2_1
    switch_1_0 = nodes.new('GeometryNodeSwitch')
    switch_1_0.input_type = 'VECTOR'
    switch_1_0.location = (600, 300)
    compare_1 = nodes.new('FunctionNodeCompare')
    compare_1.data_type = 'INT'
    compare_1.operation = 'EQUAL'
    compare_1.inputs[2].default_value = 0  # GAME_2_1
    links.new(input_node.outputs['Projection Type'], compare_1.inputs[3])
    links.new(compare_1.outputs['Result'], switch_1_0.inputs['Switch'])
    links.new(switch_2_1.outputs['Output'], switch_1_0.inputs['False'])
    links.new(game_2_1_vec.outputs['Vector'], switch_1_0.inputs['True'])

    final_rotation_vector = switch_1_0.outputs['Output']

    # === APPLY ROTATION TO CAMERA ===
    set_rotation = nodes.new('GeometryNodeSetRotation')
    set_rotation.location = (800, 0)
    links.new(instance_cam.outputs['Instances'], set_rotation.inputs['Geometry'])
    links.new(final_rotation_vector, set_rotation.inputs['Rotation'])

    # === SET CAMERA ORTHOGRAPHIC SCALE ===
    set_ortho_scale = nodes.new('GeometryNodeSetCamera')
    set_ortho_scale.location = (1000, 0)
    links.new(set_rotation.outputs['Geometry'], set_ortho_scale.inputs['Geometry'])
    links.new(input_node.outputs['Ortho Scale'], set_ortho_scale.inputs['Orthographic Scale'])

    # Connect to output
    links.new(set_ortho_scale.outputs['Geometry'], output_node.inputs['Camera'])

    return node_group
